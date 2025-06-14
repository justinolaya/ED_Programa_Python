from sympy import diff, symbols, simplify

def exacta(M, N, x=None, y=None):
    """Verifica si la ecuación diferencial M dx + N dy = 0 es exacta"""

    print("----------------------------------------------------")
    print("[DEBUG] Función 'exacta' iniciada...")
    print(f"[DEBUG] Entrada: M = {M}, N = {N}")

    # 👇 Detectar x e y si no fueron proporcionadas
    if x is None or y is None:
        print("[DEBUG] x o y no proporcionadas, buscando en símbolos libres...")
        free_vars = M.free_symbols.union(N.free_symbols)
        print(f"[DEBUG] Símbolos libres combinados: {free_vars}")

        var_names = sorted([str(var) for var in free_vars])
        print(f"[DEBUG] Nombres de variables ordenadas: {var_names}")

        if 'x' in var_names and 'y' in var_names:
            for var in free_vars:
                if str(var) == 'x':
                    x = var
                    print("[DEBUG] Variable x encontrada:", x)
                elif str(var) == 'y':
                    y = var
                    print("[DEBUG] Variable y encontrada:", y)
        else:
            raise ValueError("[ERROR] No se encontraron variables x e y en las expresiones")

    print(f"[DEBUG] Usando variables: x = {x}, y = {y}")

    # 👇 Derivadas parciales
    dM_dy = diff(M, y)
    dN_dx = diff(N, x)
    
    print("✅✅✅✅✅✅✅✅✅✅")
    print(f"[DEBUG] ∂M/∂y = {dM_dy}")
    print(f"[DEBUG] ∂N/∂x = {dN_dx}")
    diferencia = dM_dy - dN_dx
    print(f"[DEBUG] Diferencia (∂M/∂y - ∂N/∂x) = {diferencia}")

    # 👇 Verificar si la diferencia es cero
    resultado = simplify(diferencia) == 0
    print(f"[DEBUG] Resultado de exactitud: {'✅ Exacta' if resultado else '❌ No exacta'}")

    return resultado
