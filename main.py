from tkinter import *
import sys
import glob
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox, ttk
import serial
import time
from timeit import default_timer
import serial.tools.list_ports

import threading
from inputimeout import inputimeout, TimeoutOccurred
import filing as fl
import edc as crc


file_path=''
file_version=''
file_size=0
serial_port = ''
find_alt = 0

def get_all_uart_list():
    result = []
    comlist = serial.tools.list_ports.comports()
    for element in comlist:
        result.append(element.device)    
    return result

def selection_changed(event):
    serial_port = event.widget.get()
    print(serial_port)

def select_file():
    print("select file")
    from tkinter import filedialog
    file_path = filedialog.askopenfilename(filetypes=[("BIN files", "*.bin")])
    return file_path

def main():
    result = get_all_uart_list()
    crc16 = crc.EDC()
    fota = fl.Filing()
    data = [0x90, 0x88, 0x23, 0x43, 0x11]
  
    crc16.polynomial    = 0x0589
    crc16.init          = 0x0000
    crc16.RefInRefOut   = False
    crc16.XorOut        = 0x0001
    res = crc16.calculate(data, 5)
    print(res)
    # root = tk.Tk()
    # root.config(width=300, height=200)
    # root.title("Button Window")

    # b = tk.Button(root, text="select file", command=select_file)
    # b.pack()
    # fota.set_file_path(b.invoke())

    # combo = ttk.Combobox(root, values=result)
    # combo.pack()
    # combo.bind("<<ComboboxSelected>>", selection_changed)

    # root.mainloop()

main()