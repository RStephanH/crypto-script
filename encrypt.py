import os

print("Welcome into this programme ")

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
            print(f"{selec_file} doesn't exist or not in the current directory")
            print("try again")
            for file in dir_files:
                print(">",file)


print(choose_file())
