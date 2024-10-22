import tkinter as tk
from tkinter import messagebox
from npl.optimizacion_npl import optimizar
from npl.graficar_npl import graficar_solucion

# Variables globales para almacenar las entradas de usuario
entries_variables = []  # Lista para entradas de coeficientes de variables
entries_exponentes = []  # Lista para entradas de exponentes de variables
entries_restricciones = []  # Lista para entradas de restricciones
operadores_restricciones = []  # Lista para operadores de restricciones (<=, >=)


def continuar():
    """
    Función que se ejecuta al presionar el botón "Continuar".
    Valida los datos ingresados y, si son correctos, avanza al siguiente paso.
    """
    try:
        # Obtener y validar el número de variables y restricciones
        num_variables = int(entry_num_variables.get())
        num_restricciones = int(entry_num_restricciones.get())

        if not (1 <= num_variables <= 9) or not (1 <= num_restricciones <= 9):
            raise ValueError

        tipo_problema = variable_tipo.get()

        # Guardar los datos en variables globales
        global datos_iniciales
        datos_iniciales = {
            "num_variables": num_variables,
            "num_restricciones": num_restricciones,
            "tipo_problema": tipo_problema
        }

        # Limpiar la ventana
        for widget in root.winfo_children():
            widget.destroy()

        # Avanzar a la siguiente etapa
        crear_campos_variables()

    except ValueError:
        # Mostrar mensaje de error si los datos son inválidos
        messagebox.showerror(
            "Error",
            "Por favor ingrese valores válidos, el máximo de variables y restricciones permitidos es de 9"
        )


def crear_campos_variables():
    """
    Crea los campos de entrada para los coeficientes y exponentes de las variables.
    """
    global entries_variables, entries_exponentes
    entries_variables = []
    entries_exponentes = []

    num_variables = datos_iniciales["num_variables"]

    # Etiqueta para la función objetivo
    tk.Label(root, text="Función Objetivo").grid(row=0, column=0, columnspan=4, pady=10)

    # Crear campos para coeficientes y exponentes
    for i in range(num_variables):
        # Etiqueta de la variable (x1, x2, ...)
        tk.Label(root, text=f"Coeficiente x{i + 1}:").grid(row=i + 1, column=0, padx=5, pady=5)
        entry_var = tk.Entry(root, width=5)
        entry_var.grid(row=i + 1, column=1, padx=5, pady=5)
        entries_variables.append(entry_var)

        # Etiqueta para el exponente
        tk.Label(root, text=f"Exponente x{i + 1}:").grid(row=i + 1, column=2, padx=5, pady=5)
        entry_exp = tk.Entry(root, width=5)
        entry_exp.grid(row=i + 1, column=3, padx=5, pady=5)
        entries_exponentes.append(entry_exp)

    # Botón para agregar restricciones
    btn_agregar_restricciones = tk.Button(root, text="Continuar", command=crear_campos_restricciones)
    btn_agregar_restricciones.grid(row=num_variables + 2, column=1, columnspan=2, pady=10)


def crear_campos_restricciones():
    """
    Crea los campos de entrada para las restricciones.
    """
    try:
        # Validar que los coeficientes y exponentes sean numéricos
        num_variables = datos_iniciales["num_variables"]
        num_restricciones = datos_iniciales["num_restricciones"]
        tipo_problema = datos_iniciales["tipo_problema"]

        # Crear listas para guardar los coeficientes y exponentes
        global coeficientes_objetivo, exponentes_objetivo
        coeficientes_objetivo = []
        exponentes_objetivo = []

        for i in range(num_variables):
            coef = float(entries_variables[i].get())
            exp = int(entries_exponentes[i].get())
            if exp <= 0:
                raise ValueError
            coeficientes_objetivo.append(coef)
            exponentes_objetivo.append(exp)

        # Limpiar la ventana
        for widget in root.winfo_children():
            widget.destroy()

        global entries_restricciones, operadores_restricciones
        entries_restricciones = []
        operadores_restricciones = []

        # Etiqueta para restricciones
        tk.Label(root, text="Restricciones").grid(row=0, column=0, columnspan=4, pady=10)

        # Crear campos para restricciones
        for i in range(num_restricciones):
            restriccion_entries = []
            for j in range(num_variables):
                # Etiqueta de la variable en la restricción
                tk.Label(root, text=f"Coef x{j + 1} en R{i + 1}:").grid(row=i * (num_variables + 2) + j + 1, column=0,
                                                                        padx=5, pady=5)
                entry = tk.Entry(root, width=5)
                entry.grid(row=i * (num_variables + 2) + j + 1, column=1, padx=5, pady=5)
                restriccion_entries.append(entry)

            # Menú desplegable para operador
            operador = tk.StringVar(root)
            operador.set("<=")
            operadores_restricciones.append(operador)
            tk.Label(root, text="Operador:").grid(row=i * (num_variables + 2) + num_variables + 1, column=0, padx=5,
                                                  pady=5)
            tk.OptionMenu(root, operador, "<=", ">=").grid(row=i * (num_variables + 2) + num_variables + 1, column=1,
                                                           padx=5, pady=5)

            # Entrada para resultado de la restricción
            tk.Label(root, text="Resultado:").grid(row=i * (num_variables + 2) + num_variables + 2, column=0, padx=5,
                                                   pady=5)
            resultado_restriccion = tk.Entry(root, width=5)
            resultado_restriccion.grid(row=i * (num_variables + 2) + num_variables + 2, column=1, padx=5, pady=5)
            restriccion_entries.append(resultado_restriccion)

            entries_restricciones.append(restriccion_entries)

        # Botón para enviar datos y ejecutar la optimización
        btn_enviar = tk.Button(root, text="Optimizar", command=enviar_datos)
        btn_enviar.grid(row=num_restricciones * (num_variables + 2) + 1, column=0, columnspan=2, pady=10)

    except ValueError:
        # Mostrar mensaje de error si los datos son inválidos
        messagebox.showerror("Error", "Por favor, ingrese coeficientes y exponentes válidos.")


