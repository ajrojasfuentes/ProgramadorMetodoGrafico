from scipy.optimize import linprog
from tkinter import messagebox

def optimizar(datos_optimizacion):
    tipo_problema = datos_optimizacion["tipo_problema"]
    variables = datos_optimizacion["variables"]
    restricciones = datos_optimizacion["restricciones"]
    
    # Crear la matriz A y el vector b para las restricciones
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

    # Definir la función objetivo
    c = [-x for x in variables] if tipo_problema == 'max' else variables

    # Resolver el problema con linprog
    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    if res.success:
        messagebox.showinfo("Solución óptima", f"Valor óptimo: {res.fun}\nVariables óptimas: {res.x}")
        return res.x  # Retorna la solución óptima para graficarla
    else:
        messagebox.showerror("Error", "No se encontró una solución óptima.")
        return None
