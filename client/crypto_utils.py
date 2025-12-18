from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64


# Encrypt JSON using AES CBC mode
def aes_encrypt(session_key, plaintext):
    data = plaintext.encode("utf-8")

    # PKCS7 padding
    pad_len = 16 - (len(data) % 16)
    data += bytes([pad_len]) * pad_len

    iv = get_random_bytes(16)
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(data)

    return (
        base64.b64encode(iv).decode(),
        base64.b64encode(ciphertext).decode()
    )


# RSA encrypt AES session key
def rsa_encrypt_key(public_key_pem, session_key):
    key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(key)
    encrypted_key = cipher_rsa.encrypt(session_key)
    return base64.b64encode(encrypted_key).decode()


# Create HMAC signature
def create_hmac(session_key, ciphertext_b64):
    ciphertext_bytes = base64.b64decode(ciphertext_b64)

    h = HMAC.new(session_key, digestmod=SHA256)
    h.update(ciphertext_bytes)
    return base64.b64encode(h.digest()).decode()
