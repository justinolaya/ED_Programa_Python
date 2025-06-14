import re
from sympy import symbols, sympify, simplify

def simplificar_general(entrada: str) -> str:
    """
    Simplifica cualquier ecuación diferencial de la forma ... = 0,
    agrupando y sumando los coeficientes de dx y dy.
    Devuelve la ecuación en forma estándar: M(x,y) dx + N(x,y) dy = 0
    """
    x, y = symbols('x y')
    # Quitar '= 0' si está presente
    entrada = entrada.strip()
    if entrada.endswith('= 0'):
        entrada = entrada[:-3].strip()
    elif entrada.endswith('=0'):
        entrada = entrada[:-2].strip()

    # Buscar todos los términos con dx y dy (incluyendo paréntesis y espacios)
    terminos = re.findall(r'([+-]?\s*\([^\)]*\)\s*d[xy]|[+-]?\s*[^+\-]+?d[xy])', entrada)
    M = []
    N = []
    for termino in terminos:
        termino = termino.strip()
        if 'dx' in termino:
            coef = termino.replace('dx', '').strip()
            if coef in ['', '+']:
                coef = '1'
            elif coef == '-':
                coef = '-1'
            M.append(coef)
        elif 'dy' in termino:
            coef = termino.replace('dy', '').strip()
            if coef in ['', '+']:
                coef = '1'
            elif coef == '-':
                coef = '-1'
            N.append(coef)
    # Sumar los coeficientes usando sympy para evitar errores de signos
    try:
        M_expr = '+'.join(M) if M else '0'
        N_expr = '+'.join(N) if N else '0'
        M_simp = simplify(sympify(M_expr, locals={'x': x, 'y': y}))
        N_simp = simplify(sympify(N_expr, locals={'x': x, 'y': y}))
        return f"({M_simp}) dx + ({N_simp}) dy = 0"
    except Exception:
        # Si hay error, devolver la entrada original
        return entrada + ' = 0'
