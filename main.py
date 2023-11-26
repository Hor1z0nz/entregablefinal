import sys
from PyQt5.QtWidgets import QApplication
from modelo import LoginModel
from vista import LoginWindow, CargaImagenesDialog
from PyQt5.uic import loadUi
from controlador import LoginController, CargaImagenesController, SliderController
from modelo import CargaImagenesModel
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImageReader
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QFile, QTextStream

import sys
from vista import LoginWindow, CargaImagenesDialog
from modelo import LoginModel, CargaImagenesModel
import pydicom
from controlador import SliderController




def run_application():
    app = QApplication([])

    model = LoginModel()
    login_window = LoginWindow(model)
    cargaimagenes_dialog = CargaImagenesDialog()
    carga_imagenes_model = CargaImagenesModel()
    slider_model = CargaImagenesModel()
    signal_object = QObject()
    slider_controller = SliderController(slider_model, loadUi('slider.ui'), None)
    carga_imagenes_controller = CargaImagenesController(loadUi('cargaimagenes.ui'), cargaimagenes_dialog, slider_controller)
    slider_controller.back_to_login.connect(login_window.show)
    slider_controller.carga_imagenes_controller = carga_imagenes_controller
    slider_controller.close_slider.connect(slider_controller.view.close)
  
    login_controller = LoginController(login_window, model, cargaimagenes_dialog)
    login_controller.login_successful.connect(cargaimagenes_dialog.show)

    carga_imagenes_controller.ui.accepted.connect(slider_controller.view.show)

   
    carga_imagenes_controller.back_to_login.connect(login_window.show)

    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_application()