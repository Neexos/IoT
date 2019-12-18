# encoding: utf-8
from Crypto.PublicKey import RSA
import requests, time

#---------- VARS --------------
key = RSA.generate(1024)  # generation du couple de clefs
pubKey = key.publickey()  # clef publique
privateKey = key  # cle privee
url = "https://cpefiresimulation.azurewebsites.net/get"
myRequest = requests.get(url)
strt = time.time()
#--------- FUNCTIONS ----------

def encryptData(myString):
    encrypted = pubKey.encrypt(myString, 32)
    return encrypted

def getData(req):
    return req.text

def main():
    ret = ""
    data = getData(myRequest)
    '''data = data.split()
    for i in data:
        print("bla")
        # ret += i[0] + ',' + i[1] + ',' + i[2] + ';'
    '''
    print(data)
    print(len(data))

#-------- WHILE TRUE
while(1):
    main()
    time.sleep(3)

# TODO: faire la fonction get web pour recuperer les data a afficher
data = b"4.84674,45.74846,9;"  # represente le retour

encryptedData = pubKey.encrypt(data, 32)

decrypted = privateKey.decrypt(encryptedData)
print(encryptedData)
print(len(encryptedData[0]))
print('\n')
print(decrypted)
end = time.time()
print("----- Execution time: " + str(end-strt) + " -----")