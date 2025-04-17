from getpass import getpass
from simple_term_menu import TerminalMenu
from sys import exit
import os
import re
import subprocess


#Chose the file 
def choose_file(message="Choose the file:"):
    
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
def passphrase_generator():
    confirm=str(input("Do you want to use passphrase?(y/n)"))
    if confirm.lower()=='y':
        password=password_generator()
    else:
        password=None

    return password



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

    actions=["Encrypt","Decrypt","Generate key","Hash","Cancel"]
    action_menu=TerminalMenu(actions)
    action_index=action_menu.show()
    action=actions[action_index].lower()

    if action=="cancel":
        exit(1)

    elif (action=="encrypt" 
            or action=="decrypt"):
        types_action=["Symmetric","Asymmetric"]

    elif (action=="generate key"):
        types_action=["Private key", "Public key"]

    elif (action=="hash"):
        type_action=None
        return action, type_action

    else:
        print("Action Error")
        exit(1)

    type_menu=TerminalMenu(types_action,title="Which type?")
    type_index=type_menu.show()
    type_action=types_action[type_index].lower()

    return action, type_action


