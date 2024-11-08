from tkinter import *
import sys
import glob
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox, ttk
import time
from timeit import default_timer

import threading
from inputimeout import inputimeout, TimeoutOccurred
import filing as fl
import uart as ua

uart1   = ua.UART()
fota    = fl.Filing()

file_path       = ''
file_version    = ''
file_size       = 0
serial_port     = ''
find_alt        = 0

def selection_changed(event):
    serial_port = event.widget.get()
    uart1.set_uart_device(serial_port, 115200)

def select_file():
    from tkinter import filedialog
    file_path = filedialog.askopenfilename(filetypes=[("BIN files", "*.bin")])
    fota.set_file_path(file_path)

def send_data():
    data = [0x99, 0x22, 0x98]
    
    msg = uart1.compose_message('1', bytearray(data))
    uart1.transmit_message(msg)
def main():   
    result  = uart1.get_all_uart_list()
    root = tk.Tk()
    root.config(width=300, height=200)
    root.title("Button Window")

    LABEL_FILE = tk.Label(
        root,
        text="Choose File",
        font=Font(family="Arial", size=10, weight="bold")
        )
    LABEL_FILE.pack(fill="x")

    BUTTON_FILE = tk.Button(
        root, 
        text="select file", 
        command=select_file)
    BUTTON_FILE.pack()

    LABEL_UART = tk.Label(
        root,
        text="Choose UART",
        font=Font(family="Arial", size=10, weight="bold")
        )
    LABEL_UART.pack(fill="x")

    COMBO_UART_LIST = ttk.Combobox(
        root, 
        values=result)
    COMBO_UART_LIST.pack()
    COMBO_UART_LIST.bind("<<ComboboxSelected>>", selection_changed)

    BUTTON_SEND = tk.Button(
        root, 
        text="send data", 
        command=send_data)
    BUTTON_SEND.pack()

    root.mainloop()

main()