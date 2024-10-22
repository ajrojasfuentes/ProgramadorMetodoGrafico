import matplotlib.pyplot as plt
import numpy as np

def graficar_solucion(A, b, solucion_optima):
    plt.figure()

    x_vals = np.linspace(0, 10, 400)

    # Graficar cada restricción
    for i in range(len(A)):
        if A[i][1] != 0:  # Evitar división por cero
            y_vals = (b[i] - A[i][0] * x_vals) / A[i][1]
            plt.plot(x_vals, y_vals, label=f'Restricción {i+1}')
        else:
            plt.axvline(x=b[i] / A[i][0], label=f'Restricción {i+1}')

    # Graficar el punto de solución óptima
    if solucion_optima is not None:
        plt.plot(solucion_optima[0], solucion_optima[1], 'ro', label="Solución Óptima")

    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('Gráfico de la solución óptima')
    plt.legend()
    plt.grid(True)

    # Mostrar la gráfica
    plt.show()
