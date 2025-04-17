import encryption
import func

#Welcome
func.welcome("Crypto-Script")

#Choosing what kind of operation the user want
action, type_action=func.choose_action()
#value action= "Encrypt"/"Decrypt"/"Cancel"
#value type_action= "Symmetric"/"Asymmetric"

file=encryption.Encryption(type_action)

#Encryption
if action.lower()=="encrypt":
    if type_action.lower()=="symmetric":
        file.sym_encrypt()
    elif type_action.lower()=="asymmetric":
        file.asym_encryp()
#Decription
elif (action.lower()=="decrypt"):
    if type_action.lower()=="symmetric":
        file.sym_decrypt()
