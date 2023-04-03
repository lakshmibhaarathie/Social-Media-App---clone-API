from passlib.context import CryptContext

def pwd_encrypt(password:str):
    pwd_hasher = CryptContext(schemes=['bcrypt'])
    encrypted_password = pwd_hasher.hash(password)
    
    return encrypted_password
