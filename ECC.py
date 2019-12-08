# -*- coding: utf-8 -*-

def get_inverse_element(value, max_value):
  
    for i in range(1, max_value):
        if (i * value) % max_value == 1:
            return i
    return -1


def gcd_x_y(x, y):
    
    if y == 0:
        return x
    else:
        return gcd_x_y(y, x % y)
    

def calculate_p_q(x1,y1,x2,y2, a, p):
    """
    计算p+q
    """
    flag = 1  
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 算分子
        denominator = 2 * y1    # 算分母
    else:
        member = y2 - y1
        denominator = x2 - x1 
        if member* denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)
    
    # 分數化簡
    gcd_value = gcd_x_y(member, denominator)
    member = int(member / gcd_value)
    denominator = int(denominator / gcd_value)
    # 求分母的反元素    
    inverse_value = get_inverse_element(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p
    # 算x3,y3
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    # print("%d<=====>%d" % (x3, y3))
    return [x3,y3]
    

def get_order(x0, y0, a, b, p):

    # 算 -p
    x1 = x0
    y1 = (-1 * y0) % p
    temp_x = x0
    temp_y = y0
    n = 1
    while True:
        n += 1
        p_value = calculate_p_q(temp_x,temp_y, x0, y0, a, p)
        if p_value[0] == x1 and p_value[1] == y1:
            #print("==========该椭圆曲线的阶为%d=========" % (n+1))
            return n+1
            
        temp_x = p_value[0]
        temp_y = p_value[1]

    # print("%d-%d-%d-%d" % (x0,y0,x1,y1))


def get_x0_y0_x1_y1(x0, a, b, p):
    """
    计算p和-p
    """
    y0 = -1
    for i in range(0,p):
        if i ** 2 % p == (x0**3 + a*x0 + b) % p:
            y0 = i
            break
    
    # 如果y0找不到False
    if y0 == -1:
        return False
    # 算-y
    x1 = x0
    y1 = -1 * y0 % p
    # print("%d-%d-%d-%d" % (x0,y0,x1,y1))
    return [x0,y0,x1,y1]


def draw_graph(a,b,p):
   
    x_y = []
    for i in range(p):
        x_y.append(["." for i in range(p)])
    
    for i in range(p):
        value = get_x0_y0_x1_y1(i, a, b, p)
        if value != False:
            x0 = value[0]
            y0 = value[1]
            x1 = value[2]
            y1 = value[3]
            print("(%d,%d) (%d,%d)" % (x0,y0,x1,y1))
            x_y[x0][y0] = 1
            x_y[x1][y1] = 1

    YY = int(input("\n是否顯示分布圖(1.是 2.否)? "))
    if(YY == 1):
            print("橢圓曲線分布圖:\n")
            for j in range(p):
                if p-1-j >= 10:
                    print(p-1-j, end=" ")
                else:
                    print(p-1-j, end="  ")
                for i in range(p):
                    print(x_y[i][p-j-1], end="  ")
                print()
            print("   ",end="")
            for i in range(p):
                if i >= 10:
                    print(i, end=" ")
                else:
                    print(i, end="  ") 
    
    print()

def calculate_np(G_x, G_y, private_key, a, p):

    temp_x = G_x
    temp_y = G_y
    while private_key != 1:
        p_value = calculate_p_q(temp_x,temp_y, G_x, G_y, a, p)
        temp_x = p_value[0]
        temp_y = p_value[1]
        private_key -= 1
    return p_value
    
    
def ecc_encrypt():
    while True:
        a = int(input("請輸入橢圓曲線參數a:"))
        b = int(input("請輸入橢圓曲線參數b:"))
        p = int(input("請輸入橢圓曲線參數p(p為質數):"))
        
        if (4*(a**3) + 27*(b**2)) % p ==0:
            print("選擇的橢圓取縣不能加密，請重新選擇\n")
        else:
            break
    # 輸出分布圖
    print()
    draw_graph(a,b,p)

    print("\n選擇一點G")
    G_x = int(input("選擇橫坐標G_x:"))
    G_y = int(input("選擇縱坐標G_y:"))
    # 算橢圓曲線的價值
    n = get_order(G_x, G_y, a, b, p)
    # 获取私钥并且key < 椭圆曲线的阶n
    private_key = int(input("請輸入私鑰(d)(<%d):" % n))
    # 计算公钥 nG
    Q = calculate_np(G_x,G_y,private_key,a,p)

    # ECC加密
    k = int(input("請輸入整數k(<%d):" % n))
    k_G = calculate_np(G_x,G_y,k,a,p) # 算KG
    k_Q = calculate_np(Q[0],Q[1],k,a,p) # 算KQ
    plain_text = int(input("請输入要加密的明文："))
    cipher_text = plain_text * k_Q[0]  # 計算明文與KQ的乘積
    # 生成密文
    C = [k_G[0], k_G[1],cipher_text] 

    print("生成公鑰{a=%d,b=%d,p=%d,n%d,G(%d,%d),Q(%d,%d)}" % (a, b, p, n, G_x, G_y , Q[0], Q[1]))
    print("生成私鑰{d=%d}" % private_key)
    print("加密密文：{(%d,%d),%d}" % (C[0], C[1], C[2]))



def ecc_decrypt():
    # 解密
    # 計算private_key*kG
    c1 = int(input("請輸入預解密密文(C1):"))
    c2 = int(input("請輸入預解密密文(C2):"))
    c3 = int(input("請輸入預解密密文(C3):"))
    private_key = int(input("請輸入d:"))
    a = int(input("請輸入a:"))
    p = int(input("請輸入p:"))

    decrypto_text = calculate_np(c1,c2,private_key,a,p)   
    inverse_value = get_inverse_element(decrypto_text[0],p)
    m = c3 * inverse_value % p
    print("解密後的明文為%d\n" % m)
    
if __name__ == '__main__':

    while(True):
        choose = int(input("請選擇ECC模式\n=====================================\n1.加密\n2.解密\n3.離開\n=====================================\n"))
        if(choose == 1):
            ecc_encrypt()
            continue
        elif(choose == 2):
            ecc_decrypt()
            continue
        elif(choose == 3):
            break
    
    
    

