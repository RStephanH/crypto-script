from sys import exit
import func
import os
import subprocess

class Cipher():
    """Model of cipher"""
    def __init__(self, cipher_name,passphrase=None):
        self.name=cipher_name
        self.passphrase=passphrase


class Encryption():
    """Model of encryption """
    def __init__(self,type_enc):

        self.concern_file=func.choose_file()

        #value type_enc= "Symmetric"/"Asymmetric"
        if type_enc.lower()=="symmetric":
            self.cipher=Cipher(*func.get_symmetric_algorithm())
        elif type_enc.lower()=="asymmetric":
            self.cipher=Cipher(*func.get_asymmetric_algorithm())
    
        #Encrypt
    def sym_encrypt(self):

        if (self.cipher.name == "-aes-256-cbc"
            and self.cipher.passphrase== None):
            #Generate the key and the initial vector
            self.key=os.urandom(32)
            self.iv=os.urandom(16)


        #Create the file for the key and initial vector
        if self.cipher.passphrase==None:
            try:
                with open(self.concern_file+".key",'wb') as enc_key:
                    enc_key.write(self.key)
                print("Key created")
            except IOError as e:
                print(f"Error saving the key: {e}")

            #Create the file for the initial vector
            try:
                with open(self.concern_file+".iv",'wb') as enc_iv:
                    enc_iv.write(self.iv)
                print("IV created")
            except IOError as e:
                print(f"Error saving the IV: {e}")

            #Translate the binary format into hex
            hex_key=self.key.hex()
            hex_iv=self.iv.hex()

            #Define the encryption command
            cmd=[
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

        elif self.cipher.passphrase is not None:
            cmd=[
                'openssl',
                'enc',
                '-aes-256-cbc',
                '-salt',
                '-pbkdf2',
                '-iter',
                '100000',
                '-in',
                self.concern_file,
                '-out',
                self.concern_file+".enc",
                '-k',
                self.cipher.passphrase
            ]
        else:
            print("Error with the passphrase")
            exit(1)
        subprocess.run(cmd,check=True)
        print("Operation success")

        
    def asym_encryp(self):
        pass

    def sym_decrypt(self):
        print(f"The file to decrypt is {self.concern_file}")
        if self.cipher.name=="-aes-256-cbc":

            if self.cipher.passphrase is not None:
                cmd=[
                    'openssl',
                    'enc',
                    '-d',
                    '-aes-256-cbc',
                    '-salt',
                    '-pbkdf2',
                    '-iter',
                    '100000',
                    '-in',
                    self.concern_file,
                    '-out',
                    self.concern_file+".out",
                    '-k',
                    self.cipher.passphrase
                ]

            elif self.cipher.passphrase is None:
                #Getting the key
                #Getting the name of the key file
                key_file_name=func.choose_file("Enter the key file")

                key_size=256
                key_bin=bytes()
                #open the key file
                with open(key_file_name,'rb') as key_file:
                    while chunk:=key_file.read(key_size):
                        key_bin += chunk #Assign the contents of the file into key_bin
                key_hex=key_bin.hex()

                #Getting the IV
                iv_file_name=func.choose_file("Enter the IV file")

                iv_size=128
                iv_bin=bytes()

                with open(iv_file_name,'rb') as iv_file:
                    while chunk_iv:=iv_file.read(key_size):
                        iv_bin += chunk_iv #Assign the contents of the file into key_bin
                iv_hex=iv_bin.hex()

                cmd=[
                    "openssl",
                    "enc",
                    "-d",
                    self.cipher.name,
                    "-salt", "-in",
                    self.concern_file,"-out",
                    self.concern_file+".out",
                    "-K",
                    key_hex,
                    "-iv",
                    iv_hex
                ]

        subprocess.run(cmd,check=True)

        print("Decryption ended")




