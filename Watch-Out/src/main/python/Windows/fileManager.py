from codecs import decode
import struct
from asyncio.windows_events import NULL
from os.path import exists
from fastnumbers import isfloat
import json

class FileManager():

    #legge dal binario
    def getToFile(file):
        path="data/"+file+".bin"
        if not exists(path):
            return "non esiste"
        file = open(path, "rb")
        byte = file.read(1)
        byteScore = bytes()
        while byte:
            byteScore = byteScore + byte
            byte = file.read(1)
        return byteScore

    #converte da decimale a binario
    def BinaryToDecimal(binary):
        string = int(binary, 2)
        return string  

    #converte da binario a float
    def bin_to_float(b):
        """ Convert binary string to a float. """
        bf = decode('%%0%dx' % (8 << 1) % int(b, 2),
                    'hex')[-8:]  
        return struct.unpack('>d', bf)[0]

    #converte float a binario
    def float_to_bin(value):  
        """ Convert float to 64-bit binary string. """
        [d] = struct.unpack(">Q", struct.pack(">d", value))
        return '{:064b}'.format(d)

    #converte da binario a stringa
    def bin_to_str(file):
        bin_data=FileManager.getToFile(file)
        if bin_data=="non esiste":
            return 
        bin_data=(bin_data.decode('ascii')).replace(" ", "")
        str_data =' '
        for i in range(0, len(bin_data), 7):
            temp_data = bin_data[i:i + 7]
            decimal_data =FileManager.BinaryToDecimal(temp_data)
            str_data = str_data + chr(decimal_data)
        return str_data

    #legge dal file binario lo score
    def getScore():
        risBin = FileManager.getToFile("data")
        if risBin=="non esiste":
            return 0.0
        risFloat = FileManager.bin_to_float(risBin)
        return float(risFloat)

    #scrive su file binario
    def writeTO(time, file):
        path="data/"+file+".bin"
        f = open(path, "wb")
        if isfloat(time):
            byteResult = FileManager.float_to_bin(time)
            f.write(bytearray(byteResult, "utf8"))
        else:
            f.write(bytearray(time, "utf8"))
        return

    #legge da Json le size
    def JsonReader(path):
        with open(path) as f:
            data = json.load(f)

        w = data["frames"]["images"] ["frame"] ["w"] 
        h = data["frames"]["images"] ["frame"] ["h"] 
        size =[w,h] 
        return size