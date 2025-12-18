# CMPSC 497 Project-2: Secure Full-Stack Messaging Application  
Author: Brandon Ginn (blg5403)

This project implements a fully secure end-to-end messaging system using Python for both the **Client Application** and the **Server API**. The goal is to demonstrate encryption, authentication, serialization, and secure protocol handling.

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

# Installation & Running
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
# Expected Output

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
# Conclusion

This Python-based system successfully demonstrates secure full-stack messaging, implementing all cryptographic and software engineering requirements for CMPSC 497 Project-2.

