from string import digits, ascii_uppercase

def _get_integer_in_range(prompt, range_start, range_end, out_of_range_message):
    """
    Checks for user input to be between range indicated by `range_start` and `range_end` returning `out_of_range_message` if input is not valid

    """
    while True:
        candidate = input(f"{prompt} (between {range_start} and {range_end}): ")

        try:
            spot = int(candidate)
            if spot >= range_start and spot <= range_end: return spot
            
            print(out_of_range_message)
        except ValueError:
            print("Number not valid!")

def get_valid_spot(max_range):
    return _get_integer_in_range(
        "Enter a parking spot",
        0, max_range,
        "Parking spot out of range!")

def _valid_license_plate(license):
    if len(license) != 7: return False

    for i in range(0, 4):
        if license[i] not in digits: return False
    
    for i in range(4, 7):
        if license[i] not in ascii_uppercase: return False

    return True


def get_licence_plate():

    while True:
        candidate = input("Enter a license plate (with format `0000AAA`): ")

        if _valid_license_plate(candidate): return candidate

        print("Invalid license plate, please ensure that you're using the given format.")

def get_menu_option(max_option):
    return _get_integer_in_range(
        "Enter an option",
        1, max_option,
        "Option out of range!")
