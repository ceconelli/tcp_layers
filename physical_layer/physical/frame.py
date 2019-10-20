
#   frame.py - physical layer
#   The Ethernet frame is defined by RFC 895, but this code
#   will follow the norms defined by the class. That norms are:
#       - Destination MAC Address: 6 bytes
#       - Sender MAC Address: 6 bytes
#       - Payload's size : 2 bytes
#       - Payload : 0-1500 bytes
from util import string2bits, bits2string


class frame(object):
    """
    Defines a Ethernet frame with MAC addresses for destine, origin, 
    payload's size and payload
    """

    HEADER_SIZE = 48 + 48 + 16  # 2 * 6 * 8 (simulated bits) + 2
    MAX_PAYLOAD_SIZE = 1500

    def __init__(self, destMACAddr, origMACAddr, message, payloadSize=0,
                 payloadStrSize='', frameType=''):
        """Defines frame's default construct"""
        self.destMACAddr = destMACAddr
        self.origMACAddr = origMACAddr
        self.payloadSize = payloadSize
        self.payloadStrSize = payloadStrSize
        self.payload = message
        self.frameType = frameType

    def readPDU(self, pathDesired):
        """
        Reads file indicated by pathDesired and populates the frame object
        with data obtained from the file
        """
        f = open(pathDesired, 'r')
        if self.frameType == 'human':
            self.destMACAddr = f.readline()[:17]
            self.origMACAddr = f.readline()[:17]
            self.payloadSize = int(f.readline())
            self.payload = f.readline()[:self.payloadSize]
        elif self.frameType == 'bin':
            bin_str = f.readline()
            self.destMACAddr = bin_str[:48]
            self.origMACAddr = bin_str[48:96]
            self.payloadStrSize = bin_str[96:112]
            self.payload = bin_str[112:]

    def writePDU(self, pathDesired):
        """Writes original or converted PDU to disk in the pathDesired location"""
        f = open(pathDesired, 'w+')
        if self.frameType == 'human':  # original frame - human
            f.write(self.destMACAddr + '\n')
            f.write(self.origMACAddr + '\n')
            f.write(str(self.payloadSize) + '\n')
            f.write(self.payload + '\n')
        elif self.frameType == 'bin':  # converted frame - binary
            f.write(self.destMACAddr)
            f.write(self.origMACAddr)
            f.write(self.payloadStrSize)
            f.write(self.payload)
        f.close()

    def convertPDU(self):
        """Returns frame object in simulated binary way"""
        destMACAddr = self.destMACAddr.replace(':', '')
        destMACAddr = "{0:048b}".format(int(destMACAddr, 16))
        origMACAddr = self.origMACAddr.replace(':', '')
        origMACAddr = "{0:048b}".format(int(origMACAddr, 16))
        payloadStrSize = bin(self.payloadSize)[2:].zfill(16)
        message = string2bits(str(self.payload))
        return frame(destMACAddr, origMACAddr, message,
                     payloadStrSize=payloadStrSize, frameType='bin')

    def deconvertPDU(self):
        """
        Converts frame from binary to human readable format
        """
        destMACAddr = hex(int(self.destMACAddr, 2))[2:]
        destMACAddr = destMACAddr[0:2] + ':' + destMACAddr[2:4] + ':' + \
            destMACAddr[4:6] + ':' + destMACAddr[6:8] + ':' + \
            destMACAddr[8:10] + ':' + destMACAddr[10:]
        origMACAddr = hex(int(self.origMACAddr, 2))[2:]
        origMACAddr = origMACAddr[0:2] + ':' + origMACAddr[2:4] + ':' + \
            origMACAddr[4:6] + ':' + origMACAddr[6:8] + ':' + \
            origMACAddr[8:10] + ':' + origMACAddr[10:]
        payloadSize = int(self.payloadStrSize, 2)
        message = bits2string(str(self.payload))
        return frame(destMACAddr, origMACAddr, message,
                     payloadSize=payloadSize, frameType='human')
