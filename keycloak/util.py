from base64 import urlsafe_b64decode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat import backends


def b64urldecode(string):
    length = len(string) % 4
    if length == 2:
        string += b"=="
    elif length == 3:
        string += b"="
    elif length == 1:
        raise Exception("Illegal base64url string!")

    return urlsafe_b64decode(string)


def rsapubkey_from_bytes(e, n):
    if isinstance(e, str):
        e = e.encode('ascii')
    if isinstance(n, str):
        n = n.encode('ascii')

    e_ = int.from_bytes(b64urldecode(e), 'big')
    n_ = int.from_bytes(b64urldecode(n), 'big')

    rsanum = rsa.RSAPublicNumbers(e=e_, n=n_)
    return rsanum.public_key(backends.default_backend())
