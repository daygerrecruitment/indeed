import re

class PhoneExtractor:
    @staticmethod
    def extract_phone_numbers(description_text):
        clean_text = re.sub(r"[^a-zA-Z0-9]+", "", description_text)
        phone_pattern = r"\d{9,11}"
        return re.findall(phone_pattern, clean_text)