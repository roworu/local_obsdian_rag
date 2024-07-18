import json
import ollama

def fix_grammar(note_text):
    prompt = f"""
    You are a grammar corrector. Fix all grammar issues in the following text while preserving the original structure and content. Do not lose, modify, or change parts of the text that should remain intact. Return the result in a JSON object with the key 'corrected_text'. If the text has no issues, just return the text as it is:
    '''{note_text}'''
    """
    response = ollama.generate(
        format='json',
        model='llama3',  # Replace with the appropriate model for grammar correction
        prompt=prompt
    )
    try:
        response_data = json.loads(response['response'])
        return response_data['corrected_text']
    except (json.JSONDecodeError, KeyError):
        print("Failed to decode JSON response for grammar correction.")
        return None  # Return None if grammar correction fails
