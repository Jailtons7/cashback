import string
import secrets


def generate_secret_key(n: int = 24):
    sec = string.digits + string.ascii_letters + string.ascii_uppercase + string.punctuation
    secret_key = ''.join(secrets.choice(sec) for _ in range(n))
    return secret_key
