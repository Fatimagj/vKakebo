"""
1. Crear un dao y comprobar que:
    - tiene una ruta de fichero fijada a un fichero csv
    - el fichero csv tiene que ser vacio pero tener una fila de cabecera

2. guardar un ingreso y un gasto
    - que el fichero contiene las ffilas adecuadas, 1 de cabecera y 1 de ingreso y otra de gasto

3. leer datos del fichero con un dao
    - preparar un fichero con datos
    - leer esos datos con el dao
    - comprobar que nos ha creado tantos movimientos (ingresos o gastos) como hay en el fichero y que lo haga bien.


"""
from kakebo.modelos import Dao_CSV, Ingreso, Gasto, CategoriaGastos, DaoSqlite
from datetime import date
import os
import sqlite3

RUTA_SQLITE =     ruta = "datos/movimientos_test.db"
def borrar_fichero(path):
    if os.path.exists(path):
        os.remove(path)

def borrar_movimientos_sqlite():
     #preparar la tabla movimiento como toca, borrar e insetar un ingreso y un gasto
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()

    query = "DELETE FROM movimientos;"
    cur.execute(query)
    con.commit()
    con.close()

def test_crear_dao_csv():
    ruta = "datos/test_movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao_CSV(ruta)
    assert dao.ruta == ruta
    
    with open(ruta, "r") as f: #con essto nos aseguramos qeu se cierre sin poner f.close
        cabecera = f.readline()
        assert cabecera == "concepto,fecha,cantidad,categoria\n"
        registro = f.readline()
        assert registro == ""

def test_guardar_ingreso_y_gasto_csv():
    ruta = "datos/test_movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao_CSV(ruta)
    ing = Ingreso("Un concepto", date(1999, 12, 12), 12.34)
    dao.grabar(ing)
    gasto = Gasto("Un gasto", date(1999, 1, 1), 23.45, CategoriaGastos.EXTRAS)
    dao.grabar(gasto)
    
    with open(ruta, "r") as f:
        f.readline()
        registro = f.readline()
        assert registro == "Un concepto,1999-12-12,12.34,\n"
        registro = f.readline()
        assert registro == "Un gasto,1999-01-01,23.45,4\n"
        registro = f.readline()
        assert registro == ""

def test_leer_ingreso_y_gasto_csv():
    ruta = "datos/test_movimientos.csv"

    with open(ruta,"w", newline="") as f:
        f.write("concepto,fecha,cantidad,categoria\n")
        f.write("Ingreso,1999-12-31,12.34,\n")
        f.write("Gastos,1999-01-01,55.0,4\n")

    dao = Dao_CSV(ruta)
    
    movimiento1 = dao.leer()
    assert movimiento1 == Ingreso("Ingreso", date(1999, 12, 31), 12.34)
    
    movimiento2 = dao.leer()
    assert movimiento2 == Gasto("Gastos", date(1999, 1, 1), 55, CategoriaGastos.EXTRAS)
    
    movimiento3 = dao.leer()
    assert movimiento3 is None

def test_crear_dao_sqlite():
    ruta = RUTA_SQLITE
    dao = DaoSqlite(ruta)

    assert dao.ruta == ruta

def test_leer_dao_sqlite():
    borrar_movimientos_sqlite()
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()

    query = "INSERT INTO movimientos (id, tipo_movimiento, concepto, fecha, cantidad, categoria) VALUES (?, ?, ?, ?, ?, ?)"
    
    cur.executemany(query, ((1, "I", "Un ingreso cualquiera", date(2024, 5, 14), 100, None), 
                            (2, "G", "Un gasto cualquiera", date(2024, 5, 1), 123, 3)))
    
    con.commit()
    con.close()

    dao = DaoSqlite(RUTA_SQLITE)
    movimiento = dao.leer(1)
    assert movimiento == Ingreso("Un ingreso cualquiera", date(2024, 5, 14), 100)

    movimiento = dao.leer(2)
    assert movimiento == Gasto("Un gasto cualquiera", date(2024, 5, 1), 123, CategoriaGastos.OCIO_VICIO)

