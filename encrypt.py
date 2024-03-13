from cryptography.fernet import Fernet
from dotenv import set_key, dotenv_values
import os

def encrypt_pass(ORIGINAL_PASSWORD:None, env:None):
    try:
        env_vars = dotenv_values(env)
        if 'ENCRYPTION_KEY' in env_vars:
            print("ENCRYPTION_KEY already exists in .env file.")
            key = env_vars['ENCRYPTION_KEY'].encode()
        else:
            key = Fernet.generate_key()
            set_key(env, 'ENCRYPTION_KEY', key.decode())

        cipher_suite = Fernet(key)
        original_password = env_vars[ORIGINAL_PASSWORD]
        encrypted_password = cipher_suite.encrypt(original_password.encode())
        set_key(env, 'ENCRYPTED_PASSWORD', encrypted_password.decode())

    except Exception as e:
        print(f"Error during encryption: {e}")

def get_password(ENCRYPTED_PASSWORD:None, env:None,ORIGINAL_PASSWORD:None):
    try:
        encrypt_pass(ORIGINAL_PASSWORD, env)
        env_vars = dotenv_values(env)
        encryption_key = env_vars['ENCRYPTION_KEY']
        encrypted_password = env_vars[ENCRYPTED_PASSWORD]

        if not encryption_key:
            raise ValueError("ENCRYPTION_KEY not found in .env")
        if not encrypted_password:
            raise ValueError("ENCRYPTED_PASSWORD not found in .env")

        cipher_suite = Fernet(encryption_key.encode())
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        return decrypted_password
    except Exception as e:
        print(f"Error during decryption: {e}")


pass_wd = get_password(ENCRYPTED_PASSWORD = 'ENCRYPTED_PASSWORD',ORIGINAL_PASSWORD='ORIGINAL_PASSWORD', env='.env')
print(f"decrypted password:{pass_wd}")

