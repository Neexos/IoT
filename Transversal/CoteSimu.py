# encoding: utf-8
from Crypto.PublicKey import RSA
import requests, time, serial


#---------- VARS --------------

url = "https://cpefiresimulation.azurewebsites.net/get"
myRequest = requests.get(url)

SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 115200
ser = serial.Serial()

strt = time.time()


#--------- FUNCTIONS ----------
def initKeys():
    global pubKey
    global privateKey
    try:
        with open('publicClient.pem', 'r') as fk:
            pub = fk.read()
            fk.close()
    except:
        print("erreur lors de la lecture du fichier 'publicClient.pem'\n")
    try:
        with open('privateSimu.pem', 'r') as fk:
            priv = fk.read()
            fk.close()
    except:
        print("erreur lors de la lecture du fichier 'privateSimu.pem'\n")
    pubKey = RSA.importKey(pub)
    privateKey = RSA.importKey(priv)

def initUART(state):
    if state == 'open':
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.port = SERIALPORT
        ser.baudrate = BAUDRATE
        ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        ser.parity = serial.PARITY_NONE  # set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        ser.timeout = None  # block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        ser.xonxoff = False  # disable software flow control
        ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        # ser.writeTimeout = 0     #timeout for write
        print ("Starting Up Serial Monitor")
        try:
            ser.open()
        except serial.SerialException:
            print("Serial {} port not available".format(SERIALPORT))
            exit()
    elif state == 'close':
        ser.close()


def sendUARTMessage(msg):
    ser.write(msg)

def encryptData(myString):
    encrypted = pubKey.encrypt(myString, 32)
    return encrypted

def getData(req):
    return req.text

def formatList(lst):
    lst = lst[1:-1]                             # On enlève les [] de debut/fin
    lst = lst.replace('[', '').replace(']', '') # on enlèce tous les autres []
    lst = lst.split('"')                        # on split selon les ""
    lst = list(filter(None, lst))               # supressions des valeurs null
    while (',' in lst):                         # suppressions des virgules
        lst.remove(",")
    return lst

def formatPacket(myStr, sizePacket=32):
    lstPackets = []
    nbPacket = len(myStr)/sizePacket
    for i in range(nbPacket):
        lstPackets.append(myStr[:sizePacket])
        myStr = myStr[sizePacket:]
    return lstPackets

def formatRawData(myStr, size=128):
    lst = []
    nbSplit = len(myStr)/size
    for i in range(nbSplit):
        lst.append(myStr[:size])
        myStr = myStr[size:]
    return lst

def main():
    formattedStr = ""
    if myRequest.status_code == 200:
        data = getData(myRequest)
        data = formatList(data)
        count = 1
        for x in range(len(data)):
            if(count%3 != 0):
                formattedStr += data[x] + ','
            else:
                formattedStr += data[x] + ';'
            count += 1
        # On peut prendre jusqu'à 21 triplets dans cette liste pour crypter
        listSplittedPointVirgule = formattedStr.split(';')
        print(listSplittedPointVirgule)
        buffer = []
        splittedStr = ""
        for z in range(21):
            try:
                buffer.append(listSplittedPointVirgule[z])
            except:
                print("index out of range")
        for triplet in buffer:
            splittedStr += triplet
        print(len(splittedStr))
        encryptedData = encryptData(str(splittedStr))
        print(encryptedData)
'''
        # TODO: spliter la formattedStr sinon trop long pour crypter (128 carac max)
        if (not(len(formattedStr) <= 128)):
            rawData = formatRawData(formattedStr)
            for x in range(len(rawData)):
                encryptedData = encryptData(str(rawData[x]))
                print(str(encryptedData[0]))
                if ( not(len(encryptedData[0]) <= 60) ):
                    packets = formatPacket(str(encryptedData[0]))
                    initUART('open')
                    for i in range(len(packets)):
                        sendUARTMessage(packets[i])
                    initUART('close')
                else:
                    initUART('open')
                    sendUARTMessage(encryptedData)
                    initUART('close')
        else:
            encryptedData = encryptData(str(formattedStr))
            if ( not(len(encryptedData[0]) <= 60) ):
                packets = formatPacket(str(encryptedData[0]))
                initUART('open')
                for i in range(len(packets)):
                    sendUARTMessage(packets[i])
                initUART('close')
            else:
                initUART('open')
                sendUARTMessage(encryptedData)
                initUART('close')
    else:
        print("Impossible de récupérer des données du serveur, code http: " + str(myRequest.status_code))
        time.sleep(2)
'''
#-------- WHILE TRUE ---------
initKeys()
while(1):
    main()
    time.sleep(3)

'''
encryptedData = pubKey.encrypt(data, 32)
decrypted = privateKey.decrypt(encryptedData)
print(encryptedData)
print(len(encryptedData[0]))
print('\n')
print(decrypted)
end = time.time()
print("----- Execution time: " + str(end-strt) + " -----")
'''