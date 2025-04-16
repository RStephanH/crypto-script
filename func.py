from getpass import getpass
from simple_term_menu import TerminalMenu
from sys import exit
import os
import re
import subprocess


#Chose the file 
def choose_file():
    message="Choose the file:"
    
     # Get list of files in the current directory
    all_entries = os.listdir('.')
    files = []

    for entry in all_entries:
        if os.path.isfile(entry):#verify if it's file
            files.append(entry)
 
    terminal_menu = TerminalMenu(files, title=message)
    menu_entry_index = terminal_menu.show()
    return files[menu_entry_index]


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
        exit(1) 


def password_generator():
    while True:

        input_passphrase1=getpass("Enter the passphrase: ")
        input_passphrase2=getpass("Re-enter the passphrase: ")

        if input_passphrase1 == input_passphrase2 :
            print("Passphrase match! Success.")
            input_passphrase=input_passphrase2
            break
        else:
            print("Passwords don't match. Try again.\n")
    return input_passphrase


def get_symmetric_algorithm():

    output=subprocess.run(
        ['openssl','enc','-ciphers'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    ciphers=output.stdout.split()

    for _ in range(2):
        del ciphers[0]
    
    ciphers_menu=TerminalMenu(ciphers,title="Choose the algorithm")
    cipher_index=ciphers_menu.show()
    cipher=ciphers[cipher_index]
    confirm=str(input("Do you want to use passphrase?(y/n)"))

    if confirm.lower()=='y':
        password=password_generator()
    else:
        password=None
    
    return cipher,password


def get_asymmetric_algorithm():
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


def welcome(msg):
    
    subprocess.run(
        [
            "figlet",
            msg
        ],
        check=True
    )

def choose_action():
    action_msg="What do you want to do"

    cmd=["cowsay","-f","tux",action_msg]
    subprocess.run(cmd,check=True)

    actions=["Encrypt","Decrypt","Cancel"]
    action_menu=TerminalMenu(actions)
    action_index=action_menu.show()
    action=actions[action_index]

    if action.lower()=="cancel":
        exit(1)
    types_action=["Symmetric","Asymmetric"]
    type_menu=TerminalMenu(types_action,title="Which type of encryption ?")
    type_index=type_menu.show()
    type_action=types_action[type_index]

    return action, type_action


