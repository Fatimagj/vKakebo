import tkinter as tk

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

        lbl = tk.Label(self, text=text, width=10, anchor=tk.W)
        lbl.pack(side=tk.LEFT)

        self.dayVar = tk.IntVar()
        dayEntry = tk.Entry(self, textvariable=self.dayVar, width=2)
        dayEntry.pack(side=tk.LEFT)

        lbl = tk.Label(self, text="/", width=3)
        lbl.pack(side=tk.LEFT)

        self.monthVar = tk.IntVar()
        monthEntry = tk.Entry(self, textvariable=self.monthVar, width=2)
        monthEntry.pack(side=tk.LEFT)

        lbl = tk.Label(self, text="/", width=3)
        lbl.pack(side=tk.LEFT)

        self.yearVar = tk.IntVar()
        yearEntry = tk.Entry(self, textvariable=self.yearVar,width=4)
        yearEntry.pack(side=tk.LEFT)

#informar y mostrar en los entry la fecha de hoy
