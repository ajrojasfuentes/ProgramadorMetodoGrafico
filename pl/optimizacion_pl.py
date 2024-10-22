from scipy.optimize import linprog
from tkinter import messagebox
import numpy as np


def optimizar(datos_optimizacion):
    """
    Función que resuelve un problema de programación lineal utilizando scipy.optimize.linprog.

    :param datos_optimizacion: Diccionario con los datos necesarios para la optimización.
    :return: Variables óptimas si se encuentra solución; None en caso contrario.
    """
    try:
        # Validar la existencia de los campos necesarios
        if not all(k in datos_optimizacion for k in ["tipo_problema", "variables", "restricciones"]):
            messagebox.showerror("Error", "Faltan datos en la entrada.")
            return None

        tipo_problema = datos_optimizacion["tipo_problema"]
        variables = datos_optimizacion["variables"]
        restricciones_datos = datos_optimizacion["restricciones"]

        # Validar el tipo de problema
        if tipo_problema not in ['max', 'min']:
            messagebox.showerror("Error", "Tipo de problema no válido. Debe ser 'max' o 'min'.")
            return None

        # Crear la matriz A_ub, vector b_ub, A_eq, b_eq para las restricciones
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []

        for restriccion in restricciones_datos:
            # Verificar que la restricción tenga los campos necesarios
            if not all(k in restriccion for k in ["coeficientes", "operador", "resultado"]):
                messagebox.showerror("Error", "Formato de restricción no válido.")
                return None

            coeficientes = restriccion["coeficientes"]
            operador = restriccion["operador"]
            resultado_restriccion = restriccion["resultado"]

            # Validar que el resultado de la restricción sea un número
            if not isinstance(resultado_restriccion, (int, float)):
                messagebox.showerror("Error", "El resultado de la restricción debe ser un número.")
                return None

            # Manejar las restricciones según el operador
            if operador == "<=":
                A_ub.append(coeficientes)
                b_ub.append(resultado_restriccion)
            elif operador == ">=":
                # Multiplicar por -1 para convertir en <=
                A_ub.append([-1 * coef for coef in coeficientes])
                b_ub.append(-resultado_restriccion)
            elif operador == "=":
                A_eq.append(coeficientes)
                b_eq.append(resultado_restriccion)
            else:
                messagebox.showerror("Error", f"Operador de restricción no válido: {operador}")
                return None

        # Definir la función objetivo
        if tipo_problema == 'max':
            c = [-x for x in variables]  # Negar los coeficientes para maximizar
        else:
            c = variables

        num_variables = len(variables)

        # Definir límites para las variables (por defecto, no negativas)
        bounds = [(0, None) for _ in range(num_variables)]

        # Convertir listas a arrays de numpy para evitar advertencias en linprog
        A_ub = np.array(A_ub) if A_ub else None
        b_ub = np.array(b_ub) if b_ub else None
        A_eq = np.array(A_eq) if A_eq else None
        b_eq = np.array(b_eq) if b_eq else None

        # Resolver el problema con linprog
        res = linprog(
            c,
            A_ub=A_ub,
            b_ub=b_ub,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method='highs'
        )

        # Comprobar si la solución es exitosa
        if res.success:
            # Obtener el valor óptimo original (considerando si era maximización)
            valor_optimo = -res.fun if tipo_problema == 'max' else res.fun

            # Redondear los resultados para presentación
            variables_optimas = np.round(res.x, decimals=4)
            valor_optimo = np.round(valor_optimo, decimals=4)

            # Mostrar mensaje con el valor óptimo y las variables óptimas
            messagebox.showinfo(
                "Solución óptima",
                f"Valor óptimo: {valor_optimo}\nVariables óptimas: {variables_optimas}"
            )
            return variables_optimas  # Retorna la solución óptima para graficarla
        else:
            messagebox.showerror("Error", "No se encontró una solución óptima.")
            return None

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la optimización:\n{str(e)}")
        return None
