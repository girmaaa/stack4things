import secrets

def generate_token():
    return secrets.token_urlsafe(16)  # Generate a URL-safe token of length 16

if __name__ == "__main__":
    token = generate_token()
    print(f"Generated token: {token}")
