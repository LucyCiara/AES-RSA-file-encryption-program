import random as r
import math as m

#*  This function generates a public and a private key. FILENAME is the filename of the file containing all the prime numbers to pull primes from.
def RSAKeyGeneration(FILENAME: str):
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
    with open("privateKey.txt", "w") as fileInfo:
        fileInfo.write(f"{d}\n{n}\n")
    with open("publicKey.txt", "w") as fileInfo:
        fileInfo.write(f"{e}\n{n}\n")

#*  This function generates a random symmetrical key for use in AES encryption. LENGTH is the target bitlength of the AES key
def AESKeyGeneration(LENGTH: int):
    #*  This part creates the list which will be used to add a bunch of numbers to the output file.
    AESKey = []

    #* This part adds a number of bytes, as represented by a number, to the key enough times that the key reaches the required bit length (usually 128)
    for i in range(int(LENGTH/8)):
        AESKey.append(f"{r.randint(0, 256-1)}\n")
    with open("symmetricalKey.txt", "w") as fileInfo:
        fileInfo.writelines(AESKey)

#*  This function encrypts the symmetrical key of the AES with an unsymmetric key, so that it can be shared safely. FILENAME is the file with the key you want to encrypt (symmetricalKey), and FILENAME2 is the file with the key you want to encrypt with.
def RSAKeyEncryption(FILENAME: str, FILENAME2: str):
    #*  This part sets the list which will be used to output the encrypted key to a file.
    EKey = []

    #*  This part gets the exponent and the product from the public key.
    with open(FILENAME2, "r") as fileInfo:
        publicKey = fileInfo.readlines()
        e = int(publicKey[0][:-1])
        n = int(publicKey[1][:-1])

    #*  This part gets the symmetrical key and outputs the encrypted key to the EKey list.
    with open(FILENAME, "r") as fileInfo:
        for item in fileInfo.readlines():
            line = int(item[:-1])
            EKey.append(f"{line**e%n}\n")

    #*  This part outputs the encrypted symmetrical key to a file.
    with open(f"{FILENAME[:-4]}Encrypted.txt", "w") as fileInfo:
        fileInfo.writelines(EKey)

RSAKeyEncryption("symmetricalKey.txt", "publicKey.txt")