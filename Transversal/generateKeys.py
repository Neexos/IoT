# encoding: utf-8
from Crypto.PublicKey import RSA
'''
key = RSA.generate(1024)  # generation du couple de clefs

pubKey = key.publickey()  # clef publique
privateKey = key.exportKey('PEM')  # cle privee

print("clé publique: \n" + pubKey.exportKey('PEM'))
print("clé privée: \n" + privateKey)

with open('publicClient.pem','w') as pf:
	pf.write(pubKey.exportKey("PEM").decode())
	pf.close()

with open('privateClient.pem', 'w') as fp:
	fp.write(privateKey.decode())
	fp.close()

'''
with open('publicClient.pem', 'r') as fk:
	pub = fk.read()
	fk.close()

with open('privateClient.pem', 'r') as fk:
	priv = fk.read()
	fk.close()

pubKey = RSA.importKey(pub)
privateKey = RSA.importKey(priv)

test = "15,2,3;65,2,4"
encrypted = pubKey.encrypt(test, 32)
print(encrypted)
decrypted = privateKey.decrypt(encrypted)
print(decrypted)