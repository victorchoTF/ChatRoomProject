from random import random
from string import ascii_uppercase
from room_codes import room_codes
def generate_unique_code(length: int):
    code = ""

    while not code or code not in room_codes:
        for _ in range(length):
            code += random.choice(ascii_uppercase)
