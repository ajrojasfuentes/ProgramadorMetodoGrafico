import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox
from mpl_toolkits.mplot3d import Axes3D

def graficar_solucion(coeficientes_objetivo, exponentes_objetivo, solucion_optima, restricciones, tipo_problema):
    """
    Función para graficar la solución de problemas de optimización no lineal.
    Maneja casos de una a tres variables. En el caso de tres variables, fija una variable
    para poder graficar en 3D. Muestra las restricciones en el gráfico cuando es posible.

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

        # Graficar las restricciones
        for restriccion in restricciones:
            coef = restriccion['coeficientes'][0]
            operador = restriccion['operador']
            resultado = restriccion['resultado']
            if coef != 0:
                x_restriccion = resultado / coef
                if operador == "<=":
                    plt.axvspan(0, x_restriccion, color='grey', alpha=0.3)
                elif operador == ">=":
                    plt.axvspan(x_restriccion, x_vals[-1], color='grey', alpha=0.3)
                plt.axvline(x=x_restriccion, color='black', linestyle='--', label=f'Restricción')
            else:
                # Caso especial donde coeficiente es cero
                pass  # No se puede graficar una restricción sin coeficiente en x

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

        # Crear la figura y el eje 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Crear la superficie de la función objetivo
        surf = ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)

        # Agregar la barra de color
        fig.colorbar(surf, shrink=0.5, aspect=5)

        # Marcar la solución óptima
        if solucion_optima is not None:
            ax.scatter(solucion_optima[0], solucion_optima[1], funcion_objetivo(solucion_optima[0], solucion_optima[1]),
                       color='red', s=50, label='Solución Óptima')

        # Graficar las restricciones
        for restriccion in restricciones:
            coeficientes = restriccion['coeficientes']
            operador = restriccion['operador']
            resultado = restriccion['resultado']

            # Solo graficar restricciones que involucren x1 y x2
            if len(coeficientes) == 2:
                if coeficientes[1] != 0:
                    x2_restriccion = (resultado - coeficientes[0]*x1_vals) / coeficientes[1]
                    if operador == "<=":
                        ax.plot(x1_vals, x2_restriccion, 0, color='grey', linestyle='--', label='Restricción')
                    elif operador == ">=":
                        ax.plot(x1_vals, x2_restriccion, 0, color='grey', linestyle='--', label='Restricción')
                elif coeficientes[0] != 0:
                    x1_restriccion = resultado / coeficientes[0]
                    if operador == "<=":
                        ax.plot([x1_restriccion]*len(x2_vals), x2_vals, 0, color='grey', linestyle='--', label='Restricción')
                    elif operador == ">=":
                        ax.plot([x1_restriccion]*len(x2_vals), x2_vals, 0, color='grey', linestyle='--', label='Restricción')

        # Etiquetas y título
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.set_zlabel('f(x₁, x₂)')
        ax.set_title('Gráfico 3D de la función objetivo (2 variables)')

        # Mostrar la leyenda
        ax.legend()

        plt.show()

    elif num_variables == 3:
        # Caso de tres variables
        # Fijar una variable (la que tiene el valor óptimo más alto)
        idx_max = np.argmax(solucion_optima)
        var_fija = solucion_optima[idx_max]
        var_fija_label = f'x{idx_max + 1}'

        # Variables para graficar
        var_indices = [i for i in range(num_variables) if i != idx_max]
        x_vals = [np.linspace(0, max(solucion_optima[i]*1.5, 10), 100) for i in var_indices]
        X1, X2 = np.meshgrid(x_vals[0], x_vals[1])

        # Definir la función objetivo con la variable fija
        def funcion_objetivo(x1, x2):
            variables = [0]*num_variables
            variables[var_indices[0]] = x1
            variables[var_indices[1]] = x2
            variables[idx_max] = var_fija
            return sum(coeficientes_objetivo[i] * (variables[i] ** exponentes_objetivo[i]) for i in range(num_variables))

        # Calcular los valores de Z usando la función objetivo
        Z = funcion_objetivo(X1, X2)

        # Crear la figura y el eje 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Crear la superficie de la función objetivo
        surf = ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)

        # Agregar la barra de color
        fig.colorbar(surf, shrink=0.5, aspect=5)

        # Marcar la solución óptima
        if solucion_optima is not None:
            x_opt = solucion_optima[var_indices[0]]
            y_opt = solucion_optima[var_indices[1]]
            z_opt = funcion_objetivo(x_opt, y_opt)
            ax.scatter(x_opt, y_opt, z_opt, color='red', s=50, label='Solución Óptima')

        # Graficar las restricciones
        for restriccion in restricciones:
            coeficientes = restriccion['coeficientes']
            operador = restriccion['operador']
            resultado = restriccion['resultado']

            # Solo graficar restricciones que involucren las variables representadas
            if coeficientes[idx_max] == 0:
                coef_x1 = coeficientes[var_indices[0]]
                coef_x2 = coeficientes[var_indices[1]]

                if coef_x2 != 0:
                    x2_restriccion = (resultado - coef_x1*x_vals[0]) / coef_x2
                    if operador == "<=":
                        ax.plot(x_vals[0], x2_restriccion, 0, color='grey', linestyle='--', label='Restricción')
                    elif operador == ">=":
                        ax.plot(x_vals[0], x2_restriccion, 0, color='grey', linestyle='--', label='Restricción')
                elif coef_x1 != 0:
                    x1_restriccion = resultado / coef_x1
                    if operador == "<=":
                        ax.plot([x1_restriccion]*len(x_vals[1]), x_vals[1], 0, color='grey', linestyle='--', label='Restricción')
                    elif operador == ">=":
                        ax.plot([x1_restriccion]*len(x_vals[1]), x_vals[1], 0, color='grey', linestyle='--', label='Restricción')

        # Etiquetas y título
        ax.set_xlabel(f'x{var_indices[0] + 1}')
        ax.set_ylabel(f'x{var_indices[1] + 1}')
        ax.set_zlabel('f(x)')
        ax.set_title(f'Gráfico 3D con {var_fija_label} = {var_fija:.2f}')

        # Mostrar la leyenda
        ax.legend()

        plt.show()

    else:
        # Caso de más de tres variables
        messagebox.showinfo("Información", "La graficación solo está disponible para problemas con hasta tres variables.")
