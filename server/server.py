from flask import Flask, request, jsonify
from crypto_utils import (
    generate_rsa_keys,
    rsa_decrypt_key,
    aes_decrypt,
    verify_hmac,
    anomaly_detection
)

app = Flask(__name__)

# Generate RSA keys on server 
PRIVATE_KEY, PUBLIC_KEY = generate_rsa_keys()


@app.get("/public-key")
def public_key():
    return jsonify({"public_key": PUBLIC_KEY.decode()})


@app.post("/receive")
def receive_message():
    data = request.get_json()

    encrypted_session_key = data["encrypted_session_key"]
    iv = data["iv"]
    ciphertext = data["ciphertext"]
    hmac_tag = data["hmac"]

    # Decrypt AES key using RSA private key
    session_key = rsa_decrypt_key(PRIVATE_KEY, encrypted_session_key)

    #  Validate HMAC
    if not verify_hmac(session_key, hmac_tag, ciphertext):
        return jsonify({"status": "ERROR", "message": "HMAC validation failed"}), 400

    # Decrypt AES ciphertext
    decrypted_json = aes_decrypt(session_key, iv, ciphertext)

    #  Detect anomalies
    anomaly = anomaly_detection(decrypted_json)

    return jsonify({
        "status": "OK",
        "decrypted_message": decrypted_json,
        "anomaly_detected": anomaly
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
