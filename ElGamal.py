# -*- coding: utf-8 -*-
from gcd import ext_gcd
from montgomery import exp_mod
import strconvert
import random
import sympy


# p、q生成公、私鑰
def gen_key(p):
    e1 = int(input("請輸入e1\n"))
    d = random.randint(1, e1-1)
    e2 =  exp_mod(e1, d , p)  #e2 = e1^d mod p
    return    (e1, e2, p), (d,p)  #回傳公鑰<e1,e2,p>、私鑰<d,p>

# 將明文m加密成密文c
def encrypt(m, pubkey):
    e1 = pubkey[0]
    e2 = pubkey[1]
    p = pubkey[2]
    r = random.randint(1, p-1) #隨機亂數r
    c1 = exp_mod(e1, r, p) #c1 = e1^r mod p
    c2 = (m%p * exp_mod(e2, r, p))%p #c2 = m*e2^r mod p
    return (c1,c2)

# 將密文m解密成明文c
def decrypt(c, prikey):
    d = prikey[0]
    p = prikey[1]
    c1 = c[0]
    c2 = c[1]

    #m = c2*(c1^d)^-1 mod p 
    c1_d = exp_mod(c1, d, p)
    if(c1_d < 0):c1_d += p
    c1_dinv = ext_gcd(c1_d , p)[1] 
    if(c1_dinv < 0):c1_dinv += p
    m = ((c2%p) * c1_dinv)%p

    return m


if __name__ == "__main__":
    

    while(True):
        
        choose = int(input("請選擇ElGamal模式\n=====================================\n1.加密\n2.解密\n3.離開\n=====================================\n"))
        if(choose == 1):

            #明文輸入
            text = input("請輸入預加密明文:\n")
            m = strconvert.str_con(text)

            print("請輸入p (p >",m,")")   
            #生成p
            while(True):
                p = int(input('請輸入p:\n'))
                if(sympy.isprime(p) == False):
                    print(p,"不是質數")
                    continue
                elif(p < m):      
                    print("p < m，請重新輸入")
                    continue
                else:
                    break                 

            #生成公鑰<e1,e2,p>、私鑰<d,p>
            pubkey, prikey = gen_key(p)
           
            #ElGamal加密
            c= encrypt(m, pubkey)
            
            print("\n------------- 生成公鑰 ---------------\ne1 =",pubkey[0],"\ne2 =",pubkey[1],"\ne3 =",pubkey[2],"\n")
            print("------------- 生成私鑰 ---------------\nd =",prikey[0],"\np =",prikey[1],"\n")  
            print("------------- 加密密文 ---------------\n",c,"\n")

        elif(choose == 2):

            #密文輸入
            c1 = int(input("請輸入預解密密文(C1):\n"))
            c2 = int(input("請輸入預解密密文(C2):\n"))

            p1 = int(input('請輸入d:\n'))
            p2 = int(input('請輸入p:\n'))

            prikey = (p1 , p2)
            c = (c1 , c2)

            #ElGamal解密
            d = decrypt(c, prikey)
            m = strconvert.str_re(d)

            print("\n------------- 解密明文 ---------------\n",m,"\n")
        
        elif(choose == 3):
            break

            