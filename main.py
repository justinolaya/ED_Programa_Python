import sympy as sp
from sympy import symbols
from dev.exacta import exacta
from dev.casos.caso1 import caso1
from dev.casos.caso2 import caso2
from dev.casos.caso3 import caso3, caso3_algebraico

def main():
    x, y = symbols('x y', real=True)

    # Solicitar al usuario la ecuación diferencial
    print("Ingrese la EDO de la forma M(x,y) dx + N(x,y) dy = 0")
    M_input = input("Ingrese M(x, y): ")
    N_input = input("Ingrese N(x, y): ")

    try:
        M = sp.sympify(M_input)
        N = sp.sympify(N_input)
    except Exception as e:
        print(f"Error al interpretar las expresiones: {e}")
        return

    print("\nVerificando si la ecuación es exacta...")
    if exacta(M, N, x, y):
        print("La ecuación ya es exacta. No se requiere factor integrante.")
        return

    print("La ecuación no es exacta. Intentando encontrar factor integrante...\n")

    # Caso 1: μ(x)
    factor, exito = caso1(M, N, x, y)
    if exito:
        print("\nFactor integrante encontrado con el Caso 1 (función de x).")
        return

    # Caso 2: μ(y)
    factor, exito = caso2(M, N, x, y)
    if exito:
        print("\nFactor integrante encontrado con el Caso 2 (función de y).")
        return

    # Caso 3: μ(x^m * y^n)
    factor, exito = caso3(M, N, x, y)
    if exito:
        print("\nFactor integrante encontrado con el Caso 3 (forma x^m * y^n).")
        return

    # Caso 3 alternativo: método algebraico
    factor, exito = caso3_algebraico(M, N, x, y)
    if exito:
        print("\nFactor integrante encontrado con el Caso 3 alternativo (método algebraico).")
        return

    print("\nNo se pudo encontrar un factor integrante con ninguno de los métodos disponibles.")

if __name__ == "__main__":
    main()
