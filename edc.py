class EDC:
    mode = [""]
    polynomial      = 0x0000
    init            = 0x0000
    XorOut          = 0x0000
    RefInRefOut     = True

    def __init__(self):
        print("CRC Class Has Set")
    
    def __flip_polynomial(self, poly:int):
        flip_poly = 0
        for i in (range(0,16)):
            res = (poly >> (15-i)) & 0x0001
            res = res << i
            flip_poly = flip_poly | res
        return flip_poly

    def set_polynomial(self, poly:int):
        self.polynomial = poly

    def calculate(self, data: bytearray, length: int):
        crc = self.init
        poly = self.polynomial
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


