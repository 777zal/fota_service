import os

class Filing:
    path = ''

    def __init__(self):
        print("Has Set")

    def set_file_path(self, file_path:str):
        if file_path:
            if os.path.exists(file_path):
                self.file = file_path
                print("Selected .bin file : {file_path}")
            else:
                print("File not found")
