from equation_solver import solve_exact_differential_equation

# Ejemplos de ecuaciones (M, N) en formato de cadena de texto
examples = {
    "1": {"M": "x - y + 1", "N": "-1"}, # Ecuación no exacta. Se resuelve con factor integrante μ(x) (Caso 1).
    "2": {"M": "x**3 * y + 1", "N": "x**2 * y**2"}, # Ecuación no exacta. Podría requerir un factor integrante complejo.
    "3": {"M": "x - y", "N": "x + y**2 - 1"}, # Ecuación no exacta. Podría requerir un factor integrante complejo.
    "4": {"M": "y - x**2*y", "N": "x"}, # Ecuación no exacta. Se resuelve con factor integrante μ(x) (Caso 1).
    "5": {"M": "x**2 * y**3", "N": "x**3 * y + y + 3"}, # Ecuación no exacta. Podría requerir un factor integrante complejo.
    "6": {"M": "x**2", "N": "-(x**3 * y**2 + 3 * y**3)"}, # Ecuación no exacta. Se resuelve con factor integrante μ(y) (Caso 2).
    "7": {"M": "x * y**2 + x**3 * y**2 + 3", "N": "x**3 * y"}, # Ecuación no exacta. Podría requerir un factor integrante complejo.
    "8": {"M": "1/x", "N": "-(1 + x * y**2)"}, # Ecuación no exacta. Podría requerir un factor integrante complejo.
    "9": {"M": "x**2 + 2*x + y", "N": "1 - x**2 - y"}, # Ecuación no exacta. Podría requerir un factor integrante complejo.
    "10": {"M": "cos(x) - sin(x) + sin(y)", "N": "cos(x) + sin(y) + cos(y)"}, # Ecuación no exacta (ejemplo de la imagen original del usuario). Podría requerir un factor integrante complejo.
    "11": {"M": "y + x*y**2", "N": "x**2*y - x"}, # Ecuación no exacta. Se resuelve con factor integrante μ(x,y) = x^m y^n (Caso 3).
    "12": {"M": "2*x*y**3 + 1", "N": "3*x**2*y**2 - x"}, # Ecuación no exacta. Podría requerir un factor integrante complejo o no elemental.
    "13": {"M": "x**2*y**2 + y", "N": "x**3*y + x"}, # Ecuación no exacta. Podría requerir un factor integrante complejo o no elemental.
    "14": {"M": "y*sin(x*y) + x*cos(x*y)", "N": "x*sin(x*y) - y*cos(x*y)"}, # Ecuación no exacta. Con funciones trigonométricas, puede ser más compleja.
    "15": {"M": "(x**2 + y**2 + x) * x", "N": "(x**2 + y**2 + y) * y"}, # Ecuación Exacta.
    "16": {"M": "y**2", "N": "x*y - 1"}, # Ecuación no exacta. Se resuelve con factor integrante μ(y) (Caso 2).
    "17": {"M": "2*x*y", "N": "x**2 - y**2"}, # Ecuación Exacta.
    "18": {"M": "(x*y + y**2)*sin(x)", "N": "(x**2 + x*y)*cos(x)"}, # Ecuación no exacta. Puede ser compleja o requerir un factor integrante especial.
}

print("\n--- Probando el solucionador de Ecuaciones Diferenciales Exactas ---\n")

for num, eq_data in examples.items():
    M_example = eq_data["M"]
    N_example = eq_data["N"]
    
    print(f"\n=== Ejemplo {num} ===")
    print(f"M(x,y) = {M_example}")
    print(f"N(x,y) = {N_example}")
    
    results = solve_exact_differential_equation(M_example, N_example)
    
    for line in results:
        print(line)
    print("\n" + "-" * 40) 