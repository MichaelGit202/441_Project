#this is to santize rag stuff


file_path = 'C:/dev/441_python/project_1/441_Project/project/util/rag_documents/Item Reference.txt'  # Replace with the actual path


import os
import string

def sanitize_text(text):
    # Keep printable ASCII and common whitespace (tabs, newlines)
    allowed = set(string.printable) | {'\n', '\r', '\t'}
    return ''.join(c if c in allowed else '?' for c in text)

def sanitize_file(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    # Try UTF-8, then fallback to latin-1
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("Read file with UTF-8.")
    except UnicodeDecodeError:
        with open(input_path, 'r', encoding='latin-1') as f:
            content = f.read()
        print("Read file with latin-1 (fallback).")

    clean_content = sanitize_text(content)

    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_sanitized{ext}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)

    print(f"Sanitized file saved to: {output_path}")

# Example usage
if __name__ == "__main__":

    sanitize_file(file_path)
