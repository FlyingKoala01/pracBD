import re

def valid_phone(phone_number):
    pattern = r'^(\+|00)[1-9][0-9 \-\(\)\.]{7,32}$'
    print("PHONE" + phone_number)
    return (re.match(pattern, phone_number))

    
def valid_name(name):
    print("Oops")
    pattern ='^[a-zA-Z0-9 ]*$'
    
    return (re.match(pattern, name))
