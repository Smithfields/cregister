def validate_string(my_str):
    try:
        my_str = str(my_str).strip()
    except Exception as e:
        return None

    return None if my_str == "" else my_str


def validate_int(my_int):
    try:
        my_int = int(validate_string(my_int)) # insuring it's a string before casting it to a float
    except Exception:
        return None
    return my_int


def validate_float(my_float):
    try:
        my_float = float(validate_string(my_float)) # insuring it's even a string before casting it to a float
    except Exception:
        return None
    return my_float
