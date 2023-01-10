def clean_string(string: str):
    bad_chars = [' ', '.', '/']
    clean_str = string.lower()
    for char in bad_chars:
        clean_str = clean_str.replace(char, '_')
    return clean_str