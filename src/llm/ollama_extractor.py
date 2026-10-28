import os
import re
import time

from dotenv import load_dotenv
from ollama import Client, ResponseError
from pydantic import BaseModel, Field, field_validator

from .prompts import AADHAAR_EXTRACTION_PROMPT

load_dotenv()

MODEL = "gemma4:31b"
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
    care_of: str | None = Field(None, title="Father's Name")
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
        if field in TITLE_CASE_FIELDS:
            value = value.title()
        return value or None


client = Client(host="https://ollama.com", headers={"Authorization": f"Bearer {os.environ['OLLAMA_API_KEY']}"})


def extract_fields(images):
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat(
                model=MODEL,
                messages=[{"role": "user", "content": AADHAAR_EXTRACTION_PROMPT, "images": images}],
                format=AadhaarData.model_json_schema(),
                options={"temperature": 0},
            )
            break
        except (ConnectionError, ResponseError) as e:
            # Retry only network drops and server-side errors; a bad request or API key won't succeed on retry.
            if attempt == MAX_RETRIES or getattr(e, "status_code", 500) < 500:
                raise
            time.sleep(RETRY_DELAY_SECONDS)
    # Cloud models don't strictly enforce `format` and may wrap the JSON in a ```json fence.
    content = response.message.content
    return AadhaarData.model_validate_json(content[content.find("{"):content.rfind("}") + 1])
