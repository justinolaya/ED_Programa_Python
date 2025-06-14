import re

def signos_multiplicacion(expr: str) -> str:
    print(f"[DEBUG] Expresión original: {expr}")
    
    # 1. Inserta * entre número y variable: 2x → 2*x
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    print(f"[DEBUG] Después de número y variable (2x → 2*x): {expr}")
    
    # 2. Inserta * entre variable y variable: xy → x*y
    expr = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr)
    print(f"[DEBUG] Después de variable y variable (xy → x*y): {expr}")
    
    # 3. Inserta * entre ) y letra o número: )x → )*x, )2 → )*2
    expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)
    print(f"[DEBUG] Después de ) seguido de letra/número: {expr}")
    
    # 4. Inserta * entre número o letra y (: 2( → 2*( o x( → x*(
    expr = re.sub(r'([a-zA-Z0-9])(\()', r'\1*\2', expr)
    print(f"[DEBUG] Después de número/letra seguido de (: {expr}")
    
    return expr
