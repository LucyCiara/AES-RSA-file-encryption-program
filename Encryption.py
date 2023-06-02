import random as r
import math as m

#*  This function extracts the S-Box from the S-box.txt file, and converts it to numbers.
sBox = {}
rsBox = {}
def sBoxExtraction(FILENAME: str, sBox: dict, rsBox: dict):
    with open(FILENAME, "r") as fileInfo:
        for item in fileInfo:
            index = item.find(",")
            #*  Adds the left number as the key in the sBox dictionary.
            sBox[str(int(item[:index], 2))] = str(int(item[index+1:], 2))
            #*  Adds the right number as the key in the rsBox dictionary.
            rsBox[str(int(item[index+1:], 2))] = str(int(item[:index], 2))

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
    
    #*  This part creates a variable e, which will become the exponent of the public key. e has to be more than 1, and less than ϕ(n).
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

#*  This function encrypts the symmetrical key of the AES with an unsymmetric key, so that it can be shared safely. FILENAME is the file with the key you want to decrypt (symmetricalKey), and FILENAME2 is the file with the key you want to encrypt with. FILENAME3 is the filename you want to give the decrypted output file.
def RSAKeyDecryption(FILENAME: str, FILENAME2: str, FILENAME3: str):
    #*  This part sets the list which will be used to output the decrypted key to a file.
    AESKey = []

    #*  This part gets the exponent and the product from the private key.
    with open(FILENAME2, "r") as fileInfo:
        privateKey = fileInfo.readlines()
        d = int(privateKey[0][:-1])
        n = int(privateKey[1][:-1])
    
    #*  This part gets the encrypted symmetrical key and outputs the decrypted key to the AESKey list.
    with open(FILENAME, "r") as fileInfo:
        for item in fileInfo.readlines():
            line = int(item[:-1])
            AESKey.append(f"{line**d%n}\n")

    #*  This part outputs the decrypted symmetrical key to a file.
    with open(FILENAME3, "w") as fileInfo:
        fileInfo.writelines(AESKey)

