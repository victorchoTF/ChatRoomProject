import random
from string import ascii_uppercase
from room_codes import room_codes
def generate_unique_code(length: int) -> str:
    code = ""

    while not code or code in room_codes:
        for _ in range(length):
            code += random.choice(ascii_uppercase)
    
    return code
