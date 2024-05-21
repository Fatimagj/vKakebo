import tkinter as tk
from datetime import date

class Input(tk.Frame):
    def __init__(self, parent, labelText, W, H):
        super().__init__(parent, width=W, height=H)#ESENCIALaqui estamos creando al super
        self.pack_propagate(False)
        lblFecha = tk.Label(self, text=labelText, anchor=tk.NW)
        lblFecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.varFecha = tk.StringVar()
        inpFecha = tk.Entry(self, textvariable=self.varFecha)
        inpFecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btnAction = tk.Button(self,text="Clic", command=self.el_comando, width=12 )
        btnAction.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def el_comando(self):
        print(self.varFecha.get())
        self.varFecha.set("Lolailo")


class DateInput(tk.Frame):
    def __init__(self, parent, W, H, text="Fecha:"):
        super().__init__(parent, width=W, height=H)
        self.pack_propagate(False)

        self.fecha = date.today()

        lbl = tk.Label(self, text=text, width=10, anchor=tk.W)
        lbl.pack(side=tk.LEFT)

        validate_day = self.register(self.__validate_day) #registramos la función de abajo.
        self.dayEntry = tk.Entry(self, width=2, 
                                 validate="key", 
                                 validatecommand= (validate_day, "%P"))
        self.dayEntry.pack(side=tk.LEFT)
        #self.dayEntry.insert(0, f"{self.fecha.day:02d}")

        lbl = tk.Label(self, text="/", width=3)
        lbl.pack(side=tk.LEFT)

        validate_month = self.register(self.__validate_month)
        self.monthEntry = tk.Entry(self, width=2, state=tk.DISABLED, 
                                   validate="key", 
                                   validatecommand=(validate_month, "%P"))
        self.monthEntry.pack(side=tk.LEFT)
        #monthEntry.insert(0, f"{self.fecha.month:02d}")

        lbl = tk.Label(self, text="/", width=3)
        lbl.pack(side=tk.LEFT)

        validate_year = self.register(self.__validate_year)
        self.yearEntry = tk.Entry(self, width=4, state=tk.DISABLED, 
                                  validate="key",
                                  validatecommand=(validate_year, "%P"))
        self.yearEntry.pack(side=tk.LEFT)
        #yearEntry.insert(0, self.fecha.year)

    def __validate_day(self, candidato): #para que no se pueda usar fuera
        """
        0. Siempre la fecha en blanco.
        1. Comprobar que candidato es un entero, si no lo es devolver false
        2. Obligamos a rellenar de forma secuencial.
        3. Aceptamos valores entre 1 y 31
            3.1 debemos habilitar el mes
        4. Si el campo esta vacio debemos deshabilitar mes y año

        """
        print("por aqui pasa", (candidato))
        if not candidato.isdigit() and candidato !="":
            return False
        
        if candidato == "":
            #disable mes
            self.monthEntry.config(state=tk.DISABLED)
            return True
        
        if int(candidato) > 0 and int(candidato) < 32:
            #enable mes, habilitar
            self.monthEntry.config(state=tk.NORMAL)
            return True
        else:
            return False

    def __validate_month(self, candidato):   
        """
        0. El mes empieza en blanco
        1. Comprobar que es un mes entero, si no lo es dedvolver false.
        2. El mes tiene que ser compatible con el dia introducido o devolver false y, logicamente entre 1 y 12.
        3. Habilitamos año si el campo no esta vacio
        """
        if not candidato.isdigit() and candidato !="":
            return False
        
        if candidato == "":
            self.yearEntry.config(state=tk.DISABLED)
            return True
        
        try:
            date(2000, int(candidato), int(self.dayEntry.get()))
            self.yearEntry.config(state=tk.NORMAL)
            return True
        except ValueError:
            return False

    def __validate_year(self, candidato):
        """
        0. El año empieza en blanco.
        1. Comprobar que es un mes entero, si no lo es dedvolver false.
        2. Comprobar el año con el mes y el día introducido solo si el año tiene longitud 4.
        """
        if not candidato.isdigit() and candidato !="":
            return False
        if len(candidato) < 4:
            return True
        
        try:
            date(int(candidato), int(self.monthEntry.get()), int(self.dayEntry.get()))
            return True
        except ValueError:
            return False
        


