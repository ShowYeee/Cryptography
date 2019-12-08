import binascii


def str_con(m):
    a = m.encode('utf-8')
    b = int(binascii.hexlify(a), 16)
    return b


def str_re(m):
    a = hex(m)
    b = a[2:]
    c = b.encode('ascii')
    
    try:
        d = binascii.unhexlify(c)
    except binascii.Error as n:
        d = binascii.unhexlify(c+ '0'.encode('ascii'))

    e = d.decode('utf-8','ignore')
    return e




