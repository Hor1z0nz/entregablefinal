from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from cargaimagenes import Ui_Dialog 
from PyQt5.QtGui import QTextDocument
from PyQt5.QtCore import pyqtSignal
from modelo import CargaImagenesModel

class LoginWindow(QMainWindow):
    # Agregar una señal para indicar que el inicio de sesión fue exitoso
    login_successful = pyqtSignal()

class LoginWindow(QMainWindow):
    login_successful = pyqtSignal()

    def __init__(self, login_model):
        super(LoginWindow, self).__init__()
        self.login_model = login_model
        self.setup_ui()

    def setup_ui(self):
        loadUi('window2.ui', self)
        self.pushButton.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        user = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if len(user) == 0 or len(password) == 0:
            self.label_4.setText("Ingrese todos los datos")
        else:
            if self.login_model.validate_login(user, password):
                self.label_4.setText("Login exitoso")
                self.login_successful.emit()  # Emitir la señal de éxito
                self.close()  # Cerrar la ventana con éxito
            else:
                self.label_4.setText("Nombre o Contraseña incorrecto!")


class CargaImagenesDialog(QDialog):
    def __init__(self):
        super(CargaImagenesDialog, self).__init__()
        loadUi('cargaimagenes.ui', self)
        self.model = CargaImagenesModel()  # Crea una instancia del modelo al inicializar la ventana

    def setup_ui(self):
        self.pushButton_3.clicked.connect(self.seleccionar_carpeta)
        self.pushButton_2.clicked.connect(self.salir)

    def seleccionar_carpeta(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Seleccionar Carpeta", "", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder_path:
            self.label_2.setText(QTextDocument(folder_path).toPlainText())
            self.model.folder_path = folder_path
            self.model.load_image_files()