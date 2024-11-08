from enum import Enum
import serial
import serial.tools.list_ports
import edc as crc

class UART:
    def __init__(self):
        self.cr = crc.EDC("ARC")
        print("Uart has Set")

    def get_all_uart_list(self):
        result = []
        comlist = serial.tools.list_ports.comports()
        for element in comlist:
            result.append(element.device)    
        return result

    def set_uart_device(self, dev_path:str, baud_rate:int):
        try:
            print("UART set at "+dev_path)
            self.serial_instance = serial.Serial(dev_path,baud_rate)
        except Exception as e:
            print("ERROR")

    def compose_message(self, cmd:str, data:bytearray):
        packet = bytearray(b'')
        packet += (bytes('#','utf-8'))
        packet += (bytes(cmd,'utf-8'))
        length = len(data)
        print(length)
        packet += (length.to_bytes(2,'big'))
        packet += data
        crc16 = self.cr.calculate(packet, length+4)
        print(crc16)
        packet += (crc16.to_bytes(2,'big'))
        packet += (bytes(';','utf-8'))
        return packet

    def transmit_message(self, data:bytearray):
        self.serial_instance.write(data)


