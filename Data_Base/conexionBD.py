import pymysql
class ConexionBD():
    def crearConexion(self, servidor, port,  user, password, database):
        connection=pymysql.connect(host=servidor, port=port, user=user, password=password, db=database)
        return connection
    def closeBD(self, connection):
        try:
            connection.close()
            print('Conexion Cerrada')
        except pymysql.ProgrammingError as e:
            print(e)

if __name__=="__main__":
    prueba = ConexionBD()
    con = prueba.crearConexion('localhost',3306,'root','','vitales')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM pacientes")
    row = cursor.fetchone()
    print("identificacion={}, edad={}, nombre={}, apellido1={}, apellido2={}, correo={}, telefono={}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))