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
            y_optimo = funcion_objetivo(solucion_optima[0])
            plt.plot(solucion_optima[0], y_optimo, 'ro', label="Solución Óptima")
            # Añadir etiquetas
            plt.text(solucion_optima[0], y_optimo, f'({solucion_optima[0]:.2f}, {y_optimo:.2f})', color='red')

            # Mostrar el valor optimizado de la función objetivo
            plt.annotate(f'Valor óptimo: {y_optimo:.2f}',
                         xy=(solucion_optima[0], y_optimo),
                         xytext=(solucion_optima[0], y_optimo*1.1),
                         arrowprops=dict(facecolor='red', shrink=0.05),
                         color='red')

        # Graficar las restricciones
        for restriccion in restricciones:
            coef = restriccion['coeficientes'][0]
            exp = restriccion['exponentes'][0]
            operador = restriccion['operador']
            resultado = restriccion['resultado']
            # Definir la función de restricción
            def funcion_restriccion(x):
                return coef * (x ** exp)

            y_restriccion = funcion_restriccion(x_vals)
            if operador == "<=":
                plt.fill_between(x_vals, y_vals.min(), y_vals.max(), where=(y_restriccion <= resultado), color='grey', alpha=0.3)
            elif operador == ">=":
                plt.fill_between(x_vals, y_vals.min(), y_vals.max(), where=(y_restriccion >= resultado), color='grey', alpha=0.3)
            plt.plot(x_vals, y_restriccion, linestyle='--', color='black', label='Restricción')

        plt.xlabel('x₁')
        plt.ylabel('f(x₁)')
        plt.title('Gráfico de la solución óptima (1 variable)')
        plt.legend()
        plt.grid(True)
        plt.show()

    elif num_variables == 2:
        # Caso de dos variables
        x1_vals = np.linspace(0, max(solucion_optima[0]*1.5, 10), 200)
        x2_vals = np.linspace(0, max(solucion_optima[1]*1.5, 10), 200)
        X1, X2 = np.meshgrid(x1_vals, x2_vals)

        # Definir la función objetivo
        def funcion_objetivo(x1, x2):
            return (coeficientes_objetivo[0] * (x1 ** exponentes_objetivo[0]) +
                    coeficientes_objetivo[1] * (x2 ** exponentes_objetivo[1]))

        # Calcular los valores de Z usando la función objetivo
        Z = funcion_objetivo(X1, X2)

        # Ajustar la escala del mapa de color alrededor del valor óptimo
        if solucion_optima is not None:
            valor_optimo = funcion_objetivo(solucion_optima[0], solucion_optima[1])
            z_min = valor_optimo * 0.5
            z_max = valor_optimo * 1.5
        else:
            z_min = np.min(Z)
            z_max = np.max(Z)

        # Crear la figura y el eje 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Crear la superficie de la función objetivo con la escala ajustada
        surf = ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8, vmin=z_min, vmax=z_max)

        # Agregar la barra de color
        fig.colorbar(surf, shrink=0.5, aspect=5)

        # Marcar la solución óptima
        if solucion_optima is not None:
            valor_optimo = funcion_objetivo(solucion_optima[0], solucion_optima[1])
            ax.scatter(solucion_optima[0], solucion_optima[1], valor_optimo,
                       color='red', s=50, label='Solución Óptima')

            # Añadir etiquetas de los valores óptimos
            ax.text(solucion_optima[0], solucion_optima[1], valor_optimo,
                    f'({solucion_optima[0]:.2f}, {solucion_optima[1]:.2f}, {valor_optimo:.2f})',
                    color='red')

            # Mostrar el valor optimizado de la función objetivo
            ax.text2D(0.05, 0.95, f'Valor óptimo de f(x₁, x₂): {valor_optimo:.2f}',
                      transform=ax.transAxes, color='red')

        # Proyectar las restricciones sobre la superficie
        for restriccion in restricciones:
            coeficientes = restriccion['coeficientes']
            exponentes = restriccion['exponentes']
            operador = restriccion['operador']
            resultado = restriccion['resultado']

            # Definir la función de restricción
            def funcion_restriccion(x1, x2):
                return sum(coef * (x ** exp) for coef, x, exp in zip(coeficientes, [x1, x2], exponentes))

            # Calcular los valores de la restricción sobre la malla
            C = funcion_restriccion(X1, X2)

            # Crear una máscara para la región factible
            if operador == "<=":
                mask = C <= resultado
            elif operador == ">=":
                mask = C >= resultado
            else:
                continue  # Si el operador no es válido, saltamos esta restricción

            # Proyectar la restricción sobre la superficie
            Z_restriccion = np.where(mask, Z, np.nan)
            ax.plot_surface(X1, X2, Z_restriccion, color='grey', alpha=0.3)

            # Trazar la línea de la restricción en el nivel del resultado
            ax.contour(X1, X2, C, levels=[resultado], colors='black', linestyles='--')

        # Etiquetas y título
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.set_zlabel('f(x₁, x₂)')
        ax.set_title('Gráfico 3D de la función objetivo con restricciones proyectadas')

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

        # Ajustar la escala del mapa de color alrededor del valor óptimo
        if solucion_optima is not None:
            x_opt = solucion_optima[var_indices[0]]
            y_opt = solucion_optima[var_indices[1]]
            valor_optimo = funcion_objetivo(x_opt, y_opt)
            z_min = valor_optimo * 0.5
            z_max = valor_optimo * 1.5
        else:
            z_min = np.min(Z)
            z_max = np.max(Z)

        # Crear la figura y el eje 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Crear la superficie de la función objetivo con la escala ajustada
        surf = ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8, vmin=z_min, vmax=z_max)

        # Agregar la barra de color
        fig.colorbar(surf, shrink=0.5, aspect=5)

        # Marcar la solución óptima
        if solucion_optima is not None:
            ax.scatter(x_opt, y_opt, valor_optimo, color='red', s=50, label='Solución Óptima')

            # Añadir etiquetas de los valores óptimos
            ax.text(x_opt, y_opt, valor_optimo,
                    f'({x_opt:.2f}, {y_opt:.2f}, {valor_optimo:.2f})',
                    color='red')

            # Mostrar el valor optimizado de la función objetivo
            ax.text2D(0.05, 0.95, f'Valor óptimo de f(x): {valor_optimo:.2f}',
                      transform=ax.transAxes, color='red')

        # Proyectar las restricciones sobre la superficie
        for restriccion in restricciones:
            coeficientes = restriccion['coeficientes']
            exponentes = restriccion['exponentes']
            operador = restriccion['operador']
            resultado = restriccion['resultado']

            # Solo graficar restricciones que involucren las variables representadas
            if coeficientes[idx_max] == 0:
                coef_x1 = coeficientes[var_indices[0]]
                exp_x1 = exponentes[var_indices[0]]
                coef_x2 = coeficientes[var_indices[1]]
                exp_x2 = exponentes[var_indices[1]]

                # Definir la función de restricción
                def funcion_restriccion(x1, x2):
                    return (coef_x1 * (x1 ** exp_x1) + coef_x2 * (x2 ** exp_x2))

                # Calcular los valores de la restricción sobre la malla
                C = funcion_restriccion(X1, X2)

                # Crear una máscara para la región factible
                if operador == "<=":
                    mask = C <= resultado
                elif operador == ">=":
                    mask = C >= resultado
                else:
                    continue  # Si el operador no es válido, saltamos esta restricción

                # Proyectar la restricción sobre la superficie
                Z_restriccion = np.where(mask, Z, np.nan)
                ax.plot_surface(X1, X2, Z_restriccion, color='grey', alpha=0.3)

                # Trazar la línea de la restricción en el nivel del resultado
                ax.contour(X1, X2, C, levels=[resultado], colors='black', linestyles='--')

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
