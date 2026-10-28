AADHAAR_EXTRACTION_PROMPT = """Extract the Aadhaar card details from the card image(s) provided.
Aadhaar cards print details in English and in a regional Indian language. Use the English values unless a field says otherwise.
Return null for any field that is not present. Do not guess.
- name: the cardholder's full name in English
- name_local: the cardholder's name exactly as printed in the regional language script
- aadhaar_number: 12 digits formatted as "XXXX XXXX XXXX"
- vid: 16-digit Virtual ID if present
- dob: DD/MM/YYYY, or just YYYY if only the year of birth is shown
- gender: Male, Female or Transgender
- care_of: the father/husband/guardian name (from S/O, D/O, W/O, C/O)
- address: full address in English, without the care_of part
- address_local: full address exactly as printed in the regional language script
- state: the Indian state or union territory from the address, using its official English name (e.g. Delhi, Tamil Nadu)
- pincode: the 6-digit PIN code from the address
"""
