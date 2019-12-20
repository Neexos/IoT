import serial

# send serial message 
# Don't forget to establish the right serial port ******** ATTENTION
SERIALPORT = "/dev/ttyUSB0"
#SERIALPORT = "/dev/tty.usbserial-DA00G4XZ"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():
    if serialButton['text'] == "Open Serial":
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
        serialButton['text'] = "Close Serial"
        b['state'] = 'normal'
    else:
        ser.close()
        serialButton['text'] = "Open Serial"
        b['state'] = 'disabled'


def sendUARTMessage(msg):
    ser.write(msg.encode())
    print("Message <" + msg + "> sent to micro-controller." )


def readData():
    # BOUCLE ENVOIS DES DONNEES
    for i in range(1):
        column = i - (i // 10) * 10
        row = i // 10
        if scales[i].get() > 0:
            print("Fire x=%d, y=%d has value %d" % (row, column, scales[i].get()))
        sendUARTMessage("%d%d%d\n\r" % (row, column, scales[i].get()))

    b['state'] = 'normal'

def envois_de_test():
    b['state'] = 'disabled'
    sendUARTMessage("TLH")
    b['state'] = 'normal'

b = Button(master, text="Send Values", highlightcolor="blue", command=read_scales,
           state="disabled")  # button to read values
serialButton = Button(master, text="Open Serial", highlightcolor="blue", command=initUART)  # button to read values
b.grid(row=6, column=7, columnspan=3)
serialButton.grid(row=6, column=0, columnspan=3)

# initUART()

mainloop()

