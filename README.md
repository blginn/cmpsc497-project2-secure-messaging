# CMPSC 497 Project-2: Secure Full-Stack Messaging Application  
Author: Brandon Ginn (blg5403)

This project implements a fully secure end-to-end messaging system using Python for both the **Client Application** and the **Server API**. The goal is to demonstrate encryption, authentication, serialization, and secure protocol handling.


# Security Features Implemented

###  RSA (Public-Key Cryptography)
Used to **encrypt the AES symmetric key** during session establishment.

###  AES-256 (Symmetric Encryption)
Used to **encrypt the Student JSON message** for fast, secure communication.

###  HMAC-SHA256 (Integrity Validation)
Ensures the encrypted data was **not modified** in transit.

###  Base64 Encoding
All encrypted bytes are **Base64-encoded** for safe transmission over HTTP.

###  JSON Serialization
The Student object is serialized into a JSON string before encryption.

###  REST API Server
Built using Flask.  
Provides two endpoints:
- `/public-key` — returns RSA public key  
- `/receive` — accepts encrypted message, decrypts it, validates HMAC, checks anomalies

---

#  Project Structure

```
project2-secure-messaging/
│
├── client/
│   ├── client.py
│   ├── crypto_utils.py
│   ├── student.py
│   └── requirements.txt
│
└── server/
    ├── server.py
    ├── crypto_utils.py
    └── requirements.txt
```

---

# 🚀 How the System Works (End-to-End)

1. **Client fetches server’s RSA public key**
2. Client constructs a `Student` object → serializes → JSON
3. Client generates a **32-byte AES key**
4. Client encrypts the JSON message using **AES-CBC**
5. Client encrypts the AES key using **RSA**
6. Client computes an **HMAC** over the ciphertext
7. Client sends:
   - encrypted AES key  
   - AES IV  
   - ciphertext  
   - HMAC  
   to the server
8. **Server decrypts RSA → retrieves AES key**
9. Server validates the HMAC
10. Server decrypts the AES ciphertext
11. Server performs **anomaly detection**
12. Server returns decrypted message + anomaly result

---

# 📦 Installation & Running

## Server Setup
```bash
cd server
pip install -r requirements.txt
python server.py
```

Server starts on:

```
http://127.0.0.1:5000
```

## Client Setup
```bash
cd client
pip install -r requirements.txt
python client.py
```

---

# 🧪 Expected Output

# Client:
```
Received server public key.
Serialized student: {"name":"Brandon Ginn","age":22,"major":"Computer Science","psu_id":"blg5403"}

Sending encrypted secure message...

Server response:
{
  "status": "OK",
  "decrypted_message": "{...}",
  "anomaly_detected": false
}
```

### Server:
```
Decrypted message:
{"name":"Brandon Ginn", "age":22, ...}
Anomaly Detected: False
```

---

# 🎥 Requirements for Video Demo

Your video must show:
- Folder structure  
- Server code (RSA/AES/HMAC logic)  
- Client code  
- Server running  
- Client sending encrypted payload  
- Response from server  
- GitHub repository  



# Conclusion

This Python-based system successfully demonstrates secure full-stack messaging, implementing all cryptographic and software engineering requirements for CMPSC 497 Project-2.

