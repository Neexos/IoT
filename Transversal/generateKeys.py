# encoding: utf-8
from Crypto.PublicKey import RSA

key = RSA.generate(1024)  # generation du couple de clefs

pubKey = key.publickey()  # clef publique
privateKey = key.exportKey('PEM')  # cle privee

print("clé publique: \n" + pubKey.exportKey('PEM'))
print("clé privée: \n" + privateKey)

with open('public2.pem','w') as pf:
	pf.write(pubKey.exportKey("PEM").decode())
	pf.close()

with open('private2.pem', 'w') as kf:
    kf.write(privateKey.decode())
    kf.close()