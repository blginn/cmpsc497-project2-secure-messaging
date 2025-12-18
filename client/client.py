import requests
from Crypto.Random import get_random_bytes
from student import Student
from crypto_utils import aes_encrypt, rsa_encrypt_key, create_hmac

SERVER_URL = "http://127.0.0.1:5000"

# Get server public key
response = requests.get(f"{SERVER_URL}/public-key")
public_key = response.json()["public_key"]
print("Received server public key.")

# Create Student object
student = Student("Brandon Ginn", 22, "Computer Science", "blg5403")
json_data = student.to_json()
print("Serialized student:", json_data)

#  Generate AES session key
session_key = get_random_bytes(32)  # AES-256 key

# Encrypt AES session key using RSA public key
encrypted_session_key = rsa_encrypt_key(public_key, session_key)

# Encrypt JSON using AES
iv, ciphertext = aes_encrypt(session_key, json_data)

#  Compute HMAC for ciphertext integrity
hmac_tag = create_hmac(session_key, ciphertext)

payload = {
    "encrypted_session_key": encrypted_session_key,
    "iv": iv,
    "ciphertext": ciphertext,
    "hmac": hmac_tag
}

print("Sending encrypted secure message...")
resp = requests.post(f"{SERVER_URL}/receive", json=payload)

print("\nServer response:")
print(resp.json())
