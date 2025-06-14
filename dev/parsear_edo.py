import re

def parsear_edo(entrada: str):
    """
    Parsea una ecuación de la forma M(x, y) dx + N(x, y) dy = 0
    y retorna las expresiones simbólicas M y N.
    """
    from sympy import symbols, sympify, diff, simplify
    from dev.signos_multiplicacion import signos_multiplicacion
    from dev.normalizar_coeficiente import normalizar_coeficiente
    from dev.simplificar_general import simplificar_general

    x, y = symbols('x y')
    print("----------------------------------------------------")
    print("✅✅✅✅✅✅✅✅✅✅")
    print("[DEBUG] Entrada original:", entrada)

    entrada = entrada.strip()
    print("[DEBUG] Entrada sin espacios extremos:", entrada)

    # Aplicar simplificación general si la ecuación es = 0
    if entrada.endswith('= 0') or entrada.endswith('=0'):
        entrada = simplificar_general(entrada)
        print(f"[DEBUG] Ecuación simplificada general: '{entrada}'")

    entrada = entrada.replace('^', '**')
    print("[DEBUG] Entrada con potencias normalizadas (^ → **):", entrada)

    # Manejar ecuaciones que no están en forma estándar (M dx + N dy = 0)
    if '=' in entrada and not entrada.endswith('= 0') and not entrada.endswith('=0'):
        print("[DEBUG] Ecuación no está en forma estándar, convirtiendo...")
        lado_izq, lado_der = entrada.split('=', 1)
        lado_izq = lado_izq.strip()
        lado_der = lado_der.strip()
        print(f"[DEBUG] Lado izquierdo: '{lado_izq}'")
        print(f"[DEBUG] Lado derecho: '{lado_der}'")
        
        # Convertir a forma estándar: lado_izq - (lado_der) = 0
        entrada = f"{lado_izq} - ({lado_der})"
        print(f"[DEBUG] Forma estándar: '{entrada}'")
        
        from dev.simplificar import simplificar
        entrada = simplificar(entrada)
        print(f"[DEBUG] Forma estándar simplificada: '{entrada}'")
    else:
        # Remover = 0 si ya está en forma estándar
        entrada = entrada.replace('= 0', '').replace('=0', '')
        print("[DEBUG] Ecuación ya en forma estándar, removiendo '= 0'")

    entrada = entrada.replace(' dx', 'dx').replace(' dy', 'dy')
    print("[DEBUG] Entrada sin espacios antes de dx/dy:", entrada)

    dx_pos = entrada.find('dx')
    dy_pos = entrada.find('dy')
    print(f"[DEBUG] Posición de dx: {dx_pos}, posición de dy: {dy_pos}")

    if dx_pos == -1 or dy_pos == -1:
        raise ValueError("La ecuación debe tener al menos un término con dx y uno con dy")

    if dx_pos < dy_pos:
        coef_M = entrada[:dx_pos].strip()
        coef_N_raw = entrada[dx_pos + 2:dy_pos].strip()
        print(f"[DEBUG] coef_N_raw = '{coef_N_raw}'")
        if not coef_N_raw:
            coef_N = '1'
            print("[DEBUG] coef_N vacío: se asume '1'")
        elif coef_N_raw in ['+', '-']:
            coef_N = coef_N_raw + '1'
            print(f"[DEBUG] coef_N era solo '{coef_N_raw}': se convierte en '{coef_N}'")
        else:
            coef_N = coef_N_raw
        print("[DEBUG] dx aparece primero. coef_M =", coef_M, "| coef_N =", coef_N)
    else:
        coef_N = entrada[:dy_pos].strip()
        coef_M_raw = entrada[dy_pos + 2:dx_pos].strip()
        print(f"[DEBUG] coef_M_raw = '{coef_M_raw}'")
        if not coef_M_raw:
            coef_M = '1'
            print("[DEBUG] coef_M vacío: se asume '1'")
        elif coef_M_raw in ['+', '-']:
            coef_M = coef_M_raw + '1'
            print(f"[DEBUG] coef_M era solo '{coef_M_raw}': se convierte en '{coef_M}'")
        else:
            coef_M = coef_M_raw
        print("[DEBUG] dy aparece primero. coef_N =", coef_N, "| coef_M =", coef_M)

    try:
        coef_M_norm = normalizar_coeficiente(coef_M)
        coef_N_norm = normalizar_coeficiente(coef_N)

        print(f"[DEBUG] coef_M antes de signos_multiplicacion: '{coef_M_norm}'")
        coef_M_norm = signos_multiplicacion(coef_M_norm)
        print(f"[DEBUG] coef_M tras signos_multiplicacion: '{coef_M_norm}'")

        print(f"[DEBUG] coef_N antes de signos_multiplicacion: '{coef_N_norm}'")
        coef_N_norm = signos_multiplicacion(coef_N_norm)
        print(f"[DEBUG] coef_N tras signos_multiplicacion: '{coef_N_norm}'")

        print(f"[DEBUG] sympify(coef_M_norm): '{coef_M_norm}'")
        print(f"[DEBUG] sympify(coef_N_norm): '{coef_N_norm}'")

        M = sympify(coef_M_norm, locals={'x': x, 'y': y})
        N = sympify(coef_N_norm, locals={'x': x, 'y': y})

        print(f"[DEBUG] Resultado final: M = {M}, N = {N}")
        print(f"[DEBUG] M.has(x)? {M.has(x)}, M.has(y)? {M.has(y)}")
        print(f"[DEBUG] N.has(x)? {N.has(x)}, N.has(y)? {N.has(y)}")
        
        My = diff(M, y)
        Nx = diff(N, x)

        print("\n[DEBUG] Derivada parcial ∂M/∂y:", My)
        print("[DEBUG] Derivada parcial ∂N/∂x:", Nx)
        print("[DEBUG] Simplificación de ∂M/∂y - ∂N/∂x:", simplify(My - Nx))

    except Exception as e:
        print(f"[ERROR] Fallo en sympify: {e}")
        raise ValueError(f"No se pudo convertir a expresión simbólica: {e}")

    return M, N
