# from frame import frame
# from util import genMACAddr
# from util import calcCollisionProb
# from client import client
from server import server

# f = frame('12:34:56:78:90:ab', '34:56:78:90:ab:cd', 'hello',
# payloadSize=5, frameType='human')  # human format
# f = frame('', '', '', frameType='bin')  # human format
# f = frame('', '', '', frameType='human')  # human format

# fc = f.convertPDU()
# print(fc.destMACAddr + ' ' + fc.origMACAddr +
#       ' ' + fc.payloadStrSize + ' ' +
#       fc.payload)  # bin format

# fdc = fc.deconvertPDU()
# print(fdc.destMACAddr + ' ' + fdc.origMACAddr +
#       ' ' + str(fdc.payloadSize) + ' ' +
#       fdc.payload)  # human format

# f.readPDU('./bin-frame.txt')
# f.readPDU('./frame.txt')
# print(f.destMACAddr + ' ' + f.origMACAddr +
#       ' ' + str(f.payloadStrSize) + ' ' +
#       f.payload)  # bin format
# fdc = f.deconvertPDU()
# print(fdc.destMACAddr + ' ' + fdc.origMACAddr +
#       ' ' + str(fdc.payloadSize) + ' ' +
#       fdc.payload)  # human format

# print(f.destMACAddr + ' ' + f.origMACAddr +
#       ' ' + str(f.payloadSize) + ' ' +
#       f.payload)  # human format
# f.writePDU('./frame.txt')
# fc.writePDU('./bin-frame.txt')

# print(genMACAddr('192.168.0.10'))
# print(calcCollisionProb(25, 75))

# c = client()
# conn = c.connectToServer('localhost', 8081)
# c.receiveFromAbove(conn, 'localhost', "Marcelo Candido")

s = server()
s.run()
