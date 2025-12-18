from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import HMAC, SHA256
import base64
import json


def generate_rsa_keys():
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()


def rsa_decrypt_key(private_key_pem, encrypted_session_key_b64):
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_bytes = base64.b64decode(encrypted_session_key_b64)
    return cipher.decrypt(encrypted_bytes)


def aes_decrypt(session_key, iv_b64, ciphertext_b64):
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    # remove PKCS7 padding
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode()
    

def verify_hmac(session_key, hmac_b64, ciphertext_b64):
    expected_hmac = base64.b64decode(hmac_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    h = HMAC.new(session_key, digestmod=SHA256)
    h.update(ciphertext)

    try:
        h.verify(expected_hmac)
        return True
    except ValueError:
        return False


def anomaly_detection(json_string):
    allowed_fields = {"name", "age", "major", "psu_id"}

    try:
        obj = json.loads(json_string)
    except:
        return True

    return not all(key in allowed_fields for key in obj)
