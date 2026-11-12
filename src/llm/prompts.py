AADHAAR_EXTRACTION_PROMPT = """Extract the Aadhaar card details from the card image(s) provided.
Aadhaar cards print details in English and in a regional Indian language. Use the English values unless a field says otherwise.
Return null for any field that is not present. Do not guess.
- name: the cardholder's full name in English
- name_local: the cardholder's name in the regional language script, copied character by character exactly as printed (do not transliterate from the English name)
- aadhaar_number: 12 digits formatted as "1234 5678 9012". If the first 8 digits are masked or hidden, return "XXXX XXXX" followed by the 4 visible digits, e.g. "XXXX XXXX 8475". The number is printed on both the front and the back of the card, near the bottom, so read it from the back side too.
- vid: 16-digit Virtual ID if present
- dob: DD/MM/YYYY, or just YYYY if only the year of birth is shown
- gender: Male, Female or Transgender
- care_of: the name that follows S/O, D/O, W/O or C/O (may be a father, husband or other guardian), without the prefix
- address: full English address after "Address:", without the care_of part, keeping punctuation as printed (e.g. "H.No")
- address_local: the regional language address on the back of the card, printed after a label such as "पता:" or "સરનામું:", above the English address. Copy it character by character exactly as printed, without the care_of part. Do not translate or transliterate the English address.
- state: the Indian state or union territory from the address, using its official English name (e.g. Delhi, Tamil Nadu)
- pincode: the 6-digit PIN code from the address
"""
