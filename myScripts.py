import requests
import json
import re
import base64
import msgpack

# Function to decrypt the ASCII values to a string
def decrypt_ascii_to_string(ascii_values):
    return ''.join(chr(value) for value in ascii_values)

# Function to remove non-hex characters
def remove_non_hex_chars(s):
    return ''.join(re.findall(r'[0-9a-f]', s))

def undo_circular_left_rotation(s, n):
    length = len(s)
    # Rotating left by n is equivalent to rotating right by length - n
    n = n % length  # Ensure n is within the bounds of the string length
    return s[-n:] + s[:-n]

def decrypt_custom_hex(encoded_string, custom_set):
    # Create a dictionary to map custom hex characters back to standard hex characters
    standard_hex = '0123456789abcdef'
    custom_to_standard = {custom_set[i]: standard_hex[i] for i in range(16)}
    
    # Decrypt the encoded string
    decoded_string = ''.join(custom_to_standard[char] for char in encoded_string)
    return decoded_string

def unscramble(encrypted_string, base64_messagepack):
    # Decode the base64 string to get the MessagePack data
    messagepack_data = base64.b64decode(base64_messagepack)

    # Unpack the MessagePack data to get the original positions
    original_positions = msgpack.unpackb(messagepack_data)

    # Initialize a list of the same length as the encrypted string
    unscrambled = [''] * len(encrypted_string)

    # Place each character in its original position
    for original_index, scrambled_index in enumerate(original_positions):
        unscrambled[scrambled_index] = encrypted_string[original_index]

    # Join the list into the final unscrambled string
    return ''.join(unscrambled)


# Initial API call (replace this with your actual endpoint if needed)


def api_path(data):
    level = data['level']

    
    if level == 0:
        enc_path = data['encrypted_path']
        return enc_path
    
    elif level == 1:
        enc_path = data['encrypted_path']
        ext_val = json.loads(enc_path.split("task_")[1])
        decrypted_path = decrypt_ascii_to_string(ext_val)
        return "task_" + decrypted_path 
        
    elif level == 2:
        enc_path = data['encrypted_path']
        ext_val = enc_path.split("task_")[1]
        decrypted_path = remove_non_hex_chars(ext_val)
        return "task_" + decrypted_path 
    
    elif level == 3:
        enc_path = data['encrypted_path']
        ext_val = enc_path.split("task_")[1]
        v = int(data['encryption_method'][-2:])
        decrypted_path = undo_circular_left_rotation(ext_val, v)
        return "task_" + decrypted_path
    
    elif level == 4:
        enc_path = data['encrypted_path']
        ext_val = enc_path.split("task_")[1]
        v = data['encryption_method'][-16:]
        decrypted_path = decrypt_custom_hex(ext_val, v)
        return "task_" + decrypted_path
    
    elif level == 5:
        enc_path = data['encrypted_path']
        ext_val = enc_path.split("task_")[1]
        v = data['encryption_method'][-48:]
        decrypted_path = unscramble(ext_val, v)
        return "task_" + decrypted_path

    else:
        return "I Did it Anyways...!" 
        

def my_url(api_path):
    url = f"https://ciphersprint.pulley.com/{api_path}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 
    
    
api_data = my_url("dhanushbraj04@gmail.com")

while (api_data):
    local_var = api_path(api_data)

    api_data = my_url(local_var)

    print(api_data)
    print("\n")

print("I Did It....!")