#*  This function encrypts the data of a file using AES methods. FILENAME is the file name of the file you want to encrypt, FILENAME2 is the file name of the file containing the AES key, and sBox is the S-Box dictionary.
def AESEncryption(FILENAME: str, FILENAME2: str, sBox: dict):
    #*  This function extracts the binary data from a file. FILENAME is the name of the file you want to encrypt.
    def get_binary_data(FILENAME):
        with open(FILENAME, 'rb') as fileInfo:
            binary_data = fileInfo.read()
            return binary_data

    #*  This function relengthens the data of the file by adding and removing spaces at the end (ascii number 32). 'data' is the list of a files bytes represented by numbers which is going to be encrypted/is decrypted. TOGGLE is a toggle bool. if it's True, it lengthens data, and if it's False, it shortens data.
    def fileRelength(data, TOGGLE):
        if TOGGLE:
            #*  This part makes sure that the file's number of bytes is divisible by 16
            while len(data)%16 != 0:
                data.append(32)
        else:
            #*  Removes extra spaces at the end.
            while data[-1] == 32:
                data.pop()

    #*  This function expands the key. FILENAME2 is the filename of the file containing the AES key, sBox is the dictionary used as a Substitute Byte lookuptable, roundKeyList is the list you want to output the expanded key to (each round's key is its own nested list). Because we're using a 128-bit key, we will need 11 keys, since we need a key for the start, and 10 keys for each of the 10 encryption rounds.
    roundKeyList = []
    def keyExpansion(FILENAME2, sBox, roundKeyList):
        #*  Declares the variables for use in expanding the key.
        Key0, Key1, Key2, Key3, Key4, Key5, Key6, Key7, Key8, Key9, Key10 = [], [], [], [], [], [], [], [], [], [], []
        for item in [Key0, Key1, Key2, Key3, Key4, Key5, Key6, Key7, Key8, Key9, Key10]:
            roundKeyList.append(item)
        KeyChunk = []
        
        #*  This function sets Key0 to be the initial given key.
        def initialKey(FILENAME2, Key0):
            with open(FILENAME2, 'r') as fileInfo:
                for item in fileInfo.readlines():
                    Key0.append(int(item[:-1]))

        #*  This function takes the last 4 bytes of a key.
        def keyChunkPrepare(Key, KeyChunk):
            KeyChunk.clear()
            for item in Key[-4:]:
                KeyChunk.append(item)
        
        #* This function shuffles the last 4 bytes of a key.
        def rotKey(KeyChunk):
            KeyChunk.insert(0, KeyChunk.pop(-1))

        #*  This function replaces the shuffled 4 last bytes of a key with other bytes from an S-Box map I made.
        def substituteByte(KeyChunk, sBox):
            tempKey = []
            for item in KeyChunk:
                tempKey.append(int(sBox[str(item)]))
            KeyChunk.clear()
            for item in tempKey:
                KeyChunk.append(item)
        
        #*  This function XORs the shuffled and substituted 2 last bytes of a key with the keynumber (round constant).
        def roundConst(round, KeyChunk):
            tempKey = []
            for item in KeyChunk:
                tempKey.append(item^(round+1))
            KeyChunk.clear()
            for item in tempKey:
                KeyChunk.append(item)

        #*  Here the first key is pulled.
        initialKey(FILENAME2, Key0)

        #*  Here 10 keys are created using the other functions.
        for i in range(10):
            roundKeyList = [Key0, Key1, Key2, Key3, Key4, Key5, Key6, Key7, Key8, Key9, Key10]
            keyChunkPrepare(roundKeyList[i], KeyChunk)
            rotKey(KeyChunk)
            substituteByte(KeyChunk, sBox)
            roundConst(i, KeyChunk)
            for x in range(4):
                roundKeyList[i+1].append(KeyChunk[x])
            for x in range(3):
                for y in range(4):
                    #!
                    xor = roundKeyList[i][x*4:x*4+4][y]^roundKeyList[i+1][x*4:x*4+4][y]
                    roundKeyList[i+1].append(xor)

    #*  This function encrypts the file information using XOR. dataToEncrypt is the list with numbers representing the bytes in a file.
    def roundKeyEncode(dataToEncrypt, key):
        for i in range(len(dataToEncrypt)):
            dataToEncrypt.insert(i, key[i]^dataToEncrypt.pop(i))

    #*  This function substitues every byte in the 16-byte chunk. dataToEncrypt is a 16-byte chunk of data, table is either an S-Box (sBox) or a reverse S-Box (rsBox).
    def substituteBytes(dataToEncrypt, table):
        for i in range(len(dataToEncrypt)):
            dataToEncrypt.insert(i, int(table[str(dataToEncrypt.pop(i))]))

    #*  This function diffuses the result by mixing the items of each row in the 4x4 grid which AES encryption is displayed in.
    def shiftRows(dataToEncrypt):
        for i in range(3):
            for x in range(i):
                dataToEncrypt.insert(i*4, dataToEncrypt.pop(i*4+3))


    #*  Fetches and prepares the bytes of a file, and then expands the AES key
    data = list(get_binary_data(FILENAME))
    fileRelength(data, True)
    keyExpansion(FILENAME2, sBox, roundKeyList)

    #*  It takes a 16 byte big chunk (same length as the key) from dataToEncrypt and encrypts that chunk.
    for i in range(int(len(data)/16)):
        tempList = data[i*16:(i+1)*16]
        del data[i*16:(i+1)*16]

        roundKeyEncode(tempList, roundKeyList[0])
        for x in range(1, 10):
            substituteBytes(tempList, sBox)
            shiftRows(tempList)
            roundKeyEncode(tempList, roundKeyList[x])
        substituteBytes(tempList, sBox)
        shiftRows(tempList)
        roundKeyEncode(tempList, roundKeyList[10])

        for x in range(0, 16):
            data.insert(i*16+x, tempList[x])
    
    with open("EncryptedFile", "wb") as fileInfo:
        fileInfo.write(bytes(data))

