def normalizar_coeficiente(t: str) -> str:
    """
    Normaliza un coeficiente eliminando signos y espacios innecesarios.
    
    Args:
        t (str): Coeficiente a normalizar
        
    Returns:
        str: Coeficiente normalizado
    """
    print(f"[DEBUG] Normalizando coeficiente: '{t}'")
    t = t.strip()

    if t.startswith('+'):
        print("[DEBUG] Eliminando '+' inicial")
        t = t[1:].strip()

    if t == '':
        print("[DEBUG] Coeficiente vacío tras limpieza: se convierte en '1'")
        return '1'
    if t == '-':
        print("[DEBUG] Coeficiente es '-': se convierte en '-1'")
        return '-1'

    if t.startswith('- ('):
        print("[DEBUG] Eliminando espacio entre '-' y paréntesis")
        t = '-' + t[2:].strip()
    elif t.startswith('+ ('):
        print("[DEBUG] Eliminando '+' y espacio antes del paréntesis")
        t = t[2:].strip()

    print(f"[DEBUG] Coeficiente normalizado final: '{t}'")
    return t