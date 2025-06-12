def parsear_edo(entrada: str):
    """
    Parsea una ecuación de la forma M(x, y)dx + N(x, y)dy = 0
    y retorna las expresiones simbólicas M y N
    """
    from sympy import symbols, sympify
    import re

    x, y = symbols('x y')

    # Quitar el '= 0' si existe
    entrada = entrada.strip().replace("= 0", "").replace("=0", "").strip()
    
    # Unir términos como '2x' o 'xy' si el usuario no pone '*'
    entrada = entrada.replace('^', '**')  # Por si el usuario usa ^ en lugar de **
    
    # Asegurarse de que 'dx' y 'dy' estén bien separados
    entrada = entrada.replace(' dx', 'dx').replace(' dy', 'dy')

    # Buscar partes que terminan en 'dx' o 'dy'
    dx_match = re.search(r"(.*)dx", entrada)
    dy_match = re.search(r"([\+\-]?\s*.*)dy", entrada)

    if not dx_match or not dy_match:
        raise ValueError("La ecuación debe tener términos dx y dy")

    M_str = dx_match.group(1).strip()
    N_str = dy_match.group(1).strip()

    # Evaluar las cadenas como expresiones simbólicas
    try:
        M = sympify(M_str)
        N = sympify(N_str)
    except Exception as e:
        raise ValueError(f"No se pudo convertir a expresión simbólica: {e}")

    return M, N
