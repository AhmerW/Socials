import secrets

def generate(length = 12):
    return secrets.token_hex(length)