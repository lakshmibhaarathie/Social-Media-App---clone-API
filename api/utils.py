from passlib.context import CryptContext


class EnDec:
    pwd_hasher = CryptContext(schemes=['bcrypt']
                            , deprecated="auto")
    
    @staticmethod
    def pwd_encrypt(password:str):
        encrypted_password = EnDec.pwd_hasher.hash(password)
        
        return encrypted_password
   
    @staticmethod
    def password_verification(current_password, encrypted_password):
        verified = EnDec.pwd_hasher.verify(current_password, encrypted_password)

        return verified