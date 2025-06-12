import sympy as sp
from sympy import symbols, diff, integrate, simplify, exp, ln, solve
from dev.exacta import exacta

def caso2(M, N, x, y):
    """
    Caso 2: Factor integrante que es función de y
    Si (Nx - My)/M es función solamente de y, entonces p(y) = (Nx - My)/M
    f(y) = e^∫p(y)dy
    """
    print("=== CASO 2: Factor integrante función de y ===")
    
    # Calcular las derivadas parciales
    dM_dy = diff(M, y)
    dN_dx = diff(N, x)
    
    print(f"M = {M}")
    print(f"N = {N}")
    print(f"∂M/∂y = {dM_dy}")
    print(f"∂N/∂x = {dN_dx}")
    
    # Verificar si es exacta
    if exacta(M, N, x, y):
        print("La ecuación ya es exacta. No se necesita factor integrante.")
        return None, True
    
    print("La ecuación no es exacta.")
    
    # Calcular (Nx - My)/M
    numerador = dN_dx - dM_dy
    try:
        p_y = simplify(numerador / M)
        print(f"p(y) = (∂N/∂x - ∂M/∂y)/M = {p_y}")
        
        # Verificar si p(y) es función solo de y (no contiene x)
        if p_y.has(x):
            print("p(y) contiene la variable x, por lo que no es función solo de y.")
            print("El Caso 2 no aplica.")
            return None, False
        
        print("p(y) es función solo de y. Calculando factor integrante...")
        
        # Calcular el factor integrante: f(y) = e^∫p(y)dy
        integral_p = integrate(p_y, y)
        factor_integrante = exp(integral_p)
        factor_integrante = simplify(factor_integrante)
        
        print(f"∫p(y)dy = {integral_p}")
        print(f"Factor integrante μ(y) = e^∫p(y)dy = {factor_integrante}")
        
        # Multiplicar M y N por el factor integrante
        M_nueva = simplify(factor_integrante * M)
        N_nueva = simplify(factor_integrante * N)
        
        print(f"Nueva M = μ(y) × M = {M_nueva}")
        print(f"Nueva N = μ(y) × N = {N_nueva}")
        
        # Verificar si la nueva ecuación es exacta
        es_exacta = exacta(M_nueva, N_nueva, x, y)
        
        if es_exacta:
            print("✓ La nueva ecuación es exacta!")
            return factor_integrante, True
        else:
            print("✗ La nueva ecuación no es exacta. Error en el cálculo.")
            return None, False
            
    except Exception as e:
        print(f"Error en el cálculo: {e}")
        print("El Caso 2 no aplica.")
        return None, False
