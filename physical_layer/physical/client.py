
#   client.py - physical layer
#   This src implements a client class, which instances must be capable
#   to connect to a instance of the server class and transmit/receive
#   files to/from it.

import socket as sct
import os
import subprocess
from datetime import datetime as dt
import time
import random
from util import genMACAddr, calcCollisionProb
from frame import frame
import requests
import json

class client(object):
    """Defines client class"""

    def __init__(self):
        """Defines default constructor for client class"""
        self.PORT = 8082
        self.MSGS_FOLDER = 'client/messages/'
        self.FRAME = 'frame.txt'
        self.BIN_FRAME = 'bin-frame.txt'
        self.MAC_ADDRESS = subprocess.getoutput(
            ["ifconfig enp7s0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'", ''])

    def receiveFromAbove(self, connectionSocket,
                         ipAddr, message):
        """
        Receives message and destination ip from upper layers, put it into a
        frame, save this frame and convert it to binary-mode. The converted
        frame is also saved and fowarded to sendToServer method.
        """
        print(str(dt.now()) + ': receiving message (\'' +
              message + '\') from upper layer')
        destMACAddr = ''
        if ipAddr != 'localhost':
            destMACAddr = genMACAddr(ipAddr)
        else:
            destMACAddr = self.MAC_ADDRESS
        size = len(message)
        origPDU = frame(destMACAddr, self.MAC_ADDRESS, message,
                        payloadSize=size, frameType='human')
        print(str(dt.now()) + ': saving human readable frame')
        origPDU.writePDU(self.MSGS_FOLDER + 'sent/' + self.FRAME)
        cvtdPDU = origPDU.convertPDU()
        print(str(dt.now()) + ': saving binary frame')
        cvtdPDU.writePDU(self.MSGS_FOLDER + 'sent/' + self.BIN_FRAME)
        self.sendToServer(connectionSocket,
                          origPDU.payloadSize * 8,
                          self.MSGS_FOLDER + 'sent/' + self.BIN_FRAME)

    def receiveFromServer(self, connection):
        """Receives binary frame from server and sends it to upper layers"""
        frameAsString = ''
        f = open(self.MSGS_FOLDER + 'received/' + self.BIN_FRAME, 'w+')
        # Receiving the header
        print(str(dt.now()) + ': starting to receive file from server')
        while True:
            dataStr = connection.recv(
                frame.HEADER_SIZE + frame.MAX_PAYLOAD_SIZE).decode('utf-8')
            if len(dataStr) > 0:
                frameAsString += dataStr
            else:
                break
        f.write(frameAsString)
        f.close()
        print(str(dt.now()) + ': message has been received and saved (binary mode)!')
        self.sendToAbove(self.MSGS_FOLDER + 'received/' + self.BIN_FRAME)

    def sendToAbove(self, cvtdPDUPath):
        """Sends given frame (which path is pointed by cvtdPDUPath) to upper layers"""
        print(str(dt.now()) + ': sending the received message for upper layer')
        cvtdPDU = frame('', '', '', frameType='bin')
        cvtdPDU.readPDU(cvtdPDUPath)
        origPDU = cvtdPDU.deconvertPDU()
        print(str(dt.now()) + ': saving human-readable frame')
        origPDU.writePDU(self.MSGS_FOLDER + 'received/' + self.FRAME)
        print(str(dt.now()) + ': the message received was: \'' +
              origPDU.payload + '\'')

        # url = "http://localhost:3000/receive_message"
        url = "http://localhost:10524/receivemessagephycli/teste"
        data = {'msg': origPDU.payload}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        print("sendToAbove")
    def sendToServer(self, connection,
                     payloadSize, cvtdPDUFile):
        """
        Sends to server addressed by connection the converted PDU File
        cvtdPDUFile with payload size of payloadSize
        """
        with open(cvtdPDUFile, 'r') as f:
            cvtdPDU = f.read(frame.HEADER_SIZE + payloadSize)
            header = cvtdPDU[:frame.HEADER_SIZE]
            payload = cvtdPDU[frame.HEADER_SIZE:]
            sent = 0
            totalSent = 0
            if calcCollisionProb(0, 100) == True:
                timeToWait = random.randint(0, 3)
                print(str(dt.now()) + ': collision! Client waits for ' +
                      str(timeToWait) + ' second(s)')
                time.sleep(timeToWait)
            print(str(dt.now()) + ': starting to send frame to server')
            while totalSent < len(header) + len(payload):
                sent = connection.send(cvtdPDU.encode('utf-8'))
                totalSent += sent
            # blocking sends for start receiving (because if not it bugs)
            connection.shutdown(sct.SHUT_WR)
            print(str(dt.now()) + ': frame sent!')

    def connectToServer(self, ipAddr, port):
        """Returns socket connection with given ip in the given port"""
        print(str(dt.now()) + ': creating connection to server')
        connection = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
        connection.connect((ipAddr, port))
        return connection

    def waitForMessage(self,connection):
        while not os.path.exists('../../application_layer_client/messages/sent/file.txt'):
            pass

        time.sleep(1.5)

        file = open('../../application_layer_client/messages/sent/file.txt','r')
        content = file.read()
        print(content)

        os.remove('../../application_layer_client/messages/sent/file.txt')
        self.receiveFromAbove(connection, 'localhost', content)
        self.receiveFromServer(connection)
        
