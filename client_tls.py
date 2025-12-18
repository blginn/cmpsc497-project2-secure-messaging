
import argparse
import socket
import ssl
import sys
from datetime import datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="localhost", help="Server hostname")
    ap.add_argument("--port", type=int, default=8443, help="Server TLS port")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--ca", help="Path to PEM CA/server cert to trust")
    g.add_argument("--insecure", action="store_true",
                   help="Disable certificate verification (like curl -k)")
    args = ap.parse_args()

    print("=== Python TLS Client ===")
    print(f"[{datetime.now()}] Connecting to {args.host}:{args.port}")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    if args.insecure:
        # Self-signed demo: skip verification (assignment mentions curl -k)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        print("Certificate verification: DISABLED (demo / -k mode)")
    else:
        if args.ca:
            context.load_verify_locations(args.ca)
            context.check_hostname = False  # OK for self-signed server cert
            context.verify_mode = ssl.CERT_REQUIRED
            print(f"Certificate verification: ENABLED (trust {args.ca})")
        else:
            # Default system CAs
            context.load_default_certs()
            context.verify_mode = ssl.CERT_REQUIRED
            print("Certificate verification: ENABLED (system CAs)")

    request = (
        f"GET /index.html HTTP/1.1\r\n"
        f"Host: {args.host}\r\n"
        f"User-Agent: cmpsc497-tls-client/1.0\r\n"
        f"Connection: close\r\n\r\n"
    ).encode("utf-8")

    with socket.create_connection((args.host, args.port)) as sock:
        with context.wrap_socket(sock, server_hostname=args.host) as tls:
            print(f"TLS version: {tls.version()}")
            print(f"Cipher: {tls.cipher()}")
            print(f"Peer cert subject: {tls.getpeercert().get('subject', 'N/A')}")
            print("\n--- Sending HTTPS request ---")
            tls.sendall(request)

            print("--- Response start ---")
            chunks = []
            while True:
                data = tls.recv(4096)
                if not data:
                    break
                chunks.append(data)
            resp = b"".join(chunks).decode("utf-8", errors="replace")
            print(resp)
            print("--- Response end ---")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
