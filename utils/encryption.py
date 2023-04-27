import json
import os

from Crypto.Cipher import AES

import settings


class ReplayAttackException(Exception):
    pass


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def format_secret(args):
    if isinstance(args.key, str):
        pwd = args.key.encode()
    else:
        pwd = args.key()
    if len(pwd) not in [16, 24, 32]:
        raise ValueError(f"The length of key is {len(pwd)} but it should be 16, 24 or 32.")
    args.key = pwd
    print(f"Encryption mode: AES-{len(pwd) * 8}-GCM")
    print(f"Encryption key : {pwd.decode()}")


def encrypt(message: bytes | str):
    if isinstance(message, str):
        message = message.encode()
    iv = os.urandom(16)
    cipher = AES.new(settings.key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return json.dumps({
        'iv': iv.hex(),
        'ciphertext': ciphertext.hex(),
        'tag': tag.hex()
    })


def decrypt(ciphertext: str):
    data = json.loads(ciphertext)
    iv = bytes.fromhex(data['iv'])
    ciphertext = bytes.fromhex(data['ciphertext'])
    tag = bytes.fromhex(data['tag'])
    cipher = AES.new(settings.key, AES.MODE_GCM, nonce=iv)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()
