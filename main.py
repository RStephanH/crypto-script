import encryption
import func

#Welcome
func.welcome("Crypto-Script")

#Choosing what kind of operation the user want
action, type_action=func.choose_action()
#value action= "Encrypt"/"Decrypt"/"Cancel"
#value type_action= "Symmetric"/"Asymmetric"
file=encryption.Encryption(type_action)
if (action.lower()=="encrypt"
    and type_action.lower()=="symmetric"):
    file.sym_encrypt()
