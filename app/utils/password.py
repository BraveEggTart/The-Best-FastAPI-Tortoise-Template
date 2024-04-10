import os
import json

from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from Crypto.Random import get_random_bytes
from passlib import pwd
from passlib.context import CryptContext
from hashlib import pbkdf2_hmac
from base64 import b64decode, b64encode

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_password() -> str:
    return pwd.genword()


def decrypt(ciphertext):
    salted = b64decode(ciphertext)
    salt = salted[:8]
    ctext = salted[8:]
    key = pbkdf2_hmac('sha1', SECRET_KEY.encode('utf-8'), salt, 1000, dklen=32)
    cipher = AES.new(key, AES.MODE_CBC, IV=salt)
    plaintext = unpad(cipher.decrypt(ctext), AES.block_size)
    return plaintext


def encrypt(data):
    salt = get_random_bytes(8)
    key = pbkdf2_hmac('sha1', SECRET_KEY.encode('utf-8'), salt, 1000, dklen=32)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    data = json.dumps(data)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    ct = b64encode(salt + iv + ct_bytes).decode('utf-8')
    return ct
