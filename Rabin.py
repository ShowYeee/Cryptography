# -*- coding: utf-8 -*-
from gcd import ext_gcd
from montgomery import exp_mod
import strconvert
import sympy
from prettytable import PrettyTable

#中國於是定理(兩式)
def crt (a1,a2,m1,m2):
    M = m1*m2
    M1 = M//m1
    M2 = M//m2
    M1_inv = ext_gcd(M1 , m1)[1]  
    M2_inv = ext_gcd(M2 , m2)[1]
    
    if(M1_inv < 0):M1_inv = M1_inv+m1
    if(M2_inv < 0):M2_inv = M2_inv+m2

    n = (a1*M1*M1_inv+a2*M2*M2_inv)%M
    return n

def gen_key(p, q):
    n = p * q
    return (n), (p ,q)    #回傳公鑰<n>、私鑰<p,q>

# 將明文m加密成密文c
def encrypt(m, pubkey):
    n = pubkey
    c = exp_mod(m, 2, n)
    return c


# 將密文m解密成明文c
def decrypt(c, prikey):
    p = prikey[0]
    q = prikey[1]
    a1 = exp_mod(c, (p+1)//4 , p)
    a2 = p - a1
    b1 = exp_mod(c, (q+1)//4 , q)
    b2 = q - b1
    m = crt(a1,b1,p,q),crt(a1,b2,p,q),crt(a2,b1,p,q),crt(a2,b2,p,q)
    return m


if __name__ == "__main__":
    
    
    while(True):
        choose = int(input("請選擇Rabin模式\n=====================================\n1.加密\n2.解密\n3.離開\n=====================================\n"))

        if(choose == 1):

            #明文輸入
            text = input("請輸入預加密明文:\n")
            m = strconvert.str_con(text)
            
            #生成p、q
            while(True):

                print("請輸入p、q (p*q >",m,")")

                while(True):
                    p = int(input('請輸入p:\n'))
                    if(sympy.isprime(p) == False):
                        print(p,"不是質數")
                        continue
                    elif((p-3)%4 != 0): #p、q必須滿足4k+3
                        print("p(",p,")不滿足4k+3") 
                    else:
                        break

                while(True):
                    q = int(input('請輸入q:\n'))
                    if(sympy.isprime(q) == False):
                        print(q,"不是質數")
                        continue
                    elif((q-3)%4 != 0): #p、q必須滿足4k+3
                        print("q(",q,")不滿足4k+3") 
                        continue
                    else:
                        break  

                if(p*q < m):
                        print("p*q < m，請重新輸入")
                        continue
                else:
                    break         


            #生成公鑰<n>、私鑰<n,p,q>
            pubkey, prikey = gen_key(p, q)
            print(pubkey, prikey)

            #Rabin加密
            c = encrypt(m, pubkey)

            print("\n------------- 生成公鑰 ---------------\nn =",pubkey,"\n")
            print("------------- 生成私鑰 ---------------\np =",prikey[0],"\nq =",prikey[1],"\n")  
            print("------------- 加密密文 ---------------\n",c,"\n")

        elif(choose == 2):
    
            c = int(input("請輸入預解密密文\n"))

            
            while(True):
                p = int(input('請輸入p\n'))
                if(sympy.isprime(p) == False):
                    print("p不是質數")
                    continue
                elif((p-3)%4 != 0): #p、q必須滿足4k+3
                    print("p(",p,")不滿足4k+3") 
                else:
                    break

            while(True):
                q = int(input('請輸入q\n'))
                if(sympy.isprime(q) == False):
                    print("q不是質數")
                    continue
                elif((q-3)%4 != 0): #p、q必須滿足4k+3
                    print("q(",q,")不滿足4k+3") 
                    continue
                else:
                    break
                
            prikey = (p,q,p*q)

            #Rabin解密
            d = decrypt(c, prikey)
            print("\n------------- 解密明文 ---------------")
            print("",d[0],"(",strconvert.str_re(d[0]),")")
            print("-------------------------------------\n",d[1],"(",strconvert.str_re(d[1]),")")
            print("-------------------------------------\n",d[2],"(",strconvert.str_re(d[2]),")")
            print("-------------------------------------\n",d[3],"(",strconvert.str_re(d[3]),")\n")
        
        elif(choose == 3):
            break

    


 
    