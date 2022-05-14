from codecs import decode
import struct
from asyncio.windows_events import NULL
from os.path import exists
from fastnumbers import isfloat

class FileManager():
    def getToFile():
        path="Watch-Out/src/main/python/data/data.bin"
        if not exists(path):
            return "non esiste"
        file = open(path, "rb")
        byte = file.read(1)
        byteScore = bytes()
        while byte:
            byteScore = byteScore + byte
            byte = file.read(1)
        return byteScore

    def bin_to_float(b):
        """ Convert binary string to a float. """
        bf = decode('%%0%dx' % (8 << 1) % int(b, 2),
                    'hex')[-8:]  # 8 bytes needed for IEEE 754 binary64.
        return struct.unpack('>d', bf)[0]

    def float_to_bin(value):  # For testing.
        """ Convert float to 64-bit binary string. """
        [d] = struct.unpack(">Q", struct.pack(">d", value))
        return '{:064b}'.format(d)

    def getScore():
        risBin = FileManager.getToFile()
        if risBin=="non esiste":
            return 0.0
        risFloat = FileManager.bin_to_float(risBin)
        return float(risFloat)

    def writeTO(end, start, file):
        print("1a")
        path="Watch-Out/src/main/python/data/"+file+".bin"
        f = open(path, "wb")
        if isfloat(end):
            print("tsa")
            resString = round(end-start, 2)
            byteResult = FileManager.float_to_bin(resString)
            f.write(bytearray(byteResult, "utf8"))
        else:
            f.write(bytearray(end, "utf8"))
        return
