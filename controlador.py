from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog, QFileDialog, QMainWindow
from PyQt5.QtGui import QTextDocument
import sys
from vista import LoginWindow, CargaImagenesDialog
from modelo import LoginModel
import pydicom
from modelo import CargaImagenesModel
from PyQt5.uic import loadUi
from PyQt5.QtGui import QTextDocument
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from typing import List
import os
import pydicom
from PyQt5.QtGui import QTextDocument
import numpy as np
import matplotlib.pyplot as plt

class LoginModel:
    def __init__(self):
        self.valid_user = "medicoAnalitico"
        self.valid_password = "bio12345"

    def validate_login(self, user, password):
        return user == self.valid_user and password == self.valid_password

class LoginController(QObject):  
    login_successful = pyqtSignal()

    def __init__(self, view, model, carga_imagenes_dialog):
        super().__init__() 
        self.view = view
        self.model = model
        self.carga_imagenes_dialog = carga_imagenes_dialog
        self.view.setup_ui()
        self.view.pushButton.clicked.connect(self.login_clicked)

    def login_clicked(self):
        user = self.view.lineEdit.text()
        password = self.view.lineEdit_2.text()
        if len(user) == 0 or len(password) == 0:
            self.view.label_4.setText("Ingrese todos los datos")
        else:
            if self.model.validate_login(user, password):
                self.view.label_4.setText("Login exitoso")
                self.login_successful.emit()  # Emitir la señal de éxito
            else:
                self.view.label_4.setText("Nombre o Contraseña incorrecto!")
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


class CargaImagenesController(QObject):
    back_to_login = pyqtSignal()
    def __init__(self, ui, carga_imagenes_dialog, slider_controller):
        super(CargaImagenesController, self).__init__()
        self.ui = carga_imagenes_dialog
        self.carga_imagenes_dialog = carga_imagenes_dialog
        self.slider_controller = slider_controller  # Agrega el controlador del slider
        self.carga_imagenes_dialog.pushButton.clicked.connect(self.cargar_imagenes)
        self.ui.pushButton_3.clicked.connect(self.seleccionar_carpeta)
        self.ui.pushButton_2.clicked.connect(self.salir)
    def cargar_imagenes(self):
        self.carga_imagenes_dialog.close()
        self.slider_controller.view.show()

    def seleccionar_carpeta(self):
        folder_path = QFileDialog.getExistingDirectory(
            self.carga_imagenes_dialog, "Seleccionar Carpeta", "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder_path:
            self.ui.label_2.setText(QTextDocument(folder_path).toPlainText())
            self.carga_imagenes_dialog.model.folder_path = folder_path
            self.carga_imagenes_dialog.model.load_image_files()
            self.slider_controller.model.folder_path = folder_path
            self.slider_controller.model.load_image_files()
            self.slider_controller.view.horizontalSlider.setMaximum(len(self.slider_controller.model.image_files))
            self.slider_controller.view.horizontalSlider.setValue(0)

    def salir(self):
        self.ui.close()
        self.back_to_login.emit()
        

from PyQt5.QtWidgets import QWidget

class SliderController(QObject):
    back_to_login = pyqtSignal()
    close_slider = pyqtSignal()
    def __init__(self, model, view, carga_imagenes_controller,):
        super(SliderController, self).__init__()
        self.model = model
        self.view = view
        self.carga_imagenes_controller = carga_imagenes_controller  
        self.view.horizontalSlider.valueChanged.connect(self.slider_value_changed)
        self.view.pushButton_2.clicked.connect(self.volver_cargar_imagenes)
        self.view.pushButton.clicked.connect(self.volver_cargar_imagenes)

    def slider_value_changed(self):
        slider_value = self.view.horizontalSlider.value()
        image_path = self.model.get_image_path(slider_value)
        if image_path:
            dicom_data = pydicom.dcmread(image_path)

            self.view.label_2.setText(str(dicom_data.get("PatientName", "N/A")))
            self.view.label_3.setText(str(dicom_data.get("PatientAge", "N/A")))
            self.view.label_4.setText(str(dicom_data.get("PatientSex", "N/A")))
            self.view.label_5.setText(str(dicom_data.get("BodyPartExamined", "N/A")))
            self.view.label_6.setText(str(dicom_data.get("SliceThickness", "N/A")))
            self.read_and_show_dicom_image(image_path)

    def volver_cargar_imagenes(self):
        self.view.close()
        self.carga_imagenes_controller.ui.show()
        self.close_slider.emit()
    

    def read_and_show_dicom_image(self, file_path):
        dicom_data = pydicom.dcmread(file_path)
        pixel_data = dicom_data.pixel_array

        # Normalizar los datos si es necesario
        normalized_data = ((pixel_data - np.min(pixel_data)) / (np.max(pixel_data) - np.min(pixel_data)) * 255).astype(np.uint8)

        # Crear una QImage desde los datos normalizados
        q_image = QImage(normalized_data.data, normalized_data.shape[1], normalized_data.shape[0], normalized_data.strides[0], QImage.Format_Grayscale8)

        # Convertir QImage a QPixmap y mostrarlo en el QLabel
        pixmap = QPixmap.fromImage(q_image)
        self.view.label.setPixmap(pixmap)
    
    


def run_application():
    app = QApplication([])

    model = LoginModel()
    login_window = LoginWindow(model)
    cargaimagenes_dialog = CargaImagenesDialog()

    carga_imagenes_model = CargaImagenesModel()
    slider_model = CargaImagenesModel()

    slider_controller = SliderController(slider_model, loadUi('slider.ui'), None)
    carga_imagenes_controller = CargaImagenesController(cargaimagenes_dialog, slider_controller)

    slider_controller.carga_imagenes_controller = carga_imagenes_controller

    # Conectar la señal login_successful del controlador de inicio de sesión
    login_controller = LoginController(login_window, model, cargaimagenes_dialog)
    login_controller.login_successful.connect(cargaimagenes_dialog.show)

    # Conectar la señal accepted de la ventana de carga de imágenes para mostrar la ventana slider
    carga_imagenes_controller.ui.accepted.connect(slider_controller.view.show)

    # Conectar la señal para regresar a la ventana de inicio de sesión
    carga_imagenes_controller.back_to_login.connect(login_window.show)

    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_application()
