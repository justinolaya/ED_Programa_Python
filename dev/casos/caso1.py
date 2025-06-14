import sympy as sp
from sympy import symbols, diff, integrate, simplify, exp, ln, solve
from dev.exacta import exacta

def caso1(M, N, x, y):
    """
    Caso 1: Factor integrante que es función de x
    Si (My - Nx)/N es función solamente de x, entonces p(x) = (My - Nx)/N
    f(x) = e^∫p(x)dx
    """
    print("=== CASO 1: Factor integrante función de x ===")
    
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
    
    # Calcular (My - Nx)/N
    numerador = dM_dy - dN_dx
    try:
        p_x = simplify(numerador / N)
        print(f"p(x) = (∂M/∂y - ∂N/∂x)/N = {p_x}")
        
        # Verificar si p(x) es función solo de x (no contiene y)
        if p_x.has(y):
            print("p(x) contiene la variable y, por lo que no es función solo de x.")
            print("El Caso 1 no aplica.")
            return None, False
        
        print("p(x) es función solo de x. Calculando factor integrante...")
        
        # Calcular el factor integrante: f(x) = e^∫p(x)dx
        integral_p = integrate(p_x, x)
        factor_integrante = exp(integral_p)
        factor_integrante = simplify(factor_integrante)
        
        print(f"∫p(x)dx = {integral_p}")
        print("✅✅✅✅✅✅✅✅✅✅")
        print(f"Factor integrante μ(x) = e^∫p(x)dx = {factor_integrante}")
        
        # Multiplicar M y N por el factor integrante
        M_nueva = simplify(factor_integrante * M)
        N_nueva = simplify(factor_integrante * N)
        print("✅✅✅✅✅✅✅✅✅✅")
        print(f"Nueva M = μ(x) × M = {M_nueva}")
        print(f"Nueva N = μ(x) × N = {N_nueva}")
        
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
        print("El Caso 1 no aplica.")
        return None, False
