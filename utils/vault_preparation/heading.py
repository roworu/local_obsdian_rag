import re

def extract_heading(note_text):
    match = re.match(r'^(---\n(?:.*\n)*?---\n)', note_text)
    if match:
        heading = match.group(1)
        body = note_text[len(heading):]
        return heading, body
    return '', note_text

def reattach_heading(heading, body):
    return heading + body