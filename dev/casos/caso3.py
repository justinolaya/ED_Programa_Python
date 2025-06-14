import sympy as sp
from sympy import symbols, diff, integrate, simplify, exp, ln, solve, Eq
from dev.exacta import exacta

def caso3(M, N, x, y, max_exponente=3):
    """
    Caso 3: Factor integrante de la forma x^m * y^n
    Se plantea la ecuación: My - Nx = m(N/x) - n(M/y)
    Luego se determina m y n si es posible
    """
    print("=== CASO 3: Factor integrante de la forma x^m * y^n ===")
    
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
    
    # Probar diferentes valores de m y n
    m, n = symbols('m n', integer=True)
    
    # Ecuación: My - Nx = m(N/x) - n(M/y)
    lado_izq = dM_dy - dN_dx
    
    print(f"∂M/∂y - ∂N/∂x = {lado_izq}")
    
    # Intentar encontrar m y n
    for m_val in range(-max_exponente, max_exponente + 1):
        for n_val in range(-max_exponente, max_exponente + 1):
            if m_val == 0 and n_val == 0:
                continue
                
            try:
                # Calcular lado derecho: m(N/x) - n(M/y)
                lado_der = m_val * (N/x) - n_val * (M/y)
                lado_der = simplify(lado_der)
                
                # Verificar si la ecuación se cumple
                diferencia = simplify(lado_izq - lado_der)
                
                if diferencia == 0:
                    print(f"Encontrado: m = {m_val}, n = {n_val}")
                    print(f"Verificación: {lado_izq} = {lado_der}")
                    
                    # Calcular el factor integrante
                    factor_integrante = x**m_val * y**n_val
                    print("✅✅✅✅✅✅✅✅✅✅")
                    print(f"Factor integrante μ(x,y) = x^{m_val} * y^{n_val} = {factor_integrante}")
                    
                    # Multiplicar M y N por el factor integrante
                    M_nueva = simplify(factor_integrante * M)
                    N_nueva = simplify(factor_integrante * N)
                    
                    print("✅✅✅✅✅✅✅✅✅✅")
                    print(f"Nueva M = μ(x,y) × M = {M_nueva}")
                    print(f"Nueva N = μ(x,y) × N = {N_nueva}")
                    
                    # Verificar si la nueva ecuación es exacta
                    es_exacta = exacta(M_nueva, N_nueva, x, y)
                    
                    if es_exacta:
                        print("✓ La nueva ecuación es exacta!")
                        return factor_integrante, True
                    else:
                        print("✗ La nueva ecuación no es exacta. Continuando búsqueda...")
                        
            except Exception as e:
                # Continuar con el siguiente par (m, n)
                continue
    
    print("No se encontró factor integrante de la forma x^m * y^n")
    print("El Caso 3 no aplica.")
    return None, False

def caso3_algebraico(M, N, x, y):
    """
    Versión alternativa que intenta resolver algebraicamente
    """
    print("=== CASO 3: Método algebraico ===")
    
    # Calcular las derivadas parciales
    dM_dy = diff(M, y)
    dN_dx = diff(N, x)
    
    if exacta(M, N, x, y):
        print("La ecuación ya es exacta.")
        return None, True
    
    # Definir m y n como símbolos
    m, n = symbols('m n', real=True)
    
    # Ecuación: My - Nx = m(N/x) - n(M/y)
    lado_izq = dM_dy - dN_dx
    lado_der = m * (N/x) - n * (M/y)
    
    ecuacion = Eq(lado_izq, lado_der)
    
    print(f"Ecuación a resolver: {ecuacion}")
    
    try:
        # Intentar resolver para m y n
        soluciones = solve(ecuacion, [m, n])
        
        if soluciones:
            print(f"Soluciones encontradas: {soluciones}")
            
            for sol in soluciones:
                if isinstance(sol, (tuple, list)) and len(sol) == 2:
                    m_val, n_val = sol
                    
                    # Verificar que m y n sean enteros o racionales simples
                    if (m_val.is_integer or m_val.is_rational) and (n_val.is_integer or n_val.is_rational):
                        factor_integrante = x**m_val * y**n_val
                        
                        # Verificar
                        M_nueva = simplify(factor_integrante * M)
                        N_nueva = simplify(factor_integrante * N)
                        
                        if exacta(M_nueva, N_nueva, x, y):
                            print("✅✅✅✅✅✅✅✅✅✅")
                            print(f"Factor integrante encontrado: μ(x,y) = {factor_integrante}")
                            return factor_integrante, True
        
        print("No se encontró factor integrante algebraicamente.")
        return None, False
        
    except Exception as e:
        print(f"Error en método algebraico: {e}")
        return None, False
