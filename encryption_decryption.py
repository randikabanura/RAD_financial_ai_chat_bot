import configparser

from cryptography.fernet import Fernet


# Decrypt the value
def decrypt_value(key, encrypted_value):
    fernet = Fernet(key)
    decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()
    return decrypted_value

