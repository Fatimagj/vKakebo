from datetime import date
from enum import Enum
import csv
import os
import sqlite3

class Movimiento:
    def __init__(self, concepto, fecha, cantidad, id=None):
        self.concepto = concepto
        self.fecha = fecha
        self.cantidad = cantidad
        self.id = id
        self.validar_tipos()
        self.validar_inputs()
   
        
    def validar_tipos(self):
        if not isinstance(self.concepto, str):
            raise TypeError("Concepto debe ser cadena de texto.")

        if not isinstance(self.fecha, date):
            raise TypeError("Fecha debe ser de tipo date.")
        
        if not (isinstance(self.cantidad, float) or isinstance(self.cantidad, int)):
            raise TypeError("Cantidad debe ser numerica.")

    def validar_inputs(self):
        if self.cantidad == 0:
            raise ValueError("La cantidad no puede ser 0")
        if len(self.concepto) < 5:
            raise ValueError("El concepto no puede estar vacio, o menor de 5 caracteres")   
        if self.fecha > date.today():
            raise ValueError("La fecha no puede ser posterior al dia de hoy")      
        
    def __repr__(self):
        return f"Movimiento: {self.fecha} {self.concepto} {self.cantidad:.2f}"

class Ingreso(Movimiento):     
    def __repr__(self):
        return f"Ingreso: {self.fecha} {self.concepto} {self.cantidad:.2f}"
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.concepto == other.concepto and self.cantidad == other.cantidad and self.fecha == other.fecha
        
class Gasto(Movimiento):
    def __init__(self, concepto, fecha, cantidad, categoria, id=None):
        super().__init__(concepto, fecha, cantidad, id)

        self.categoria = categoria
        self.validar_categoria()

    def validar_categoria(self):
        if not isinstance(self.categoria, CategoriaGastos):
            raise TypeError("Categoria debe ser CategoriaGastos.")
        
    def __repr__(self):
        return f"Gasto ({self.categoria.name}): {self.fecha} {self.concepto} {self.cantidad:.2f}"
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.concepto == other.concepto and self.cantidad == other.cantidad and self.fecha == other.fecha and self.categoria == other.categoria

class CategoriaGastos(Enum):
    NECESIDAD = 1
    CULTURA = 2
    OCIO_VICIO = 3
    EXTRAS = 4

class Dao_CSV:
    def __init__(self, ruta):
        self.ruta = ruta
        if not os.path.exists(self.ruta):
            with open(self.ruta, "w", newline="") as f:
                f.write("concepto,fecha,cantidad,categoria\n")
        self.puntero_lectura = 0

    def grabar(self,movimiento):
      
        with open(self.ruta, "a", newline="") as f:
            writer = csv.writer(f, delimiter =",", quotechar = '"')
            if isinstance(movimiento, Ingreso):
                #f.write(f"{movimiento.concepto},{movimiento.fecha},{movimiento.cantidad},\n")
                writer.writerow([movimiento.concepto, movimiento.fecha, movimiento.cantidad, ""])
            elif isinstance(movimiento, Gasto):
                #f.write(f"{movimiento.concepto},{movimiento.fecha},{movimiento.cantidad},{movimiento.categoria.value}\n")
                writer.writerow([movimiento.concepto,movimiento.fecha,movimiento.cantidad,movimiento.categoria.value])
    
    def leer(self):
        with open(self.ruta, "r") as f:
            reader = csv.DictReader(f)
            contador = 0
            for registro in reader:
                if registro['categoria'] == "":
                    #instanciar ingreso con los datos de registro
                    variable = Ingreso(registro['concepto'], date.fromisoformat(registro['fecha']), float(registro['cantidad']))
                elif registro['categoria'] in  [str(cat.value) for cat in CategoriaGastos]:
                    #instanciar Gasto con los datos de registro
                    variable = Gasto(registro['concepto'], date.fromisoformat(registro['fecha']), float(registro['cantidad']), CategoriaGastos(int(registro['categoria'])))

                if contador == self.puntero_lectura:
                    self.puntero_lectura += 1
                    return variable
                contador += 1

            return None

                
