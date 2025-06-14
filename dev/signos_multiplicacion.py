import re

def signos_multiplicacion(expr: str) -> str:
    # Inserta * entre número y variable: 2x → 2*x
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    # Inserta * entre variable y variable: xy → x*y
    expr = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr)
    # Inserta * entre ) y letra o número: )x → )*x, )2 → )*2
    expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)
    # Inserta * entre número o letra y (: 2( → 2*( o x( → x*(
    expr = re.sub(r'([a-zA-Z0-9])(\()', r'\1*\2', expr)
    return expr
