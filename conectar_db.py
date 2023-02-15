import sqlite3 

def crear_db():
    conexion = sqlite3.connect("Data/db/db_malwate.db")
    return conexion

def crear_tables(conexion):
    cursor = conexion.cursor()
    bandera = 0
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS tipos_malware(
            id integer primary key autoincrement, 
            caracteristicas text,
            nivel_peligro text,
            clasificacion text
        )""")
        print("Se creó la tabla tipos_malware correctamente")
        bandera = 1
    except sqlite3.OperationalError:
        print("Error al crear una tabla")
    return bandera


def insertar_tipos_malware():
    conexion = sqlite3.connect("Data/db/db_malwate.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO tipos_malware(caracteristicas, nivel_peligro, clasificacion) values (?,?,?)", ('Troyano', 'Alto', 'Malicioso'))
        cursor.execute("INSERT INTO tipos_malware(caracteristicas, nivel_peligro, clasificacion) values (?,?,?)", ('Troyano', 'Medio', 'Malicioso'))
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Registros insertados")
    except sqlite3.OperationalError:
        print("Error al insertar registros")

if __name__ == '__main__':
    crear_tables(crear_db())
    insertar_tipos_malware()