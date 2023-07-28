from PyQt5.QtWidgets import QApplication, QMainWindow
from enfermera import Enfermera
from medico import Medico
from PyQt5 import uic
import sys

#CARGA DE ARCHIVO.UI DE MENU
menu = uic.loadUiType("menuInterface.ui")[0]

#CLASE MENU
class men(QMainWindow, menu):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('MENU')

        #CREACION DE OBJETOS CRUD
        self.m = Medico()
        self.e = Enfermera()
        # BOTONES DEL MENU
        self.BotonMedicos.clicked.connect(self.MenuAmedicos)
        self.BotonEnfermeras.clicked.connect(self.MenuAEnfermeras)



    # ====Menu a pacientes===
    # ====Menu a medicos===
    def MenuAmedicos(self):
        self.m.show()

    # ====Menu a enfermeras===
    def MenuAEnfermeras(self):
        self.e.show()


if __name__ == "__main__":
    app = QApplication([])
    ventana = men()
    ventana.show()
    sys.exit(app.exec())



