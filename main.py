import encryption
import func

#Welcome
func.welcome("Crypto-Script")

#Choosing what kind of operation the user want
action, type_action=func.choose_action()
# value action= "Encrypt"/"Decrypt"/"Generate key"/"Hash"/"Cancel"

# value type_action
#  for Encrypt and Decrypt:
#    "Symmetric"/"Asymmetric"
#  for Generate key:
#    "Private key"/"Public key"
    

if action=='encrypt':
    pass
elif action=='decrypt':
    pass
elif action=='generate key':
    if type_action=='private key':
        encryption.Asymmetric_Encryption.generate_private_key()
    elif type_action=='public key':
        encryption.Asymmetric_Encryption.generate_public_key()
    elif type_action=='encrypt private key':
        encryption.Asymmetric_Encryption.encrypt_private_key()
elif action=='hash':
    pass


