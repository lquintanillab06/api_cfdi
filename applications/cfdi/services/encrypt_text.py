from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_text(text, key):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode('utf-8'))
    return encrypted_text

def decrypt_text(encrypted_text, key):
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode('utf-8')
    return decrypted_text