#*  This function encrypts the data of a file using AES methods. FILENAME is the file name of the file you want to decrypt, FILENAME2 is the file name of the file containing the AES key, sBox is the S-Box dictionary, rsBox is the inverse S-Box dictionary.
def AESDecryption(FILENAME: str, FILENAME2: str, sBox: dict, rsBox: dict):
    #*  This function extracts the binary data from a file. FILENAME is the name of the file you want to encrypt.
    def get_binary_data(FILENAME):
        with open(FILENAME, 'rb') as fileInfo:
            binary_data = fileInfo.read()
            return binary_data

    #*  This function relengthens the data of the file by adding and removing spaces at the end (ascii number 32). 'data' is the list of a files bytes represented by numbers which is going to be encrypted/is decrypted. TOGGLE is a toggle bool. if it's True, it lengthens data, and if it's False, it shortens data.
    def fileRelength(data, TOGGLE):
        if TOGGLE:
            #*  This part makes sure that the file's number of bytes is divisible by 16
            while len(data)%16 != 0:
                data.append(32)
        else:
            #*  Removes extra spaces at the end.
            while data[-1] == 32:
                data.pop()

    #*  This function expands the key. FILENAME2 is the filename of the file containing the AES key, sBox is the dictionary used as a Substitute Byte lookuptable, roundKeyList is the list you want to output the expanded key to (each round's key is its own nested list). Because we're using a 128-bit key, we will need 11 keys, since we need a key for the start, and 10 keys for each of the 10 encryption rounds.
    roundKeyList = []
    def keyExpansion(FILENAME2, sBox, roundKeyList):
        #*  Declares the variables for use in expanding the key.
        Key0, Key1, Key2, Key3, Key4, Key5, Key6, Key7, Key8, Key9, Key10 = [], [], [], [], [], [], [], [], [], [], []
        for item in [Key0, Key1, Key2, Key3, Key4, Key5, Key6, Key7, Key8, Key9, Key10]:
            roundKeyList.append(item)
        KeyChunk = []
        
        #*  This function sets Key0 to be the initial given key.
        def initialKey(FILENAME2, Key0):
            with open(FILENAME2, 'r') as fileInfo:
                for item in fileInfo.readlines():
                    Key0.append(int(item[:-1]))

        #*  This function takes the last 4 bytes of a key.
        def keyChunkPrepare(Key, KeyChunk):
            KeyChunk.clear()
            for item in Key[-4:]:
                KeyChunk.append(item)
        
        #* This function shuffles the last 4 bytes of a key.
        def rotKey(KeyChunk):
            KeyChunk.insert(0, KeyChunk.pop(-1))

        #*  This function replaces the shuffled 4 last bytes of a key with other bytes from an S-Box map I made.
        def substituteByte(KeyChunk, sBox):
            tempKey = []
            for item in KeyChunk:
                tempKey.append(int(sBox[str(item)]))
            KeyChunk.clear()
            for item in tempKey:
                KeyChunk.append(item)
        
        #*  This function XORs the shuffled and substituted 2 last bytes of a key with the keynumber (round constant).
        def roundConst(round, KeyChunk):
            tempKey = []
            for item in KeyChunk:
                tempKey.append(item^(round+1))
            KeyChunk.clear()
            for item in tempKey:
                KeyChunk.append(item)

        #*  Here the first key is pulled.
        initialKey(FILENAME2, Key0)

        #*  Here 10 keys are created using the other functions.
        for i in range(10):
            roundKeyList = [Key0, Key1, Key2, Key3, Key4, Key5, Key6, Key7, Key8, Key9, Key10]
            keyChunkPrepare(roundKeyList[i], KeyChunk)
            rotKey(KeyChunk)
            substituteByte(KeyChunk, sBox)
            roundConst(i, KeyChunk)
            for x in range(4):
                roundKeyList[i+1].append(KeyChunk[x])
            for x in range(3):
                for y in range(4):
                    #!
                    xor = roundKeyList[i][x*4:x*4+4][y]^roundKeyList[i+1][x*4:x*4+4][y]
                    roundKeyList[i+1].append(xor)

    #*  This function decrypts the file information using XOR. dataToDecrypt is the list with numbers representing the bytes in a file.
    def roundKeyDecode(dataToDecrypt, key):
        for i in range(len(dataToDecrypt)):
            dataToDecrypt.insert(i, key[i]^dataToDecrypt.pop(i))

    #*  This function diffuses the result by mixing the items of each row in the 4x4 grid which AES encryption is displayed in.
    def invShiftRows(dataToDecrypt):
        for i in range(3):
            for x in range(i):
                dataToDecrypt.insert(i*4+3, dataToDecrypt.pop(i*4))

    #*  This function substitues every byte in the 16-byte chunk. dataToDecrypt is a 16-byte chunk of data, table is either an S-Box (sBox) or a reverse S-Box (rsBox).
    def substituteBytes(dataToDecrypt, table):
        for i in range(len(dataToDecrypt)):
            dataToDecrypt.insert(i, int(table[str(dataToDecrypt.pop(i))]))

    #*  Fetches and prepares the bytes of a file, and then expands the AES key
    data = list(get_binary_data(FILENAME))
    keyExpansion(FILENAME2, sBox, roundKeyList)

    #*  It takes a 16 byte big chunk (same length as the key) from dataToEncrypt and decrypts that chunk.
    for i in range(int(len(data)/16)):
        tempList = data[i*16:(i+1)*16]
        del data[i*16:(i+1)*16]

        roundKeyDecode(tempList, roundKeyList[10])
        invShiftRows(tempList)
        substituteBytes(tempList, rsBox)
        for x in range(1, 10):
            roundKeyDecode(tempList, roundKeyList[-x-1])
            invShiftRows(tempList)
            substituteBytes(tempList, rsBox)
        roundKeyDecode(tempList, roundKeyList[0])


        for x in range(0, 16):
            data.insert(i*16+x, tempList[x])
    
    fileRelength(data, False)
    with open("DecryptedFile", "wb") as fileInfo:
        fileInfo.write(bytes(data))

