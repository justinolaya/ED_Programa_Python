def parsear_edo(entrada: str):
    """
    Parsea una ecuación de la forma M(x, y) dx + N(x, y) dy = 0
    y retorna las expresiones simbólicas M y N.
    """
    from sympy import symbols, sympify
    from dev.signos_multiplicacion import signos_multiplicacion

    x, y = symbols('x y')

    print("----------------------------------------------------")
    print("[DEBUG] Entrada original:", entrada)

    entrada = entrada.strip()
    print("[DEBUG] Entrada sin espacios extremos:", entrada)

    entrada = entrada.replace('= 0', '').replace('=0', '')
    print("[DEBUG] Entrada sin '=0':", entrada)

    entrada = entrada.replace('^', '**')
    print("[DEBUG] Entrada con potencias normalizadas (^ → **):", entrada)

    entrada = entrada.replace(' dx', 'dx').replace(' dy', 'dy')
    print("[DEBUG] Entrada sin espacios antes de dx/dy:", entrada)

    dx_pos = entrada.find('dx')
    dy_pos = entrada.find('dy')
    print(f"[DEBUG] Posición de dx: {dx_pos}, posición de dy: {dy_pos}")

    if dx_pos == -1 or dy_pos == -1:
        raise ValueError("La ecuación debe tener al menos un término con dx y uno con dy")

    if dx_pos < dy_pos:
        coef_M = entrada[:dx_pos].strip()
        # 👇 AQUÍ ESTÁ EL CAMBIO: Extraer correctamente el coeficiente de N
        coef_N_raw = entrada[dx_pos + 2:dy_pos].strip()
        if not coef_N_raw:
            coef_N = '1'  # Si no hay nada entre dx y dy, asumimos coeficiente 1
        elif coef_N_raw in ['+', '-']:
            coef_N = coef_N_raw + '1'  # + → +1, - → -1
        else:
            coef_N = coef_N_raw
        print("[DEBUG] dx aparece primero. coef_M =", coef_M, "| coef_N =", coef_N)
    else:
        coef_N = entrada[:dy_pos].strip()
        # 👇 AQUÍ ESTÁ EL CAMBIO: Aplicar la misma lógica para el caso inverso
        coef_M_raw = entrada[dy_pos + 2:dx_pos].strip()
        if not coef_M_raw:
            coef_M = '1'  # Si no hay nada entre dy y dx, asumimos coeficiente 1
        elif coef_M_raw in ['+', '-']:
            coef_M = coef_M_raw + '1'  # + → +1, - → -1
        else:
            coef_M = coef_M_raw
        print("[DEBUG] dy aparece primero. coef_N =", coef_N, "| coef_M =", coef_M)

    def normalizar_coeficiente(t):
        print(f"[DEBUG] Normalizando coeficiente: '{t}'")
        t = t.strip()

        # Eliminar signos '+' innecesarios
        if t.startswith('+'):
            t = t[1:].strip()

        # Casos especiales: solo '+' o '-'
        if t == '':
            print("[DEBUG] Coeficiente vacío: se convierte en '1'")
            return '1'
        if t == '-':
            print("[DEBUG] Coeficiente es '-': se convierte en '-1'")
            return '-1'

        # Eliminar espacio entre '-' y paréntesis
        if t.startswith('- ('):
            t = '-' + t[2:].strip()
        elif t.startswith('+ ('):
            t = t[2:].strip()

        print(f"[DEBUG] Coeficiente normalizado final: '{t}'")
        return t

    try:
        coef_M_norm = normalizar_coeficiente(coef_M)
        coef_N_norm = normalizar_coeficiente(coef_N)

        # Inserta los signos de multiplicación faltantes
        coef_M_norm = signos_multiplicacion(coef_M_norm)
        coef_N_norm = signos_multiplicacion(coef_N_norm)

        print(f"[DEBUG] sympify(coef_M_norm): '{coef_M_norm}'")
        print(f"[DEBUG] sympify(coef_N_norm): '{coef_N_norm}'")

        M = sympify(coef_M_norm)
        N = sympify(coef_N_norm)

        print(f"[DEBUG] Resultado final: M = {M}, N = {N}")
    except Exception as e:
        print(f"[ERROR] Fallo en sympify: {e}")
        raise ValueError(f"No se pudo convertir a expresión simbólica: {e}")

    return M, N