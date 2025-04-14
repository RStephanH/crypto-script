import func
import os
import subprocess

class Cipher:
    """Model of cipher"""
    def __init__(self, cipher_name,passphrase=None):
        self.name=cipher_name
        self.passphrase=passphrase

        if (self.name == "-aes-256-cbc"
            and self.passphrase== None):
            #Generate the key and the initial vector
            self.option={
                'key':os.urandom(32),
                'iv':os.urandom(16)
            }


class Encryption:
    """Model of encryption """
    def __init__(self):
        self.concern_file=func.choose_file()
        self.cipher=Cipher(*func.encryption_method())
    
    def encrypt(self):

        #Create the file for the key and initial vector
        if self.cipher.passphrase==None:
            try:
                with open(self.concern_file+".key",'wb') as enc_key:
                    enc_key.write(self.cipher.option['key'])
                print("Key created")
            except IOError as e:
                print(f"Error saving the key: {e}")

            #Create the file for the initial vector
            try:
                with open(self.concern_file+".iv",'wb') as enc_iv:
                    enc_iv.write(self.cipher.option['iv'])
                print("IV created")
            except IOError as e:
                print(f"Error saving the IV: {e}")

            #Translate the binary format into hex
            hex_key=self.cipher.option['key'].hex()
            hex_iv=self.cipher.option['iv'].hex()
            print(f"hex_key: {hex_key}\n"
                f"hex_iv: {hex_iv}")
        
            subprocess.run(
                [
                    "openssl",
                    "enc",
                    self.cipher.name,
                    "-salt",
                    "-in",
                    self.concern_file,
                    "-out",
                    self.concern_file+".enc",
                    "-K",
                    hex_key,
                    "-iv",
                    hex_iv
                ]
            )

    def decrypt(self):
        pass


f=Encryption()
f.encrypt()
