def exp_mod(base, exponent, n):
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []
    pre_base = base
    base_array.append(pre_base)
    

    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n 
        base_array.append(next_base)
        pre_base = next_base

    a_w_b = __multi(base_array, bin_array)
    return a_w_b % n

def __multi(array, bin_array):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
    return result