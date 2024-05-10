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
from kakebo.modelos import Dao, Ingreso, Gasto, CategoriaGastos
from datetime import date
import os

def borrar_fichero(path):
    if os.path.exists(path):
        os.remove(path)

def test_crear_dao():
    ruta = "datos/test_movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao(ruta)
    assert dao.ruta == ruta
    
    with open(ruta, "r") as f: #con essto nos aseguramos qeu se cierre sin poner f.close
        cabecera = f.readline()
        assert cabecera == "concepto,fecha,cantidad,categoria\n"
        registro = f.readline()
        assert registro == ""

def test_guardar_ingreso_y_gasto():
    ruta = "datos/test_movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao(ruta)
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

def test_leer_ingreso_y_gasto():
    ruta = "datos/test_movimientos.csv"

    with open(ruta,"w", newline="") as f:
        f.write("concepto,fecha,cantidad,categoria\n")
        f.write("Ingreso,1999-12-31,12.34,\n")
        f.write("Gastos,1999-01-01,55.0,4\n")

    dao = Dao(ruta)
    
    movimiento1 = dao.leer()
    assert movimiento1 == Ingreso("Ingreso", date(1999, 12, 31), 12.34)
    
    movimiento2 = dao.leer()
    assert movimiento2 == Gasto("Gastos", date(1999, 1, 1), 55, CategoriaGastos.EXTRAS)
    
    movimiento3 = dao.leer()
    assert movimiento3 is None