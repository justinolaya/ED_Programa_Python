from sympy import diff, simplify

def exacta(M, N, x, y):
    """Verifica si la ecuación diferencial M dx + N dy = 0 es exacta"""
    dM_dy = diff(M, y)
    dN_dx = diff(N, x)
    return simplify(dM_dy - dN_dx) == 0