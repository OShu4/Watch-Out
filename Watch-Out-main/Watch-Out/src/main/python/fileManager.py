from codecs import decode
import struct

class FileManager():
    def getToFile():
        file=open("Watch-Out/src/main/python/data/data.bin","rb")
        byte = file.read(1)
        byteScore = bytes()
        while byte:
            byteScore=byteScore+ byte
            byte = file.read(1)
        return byteScore

    def bin_to_float(b):
        """ Convert binary string to a float. """
        bf = decode('%%0%dx' % (8 << 1) % int(b, 2), 'hex')[-8:]  # 8 bytes needed for IEEE 754 binary64.
        return struct.unpack('>d', bf)[0]


    def float_to_bin(value):  # For testing.
        """ Convert float to 64-bit binary string. """
        [d] = struct.unpack(">Q", struct.pack(">d", value))
        return '{:064b}'.format(d)


