from typing import List
import os
import pydicom
from PyQt5.QtGui import QTextDocument

class LoginModel:
    def __init__(self):
        self.valid_user = "medicoAnalitico"
        self.valid_password = "bio12345"

    def validate_login(self, user, password):
        return user == self.valid_user and password == self.valid_password

class CargaImagenesModel:
    def __init__(self):
        self.folder_path = None
        self.image_files = []

    def load_image_files(self):
        if self.folder_path:
            self.image_files = [os.path.join(self.folder_path, file) for file in os.listdir(self.folder_path) if file.endswith(".dcm")]

    def get_image_path(self, index):
        if 0 <= index < len(self.image_files):
            return self.image_files[index]
        return None