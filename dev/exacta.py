from sympy import diff, symbols

def exacta(M, N, x=None, y=None):
    """Verifica si la ecuación diferencial M dx + N dy = 0 es exacta"""
    
    # 👇 AQUÍ ESTÁ EL CAMBIO: Usar las variables que están en M y N
    if x is None or y is None:
        # Extraer las variables de los símbolos libres
        free_vars = M.free_symbols.union(N.free_symbols)
        var_names = sorted([str(var) for var in free_vars])
        if 'x' in var_names and 'y' in var_names:
            # Obtener las variables simbólicas reales de las expresiones
            for var in free_vars:
                if str(var) == 'x':
                    x = var
                elif str(var) == 'y':
                    y = var
        else:
            raise ValueError("No se encontraron variables x e y en las expresiones")
    
    print(f"[DEBUG] Variables libres en M: {M.free_symbols}")
    print(f"[DEBUG] Variables libres en N: {N.free_symbols}")
    print(f"[DEBUG] Usando x = {x}, y = {y}")
    
    dM_dy = diff(M, y)
    dN_dx = diff(N, x)

    print(f"[DEBUG] ∂M/∂y = {dM_dy}")
    print(f"[DEBUG] ∂N/∂x = {dN_dx}")
    print(f"[DEBUG] Diferencia = {dM_dy - dN_dx}")

    return (dM_dy - dN_dx).equals(0)