
def ping(ipAddr):
    """Returns if ping command was successful for given ipAddr"""
    import subprocess
    import platform

    if platform.system().lower() != 'windows':
        ping_str = '-c 1'

    resposta = subprocess.getstatusoutput('ping ' + ping_str + ' ' + ipAddr)
    return resposta[0]


def genMACAddr(ipAddr):
    """
    Tests if the given ipAddr is on the local network and returns the 
    MAC Address of the respective device
    """
    import subprocess

    if ping(ipAddr) == 0:
        return subprocess.getoutput(
            "arp -a " + ipAddr + " | cut -d' ' -f4")
    else:
        return 0


def string2bits(s='', fill=8):
    """
    Converts given string to the respective ascii-binary 
    version (using 8 bits)
    """
    # src: https://stackoverflow.com/a/40949538
    l = [bin(ord(x))[2:].zfill(fill) for x in s]
    string = ''
    for i in l:
        string += i
    return string


def bits2string(b=None):
    """
    Converts given ascii-binary string to the respective ascii 
    version (using 8 bits)
    """
    # src: https://stackoverflow.com/a/40949538
    #      https://stackoverflow.com/a/7397195
    b=-len(b) % 8 * '0' + b
    string_blocks=(b[i:i+8] for i in range(0, len(b), 8))
    string=''.join([chr(int(x, 2)) for x in string_blocks])
    string=string.replace('\x00', '')
    return string


def calcCollisionProb(down, up):
    """Return if there is a collision for given interval"""
    import random

    randomValue=random.randint(0, 100)
    if randomValue >= down and randomValue <= up:
        return True
    else:
        return False
