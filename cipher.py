import hashlib
import string

# Caesar Salad: Way better Caesar cipher (totally safe)...

char_map = string.printable

def calc_secret_hash():
    with open("keys/shared.bin", 'rb') as f:
        bytes = f.read()
        hash = hashlib.sha512(bytes).hexdigest()
        return hash

class CaesarSalad:
    def __init__(self):
        pass

    def cs_encode(self, msg):
        encoded = ""
        hash = calc_secret_hash()
        while True:
            if len(msg) > len(hash):
                hash += hash
            else:
                break
        msg_index = 0
        for char in msg:
            if char == " ":
                encoded += " "
                continue
            else:
                index = char_map.index(char)
                raw_offset = ord(hash[msg_index])
                if (raw_offset > len(char_map)):
                    mod_offset = raw_offset % len(char_map)
                    new_index = index + mod_offset
                    if new_index > len(char_map)-1:
                        new_index = new_index - len(char_map)
                    new_char = char_map[new_index]
                    encoded += new_char
                else:
                    new_index = index + raw_offset
                    if new_index > len(char_map)-1:
                        new_index = new_index - len(char_map)
                    new_char = char_map[new_index]
                    encoded += new_char
            msg_index += 1
        return encoded


    def cs_decode(self, msg):
        decoded = ""
        hash = calc_secret_hash()
        while True:
            if len(msg) > len(hash):
                hash += hash
            else:
                break
        msg_index = 0
        for char in msg:
            if char == " ":
                decoded += " "
                continue
            else:
                index = char_map.index(char)
                raw_offset = ord(hash[msg_index])
                if (raw_offset > len(char_map)):
                    mod_offset = raw_offset % len(char_map)
                    new_index = index - mod_offset
                    if (new_index < 0):
                        new_index = len(char_map) + new_index
                    new_char = char_map[new_index]
                    decoded += new_char
                else:
                    new_index = index - raw_offset
                    if (new_index < 0):
                        new_index = len(char_map) + new_index
                    new_char = char_map[new_index]
                    decoded += new_char
            msg_index += 1
        return decoded