def test_grabar_sqlite():
    #preparar el test
    borrar_movimientos_sqlite()
    
    ing = Ingreso("Un concepto cualquiera", date(1990,1,1), 123)
    dao = DaoSqlite(RUTA_SQLITE)
    dao.grabar(ing)

    #comprobar el test, aqui comprobamos una tupla
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()

    query = "SELECT id, tipo_movimiento, concepto, fecha, cantidad, categoria FROM movimientos order by id desc LIMIT 1"
    res = cur.execute(query)
    fila = res.fetchone()
    con.close()

    assert fila[1] == "I"
    assert fila[2] == "Un concepto cualquiera"
    assert fila[3] == "1990-01-01"
    assert fila[4] == 123.0
    assert fila [5] is None

def test_update_sqlite():
    borrar_movimientos_sqlite() #borramos
    
    con = sqlite3.connect(RUTA_SQLITE) #conectamos
    cur = con.cursor() #cursor

    query = "INSERT INTO movimientos (id, tipo_movimiento, concepto, fecha, cantidad) VALUES (1, 'I', 'concepto original', '0001-01-01', 0.1)"

    cur.execute(query)
    con.commit()
    con.close()

    dao = DaoSqlite(RUTA_SQLITE)

    movimiento = dao.leer(1) #id
    movimiento.concepto = "Concepto cambiado"
    movimiento.fecha = "2024-01-04"
    movimiento.cantidad = 32

    dao.grabar(movimiento)

    #commprobar la modificación

    modificado = dao.leer(1)
    assert isinstance(modificado, Ingreso)
    assert modificado.concepto == "Concepto cambiado"
    assert modificado.fecha == date(2024, 1, 4)
    assert modificado.cantidad == 32

def test_delete_squlite():
    borrar_movimientos_sqlite()

    con = sqlite3.connect(RUTA_SQLITE)
    cur =con.cursor()

    query = "INSERT INTO movimientos (id, tipo_movimiento, concepto, fecha, cantidad) VALUES (1, 'I', 'Concepto original', '0001-01-01', 0.1)"
    cur.execute(query)
    con.commit()
    con.close()
    

def test_leerTodo_dao_sqlite():
    borrar_movimientos_sqlite()
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()

    query = "INSERT INTO movimientos (id, tipo_movimiento, concepto, fecha, cantidad, categoria) VALUES (?, ?, ?, ?, ?, ?)"
    
    cur.executemany(query, [(1, "I", "Un ingreso cualquiera", date(2024, 5, 14), 100, None), 
                            (2, "G", "Un gasto cualquiera", date(2024, 5, 1), 123, 3), 
                            (6, "I", "nomina", date(2024, 5, 1), 1500, None), 
                            (4, "G", "comida familiar", date(2024, 4, 6), 35, 3), 
                            (8, "G", "zapatillas", date(2024, 5, 6), 57.5, 1), 
                            (9, "G", "comida familiar", date(2024, 4, 16), 90, 3)])
    
    con.commit()
    con.close()

    dao = DaoSqlite(RUTA_SQLITE)
    movimiento = dao.leerTodo()
   
    movimiento1 = dao.leerTodo()
    assert Ingreso("Un ingreso cualquiera", date(2024, 5, 14), 100) ==  movimiento[0]

    movimiento2 = dao.leerTodo()
    assert Gasto("Un gasto cualquiera", date(2024, 5, 1), 123, CategoriaGastos.OCIO_VICIO) == movimiento[1]

    movimiento3 = dao.leerTodo()
    assert Ingreso("nomina", date(2024, 5, 1), 1500) == movimiento[3]

    movimiento4 = dao.leerTodo()
    assert Gasto("comida familiar", date(2024, 4, 6), 35, CategoriaGastos.OCIO_VICIO) == movimiento[2]

    movimiento5 = dao.leerTodo()
    assert Gasto("zapatillas", date(2024, 5, 6), 57.5, CategoriaGastos.NECESIDAD) == movimiento[4]

    movimiento6 = dao.leerTodo()
    assert Gasto("comida familiar", date(2024, 4, 16), 90, CategoriaGastos.OCIO_VICIO) == movimiento[5]