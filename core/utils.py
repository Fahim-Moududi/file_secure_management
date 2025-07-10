from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FILE_ENCRYPTION_KEY)

def encrypt_file(data):
    return fernet.encrypt(data)

def decrypt_file(data):
    return fernet.decrypt(data)
