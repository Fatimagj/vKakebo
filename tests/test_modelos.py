from datetime import date
from kakebo.modelos import Ingreso, CategoriaGastos, Gasto
import pytest

def test_instanciar_ingreso():
    movimiento = Ingreso("Loteria del niño, premio", date(2024, 1, 5), 1000)
    
    assert movimiento.concepto == "Loteria del niño, premio"
    assert movimiento.fecha == date(2024, 1, 5)
    assert movimiento.cantidad == 1000

def test_ingreso_concepto_debe_ser_string():
    with pytest.raises(TypeError):
        movimiento = Ingreso(19, date(2024, 1, 5), 1000) 

def test_ingreso_fecha_typeError():
    with pytest.raises(TypeError):
        movimiento = Ingreso("Loteria del niño, premio", "1 de enero del 2024", 1000) 

def test_ingreso_cantidad_typeError():
    with pytest.raises(TypeError):
        movimiento = Ingreso("Loteria del niño, premio", date(2024, 1, 5), "0") 
    movimiento = Ingreso("Loteria del niño, premio", date(2024, 1, 5), 1000) 
    movimiento = Ingreso("Loteria del niño, premio", date(2024, 1, 5), 1000.1) 

def test_cantidad_no_0():
    with pytest.raises(ValueError):
        movimiento = Ingreso("Loteria del niño, premio", date(2024, 1, 5), 0)

def test_longitud_5caracteres():
    with pytest.raises(ValueError):
        movimiento = Ingreso("Lote", date(2024, 1, 5), 1000 )
    
def test_fecha_posterior():
    with pytest.raises(ValueError):
        movimiento = Ingreso("Lotería del niño, premio", date(2225, 5, 2), 1000)

def test_crear_gasto():
    movimiento = Gasto("Factura del agua", date(2024, 5, 1), 70, CategoriaGastos.NECESIDAD)
    assert movimiento.concepto == "Factura del agua"
    assert movimiento.fecha == date(2024, 5, 1)
    assert movimiento.cantidad == 70
    assert movimiento.categoria == CategoriaGastos.NECESIDAD

def test_gasto_categoria_tipo_correcto():
    with pytest.raises(TypeError):
        movimiento = Gasto("Factura del agua", date(2024, 5, 1), 70, "Necesidad")