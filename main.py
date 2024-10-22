import tkinter as tk
from pl.formulario_pl import crear_formulario as crear_formulario_pl
from npl.formulario_npl import crear_formulario as crear_formulario_npl

def abrir_programacion_lineal():
    root = tk.Tk()
    root.title("Programación Lineal")
    crear_formulario_pl(root)
    root.mainloop()

def abrir_programacion_no_lineal():
    root = tk.Tk()
    root.title("Programación No Lineal")
    crear_formulario_npl(root)
    root.mainloop()

def mostrar_opciones():
    def on_pl_button():
        abrir_programacion_lineal()

    def on_npl_button():
        abrir_programacion_no_lineal()

    ventana = tk.Tk()
    ventana.title("Selecciona una opción")

    btn_pl = tk.Button(ventana, text="Resolver Programación Lineal", command=on_pl_button)
    btn_pl.pack(pady=10)

    btn_npl = tk.Button(ventana, text="Resolver Programación No Lineal", command=on_npl_button)
    btn_npl.pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    mostrar_opciones()