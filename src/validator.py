import re
from datetime import date, datetime

VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]
VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]

REQUIRED_FIELDS = ["name", "dob", "gender", "aadhaar_number", "address", "state", "pincode"]
GENDERS = {"Male", "Female", "Transgender"}
MAX_AGE = 120

# First digit of the PIN code for each state / union territory (names in the Title Case the extractor produces).
PIN_ZONES = {
    "Delhi": "1", "Haryana": "1", "Punjab": "1", "Himachal Pradesh": "1", "Jammu And Kashmir": "1",
    "Ladakh": "1", "Chandigarh": "1",
    "Uttar Pradesh": "2", "Uttarakhand": "2",
    "Rajasthan": "3", "Gujarat": "3", "Dadra And Nagar Haveli And Daman And Diu": "3",
    "Maharashtra": "4", "Madhya Pradesh": "4", "Chhattisgarh": "4", "Goa": "4",
    "Andhra Pradesh": "5", "Telangana": "5", "Karnataka": "5",
    "Tamil Nadu": "6", "Kerala": "6", "Puducherry": "6", "Lakshadweep": "6",
    "West Bengal": "7", "Odisha": "7", "Assam": "7", "Arunachal Pradesh": "7", "Manipur": "7", "Meghalaya": "7",
    "Mizoram": "7", "Nagaland": "7", "Tripura": "7", "Sikkim": "7", "Andaman And Nicobar Islands": "7",
    "Bihar": "8", "Jharkhand": "8",
}


def verhoeff_ok(digits):
    check = 0
    for i, d in enumerate(reversed(digits)):
        check = VERHOEFF_D[check][VERHOEFF_P[i % 8][int(d)]]
    return check == 0


def scripts(text):
    # Indian scripts occupy consecutive 128-character Unicode blocks from Devanagari (U+0900) to Malayalam (U+0D7F).
    return {(ord(c) - 0x900) // 0x80 for c in text if 0x900 <= ord(c) <= 0xD7F}


def validate(data):
    label = {name: field.title for name, field in type(data).model_fields.items()}
    issues = [f"{label[f]} missing" for f in REQUIRED_FIELDS if not getattr(data, f)]

    if data.aadhaar_number:
        digits = re.sub(r"\D", "", data.aadhaar_number)
        if not re.fullmatch(r"[2-9]\d{11}", digits):
            issues.append("invalid Aadhaar Number format")
        elif not verhoeff_ok(digits):
            issues.append("Aadhaar Number checksum failed")

    if data.vid:
        digits = re.sub(r"\D", "", data.vid)
        if not re.fullmatch(r"\d{16}", digits) or not verhoeff_ok(digits):
            issues.append("invalid VID")

    if data.dob:
        try:
            dob = datetime.strptime(data.dob, "%d/%m/%Y").date() if "/" in data.dob else date(int(data.dob), 1, 1)
        except ValueError:
            dob = None
        today = date.today()
        if not dob or dob > today or dob.year < today.year - MAX_AGE:
            issues.append("invalid Date of Birth")

    if data.gender and data.gender not in GENDERS:
        issues.append("invalid Gender")

    if data.state and data.state not in PIN_ZONES:
        issues.append("unknown State")

    if data.pincode:
        if not re.fullmatch(r"[1-9]\d{5}", data.pincode):
            issues.append("invalid PIN Code")
        elif data.state in PIN_ZONES and data.pincode[0] != PIN_ZONES[data.state]:
            issues.append("PIN Code does not match State")

    for f in ("name_local", "address_local"):
        if len(scripts(getattr(data, f) or "")) > 1:
            issues.append(f"{label[f]} mixes scripts")

    return issues
