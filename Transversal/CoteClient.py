# encoding: utf-8
from Crypto.PublicKey import RSA
import requests 

key = RSA.generate(1024)  # generation du couple de clefs
pubKey = key.publickey()  # clef publique
privateKey = key.exportKey('PEM')  # cle privee
url = "https://emergencymanager.azurewebsites.net/fire/send"

myRequest = requests.post(url, data="45.4878843,55.666,8;")
print(myRequest.status_code)