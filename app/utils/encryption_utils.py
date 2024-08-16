# Libraries
import os

# Imports
from dotenv import load_dotenv, find_dotenv
from cryptography.fernet import Fernet

# Load .env variables
load_dotenv(find_dotenv())

# Initialize variables
key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(key)

# Encryption function
def encrypt_email(email):
    encrypted_email = cipher_suite.encrypt(email.encode())
    return encrypted_email

# Decryption function
def decrypt_email(encrypted_email):
    decrypted_email = cipher_suite.decrypt(encrypted_email).decode()
    return decrypted_email

# Example usage
# email = "user@example.com"
# encrypted_email = encrypt_email(email)
# print(f"Encrypted: {encrypted_email}")

# decrypted_email = decrypt_email(encrypted_email)
# print(f"Decrypted: {decrypted_email}")