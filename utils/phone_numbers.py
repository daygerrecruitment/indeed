import re

def extract_phone_numbers(description_text):
    """
    Extracts phone numbers from the provided text.

    Args:
        description_text: The text from which to extract phone numbers.

    Returns:
        list: A list of extracted phone numbers.
    """

    clean_text = re.sub(r"[^a-zA-Z0-9]+", "", description_text)
    phone_pattern = r"\d{9,}"
    phone_numbers = re.findall(phone_pattern, clean_text)
    return [num for num in phone_numbers if len(num) <= 11]
