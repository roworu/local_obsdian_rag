import os
import shutil
import time
from tqdm import tqdm
from .vault_preparation.translator import translate_to_english
from .vault_preparation.grammar import fix_grammar
from .vault_preparation.heading import extract_heading, reattach_heading

def process_note_with_retries(note_text, retries=5):
    heading, body = extract_heading(note_text)
    translation_failed = False
    grammar_failed = False

    for attempt in range(retries):
        translated_text = translate_to_english(body)
        if translated_text is None:
            print(f"Retrying translation (attempt {attempt + 1}/{retries})...")
            translation_failed = True
            time.sleep(1)  # Wait for a short period before retrying
            continue
        
        if translation_failed:
            print("Translation succeeded after retry.")
            translation_failed = False
        
        corrected_text = fix_grammar(translated_text)
        if corrected_text is None:
            print(f"Retrying grammar correction (attempt {attempt + 1}/{retries})...")
            grammar_failed = True
            time.sleep(1)  # Wait for a short period before retrying
            continue

        if grammar_failed:
            print("Grammar correction succeeded after retry.")
            grammar_failed = False
        
        final_text = reattach_heading(heading, corrected_text)
        return final_text

    print("Failed to process note after multiple attempts.")
    return note_text  # Return the original text if all attempts fail

def prepare_vault(vault_path, output_path):
    # Check if output_path exists and remove it if it does
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    # Create a new output_path directory
    os.makedirs(output_path)

    # Count total number of .md files for progress tracking
    total_files = sum([len(files) for _, _, files in os.walk(vault_path) if any(fname.endswith('.md') for fname in files)])
    
    # Initialize tqdm progress bar
    pbar = tqdm(total=total_files, desc='Processing notes', unit='file')

    # Traverse the vault_path and process each note
    for root, dirs, files in os.walk(vault_path):
        for dir_name in dirs:
            os.makedirs(os.path.join(output_path, os.path.relpath(os.path.join(root, dir_name), vault_path)), exist_ok=True)
        
        for file_name in files:
            if file_name.endswith('.md'):
                note_path = os.path.join(root, file_name)
                output_note_path = os.path.join(output_path, os.path.relpath(note_path, vault_path))

                with open(note_path, 'r') as f:
                    note_text = f.read()
                    processed_text = process_note_with_retries(note_text)

                with open(output_note_path, 'w') as f:
                    f.write(processed_text)

                # Update tqdm progress bar
                pbar.update(1)

    # Close tqdm progress bar
    pbar.close()