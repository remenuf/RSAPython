import math

def menu():
    print("""[0] Sair.\n[1] Gerar chave pública.\n[2] Criptografar.\n[3] Descriptografar.""")
    valid = int(input("Insira a operação que deseja realizar: "))
    while valid > 3 or valid < 0:
        print("Insira uma operação válida!")
        valid = int(input("Insira a operação que deseja realizar: "))
    return valid


def isPrime(n):
    for i in range(2, math.ceil(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True


def mdcEuclides(n, m):
    while True:
        if n % m == 0:
            return m
        n, m = m, n % m


def mdcAux(n, m, div):
    while True:
        if n % m == 0:
            div.append(n//m)
            break
        if n > m:
            div.append(n//m)
        n, m = m, n % m


def getInverse(div, table, phi):
    div.pop()
    div.reverse()
    mult, sum = 1, 0
    for i in range(len(div)):
        table.append(div[i]*mult+sum)
        mult, sum = table[i], mult
    if len(table) % 2 == 0 and len(table) > 1:
        table[-2] *= -1
        return table[-2] + phi
    elif len(table) == 1:
        return 1


def expM(M, n, e):
    return pow(M, e, n)

def generateKey():
    p = int(input("Digite um número primo p: "))
    while not isPrime(p):
        print("Não foi inserido um número primo!")
        p = int(input("Digite um número primo p: "))
    q = int(input("Digite um número primo q: "))
    while not isPrime(q):
        print("Não foi inserido um número primo!")
        q = int(input("Digite um número primo q: "))
    phi = (p-1)*(q-1)
    print(f'Expoente relativamente primo sugerido: {phi+1}')
    e = int(input("Insira um expoente relativamente primo a (p-1)(q-1): "))
    while not mdcEuclides(phi, e) == 1:
        print("Não foi inserido um expoente relativamente primo!")
        e = int(input("Insira um expoente relativamente primo a (p-1)(q-1): "))
    publicKey = open("publicKey.txt", 'w')
    publicKey.write(f'{p * q} {e}')
    publicKey.close()


def encryptText():
    encryptedFile = open("encryptedFile.txt", 'w')
    encryptedFile = open("encryptedFile.txt", 'a')
    n = int(input("Digite o n da chave pública: "))
    e = int(input("Digite o e da chave pública: "))
    toEncrypt = input("Digite o texto que deseja criptografar: ").lower()
    toEncrypt = toEncrypt.encode('ASCII')
    size = len(toEncrypt)
    for i in range(0, size):
        M = toEncrypt[i] - 97
        if M < 0:
            M = 26
        M = int(expM(M, n, e))
        encryptedFile.write(f'{M} ')
    encryptedFile.close()


def decryptText():
    decryptedFile = open("decryptedFile.txt", 'w')
    decryptedFile = open("decryptedFile.txt", 'a')
    div, table = [], []
    p = int(input("Digite o p da chave privada: "))
    while not isPrime(p):
        print("Não foi digitado um número primo!")
        p = int(input("Digite o p da chave privada: "))
    q = int(input("Digite o q da chave privada: "))
    while not isPrime(q):
        print("Não foi digitado um número primo!")
        q = int(input("Digite o q da chave privada: "))
    e = int(input("Digite o e da chave pública: "))
    phi = (p-1)*(q-1)
    n = p*q
    while not mdcEuclides(phi, e) == 1:
        print("Não foi inserido um expoente relativamente primo!")
        e = int(input("Insira um expoente relativamente primo a (p-1)(q-1): "))
    mdcAux(e, phi, div)
    d = getInverse(div, table, phi)
    encryptedFile = open("encryptedFile.txt", 'r')
    encryptedString = encryptedFile.readline().split()
    for value in encryptedString:
        dChar = expM(int(value), n, d) + 97
        if dChar > 122:
            dChar = 32
        decryptedFile.write(f'{str(chr(dChar))}')


while True:
    option = menu()
    if option == 0:
        break
    elif option == 1:
        generateKey()
    elif option == 2:
        encryptText()
    elif option == 3:
        decryptText()
