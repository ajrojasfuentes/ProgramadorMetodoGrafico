import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

def graficar_solucion(datos_optimizacion, solucion_optima):
    """
    Función para graficar la solución de problemas de programación lineal.
    Solo es aplicable a problemas con dos variables.

    :param datos_optimizacion: Diccionario con los datos del problema.
    :param solucion_optima: Array con los valores óptimos de las variables.
    """
    variables = datos_optimizacion["variables"]
    restricciones = datos_optimizacion["restricciones"]
    tipo_problema = datos_optimizacion["tipo_problema"]

    num_variables = len(variables)

    if num_variables != 2:
        # Mostrar mensaje informando que solo se pueden graficar problemas de dos variables
        messagebox.showinfo("Información", "La graficación solo está disponible para problemas con dos variables.")
        return

    # Crear el rango de valores para las variables
    x1_vals = np.linspace(0, max(solucion_optima[0]*1.5, 10), 400)
    x2_vals = np.linspace(0, max(solucion_optima[1]*1.5, 10), 400)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Definir la función objetivo
    def funcion_objetivo(x1, x2):
        return variables[0]*x1 + variables[1]*x2

    # Calcular los valores de Z usando la función objetivo
    Z = funcion_objetivo(X1, X2)

    # Crear la gráfica
    plt.figure()
    contour = plt.contourf(X1, X2, Z, levels=50, cmap='viridis', alpha=0.7)
    plt.colorbar(contour)
    plt.xlabel('x₁')
    plt.ylabel('x₂')
    plt.title('Región Factible y Solución Óptima')

    # Sombrear la región factible
    for restriccion in restricciones:
        coeficientes = restriccion['coeficientes']
        operador = restriccion['operador']
        resultado = restriccion['resultado']

        # Crear una máscara para la restricción
        if coeficientes[1] != 0:
            x2_restriccion = (resultado - coeficientes[0]*x1_vals) / coeficientes[1]
            if operador == "<=":
                plt.fill_between(x1_vals, x2_restriccion, x2_vals[0], where=(x2_restriccion >= 0), color='grey', alpha=0.3)
            elif operador == ">=":
                plt.fill_between(x1_vals, x2_vals[-1], x2_restriccion, where=(x2_restriccion <= x2_vals[-1]), color='grey', alpha=0.3)
        elif coeficientes[0] != 0:
            x1_line = np.full_like(x2_vals, resultado / coeficientes[0])
            if operador == "<=":
                plt.fill_betweenx(x2_vals, x1_line, x1_vals[0], where=(x1_line >= 0), color='grey', alpha=0.3)
            elif operador == ">=":
                plt.fill_betweenx(x2_vals, x1_vals[-1], x1_line, where=(x1_line <= x1_vals[-1]), color='grey', alpha=0.3)

    # Graficar las líneas de las restricciones
    for i, restriccion in enumerate(restricciones):
        coeficientes = restriccion['coeficientes']
        operador = restriccion['operador']
        resultado = restriccion['resultado']

        if coeficientes[1] != 0:
            x2_restriccion = (resultado - coeficientes[0]*x1_vals) / coeficientes[1]
            plt.plot(x1_vals, x2_restriccion, label=f'Restricción {i + 1}')
        elif coeficientes[0] != 0:
            x1_restriccion = resultado / coeficientes[0]
            plt.axvline(x=x1_restriccion, label=f'Restricción {i + 1}')
        else:
            messagebox.showerror("Error", f"Coeficientes inválidos en la restricción {i + 1}")
            return

    # Marcar la solución óptima
    if solucion_optima is not None and len(solucion_optima) == 2:
        plt.plot(solucion_optima[0], solucion_optima[1], 'ro', label="Solución Óptima")
    else:
        messagebox.showerror("Error", "Solución óptima no válida")
        return

    plt.legend()
    plt.grid(True)
    plt.show()
