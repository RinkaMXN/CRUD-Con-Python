from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Data_Base.conexionBD import ConexionBD
from PyQt5 import QtWidgets
from PyQt5 import uic
import pymysql
import sys
import re



enfermeras = uic.loadUiType("Interfaceenfermeras.ui")[0]




class Enfermera(QMainWindow, enfermeras):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('MENU')

        #CREAMOS CONEXION A BASE DE DATOS
        try:
            self.c = ConexionBD()
            self.conn = self.c.crearConexion('localhost', 3306, 'root', '', 'vitales')
            self.cursor = self.conn.cursor()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        #CONECTAMOS LOS BOTONES PARA QUE HAGAN ENL CRUD
        self.BT_Registra.clicked.connect(self.InsertarEnfermeras)
        self.BT_Buscar_Eliminar.clicked.connect(self.buscaEliminaEnfermera)
        self.BT_Eliminar_Enfermera.clicked.connect(self.eliminaEnfermeras)
        self.BT_ACT_Buscar_Enfermera.clicked.connect(self.BuscaActualizaEnfermeras)
        self.BT_ACT_Enfermera.clicked.connect(self.actualizaEnfermera)
        self.BT_Refrescar.clicked.connect(self.mostrar_enfermeras)



        #ASIGNAMOS LAS MULTIPAGINAS DE DE CRUD
        self.BT_Insertar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.W_Insertar))
        self.BT_Eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.W_Eliminar))
        self.BT_Actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.W_Actualizar))
        self.BT_Mostrar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.W_Mostrar))

    #========Metodos de Clientes================
    def InsertarEnfermeras(self):
        #SE OBTIENE DATOS DE LA INTERFAZ
        identificacionE=int(self.IN_ID.text())
        nombre=self.IN_Nom.text()
        apellido1=self.IN_ApellidoM.text()
        apellido2=self.IN_ApellidoP.text()
        edad=self.IN_Edad.currentText()
        cedula=self.IN_Cedula.text()
        tel=self.IN_Tel.text()

        # VALIDACIÓN DEL NOMBRE
        patron_nombre = r'^[A-ZÑ][a-záéíóúüñ]+$'
        patron_numeros = r'^\d{6}$'

        if re.match(patron_nombre, nombre):
            if re.match(patron_nombre, apellido1):
                if re.match(patron_nombre, apellido2):
                    if re.match(patron_numeros, cedula):
                        if re.match(patron_numeros, tel):
                            # SE INSERTAN EN LA BASE DE DATOS
                            try:
                                insertar_registro = '''INSERT INTO enfermeras(identificacionE, nombre, apellido1, apellido2, edad, cedula, telefono) 
                                                                                VALUES(%s,%s,%s,%s,%s,%s,%s)'''
                                datos = (identificacionE, nombre, apellido1, apellido2, edad, cedula, tel)
                                self.cursor.execute(insertar_registro, datos)
                                self.conn.commit()
                            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                                print("Ocurrió un error al conectar: ", e)

                            # SE COLOCA UN ANUNCIO Y SE LIMPIAN LOS APARTADOS DE LA INTERFAZ
                            mensaje = "Enfermera registrada."
                            QMessageBox.warning(self, "Advertencia", mensaje)
                            self.IN_ID.clear()
                            self.IN_Nom.clear()
                            self.IN_ApellidoM.clear()
                            self.IN_ApellidoP.clear()
                            self.IN_Cedula.clear()
                            self.IN_Tel.clear()

                        else:
                            mensaje = "El telefono no cumple con el formato requerido."
                            QMessageBox.warning(self, "Advertencia", mensaje)
                            self.IN_Tel.clear()

                    else:
                        mensaje = "La Cedula no cumple con el formato requerido."
                        QMessageBox.warning(self, "Advertencia", mensaje)
                        self.IN_Cedula.clear()

                else:
                    mensaje = "El apellido paterno no cumple con el formato requerido."
                    QMessageBox.warning(self, "Advertencia", mensaje)
                    self.IN_ApellidoP.clear()

            else:
                mensaje = "El apellido materno no cumple con el formato requerido."
                QMessageBox.warning(self, "Advertencia", mensaje)
                self.IN_ApellidoM.clear()

        else:
            mensaje = "El nombre no cumple con el formato requerido."
            QMessageBox.warning(self, "Advertencia", mensaje)
            self.IN_Nom.clear()









    def buscaEliminaEnfermera(self):

        id = self.IN_Buscar_ID_Enfermera.text()
        try:
            consulta = "SELECT * FROM enfermeras WHERE identificacionE = %s;"
            self.cursor.execute(consulta, id)
            nom = self.cursor.fetchall()
            self.conn.commit()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

        self.TB_Eliminar_Enfermera.setRowCount(len(nom))
        if len(nom) == 0:
            mensaje = "La Enfermera no existe."
            QMessageBox.warning(self, "Advertencia", mensaje)
            self.IN_Buscar_ID_Enfermera.clear()
        tabla=0
        for j in nom:
            self.TB_Eliminar_Enfermera.setItem(tabla,0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.TB_Eliminar_Enfermera.setItem(tabla,1, QtWidgets.QTableWidgetItem(str(j[1])))
            self.TB_Eliminar_Enfermera.setItem(tabla,2, QtWidgets.QTableWidgetItem(str(j[2])))
            self.TB_Eliminar_Enfermera.setItem(tabla,3, QtWidgets.QTableWidgetItem(str(j[3])))
            self.TB_Eliminar_Enfermera.setItem(tabla,4, QtWidgets.QTableWidgetItem(str(j[4])))
            self.TB_Eliminar_Enfermera.setItem(tabla,5, QtWidgets.QTableWidgetItem(str(j[5])))
            self.TB_Eliminar_Enfermera.setItem(tabla,6, QtWidgets.QTableWidgetItem(str(j[6])))
            #pacientes.TablaEliminacliente.setItem(tabla,7, QtWidgets.QTableWidgetItem(j[7]))
            tabla += 1

    def eliminaEnfermeras(self):
        self.TB_Eliminar_Enfermera.currentRow()
        id = self.IN_Buscar_ID_Enfermera.text()
        self.TB_Eliminar_Enfermera.removeRow(0)

        try:
            consulta = "DELETE FROM enfermeras WHERE identificacionE = %s;"
            self.cursor.execute(consulta, (id))
            self.conn.commit()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

        self.IN_Buscar_ID_Enfermera.clear()
        mensaje = "La Enfermera ha sido eliminada."
        QMessageBox.warning(self, "Advertencia", mensaje)

    def BuscaActualizaEnfermeras(self):
        id=self.ACT_ID.text()
        try:
            consulta = "SELECT * FROM enfermeras WHERE identificacionE = %s;"
            self.cursor.execute(consulta, id)
            busca = self.cursor.fetchall()
            self.conn.commit()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

        if len(busca)!= 0:
            self.ACT_Nom.setText(str(busca[0][1]))
            self.ACT_Apellido.setText(str(busca[0][2]))
            self.ACT_ApellidoP.setText(str(busca[0][3]))
            self.ACT_Edad.setText(str(busca[0][4]))
            self.ACT_Cedula.setText(str(busca[0][5]))
            self.ACT_TEL.setText(str(busca[0][6]))


            #pacientes.observaedita.setPlainText(busca[0][7])
        else:
            mensaje = "No se encontró la enfermera."
            QMessageBox.warning(self, "Advertencia", mensaje)
            self.ACT_ID.clear()
            self.ACT_Nom.clear()
            self.ACT_Apellido.clear()
            self.ACT_ApellidoP.clear()
            self.ACT_Cedula.clear()
            self.ACT_TEL.clear()
            self.ACT_Edad.clear()



    def actualizaEnfermera(self):
        id = self.ACT_ID.text()
        try:
            consulta = "SELECT * FROM enfermeras WHERE identificacionE = %s;"
            self.cursor.execute(consulta, id)
            buscanom = self.cursor.fetchall()
            self.conn.commit()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)


        nom=self.ACT_Nom.text()
        ap1=self.ACT_Apellido.text()
        ap2=self.ACT_ApellidoP.text()
        cedula=self.ACT_Cedula.text()
        tel=self.ACT_TEL.text()
        edad=self.ACT_Edad.text()

        # VALIDACIÓN DEL NOMBRE
        patron_nombre = r'^[A-ZÑ][a-záéíóúüñ]+$'
        patron_numeros = r'^\d{6}$'

        if re.match(patron_nombre, nom):
            if re.match(patron_nombre, ap1):
                if re.match(patron_nombre, ap2):
                    if re.match(patron_numeros, cedula):
                        if re.match(patron_numeros, tel):
                            # observa=pacientes.observaedita.toPlainText()
                            if nom != "" and ap1 != "" and ap2 != "" and cedula != "" and tel != "" and edad != "":
                                consulta1 = "UPDATE enfermeras SET edad = %s WHERE identificacionE = %s;"
                                consulta2 = "UPDATE enfermeras SET apellido1 = %s WHERE identificacionE = %s;"
                                consulta3 = "UPDATE enfermeras SET apellido2 = %s WHERE identificacionE = %s;"
                                consulta4 = "UPDATE enfermeras SET nombre = %s WHERE identificacionE = %s;"
                                consulta5 = "UPDATE enfermeras SET cedula = %s WHERE identificacionE = %s;"
                                consulta6 = "UPDATE enfermeras SET telefono = %s WHERE identificacionE = %s;"
                                self.cursor.execute(consulta1, (edad, id))
                                self.cursor.execute(consulta2, (ap1, id))
                                self.cursor.execute(consulta3, (ap2, id))
                                self.cursor.execute(consulta4, (nom, id))
                                self.cursor.execute(consulta5, (cedula, id))
                                self.cursor.execute(consulta6, (tel, id))
                                self.conn.commit()

                                mensaje = "Los datos de la enfermera han sido actualizados."
                                QMessageBox.warning(self, "Advertencia", mensaje)
                                self.ACT_ID.clear()
                                self.ACT_Nom.clear()
                                self.ACT_Apellido.clear()
                                self.ACT_ApellidoP.clear()
                                self.ACT_Cedula.clear()
                                self.ACT_TEL.clear()
                                self.ACT_Edad.clear()

                            else:
                                mensaje = "Los datos de la enfermera no han sido actualizados."
                                QMessageBox.warning(self, "Advertencia", mensaje)


                        else:
                            mensaje = "El telefono no cumple con el formato requerido."
                            QMessageBox.warning(self, "Advertencia", mensaje)
                            self.ACT_TEL.clear()

                    else:
                        mensaje = "La Cedula no cumple con el formato requerido."
                        QMessageBox.warning(self, "Advertencia", mensaje)
                        self.ACT_Cedula.clear()

                else:
                    mensaje = "El apellido paterno no cumple con el formato requerido."
                    QMessageBox.warning(self, "Advertencia", mensaje)
                    self.ACT_ApellidoP.clear()

            else:
                mensaje = "El apellido materno no cumple con el formato requerido."
                QMessageBox.warning(self, "Advertencia", mensaje)
                self.ACT_apellido.clear()

        else:
            mensaje = "El nombre no cumple con el formato requerido."
            QMessageBox.warning(self, "Advertencia", mensaje)
            self.ACT_Nom.clear()







    def mostrar_enfermeras(self):
        try:
            consulta = "SELECT * FROM enfermeras;"
            self.cursor.execute(consulta)
            id = self.cursor.fetchall()
            self.conn.commit()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

        i=len(id)
        self.TB_Enfermeras.setRowCount(i)
        tabla = 0
        for j in id:
            self.TB_Enfermeras.setItem(tabla, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.TB_Enfermeras.setItem(tabla, 1, QtWidgets.QTableWidgetItem(str(j[1])))
            self.TB_Enfermeras.setItem(tabla, 2, QtWidgets.QTableWidgetItem(str(j[2])))
            self.TB_Enfermeras.setItem(tabla, 3, QtWidgets.QTableWidgetItem(str(j[3])))
            self.TB_Enfermeras.setItem(tabla, 4, QtWidgets.QTableWidgetItem(str(j[4])))
            self.TB_Enfermeras.setItem(tabla, 5, QtWidgets.QTableWidgetItem(str(j[5])))
            self.TB_Enfermeras.setItem(tabla, 6, QtWidgets.QTableWidgetItem(str(j[6])))
            #self.tablaClientes.setItem(tabla, 7, QtWidgets.QTableWidgetItem(j[7]))

            tabla += 1




if __name__ == "__main__":

    app = QApplication([])
    ventana = Enfermera()
    ventana.show()
    sys.exit(app.exec())

