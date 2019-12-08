import os

def rsa():
    os.system("python RSA.py")

def rabin():
    os.system("python Rabin.py")

def elgamal():
    os.system("python ElGamal.py")

def ecc():
    os.system("python ECC.py")
    

if __name__ == "__main__":

    while(True):
        print("=====================================")
        print("           請選擇加密模式")
        print("=====================================")
        print("1.RSA\n2.Rabin\n3.ElGamal\n4.ECC\n5.離開")
        print("=====================================")

        c = int(input(">> "))


        if(c == 1):
            print("#您選擇RSA加密\n")
            rsa()
            continue
        elif(c == 2):
            print("#您選擇Rabin加密\n")
            rabin()
            continue
        elif(c == 3):
            print("#您選擇ElGamal加密\n")
            elgamal()
            continue
        elif(c == 4):
            print("#您選擇ECC\n")
            ecc()
            continue
        elif(c == 5):
            break



