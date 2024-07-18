import json
import ollama

def translate_to_english(note_text):
    prompt = f"""
    You are a professional translator. Translate the following text to English. If the message is already in English, just return the text as it is. Do not lose, modify, or change parts of the text that should remain intact. Return the result in a JSON object with the key 'translated_text':
    '''{note_text}'''
    """
    response = ollama.generate(
        format='json',
        model='llama3',
        prompt=prompt
    )
    try:
        response_data = json.loads(response['response'])
        return response_data['translated_text']
    except (json.JSONDecodeError, KeyError):
        print("Failed to decode JSON response for translation.")
        return None  # Return None if translation fails
