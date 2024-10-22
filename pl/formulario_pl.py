import tkinter as tk
from tkinter import messagebox
from pl.optimizacion_pl import optimizar
from pl.graficar_pl import graficar_solucion

entries_variables = []
entries_restricciones = []
operadores_restricciones = []

def enviar_datos():
    try:
        num_variables = int(entry_num_variables.get())
        tipo_problema = variable_tipo.get()
        num_restricciones = int(entry_num_restricciones.get())

        variables = []
        for i in range(num_variables):
            variables.append(float(entries_variables[i].get()))

        restricciones = []
        for i in range(num_restricciones):
            restriccion = []
            for j in range(num_variables):
                restriccion.append(float(entries_restricciones[i][j].get()))
            operador = operadores_restricciones[i].get()
            resultado_restriccion = float(entries_restricciones[i][-1].get())
            restriccion.append(operador)
            restriccion.append(resultado_restriccion)
            restricciones.append(restriccion)

        datos_optimizacion = {
            "variables": variables,
            "tipo_problema": tipo_problema,
            "restricciones": restricciones
        }

        # Ejecutar la optimización
        solucion_optima = optimizar(datos_optimizacion)
        
        # Graficar la solución
        if solucion_optima is not None:
            A = []
            b = []
            for restriccion in restricciones:
                coeficientes = restriccion[:-2]
                operador = restriccion[-2]
                resultado_restriccion = restriccion[-1]

                if operador == "<=":
                    A.append(coeficientes)
                    b.append(resultado_restriccion)
                elif operador == ">=":
                    A.append([-1 * coef for coef in coeficientes])
                    b.append(-resultado_restriccion)

            graficar_solucion(A, b, solucion_optima)

        root.destroy()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese datos válidos.")

def agregar_variables():
    global entry_resultado_ecuacion
    try:
        for widget in root.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        num_variables = int(entry_num_variables.get())
        num_restricciones = int(entry_num_restricciones.get())

        for i in range(num_variables):
            entry = tk.Entry(root, width=5)
            entry.grid(row=2, column=i * 2, padx=2, pady=5)
            tk.Label(root, text=f"x{i+1}").grid(row=2, column=(i * 2) + 1, padx=2, pady=5)
            entries_variables.append(entry)

        tk.Label(root, text="Restricciones").grid(row=3, column=0, columnspan=2, padx=2, pady=5)
        for i in range(num_restricciones):
            restriccion_entries = []
            for j in range(num_variables):
                entry = tk.Entry(root, width=5)
                entry.grid(row=4 + i, column=j * 2, padx=2, pady=5)
                tk.Label(root, text=f"x{j+1}").grid(row=4 + i, column=(j * 2) + 1, padx=2, pady=5)
                restriccion_entries.append(entry)

            operador = tk.StringVar(root)
            operador.set("<=")
            operadores_restricciones.append(operador)
            tk.OptionMenu(root, operador, "<=", ">=").grid(row=4 + i, column=num_variables * 2, padx=2, pady=5)

            resultado_restriccion = tk.Entry(root, width=5)
            resultado_restriccion.grid(row=4 + i, column=(num_variables * 2) + 1, padx=2, pady=5)
            restriccion_entries.append(resultado_restriccion)
            entries_restricciones.append(restriccion_entries)

        btn_enviar = tk.Button(root, text="Enviar", command=enviar_datos)
        btn_enviar.grid(row=6 + num_restricciones, column=1)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese datos válidos.")

def crear_formulario(parent):
    global root
    root = parent

    tk.Label(root, text="Número de variables:").grid(row=0, column=0)
    global entry_num_variables
    entry_num_variables = tk.Entry(root)
    entry_num_variables.grid(row=0, column=1)

    btn_agregar = tk.Button(root, text="Agregar Variables y Restricciones", command=agregar_variables)
    btn_agregar.grid(row=0, column=2)

    tk.Label(root, text="Maximizar o minimizar (max/min):").grid(row=1, column=0)
    global variable_tipo
    variable_tipo = tk.StringVar(root)
    variable_tipo.set("max")  # Valor por defecto
    tk.OptionMenu(root, variable_tipo, "max", "min").grid(row=1, column=1)

    global entry_num_restricciones
    tk.Label(root, text="Número de restricciones:").grid(row=0, column=3)
    entry_num_restricciones = tk.Entry(root)
    entry_num_restricciones.grid(row=0, column=4)