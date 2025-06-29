import utils.encryption as encryption
import utils.func as func

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
    if type_action=='asymmetric':
        file=encryption.Asymmetric_Encryption()
        file.encrypt()
    elif type_action=='symmetric':
        file=encryption.Symmetric_Encryption()
        file.encrypt()
elif action=='decrypt':
    if type_action=='asymmetric':
        file=encryption.Asymmetric_Encryption()
        file.decrypt()
    elif type_action=='symmetric':
        file=encryption.Symmetric_Encryption()
        file.decrypt()
elif action=='generate key':
    if type_action=='private key':
        encryption.Asymmetric_Encryption.generate_private_key()
    elif type_action=='public key':
        encryption.Asymmetric_Encryption.generate_public_key()
    elif type_action=='encrypt private key':
        encryption.Asymmetric_Encryption.encrypt_private_key()
elif action=='hash':
    if type_action=='create':
        file=encryption.Hash()
        file.create_hash()
    elif type_action=='sign':
        file=encryption.Hash()
        file.sign_hash()
    elif type_action=='verify':
        file=encryption.Hash()
        file.verify_hash()

