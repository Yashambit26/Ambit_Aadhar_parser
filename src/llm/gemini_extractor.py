import os
import re
import time

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pydantic import BaseModel, Field, field_validator

from .prompts import AADHAAR_EXTRACTION_PROMPT

load_dotenv()

MODEL = "gemini-3.8-flash"
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 5
TITLE_CASE_FIELDS = {"name", "gender", "care_of", "address", "state"}


# Titles are used as the Excel column headers.
class AadhaarData(BaseModel):
    name: str | None = Field(None, title="Name")
    name_local: str | None = Field(None, title="Name (Regional Language)")
    dob: str | None = Field(None, title="Date of Birth")
    gender: str | None = Field(None, title="Gender")
    aadhaar_number: str | None = Field(None, title="Aadhaar Number")
    vid: str | None = Field(None, title="VID")
    care_of: str | None = Field(None, title="Care Of")
    address: str | None = Field(None, title="Address")
    address_local: str | None = Field(None, title="Address (Regional Language)")
    state: str | None = Field(None, title="State")
    pincode: str | None = Field(None, title="PIN Code")

    @field_validator("*")
    @classmethod
    def normalize(cls, value, info):
        if value is None:
            return None
        field = info.field_name
        value = " ".join(value.split()).strip(" ,")
        if field == "care_of":
            value = re.sub(r"^[SDWC]\s*/\s*O\b[\s:,-]*", "", value, flags=re.IGNORECASE)
        elif field in ("address", "address_local"):
            # The PIN code has its own column.
            value = re.sub(r"[\s,-]*\b\d{6}$", "", value)
        elif field in ("aadhaar_number", "vid"):
            digits = re.sub(r"\D", "", value)
            if len(digits) in (12, 16):
                value = " ".join(digits[i:i + 4] for i in range(0, len(digits), 4))
            elif field == "aadhaar_number" and len(digits) == 4:
                # Masked cards show only the last 4 digits.
                value = f"XXXX XXXX {digits}"
        if field in TITLE_CASE_FIELDS:
            value = value.title()
        return value or None


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def extract_fields(images):
    # Both parsers produce PNG images.
    contents = [*(types.Part.from_bytes(data=img, mime_type="image/png") for img in images), AADHAAR_EXTRACTION_PROMPT]
    config = types.GenerateContentConfig(temperature=0, response_mime_type="application/json", response_schema=AadhaarData)
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(model=MODEL, contents=contents, config=config)
            break
        except (errors.APIError, httpx.TransportError) as e:
            # Retry network drops (no code), rate limits and server errors; a bad request or API key won't succeed on retry.
            code = getattr(e, "code", None)
            if attempt == MAX_RETRIES or (code is not None and code != 429 and code < 500):
                raise
            time.sleep(RETRY_DELAY_SECONDS)
    return AadhaarData.model_validate_json(response.text)
