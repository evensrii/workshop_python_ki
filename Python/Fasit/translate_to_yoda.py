import requests

def translate_to_yoda_speech(text):
    """
    Translates the given text to Yoda speech using the Fun Translations Yoda API.

    Args:
        text (str): The text to translate.

    Returns:
        str: The translated text in Yoda speech.
    """
    url = "https://api.funtranslations.com/translate/yoda.json"
    payload = {"text": text}

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("contents", {}).get("translated", "Translation failed.")
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    text_to_translate = input("Enter the text you want to translate to Yoda speech: ")
    translated_text = translate_to_yoda_speech(text_to_translate)
    print(f"Yoda says: {translated_text}")