class DaoSqlite:
    def __init__(self, ruta):
        self.ruta = ruta

    def leer(self, id):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()

        query = "SELECT id, tipo_movimiento, concepto, fecha, cantidad, categoria FROM movimientos WHERE id = ?"

        res = cur.execute(query, (id,))
        valores = res.fetchone() # para coger de la base de datos 
        con.close()

        if valores :
            if valores[1] == "I":
                return Ingreso(valores[2], date.fromisoformat(valores[3]), valores[4], valores[0])
                
            elif valores[1] == "G":
                return Gasto(valores[2], date.fromisoformat(valores[3]), valores[4], CategoriaGastos(valores[5]), valores[0])
                
        return None
    
    def grabar(self, movimiento):
        con =sqlite3.connect(self.ruta) #conexción y damos la ruta del fichero
        cur = con.cursor() #creamos el cursor


        if isinstance(movimiento, Ingreso):
            tipo_movimiento = "I"
            categoria = None
        elif isinstance(movimiento, Gasto):
            tipo_movimiento = "G"
            categoria = movimiento.categoria.value

        if movimiento.id is None:
            query = "INSERT INTO movimientos (tipo_movimiento, concepto, fecha, cantidad, categoria) VALUES (?, ?, ?, ?, ?)" #"INSERT INTO movimientos (tipo_movimiento, concepto, fecha, cantidad, categoria) VALUES ('G', 'comprar pienso perro', '2024-05-14', 40, 1)"#crear la consulta para luego poderla consultar. En la scomillas hablamos SQL.
            
            #cur.execute(query, ('G', 'pienso para Ron', '2024-05-14', 40, 1)) #ejecutar esto es lo que queremos hacer ahora, con los if, y luego ejecutamos abajo ya que si lo hacemos asi es una chapuza.
  
            cur.execute(query, (tipo_movimiento, movimiento.concepto, movimiento.fecha, movimiento.cantidad, categoria )) #los comunes los podemos  poner aqui, ESTO ES SOLO PARA MODIFICAR LA BASE DE DATOS, NO DEVUELVE RESULTADO


        else:
            query = "UPDATE movimientos set concepto = ?, fecha = ?, cantidad = ?, categoria = ? WHERE id = ?"

            cur.execute(query, (movimiento.concepto, movimiento.fecha, movimiento.cantidad, categoria, movimiento.id))
            
        con.commit() #confirmamos la consulta
        con.close() #cerramos la consulta si no queremos hacer nada más.
            #este metodo no devuelve nada, solo se puede quejar, ya que solo tiene que grabar

    def borrar(self, id):
        con =sqlite3.connect(self.ruta) #conexción y damos la ruta del fichero
        cur = con.cursor() #creamos el cursor

        query  = "DELETE FROM movimientos WHERE id= ?"
        cur.execute(query, (id,))
        con.commit()
        con.close()

    def leerTodo(self):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()

        query = "SELECT id, tipo_movimiento, concepto, fecha, cantidad, categoria FROM movimientos"

        res = cur.execute(query)
        valores = res.fetchall() # para coger de la base de datos 
        con.close()
        
        lista_completa= []
        for valor in valores :
            if valor[1] == "I":
                lista_completa.append(Ingreso(valor[2], date.fromisoformat(valor[3]), valor[4], valor[0]))
                
            elif valor[1] == "G":
                lista_completa.append(Gasto(valor[2], date.fromisoformat(valor[3]), valor[4], CategoriaGastos(valor[5]), valores[0]))
                
        return lista_completa

    """devuelve una lista con todos los registros de la tabla movimeinto, ordenados por id ascendente y en forma de instancia de ingreso o gasto según convenga. Cada item de la lissta deber ser una instancia de Ingreso o Gasto, no la tupla que devuelve Squlite3"""
    #hacer test y metodo que nos devuelva todos los movimientos que haya en la base de datos, que me los devuelva ordandos por id, devolver en una lista. si no hya movimientos devoler lista vacia
    
    #mirar la función leer cambiando el return por un append para meterlo en una lista, hay que modificar el WHERE y en vez de fetchone un all