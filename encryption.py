from sys import exit
from simple_term_menu import TerminalMenu
import func
import os
import re
import subprocess



class Encryption():
    """Model of encryption """
    def __init__(self):

        self.concern_file=func.choose_file()

        #value type_enc= "Symmetric"/"Asymmetric"
        if type_enc.lower()=="symmetric":
            pass
        elif type_enc.lower()=="asymmetric":
            self.cipher=Encryption.get_asymmetric_algorithm()



    @classmethod
    def get_asymmetric_algorithm(cls):
        cmd=['openssl', 'list', '-public-key-algorithms']
        output= subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        algorithms=set()
        for line in output.stdout.strip().splitlines():
            match = re.search(r'PEM string:\s*(\S+)', line)
            if match:
                algorithms.add(match.group(1))

        algorithms=sorted(algorithms)
        algorithms_menu=TerminalMenu(algorithms)
        algorithm_index=algorithms_menu.show()
        algorithm=algorithms[algorithm_index]

        return algorithm


        
    def asym_encryp(self):
        pass

    def sym_decrypt(self):
        print(f"The file to decrypt is {self.concern_file}")
        # if self.cipher=="-aes-256-cbc":

        if self.passphrase is not None:
            cmd=[
                'openssl',
                'enc',
                '-d',
                "-"+self.cipher,
                '-salt',
                '-pbkdf2',
                '-iter',
                '100000',
                '-in',
                self.concern_file,
                '-out',
                self.concern_file+".out",
                '-k',
                self.passphrase
            ]

        elif self.passphrase is None:
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
                while chunk_iv:=iv_file.read(iv_size):
                    iv_bin += chunk_iv #Assign the contents of the file into key_bin
            iv_hex=iv_bin.hex()

            cmd=[
                "openssl",
                "enc",
                "-d",
                "-"+self.cipher,
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


    def asym_decrypt(self,prv_key):
        pass


class Hash():
    @classmethod
    def get_hash_algorithm(cls):
        cmd=[
            "openssl",
            "list",
            "-digest-commands"
        ]
        output=subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        outputs=output.stdout.split()
        menu_algorithm=TerminalMenu(outputs,title="Choose the algorithm:")
        algorithm_index=menu_algorithm.show()
        return outputs[algorithm_index]

    def __init__(self,algo,file):
        self.algorithm=algo
        self.file=file
    def create_hash(self):
        cmd=[
            "openssl",
            "dgst",
            self.algorithm,
            "-in",
            self.file,
            "-out",
            self.file+".hash"
        ]
        subprocess.run(cmd,check=True)

class Symmetric_Encryption(Encryption):
    def __init__(self):
        super().__init__():
        self.cipher=Symmetric_Encryption.get_symmetric_algorithm()
        self.passphrase=func.passphrase_generator()
        self.mode=Symmetric_Encryption.detect_mode(self.cipher)

    @classmethod
    def get_symmetric_algorithm(cls):

        output=subprocess.run(
            ['openssl','list','-cipher-commands'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        ciphers=output.stdout.split()

        ciphers_menu=TerminalMenu(ciphers,title="Choose the algorithm")
        cipher_index=ciphers_menu.show()
        cipher=ciphers[cipher_index]

        return cipher

    @classmethod
    def detect_mode(cls,string):
        # Define the regex pattern to match the specified formats
        pattern = r'^(.*?)-(\d+)?-(.*?)(cbc|cfb|ofb|ctr)(.*)$'
        
        # Search for the pattern in the input string
        match = re.search(pattern, string)
        
        if match:
            # If a match is found, return the detected mode
            return match.group(4)  # The mode (CBC, CFB, OFB, CTR)
            # return True
        
        return None  # Return None if no mode is detected

    @classmethod
    def generate_iv(cls):
        iv=os.urandom(16)
        hex_iv=iv.hex()
        return iv,hex_iv

    @classmethod
    def generate_key(cls,size):
        key=os.urandom(size)
        hex_key=key.hex()
        return key,hex_key

        #Encrypt
    def encrypt(self):
        # if (self.cipher == "-aes-256-cbc"
        #     and self.passphrase== None):
        #     #Generate the key and the initial vector
        #     self.key=os.urandom(32)


        #Create the file for the key and initial vector
        if (self.passphrase==None 
                and self.mode is not None ):
            #Create the file for the initial vector
            self.iv,self.hex_iv=Symmetric_Encryption.generate_iv()
            try:
                with open(self.concern_file+".iv",'wb') as enc_iv:
                    enc_iv.write(self.iv)
                print("IV created")
            except IOError as e:
                print(f"Error saving the IV: {e}")
            #Create the key and the file to store the key
            try:
                with open(self.concern_file+".key",'wb') as enc_key:
                    enc_key.write(self.key)
                print("Key created")
            except IOError as e:
                print(f"Error saving the key: {e}")


            #Translate the binary format into hex
            hex_key=self.key.hex()

            #Define the encryption command
            cmd=[
                    "openssl",
                    "enc",
                    "-"+self.cipher,
                    "-salt",
                    "-in",
                    self.concern_file,
                    "-out",
                    self.concern_file+".enc",
                    "-K",
                    hex_key,
                    "-iv",
                    self.hex_iv
                ]

        elif self.passphrase is not None:
            cmd=[
                'openssl',
                'enc',
                "-"+self.cipher,
                '-salt',
                '-pbkdf2',
                '-iter',
                '100000',
                '-in',
                self.concern_file,
                '-out',
                self.concern_file+".enc",
                '-k',
                self.passphrase
            ]
        else:
            print("Error with the passphrase")
            exit(1)
        subprocess.run(cmd,check=True)
        print("Operation success")
