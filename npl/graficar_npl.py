import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

def graficar_solucion(coeficientes_objetivo, exponentes_objetivo, solucion_optima, restricciones, tipo_problema):
    """
    Función para graficar la solución de problemas de optimización no lineal.
    Maneja casos de una y dos variables. Para más variables, informa al usuario
    que la graficación no es posible.

    :param coeficientes_objetivo: Lista de coeficientes de la función objetivo.
    :param exponentes_objetivo: Lista de exponentes de la función objetivo.
    :param solucion_optima: Array con los valores óptimos de las variables.
    :param restricciones: Lista de restricciones del problema.
    :param tipo_problema: Tipo de problema ('max' o 'min').
    """
    num_variables = len(coeficientes_objetivo)

    if num_variables == 1:
        # Caso de una variable
        x_vals = np.linspace(0, max(solucion_optima[0]*1.5, 10), 400)

        # Definir la función objetivo
        def funcion_objetivo(x):
            return coeficientes_objetivo[0] * (x ** exponentes_objetivo[0])

        # Calcular los valores de y usando la función objetivo
        y_vals = funcion_objetivo(x_vals)

        # Crear la gráfica
        plt.figure()
        plt.plot(x_vals, y_vals, label="Función Objetivo")

        # Marcar la solución óptima
        if solucion_optima is not None:
            plt.plot(solucion_optima[0], funcion_objetivo(solucion_optima[0]), 'ro', label="Solución Óptima")

        plt.xlabel('x₁')
        plt.ylabel('f(x₁)')
        plt.title('Gráfico de la solución óptima (1 variable)')
        plt.legend()
        plt.grid(True)
        plt.show()

    elif num_variables == 2:
        # Caso de dos variables
        x1_vals = np.linspace(0, max(solucion_optima[0]*1.5, 10), 100)
        x2_vals = np.linspace(0, max(solucion_optima[1]*1.5, 10), 100)
        X1, X2 = np.meshgrid(x1_vals, x2_vals)

        # Definir la función objetivo
        def funcion_objetivo(x1, x2):
            return (coeficientes_objetivo[0] * (x1 ** exponentes_objetivo[0]) +
                    coeficientes_objetivo[1] * (x2 ** exponentes_objetivo[1]))

        # Calcular los valores de Z usando la función objetivo
        Z = funcion_objetivo(X1, X2)

        # Crear la gráfica de contorno
        plt.figure()
        contour = plt.contourf(X1, X2, Z, levels=50, cmap='viridis')
        plt.colorbar(contour)
        plt.xlabel('x₁')
        plt.ylabel('x₂')
        plt.title('Curvas de nivel de la función objetivo (2 variables)')

        # Graficar las restricciones
        for restriccion in restricciones:
            coeficientes = restriccion['coeficientes']
            operador = restriccion['operador']
            resultado = restriccion['resultado']

            if coeficientes[1] != 0:
                x2_restriccion = (resultado - coeficientes[0]*x1_vals) / coeficientes[1]
                if operador == "<=":
                    plt.fill_between(x1_vals, x2_restriccion, x2_vals[-1], color='grey', alpha=0.3)
                elif operador == ">=":
                    plt.fill_between(x1_vals, x2_vals[0], x2_restriccion, color='grey', alpha=0.3)
            else:
                x1_line = np.full_like(x2_vals, resultado / coeficientes[0])
                if operador == "<=":
                    plt.fill_betweenx(x2_vals, x1_line, x1_vals[-1], color='grey', alpha=0.3)
                elif operador == ">=":
                    plt.fill_betweenx(x2_vals, x1_vals[0], x1_line, color='grey', alpha=0.3)

        # Marcar la solución óptima
        if solucion_optima is not None:
            plt.plot(solucion_optima[0], solucion_optima[1], 'ro', label="Solución Óptima")

        plt.legend()
        plt.grid(True)
        plt.show()

    else:
        # Caso de más de dos variables
        messagebox.showinfo("Información", "La graficación solo está disponible para problemas con una o dos variables.")

