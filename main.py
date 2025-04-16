import encryption
import func

#Welcome
func.welcome("Crypto-Script")
action, type_action=func.choose_action()
file=encryption.Encryption()
file.encrypt()
