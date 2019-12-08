# -*- coding: utf-8 -*-
from gcd import ext_gcd
from gcd import gcd
from montgomery import exp_mod
import strconvert
import sympy
from prettytable import PrettyTable



# p、q生成公、私鑰
def gen_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)     # 算phi(n)

    # 選e

    while(True):
        e = int(input("請輸入e (e與phi(n)必須互質)\n"))
        if(gcd(e,phi) != 1): 
            print("e與phi(n)沒有互質，請重新輸入")
            continue
        else:
            break

    r, x, y = ext_gcd(e, phi)   # 用擴展歐幾里得算 d = e^-1 mod phi(n)
    d = x
    if (d < 0): d += phi
    return    (n, e), (n, d)    #回傳公鑰<n,e>、私鑰<n,d>

# 將明文m加密成密文c
def encrypt(m, pubkey):
    n = pubkey[0]//1
    e = pubkey[1]//1
    c = exp_mod(m, e, n)
    return c

# 將密文m解密成明文c
def decrypt(c, prikey):
    n = prikey[0]
    d = prikey[1]
    m = exp_mod(c, d, n)
    return m


if __name__ == "__main__":
    
    while(True):
        choose = int(input("請選擇RSA模式\n=====================================\n1.加密\n2.解密\n3.離開\n=====================================\n"))
        if(choose == 1):

            #明文輸入
            text = input("請輸入預加密明文:\n")
            m = strconvert.str_con(text)
            #生成p、q
            print("請輸入p、q (p*q >",m,")")


            while(True):
                
                while(True):
                    p = int(input('請輸入p:  \n'))
                    if(sympy.isprime(p) == False):
                        print(p,"不是質數")
                        continue
                    else:
                        break

                while(True):
                    q = int(input('請輸入q:  \n'))
                    if(sympy.isprime(q) == False):
                        print(q,"不是質數")
                        continue
                    else:
                        break

                if(p*q < m):
                    print("p*q < m，請重新輸入")
                    continue
                else:
                    break

            #生成公鑰<n,e>、私鑰<n,d>
            pubkey, prikey = gen_key(p, q)

             #RSA加密
            c = encrypt(m, pubkey)

            print("\n------------- 生成公鑰 ---------------\nn =",pubkey[0],"\ne =",pubkey[1],"\n")
            print("------------- 生成私鑰 ---------------\nn =",prikey[0],"\nd =",prikey[1],"\n")  
            print("------------- 加密密文 ---------------\n",c,"\n")
         

        elif(choose == 2):
            
            #密文輸入
            text = int(input("請輸入預解密密文  \n"))

            #RSA解密
            n = input('請輸入n\n')
            d = input('請輸入d\n')
            prikey = (int(n),int(d))
            m1 = decrypt(text, prikey)
            m = strconvert.str_re(m1)
            print("\n------------- 解密明文 ---------------\n",m,"\n")

        elif(choose == 3):
            break


    