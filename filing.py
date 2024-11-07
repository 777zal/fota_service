import os

class Filing:
    path = ''

    def __init__(self):
        print("Has Set")

    def _get_bin_file_size(self, path:str):
        try:
            file_size = 0
            file_size = os.path.getsize(path)
            return file_size
        except Exception as e:
            return 0

    def set_file_path(self, file_path:str):
        if file_path:
            if os.path.exists(file_path):
                self.file = file_path
                print("Selected .bin file :"+ file_path)
                size = self._get_bin_file_size(self.file)
                print(size)
            else:
                print("File not found")