def enviar_datos():
    """
    Recopila todos los datos ingresados y ejecuta la optimización.
    """
    try:
        num_variables = datos_iniciales["num_variables"]
        num_restricciones = datos_iniciales["num_restricciones"]
        tipo_problema = datos_iniciales["tipo_problema"]

        # Las listas coeficientes_objetivo y exponentes_objetivo ya fueron obtenidas
        global coeficientes_objetivo, exponentes_objetivo

        # Recoger restricciones
        restricciones = []
        for i in range(num_restricciones):
            coeficientes_restriccion = []
            for j in range(num_variables):
                coeficiente = float(entries_restricciones[i][j].get())
                coeficientes_restriccion.append(coeficiente)
            operador = operadores_restricciones[i].get()
            resultado_restriccion = float(entries_restricciones[i][-1].get())

            restricciones.append({
                'coeficientes': coeficientes_restriccion,
                'operador': operador,
                'resultado': resultado_restriccion
            })

        # Preparar datos para la optimización
        datos_optimizacion = {
            "coeficientes_objetivo": coeficientes_objetivo,
            "exponentes_objetivo": exponentes_objetivo,
            "tipo_problema": tipo_problema,
            "restricciones": restricciones
        }

        # Ejecutar la optimización no lineal
        solucion_optima = optimizar(datos_optimizacion)

        # Graficar la solución si existe
        if solucion_optima is not None:
            graficar_solucion(coeficientes_objetivo, exponentes_objetivo, solucion_optima, restricciones, tipo_problema)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Optimización completada exitosamente.")
        root.destroy()

    except ValueError:
        # Mostrar mensaje de error si hay valores inválidos
        messagebox.showerror("Error", "Por favor, ingrese datos válidos.")


def crear_formulario(parent):
    """
    Función para crear el formulario inicial de la interfaz gráfica.
    """
    global root
    root = parent

    # Etiqueta y entrada para número de variables
    tk.Label(root, text="Número de variables (máximo 9):").grid(row=0, column=0, padx=5, pady=5)
    global entry_num_variables
    entry_num_variables = tk.Entry(root)
    entry_num_variables.grid(row=0, column=1, padx=5, pady=5)

    # Etiqueta y entrada para número de restricciones
    tk.Label(root, text="Número de restricciones (máximo 9):").grid(row=1, column=0, padx=5, pady=5)
    global entry_num_restricciones
    entry_num_restricciones = tk.Entry(root)
    entry_num_restricciones.grid(row=1, column=1, padx=5, pady=5)

    # Etiqueta y menú para seleccionar tipo de problema
    tk.Label(root, text="Tipo de problema:").grid(row=2, column=0, padx=5, pady=5)
    global variable_tipo
    variable_tipo = tk.StringVar(root)
    variable_tipo.set("max")  # Valor por defecto
    tk.OptionMenu(root, variable_tipo, "max", "min").grid(row=2, column=1, padx=5, pady=5)

    # Botón "Continuar"
    btn_continuar = tk.Button(root, text="Continuar", command=continuar)
    btn_continuar.grid(row=3, column=0, columnspan=2, pady=10)


# Código para iniciar la aplicación
if __name__ == "__main__":
    # Crear ventana principal
    root = tk.Tk()
    root.title("Optimización No Lineal")

    # Llamar a la función para crear el formulario inicial
    crear_formulario(root)

    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()
