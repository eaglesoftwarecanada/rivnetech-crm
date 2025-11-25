import base64
import hashlib

from cryptography.fernet import Fernet
from django.conf import settings


def _get_fernet() -> Fernet:
    digest = hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_str(plain: str | None) -> str | None:
    if plain is None:
        return None
    f = _get_fernet()
    token = f.encrypt(plain.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_str(token: str | None) -> str | None:
    if token is None:
        return None
    f = _get_fernet()
    plain = f.decrypt(token.encode("utf-8"))
    return plain.decode("utf-8")