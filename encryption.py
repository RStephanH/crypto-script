import func
import os

class Cipher:
    """Model of cipher"""
    def __init__(self, cipher_name):
        self.name=cipher_name

        if cipher_name == "-aes-256-cbc":
            self.option={
                "key":str(os.urandom(32)),
                "iv":str(os.urandom(16))
                }


class Encryption:
    """Model of encryption """
    def __init__(self):
        self.concern_file=func.choose_file()
        self.cipher=Cipher(func.encryption_method())

    def encrypt(self):
        pass

    def decrypt(self):
        pass


f=Encryption()
print(f.cipher.option["key"])
