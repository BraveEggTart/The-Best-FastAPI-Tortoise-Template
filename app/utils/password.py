import hashlib
import logging

logger = logging.getLogger(__name__)


def encrypt_aes256(plain_text: str):
    hash_object = hashlib.sha256(plain_text.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex


def verify_password(
    plain_password: str,
    password: str
) -> bool:
    return password == encrypt_aes256(plain_password)
