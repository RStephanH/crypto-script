import func
import os
import subprocess

class Cipher:
    """Model of cipher"""
    def __init__(self, cipher_name):
        self.name=cipher_name

        if self.name == "-aes-256-cbc":
            #Generate the key and the initial vector
            self.option={
                'key':os.urandom(32),
                'iv':os.urandom(16)
            }


class Encryption:
    """Model of encryption """
    def __init__(self):
        self.concern_file=func.choose_file()
        self.cipher=Cipher(str(func.encryption_method()))
    
    def te(self):
        if "key" in self.cipher.option:
            print("dictionaries works fine")

    def encrypt(self):

        #Create the file for the key and initial vector
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
        
        # subprocess.run(
        #     [
        #         "openssl",
        #         "enc",
        #         self.cipher.name,
        #         "-salt",
        #         "-in",
        #         self.concern_file,
        #         "-out",
        #         self.concern_file+".enc",
        #         "-K",
        #         "$(xxd",
        #         "-p",
        #         self.concern_file+".key",
        #         "|",
        #         "tr",
        #         "-d",
        #         "'\n')",
        #         "-iv",
        #         "$(xxd",
        #         "-p",
        #         self.concern_file+".iv",
        #         "|",
        #         "tr",
        #         "-d",
        #         "'\n')"
        #
        #     ]
        # )

    def decrypt(self):
        pass


f=Encryption()
f.encrypt()
