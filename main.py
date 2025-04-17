import encryption
import func

#Welcome
func.welcome("Crypto-Script")

#Choosing what kind of operation the user want
action, type_action=func.choose_action()
#value action= "Encrypt"/"Decrypt"/"Cancel"
#value type_action= "Symmetric"/"Asymmetric"

f=encryption.Encryption(type_action)

# if (action=="encrypt"
#         or action=="decrypt"):
#     file=encryption.Encryption(type_action)
# #Encryption
#     if action=="encrypt":
#         if type_action=="symmetric":
#             file.sym_encrypt()
#         elif type_action=="asymmetric":
#             file.asym_encryp()
# #Decription
#     elif (action=="decrypt"):
#         if type_action=="symmetric":
#             file.sym_decrypt()
#         elif type_action=="asymmetric":
#             file.asym_decryp()
