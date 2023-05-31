import random as r
import math as m

#*  This function generates a public and a private key.
def RSAKeyGeneration(FILENAME):
     #*  This is a function for executing the Euler Function ϕ(n), which is a mathematical operation used in RSA encryption which inputs the product of two primes "n", and returns the answer to the mathematical operation (p-1)*(q-1), where p and q are the two prime factors of n. Having "n" as a parameter doesn't have any effective use in the code, but is there for formality's sake to show that it's the euler function.
    def Euler(n):
        return (p-1)*(q-1)
    
    #*  This line sets the variables used for the private and the public key, where p and q will become two different random prime numbers, and n will become the product of those two primes.
    p, q, n = 0, 0, 0
    
    #*  This part extracts numbers from a file.
    with open(FILENAME, "r") as fileInfo:
        largePrimeList = []
        for number in fileInfo.readlines():
            largePrimeList.append(int(number[:-1]))
    
    #*  This part ensures that q and p become two random different numbers from the file.
    while p == q:
        p = largePrimeList[r.randint(0, len(largePrimeList)-1)]
        q = largePrimeList[r.randint(0, len(largePrimeList)-1)]
    
    #*  This part sets variable n, which is the product of the factors p and q.
    n = p*q
    
    #*  This part creates a variable e, which will become the exponent of the public key. e has to be more than 1, and less than ϕ(n)
    e = r.randint(1000, Euler(n)-1)
    while m.gcd(e, Euler(n)) != 1:
        e -= 1

    #*  This part creates the unique part of the private key, the exponent, by trying different values of a, such that the private key equation d = (a*Euler(n)+1)/e becomes a whole number.
    run = True
    a = 0
    while run:
        a += 1
        d = (a*Euler(n)+1)/e
        if d.is_integer():
            d = int(d)
            run = False
    
    #*  This part creates an output file for the private and public keys.
    with open("privateKey", "w") as fileInfo:
        fileInfo.write(f"{d}\n{n}")
    with open("publicKey", "w") as fileInfo:
        fileInfo.write(f"{e}\n{n}")

RSAKeyGeneration("largePrimes")