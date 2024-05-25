import tkinter as tk
from tkinter import ttk
from kakebo.vistas import Input, DateInput, FormMovimiento
"""
Jerarquia de controles a crear

    + KakeboWin
        + FiltroFechas
          - InputDateFrom
          - InputDateTo
          - btnFilter
        + ListaMovimientos
        + FormMovimiento
          - InputDate
          - InputConcepto
          - InputCantidad
          - ComboCategoria
          - BtnAceptar
          - BtnCancelar
"""

## SIEMPRE USAR LA DOCUMENTACIÓN PARA SABER QUE USAR EN LAS OPCIONES
root = tk.Tk() #ventana contenedora / VENTANA PRINCIPAL
#root.pack_propagate() #aqui le estamos diciendo que se expanda por la ventana pero que no coja todo el contenido si popnemos False si no coge toda la ventana

"""marco = tk.Frame(root, width=200, height=80, background="red") #marco inicial dentro del principal, le ponemos del padre que deriva que es root(el principal) luego se ponen las opciones
marco.pack() #para que te aparecezca por ejemplo lo rojo
#arco.pack_propagate(False)
lblFecha = tk.Label(marco, text = "Fecha:", anchor=tk.NW) #aqui el padre es marco. y crea el texto Fecha
lblFecha.pack(side=tk.LEFT, fill=tk.BOTH, expand = True) #se le dan las opciones a Feecha
varFecha = tk.StringVar() #para las variables de entry
inpFecha = tk.Entry(marco, textvariable=varFecha) #para escribir dentro de la venta de fecha de arriba
inpFecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

i1 = Input(root, "Primer Input", 250, 60)
i1.pack(side=tk.TOP)

i2 = Input(root, "Segundo Input", 250, 60)
i2.pack(side=tk.TOP)

di = DateInput(root, 350, 35)
di.pack(side=tk.TOP)"""

form = FormMovimiento(root)
form.pack(side=tk.TOP)

root.mainloop() #para activar la ventana contenedora y nos salga un ventana

