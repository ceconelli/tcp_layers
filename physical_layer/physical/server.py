
#   server.py - physical layer
#   This scr implements server class, that must to be capable
#   of transmit/receive Ethernet frames (RFC 895) to/from clients, in a file
#   with 0's and 1's mimicking the bits specified in the RFC cited.
#   That class must also be capable to communicate with the network one.

import socket as sct
import subprocess
from datetime import datetime as dt
import random
import time
from frame import frame
from util import genMACAddr, calcCollisionProb
import requests
import json

class server(object):
    """Defines a server class"""

    def __init__(self):
        """Defines server's default constructor"""
        self.HOST = 'localhost'
        self.PORT = 8084
        self.MSGS_FOLDER = 'server/messages/'
        self.FRAME = 'frame.txt'
        self.BIN_FRAME = 'bin-frame.txt'
        self.serverSocket = None
        self.MAC_ADDRESS = subprocess.getoutput(
            ["ifconfig enp7s0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'", ''])

    def receiveFromAbove(self, connectionSocket,
                         ipAddr, message):
        """
        Receives message from upper layer, saves it as human readable and 
        binary frames and send it to client
        """
        print(str(dt.now()) + ': receiving message (\'' +
              message + '\') from upper layer')
        destMACAddr = ''
        if ipAddr != 'localhost':
            destMACAddr = genMACAddr(ipAddr)
        else:
            destMACAddr = self.MAC_ADDRESS
        size = len(message)
        print(str(dt.now()) + ': saving human readable frame')
        origPDU = frame(destMACAddr, self.MAC_ADDRESS, message,
                        payloadSize=size, frameType='human')
        origPDU.writePDU(self.MSGS_FOLDER + 'sent/' + self.FRAME)
        cvtdPDU = origPDU.convertPDU()
        print(str(dt.now()) + ': saving binary frame')
        cvtdPDU.writePDU(self.MSGS_FOLDER + 'sent/' + self.BIN_FRAME)
        self.sendToClient(connectionSocket,
                          origPDU.payloadSize * 8,
                          self.MSGS_FOLDER + 'sent/' + self.BIN_FRAME)

    def receiveFromClient(self, clientSocket):
        """Returns the frame data received from client as file"""
        frameAsString = ''
        f = open(self.MSGS_FOLDER + 'received/' + self.BIN_FRAME, 'w+')
        # Receiving the header
        print(str(dt.now()) + ': starting to receive file from client')
        while True:
            dataStr = clientSocket.recv(
                frame.HEADER_SIZE + frame.MAX_PAYLOAD_SIZE).decode('utf-8')
            if len(dataStr) > 0:
                frameAsString += dataStr
            else:
                break
        f.write(frameAsString)
        f.close()
        print(str(dt.now()) + ': message has been received and saved (binary mode)!')
        return self.MSGS_FOLDER + 'received/' + self.BIN_FRAME

    def sendToAbove(self, cvtdPDUPath):
        """Sends message received from client to the upper layer"""
        print(str(dt.now()) + ': sending the received message for upper layer')
        cvtdPDU = frame('', '', '', frameType='bin')
        cvtdPDU.readPDU(cvtdPDUPath)
        print(str(dt.now()) + ': saving human-readable frame')
        origPDU = cvtdPDU.deconvertPDU()
        origPDU.writePDU(self.MSGS_FOLDER + 'received/' + self.FRAME)
        return origPDU.payload

    def sendToClient(self, connection,
                     payloadSize, cvtdPDUFile):
        """Sends binary frame to client"""
        with open(cvtdPDUFile, 'r') as f:
            cvtdPDU = f.read(frame.HEADER_SIZE + payloadSize)
            header = cvtdPDU[:frame.HEADER_SIZE]
            payload = cvtdPDU[frame.HEADER_SIZE:]
            sent = 0
            totalSent = 0
            if calcCollisionProb(0, 100) == True:
                timeToWait = random.randint(0, 3)
                print(str(dt.now()) + ': collision! Server waits for ' +
                      str(timeToWait) + ' second(s)')
                time.sleep(timeToWait)
            print(str(dt.now()) + ': starting to send frame to client')
            while totalSent < len(header) + len(payload):
                sent = connection.send(cvtdPDU.encode('utf-8'))
                totalSent += sent
            print(str(dt.now()) + ': frame sent!')

    def run(self):
        """
        Turns server's socket binded to hostname and PORT and that
        listens to up to one connections
        """
        print(str(dt.now()) + ': creating socket and binding to the port')
        self.serverSocket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
        self.serverSocket.bind((self.HOST, self.PORT))
        self.serverSocket.listen(1)

        print(str(dt.now()) + ': waiting for client')
        clientSocket, addr = self.serverSocket.accept()

        # Returns socket object and a address tuple composed by ip and port
        cvtdPDUPath = self.receiveFromClient(clientSocket)
        messageReceived = self.sendToAbove(cvtdPDUPath)
        print(str(dt.now()) + ': the message received was: \'' +
              messageReceived + '\'')

        print(str(dt.now()) + ': sending the received message for upper layer')
        url = "http://localhost:8000/receive_message"
        data = {'msg': messageReceived}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        self.receiveFromAbove(clientSocket, 'localhost', r.text)
        print('bye python')
        
