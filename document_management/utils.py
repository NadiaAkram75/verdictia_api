from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_SECRET)

def encrypt_file_content(content: bytes) -> bytes:
    return fernet.encrypt(content)

def decrypt_file_content(token: bytes) -> bytes:
    return fernet.decrypt(token)
