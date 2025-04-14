from getpass import getpass
import os
import subprocess
import sys




#Chose the file 
def choose_file():
    print("Wich file will be encrypted :")

    dir_files=os.listdir()
    
    for file in dir_files:
        print(">",file)

    while True :

        selec_file=str(input()).strip()

        if selec_file in dir_files:
            return selec_file
        else:
            print(f"{selec_file}"
                  "doesn't exist"
                  "or not in the current directory")
            print("try again")

            for file in dir_files:
                print(">",file)


#Check the command
def command_exists(command):
    result = subprocess.run(
        ['which', command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


#check openssl
def check_openSSL():
    if command_exists("openssl"):
        return True
    else:
        print("openssl is not installed!\n",\
              "Please install it and run this programm again.")
        sys.exit(1) 


def encryption_method():

    output=subprocess.run(
        ['openssl','enc','-ciphers'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    ciphers=output.stdout.split()

    for _ in range(2):
        del ciphers[0]
    
    for ciph in ciphers:
        print(">",ciph)
    print("Enter one of the cipher above"
          "(by default cipher -aes-256-cbc used): ")
    cipher_input=str(input()).strip()

    if cipher_input=="":
        cipher_input="-aes-256-cbc"
    confirm=str(input("Do you want to use passphrase?(y/n)"))

    if confirm.lower()=='y':

        while True:

            input_passphrase1=getpass("Enter the passphrase: ")
            input_passphrase2=getpass("Re-enter the passphrase: ")

            if input_passphrase1 == input_passphrase2 :
                print("Passphrase match! Success.")
                input_passphrase=input_passphrase2
                break
            else:
                print("Passwords don't match. Try again.\n")

    else:
        input_passphrase=None
    
    return cipher_input,input_passphrase