sBoxExtraction("S-box.txt", sBox, rsBox)

#*  A UI for the encryption program.
run = True
while run:
    inputString = input("Do you want to Generate RSA keys (1)\nGenerate AES key (2)\nEncrypt AES key with an RSA key (3)\nDecrypt AES key with RSA key (4)\nEncrypt file with AES key (5)\nDecrypt file with AES key (6)\nExit (7)\n(Know that generating new keys will replace the old ones)\n")
    if inputString == "1":
        input("One public key will be created, and one private key will be created.\nYou can share your public key with anyone, but you must keep your private key secret.\nYour new generated key will replace the old key.\nUnderstood?\n")
        RSAKeyGeneration("largePrimes.txt")
    elif inputString == "2":
        input("Only share this key with people you trust.\nYour new generated key will replace the old key.\nUnderstood?\n")
        AESKeyGeneration(128)
    elif inputString == "3":
        inputString = input("Write the name of the file containing the key you want to encrypt.\n")
        inputString2 = input("Write the filename of the file containing the RSA key you want to encrypt with\nExample:   publicKey.txt\n(It is recommended against encrypting sensitive data with only your private key for security reasons)\n")
        RSAKeyEncryption(inputString, inputString2)
    elif inputString == "4":
        inputString = input("Write the name of the file containing the key you want to decrypt.\n")
        inputString2 = input("Write the filename of the file containing the RSA key you want to decrypt with\nExample:   privateKey.txt\n")
        inputString3 = input("Name the new file\nExample:   symmetricalKeyDecrypted.txt\n")
        RSAKeyDecryption(inputString, inputString2, inputString3)
    elif inputString == "5":
        inputString = input("Write the name of the file you want to encrypt.\n")
        inputString2 = input("Write the filename of the file containing the AES key you want to encrypt with.\nExample:   symmetricalKey.txt\n")
        AESEncryption(inputString, "symmetricalKey.txt", sBox)
    elif inputString == "6":
        inputString = input("Write the name of the file you want to decrypt.\n")
        inputString2 = input("Write the filename of the file containing the AES key you want to decrypt with.\nExample:   symmetricalKey.txt\n")
        AESDecryption(inputString, "symmetricalKey.txt", sBox, rsBox)
    else:
        run = False


