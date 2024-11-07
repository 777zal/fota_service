from enum import Enum

class CRC16_Type(Enum):
    ARC     = "ARC"
    XMODEM  = "XMODEM"

class EDC:
    notReady        = True
    polynomial      = 0x0000
    init            = 0x0000
    XorOut          = 0x0000
    RefInRefOut     = True

    def __flip_polynomial(self, poly:int):
        flip_poly = 0
        for i in (range(0,16)):
            res = (poly >> (15-i)) & 0x0001
            res = res << i
            flip_poly = flip_poly | res
        return flip_poly

    def __set_polynomial(self, poly:int):
        self.polynomial = poly

    def __set_refInrefOut(self, state: bool):
        self.RefInRefOut = state
    
    def __set_init(self, value:int):
        self.init = value

    def __set_xorout(self, value:int):
        self.XorOut = value

    def calculate(self, data: bytearray, length: int):
        crc = self.init
        poly = self.polynomial

        if self.notReady:
            print("ERROR : CRC16 Type is not defined")
            return 
        if self.RefInRefOut:
            poly = self.__flip_polynomial(self.polynomial)
            
        for i in (range(0, length)):
            if self.RefInRefOut:
                crc ^= data[i]
            else:
                crc ^= data[i] << 8
            for j in range(0, 8):
                if self.RefInRefOut:
                    if (crc & 0x0001) > 0:
                        crc = (crc >> 1) ^ poly
                    else:
                        crc = crc >> 1
                else :
                    if (crc & 0x8000) > 0:
                        crc =(crc << 1) ^ poly
                    else:
                        crc = crc << 1
                    crc = crc & 0xFFFF #avoid overflowing
        return crc^self.XorOut

    def __set_mode(self, type: str):
        poly                = 0x0000
        init_val            = 0x0000
        XorOut_val          = 0x0000
        RefInRefOut_state   = True
        match type:
            case 'ARC':
                poly                = 0x8005
                init_val            = 0x0000
                XorOut_val          = 0x0000
                RefInRefOut_state   = True
            case 'XMODEM' :
                poly                = 0x1021
                init_val            = 0x0000
                XorOut_val          = 0x0000
                RefInRefOut_state   = False
            case _:
                poly                = 0x0000
                init_val            = 0x0000
                XorOut_val          = 0x0000
                RefInRefOut_state   = True
        self.__set_polynomial(poly)
        self.__set_init(init_val)
        self.__set_xorout(XorOut_val)
        self.__set_refInrefOut(RefInRefOut_state)

    def __init__(self, type:str):
        for crctype in (CRC16_Type):
            if( type == crctype.value):
                print("Set as "+type)
                self.__set_mode(type)
                self.notReady = False
                break
        if self.notReady :
            print("Error :"+type+" not found available options are :")
            for crctype in (CRC16_Type):
                print('  -'+crctype.value)    