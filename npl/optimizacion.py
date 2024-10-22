from scipy.optimize import minimize
from tkinter import messagebox
import numpy as np

def construir_funcion_objetivo(coeficientes, exponentes):
    """
    Construye la función objetivo basada en coeficientes y exponentes.

    :param coeficientes: Lista de coeficientes para cada variable.
    :param exponentes: Lista de exponentes para cada variable.
    :return: Función objetivo lista para ser utilizada en la optimización.
    """
    def funcion_objetivo(variables):
        # Calcula la suma de c_i * (x_i ** e_i) para cada variable
        return sum(c * (v ** e) for c, v, e in zip(coeficientes, variables, exponentes))

    return funcion_objetivo

def crear_funcion_restriccion(coeficientes, resultado, operador):
    """
    Crea una función de restricción lineal basada en el operador.

    :param coeficientes: Lista de coeficientes para la restricción.
    :param resultado: Resultado esperado de la restricción.
    :param operador: Operador de la restricción ('<=' o '>=').
    :return: Función de restricción lista para ser utilizada en la optimización.
    """
    if operador == "<=":
        def restriccion_func(variables):
            # Para '<=': b - sum(a_i * x_i) >= 0
            return resultado - sum(coef * var for coef, var in zip(coeficientes, variables))
    elif operador == ">=":
        def restriccion_func(variables):
            # Para '>=': sum(a_i * x_i) - b >= 0
            return sum(coef * var for coef, var in zip(coeficientes, variables)) - resultado
    else:
        raise ValueError(f"Operador de restricción inválido: {operador}")

    return restriccion_func

def construir_restricciones(restricciones_datos):
    """
    Construye una lista de restricciones para la optimización.

    :param restricciones_datos: Lista de diccionarios con datos de restricciones.
    :return: Lista de restricciones en el formato requerido por scipy.optimize.
    """
    restricciones = []
    for dato in restricciones_datos:
        # Extraer datos de la restricción
        coeficientes = dato['coeficientes']
        resultado = dato['resultado']
        operador = dato['operador']

        # Crear la función de restricción considerando el operador
        funcion_restriccion = crear_funcion_restriccion(coeficientes, resultado, operador)

        # Agregar la restricción al listado como una inecuación
        restricciones.append({'type': 'ineq', 'fun': funcion_restriccion})

    return restricciones

def optimizar(datos_optimizacion):
    """
    Ejecuta la optimización no lineal basada en los datos proporcionados.

    :param datos_optimizacion: Diccionario con datos necesarios para la optimización.
    :return: Variables óptimas si se encuentra solución; None en caso contrario.
    """
    try:
        # Extraer coeficientes y exponentes de la función objetivo
        coeficientes_objetivo = datos_optimizacion["coeficientes_objetivo"]
        exponentes_objetivo = datos_optimizacion["exponentes_objetivo"]
        funcion_objetivo = construir_funcion_objetivo(coeficientes_objetivo, exponentes_objetivo)

        # Construir las restricciones
        restricciones_datos = datos_optimizacion["restricciones"]
        restricciones = construir_restricciones(restricciones_datos)

        # Número de variables en el problema
        num_variables = len(coeficientes_objetivo)

        # Determinar si el problema es de maximización o minimización
        tipo_problema = datos_optimizacion["tipo_problema"]
        if tipo_problema == "max":
            # Si es maximización, minimizar el negativo de la función objetivo
            funcion_objetivo_modificada = lambda x: -funcion_objetivo(x)
        else:
            # Si es minimización, utilizar la función objetivo tal cual
            funcion_objetivo_modificada = funcion_objetivo

        # Definir límites para las variables (por ejemplo, no negativas)
        bounds = [(0, None) for _ in range(num_variables)]

        # Ejecutar la optimización
        resultado = minimize(
            funcion_objetivo_modificada,          # Función objetivo a minimizar
            x0=[1] * num_variables,               # Valor inicial para las variables
            bounds=bounds,                        # Límites de las variables
            constraints=restricciones,            # Restricciones del problema
            method='SLSQP',                       # Método de optimización
            options={'disp': False}               # No mostrar mensajes en consola
        )

        # Verificar si la optimización fue exitosa
        if resultado.success:
            # Obtener el valor óptimo original (considerando si era maximización)
            valor_optimo = -resultado.fun if tipo_problema == "max" else resultado.fun

            # Redondear los resultados para presentación
            variables_optimas = np.round(resultado.x, decimals=4)
            valor_optimo = np.round(valor_optimo, decimals=4)

            # Mostrar mensaje con el valor óptimo y las variables óptimas
            messagebox.showinfo(
                "Solución óptima",
                f"Valor óptimo: {valor_optimo}\nVariables óptimas: {variables_optimas}"
            )
            return variables_optimas  # Retornar las variables óptimas
        else:
            # Mostrar mensaje de error si no se encontró solución
            messagebox.showerror("Error", "No se encontró una solución óptima.")
            return None  # Retornar None si no hay solución

    except Exception as e:
        # Manejar excepciones y mostrar mensaje de error
        messagebox.showerror("Error", f"Ocurrió un error durante la optimización:\n{str(e)}")
        return None
