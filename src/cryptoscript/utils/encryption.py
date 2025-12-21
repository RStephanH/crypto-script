from sys import exit
from simple_term_menu import TerminalMenu
from .func import choose_file
from .func import passphrase_generator
import os
import re
import subprocess



class Encryption():
    """Model of encryption """
    def __init__(self):
        self.concern_file=choose_file()

    def asym_encryp(self):
        pass

    def asym_decrypt(self,prv_key):
        pass

class Hash(Encryption):
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

    def __init__(self):
        super().__init__()
        self.algorithm=Hash.get_hash_algorithm()

    def create_hash(self):
        cmd=[
            "openssl",
            "dgst",
            "-"+self.algorithm,
            "-out",
            self.concern_file+".hash",
            self.concern_file,
        ]
        subprocess.run(cmd,check=True)

        return True

    def sign_hash(self):
        private_key=choose_file("Enter the private key:")
        cmd=[
            'openssl',
            'dgst',
            '-'+self.algorithm,
            '-sign',
            private_key,
            '-out',
            'signature.bin',
            self.concern_file,
        ]
        subprocess.run(cmd,check=True)

        return True

    def verify_hash(self):
        public_key=choose_file("Enter the public key:")
        signature=choose_file("Enter the signature:")
        cmd=[
            'openssl',
            'dgst',
            '-'+self.algorithm,
            '-verify',
            public_key,
            '-signature',
            signature,
            self.concern_file,
        ]
        subprocess.run(cmd,check=True)

        return True


class Symmetric_Encryption(Encryption):
    def __init__(self):
        super().__init__()
        self.cipher=Symmetric_Encryption.get_symmetric_algorithm()
        self.passphrase=passphrase_generator()
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
    def detect_key_sizes_only(cls,text):
        pattern = r'\b[a-zA-Z0-9_]+-(\d+)(?:-[a-zA-Z0-9_]+)?\b'
        matches = re.findall(pattern, text)
        if matches:
            bit_size=int(matches[0])
            byte_size=bit_size/8
            return  byte_size
        else:
            print("Error key size")
            exit(1)


    @classmethod
    def generate_key(cls,size):
        key=os.urandom(size)
        hex_key=key.hex()
        return key,hex_key

        #Encrypt
    def encrypt(self):


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
            self.key,self.hex_key=Symmetric_Encryption.generate_key(
                Symmetric_Encryption.detect_key_sizes_only(self.passphrase)
            )
            try:
                with open(self.concern_file+".key",'wb') as enc_key:
                    enc_key.write(self.key)
                print("Key created")
            except IOError as e:
                print(f"Error saving the key: {e}")



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
                    self.hex_key,
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
        print("Encryption success")

    def decrypt(self):
        print(f"The file to decrypt is {self.concern_file}")

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
            key_file_name=choose_file("Enter the key file")

            key_size=256
            key_bin=bytes()
            #open the key file
            with open(key_file_name,'rb') as key_file:
                while chunk:=key_file.read(key_size):
                    key_bin += chunk #Assign the contents of the file into key_bin
            key_hex=key_bin.hex()

            #Getting the IV
            iv_file_name=choose_file("Enter the IV file")

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


class Asymmetric_Encryption(Encryption):
    def __init__(self):
        super().__init__()
        self.cipher=Asymmetric_Encryption.get_asymmetric_algorithm()
        self.name_private_key=choose_file("Enter the private key")
        self.name_public_key=choose_file("Enter the public key")

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

    @classmethod
    def generate_private_key(cls):
        algorithm=Asymmetric_Encryption.get_asymmetric_algorithm()
        algo = algorithm.upper()

        if algo in ["RSA"]:
            print("This is an RSA key (encryption + signing).")
            cmd=[
                'openssl',
                'genpkey',
                '-algorithm',
                'RSA',
                '-out',
                'private_rsa.pem',
                '-pkeyopt',
                'rsa_keygen_bits:2048'
            ]
            subprocess.run(cmd,check=True)

            return True
        elif algo in ["DSA"]:
            print("This is a DSA key (signing only).")
            # Step 1: Generate parameters
            cmd1=[
                'openssl',
                'genpkey',
                '-genparam',
                '-algorithm',
                'DSA',
                '-out',
                'dsa_params.pem',
                '-pkeyopt',
                'dsa_paramgen_bits:2048'

            ]
            subprocess.run(cmd1,check=True)
            cmd2=[
                'openssl',
                'genpkey',
                '-paramfile',
                'dsa_params.pem',
                '-out',
                'private_dsa.pem'
            ]
            subprocess.run(cmd2,check=True)

            return True
        elif algo in ["DH"]:
            print(
                "This is a Diffie-Hellman key (key exchange only)."
            )
            # Step 1: Generate parameters 
            cmd1=[
                'openssl',
                'genpkey',
                '-genparam',
                '-algorithm',
                'DH',
                '-out',
                'dh_params.pem',
                '-pkeyopt',
                'dh_paramgen_prime_len:2048'
            ]
            subprocess.run(cmd1,check=True)

            # Step 2: Generate private key 
            cmd2=[
                'openssl',
                'genpkey',
                '-paramfile',
                'dh_params.pem',
                '-out',
                'private_dh.pem'
            ]
            subprocess.run(cmd2,check=True)
            
            return True

        elif algo in ["EC"]:
            print(
                "This is an Elliptic Curve key (signing + key exchange)."
            )
            return True

        elif algo in ["ED25519", "ED448"]:
            print(
                "This is an Edwards-curve key (signing only)."
            )
            return True
        elif algo in ["X25519", "X448"]:
            print(
                "This is an X25519/X448 key (key exchange only)."
            )
            return True
        else:
            print("Unknown algorithm:", algo)
            return False


    def encrypt(self):
        cmd=[
            'openssl',
            'pkeyutl',
            '-encrypt',
            '-inkey',
            self.name_public_key,
            '-pubin',
            '-in',
            self.concern_file,
            '-out',
            self.concern_file+".enc"
        ]
        subprocess.run(cmd,check=True)

    @classmethod
    def generate_public_key(cls):
        private_key=choose_file(
            "Enter the private key:"
        )
        cmd=[
            'openssl',
            'pkey',
            '-in',
            private_key,
            '-pubout',
            '-out',
            'public.pem'
        ]
        subprocess.run(cmd,check=True)

        return True
    @classmethod
    def encrypt_private_key(cls):
        private_key=choose_file(
            "Enter the private key:"
        )
        algos=["aes","des3"]
        algo_menu=TerminalMenu(algos,title="Choose the algorithm")
        algo_index=algo_menu.show()
        algo=algos[algo_index]
        if algo=="aes":
            print(private_key,algo)
            cmd=[
                'openssl',
                'pkcs8',
                '-topk8',
                '-in',
                private_key,
                '-out',
                'encryptedkey.pem',
                '-v2',
                'aes-256-cbc'
            ]
        else:
            cmd=[
                'openssl',
                'pkcs8',
                '-topk8',
                '-in',
                private_key,
                '-out',
                'encryptedkey.pem',
                '-v1',
                'PBE-SHA1-3DES'

            ]
        subprocess.run(cmd,check=True)
        return True


    def decrypt(self):
        cmd=[
            'openssl',
            'pkeyutl',
            '-decrypt',
            '-inkey',
            self.name_private_key,
            '-in',
            self.concern_file,
            '-out',
            self.concern_file+".out"
        ]
        subprocess.run(cmd,check=True)
    
