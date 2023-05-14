import re, os, string

def valid_phone(phone_number):
    pattern = '^[0-9]+$'#r'^(\+|00)[1-9][0-9 \-\(\)\.]{7,32}$'
    return bool(re.match(pattern, phone_number))

    
def valid_name(name):
    pattern ='^[a-zA-Z0-9 ]+$'
    return bool(re.match(pattern, name))


def valid_image(filename):
    """
    Returns True if the given filename has an image extension
    """
    if filename == '': return False
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    return os.path.isfile(filename) and any(filename.lower().endswith(ext) for ext in image_extensions)
