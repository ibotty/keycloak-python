from base64 import urlsafe_b64decode
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat import backends


def base64_urldecode(string):
    length = len(string) % 4

    if length == 2:
        string += b"=="
    elif length == 3:
        string += b"="
    elif length == 1:
        raise Exception("Illegal base64url string!")

    return urlsafe_b64decode(string)

#
# def rsa_pubkey_from_bytes(e, n):
#     if isinstance(e, str):
#         e_bytes = e.encode('ascii')
#     if isinstance(n, str):
#         n_bytes = n.encode('ascii')
#
#     e_int = int.from_bytes(base64_urldecode(e_bytes), 'big')
#     n_int = int.from_bytes(base64_urldecode(n_bytes), 'big')
#
#     rsa_num = rsa.RSAPublicNumbers(e=e_int, n=n_int)
#
#     return rsa_num.public_key(backends.default_backend())
