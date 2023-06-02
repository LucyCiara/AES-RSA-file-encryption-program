
#!  source: will add if it's used
def mixColumns(a, b, c, d):
    def gmul(x, y):
        if y == 1:
            return x
        tmp = (x*2) & 255
        if y == 2:
            return tmp if x < 128 else tmp ^ 0x1b
        if y == 3:
            return gmul(x, 2) ^ x

    print(gmul(a, 2))

mixColumns(4, 13, 163, 250)

#!  source: will add if it's used
def mpy(x, y):                  # mpy two 8 bit values
    p = 0b100011011             # mpy modulo x^8+x^4+x^3+x+1
    m = 0                       # m will be product
    for i in range(8):
        m = m << 1
        if m & 0b100000000:
            m = m ^ p
        if y & 0b010000000:
            m = m ^ x
        y = y << 1
    return m
