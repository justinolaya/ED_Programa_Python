import streamlit as st
import sympy as sp
from st_mathlive import mathfield
import re
import unicodedata
from equation_solver import find_integrating_factor  # Cambiado a la nueva función

# Definir símbolos globalmente para SymPy
x, y = sp.symbols('x y')

def latex_to_sympy(latex_str: str) -> str:
    """Convierte una cadena LaTeX a una cadena compatible con SymPy."""
    if latex_str is None:
        return ""
    if not isinstance(latex_str, str):
        return str(latex_str)

    result = latex_str.strip()
    print(f"[DEBUG] Input: {result}")

    # Paso 1: Normalización de Unicode y limpieza inicial
    result = normalize_unicode(result)
    result = remove_latex_commands(result)
    result = re.sub(r'{}', '', result)

    # Paso 2: Manejar funciones trigonométricas
    result = process_trigonometric_functions(result)
    print(f"[DEBUG] After function replacements: {result}")

    # Paso 3: Manejo de potencias
    print(f"[DEBUG] Before power processing: {result}")
    result = process_powers(result)
    print(f"[DEBUG] After power processing: {result}")

    # Paso 4: Manejar fracciones
    result = process_fractions(result)

    # Paso 5: Proteger dx y dy
    result = protect_dx_dy(result)
    print(f"[DEBUG] After dx/dy protection: {result}")

    # Paso 6: Multiplicación implícita
    print(f"[DEBUG] Before implicit multiplication: {result}")
    result = process_implicit_multiplication(result)
    print(f"[DEBUG] After implicit multiplication: {result}")

    # Paso 8: Limpiar multiplicaciones dobles
    result = re.sub(r'\*{2,}', '**', result)
    print(f"[DEBUG] Final result from latex_to_sympy: {result}")
    return result

def normalize_unicode(text: str) -> str:
    """Normaliza el texto Unicode a ASCII."""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

def remove_latex_commands(text: str) -> str:
    """Elimina comandos LaTeX innecesarios."""
    text = re.sub(r'\\left|\\right', '', text)
    text = re.sub(r'\\(?:mathrm|text[a-zA-Z]*|textbf|text){([^}]+)}', r'\1', text)
    return text

def process_trigonometric_functions(text: str) -> str:
    """Procesa funciones trigonométricas en formato LaTeX."""
    function_replacements = {
        r'\\sin\s*\(([^)]+)\)': r'sin(\1)',
        r'\\cos\s*\(([^)]+)\)': r'cos(\1)',
        r'\\tan\s*\(([^)]+)\)': r'tan(\1)',
        r'\\sin\s*([a-zA-Z])': r'sin(\1)',
        r'\\cos\s*([a-zA-Z])': r'cos(\1)',
        r'\\tan\s*([a-zA-Z])': r'tan(\1)',
        r'\\ln\s*\(([^)]+)\)': r'log(\1)',
        r'\\log\s*\(([^)]+)\)': r'log(\1)',
        r'\\exp\s*\(([^)]+)\)': r'exp(\1)',
        r'\\sqrt\s*\{([^}]+)\}': r'sqrt(\1)',
    }
    for pattern, replacement in function_replacements.items():
        text = re.sub(pattern, replacement, text)
    return text

def process_powers(text: str) -> str:
    """Procesa potencias en formato LaTeX."""
    # Potencias con llaves
    text = re.sub(r'(\([^\)]+\)|[a-zA-Z0-9]+)\s*\^\s*\{([^}]+)\}', r'\1**(\2)', text)
    # Potencias sin llaves
    text = re.sub(r'(\([^\)]+\)|[a-zA-Z0-9]+)\s*\^\s*([a-zA-Z0-9]+)', r'\1**(\2)', text)
    # Cualquier resto de '^'
    return text.replace('^', '**')

def process_fractions(text: str) -> str:
    """Procesa fracciones en formato LaTeX."""
    return re.sub(r'\\frac{([^{}]+)}{([^{}]+)}', r'(\1)/(\2)', text)

def protect_dx_dy(text: str) -> str:
    """Protege dx y dy en la expresión."""
    text = re.sub(r'\bdx\b', ' __DX__ ', text)
    text = re.sub(r'\bdy\b', ' __DY__ ', text)
    return text

def process_implicit_multiplication(text: str) -> str:
    """Procesa multiplicación implícita."""
    rules = [
        (r'(sin|cos|tan|log|exp|sqrt)\(([^)]+)\)\s*(sin|cos|tan|log|exp|sqrt)', r'\1(\2)*\3'),
        (r'([a-zA-Z])\s*(sin|cos|tan|log|exp|sqrt)\(([^)]+)\)', r'\1*\2(\3)'),
        (r'(sin|cos|tan|log|exp|sqrt)\(([^)]+)\)\s*([a-zA-Z])', r'\1(\2)*\3'),
        (r'(\d+)([a-zA-Z])', r'\1*\2'),
        (r'(\d+)\s*\(', r'\1*('),
        (r'\)\s*([a-zA-Z])', r')*\1'),
        (r'\)\s*\(', r')*(')
    ]
    
    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text)
    
    # Manejo especial para variables seguidas de paréntesis
    text = re.sub(
        r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
        lambda m: m.group(1) + '*(' if m.group(1) not in ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt'] else m.group(0),
        text
    )
    return text

def parse_differential_equation_from_full_string(equation_str: str) -> tuple[str, str]:
    """Parsea la cadena de la ecuación diferencial para extraer M(x,y) y N(x,y)."""
    print(f"[DEBUG] Parsing full equation string: {equation_str}")

    # Paso 1: Normalizar la ecuación
    normalized_eq_str = normalize_equation(equation_str)
    print(f"[DEBUG] Normalized equation for SymPy parsing: {normalized_eq_str}")

    # Paso 2: Preparar expresión para SymPy
    temp_expr_str = prepare_sympy_expression(normalized_eq_str)
    print(f"[DEBUG] Expression for sympify coefficient extraction: {temp_expr_str}")
    
    try:
        # Paso 3: Convertir a SymPy y extraer coeficientes
        sym_expr = convert_to_sympy(temp_expr_str)
        print(f"[DEBUG] Sympified expression: {sym_expr}")

        sym_expr = sp.expand(sym_expr)
        print(f"[DEBUG] Expanded expression: {sym_expr}")

        M_str, N_str = extract_coefficients(sym_expr)
        print(f"[DEBUG] Extracted M_str: {M_str}, N_str: {N_str}")
        
        return M_str, N_str

    except Exception as e:
        print(f"[ERROR] Error in sympify during parse_differential_equation_from_full_string: {e}")
        raise ValueError(f"No se pudo parsear la ecuación diferencial compleja: '{equation_str}'. Error: {e}")

def normalize_equation(equation_str: str) -> str:
    """Normaliza la ecuación a la forma LadoIzquierdo = 0."""
    equation_str = equation_str.strip()
    if '=' in equation_str:
        left_side, right_side = equation_str.split('=', 1)
        return f"({left_side}) - ({right_side})"
    return f"({equation_str})"

def prepare_sympy_expression(expr_str: str) -> str:
    """Prepara la expresión para SymPy."""
    _dx_temp, _dy_temp = sp.symbols('__dx_temp__ __dy_temp__')
    
    # Manejar multiplicación implícita con dx y dy
    temp_expr_str = re.sub(r'([a-zA-Z0-9)])\s*__DX__', r'\1*__dx_temp__', expr_str)
    temp_expr_str = re.sub(r'([a-zA-Z0-9)])\s*__DY__', r'\1*__dy_temp__', temp_expr_str)
    
    # Reemplazar marcadores restantes
    temp_expr_str = temp_expr_str.replace('__DX__', str(_dx_temp))
    temp_expr_str = temp_expr_str.replace('__DY__', str(_dy_temp))
    
    return temp_expr_str

def convert_to_sympy(expr_str: str) -> sp.Expr:
    """Convierte una expresión a formato SymPy."""
    return sp.sympify(expr_str, locals={
        'x': x, 'y': y, 
        'sin': sp.sin, 'cos': sp.cos, 
        'tan': sp.tan, 'log': sp.log, 
        'exp': sp.exp, 'pi': sp.pi, 
        'sqrt': sp.sqrt
    })

def extract_coefficients(sym_expr: sp.Expr) -> tuple[str, str]:
    """Extrae los coeficientes M y N de la expresión SymPy."""
    _dx_temp, _dy_temp = sp.symbols('__dx_temp__ __dy_temp__')
    
    M_sym = sp.simplify(sym_expr.coeff(_dx_temp, 1))
    N_sym = sp.simplify(sym_expr.coeff(_dy_temp, 1))
    
    M_str = str(M_sym).replace(str(_dx_temp), '').replace(str(_dy_temp), '').strip()
    N_str = str(N_sym).replace(str(_dx_temp), '').replace(str(_dy_temp), '').strip()
    
    if M_sym == 0: M_str = '0'
    if N_sym == 0: N_str = '0'
    
    return M_str, N_str

def display_result_line(line: str):
    """Muestra una línea de resultado en la interfaz de Streamlit."""
    if line.startswith("###"):
        st.markdown(line)
    elif line.startswith("$") and line.endswith("$"):
        st.latex(line[1:-1])
    elif line.startswith("✅"):
        st.success(line)
    elif line.startswith("❌"):
        st.error(line)
    elif line.startswith("⚠️"):
        st.warning(line)
    elif line.startswith("**"):
        st.markdown(line)
    else:
        st.write(line)

def display_results(results: list):
    """Muestra los resultados en la interfaz de Streamlit."""
    for line in results:
        display_result_line(line)

def process_equation(full_equation_latex_input: str):
    """Procesa la ecuación ingresada y muestra el factor integrante si existe."""
    try:
        # Convertir LaTeX a SymPy
        full_equation_str_processed = latex_to_sympy(full_equation_latex_input)
        
        # Parsear la ecuación
        M_str_parsed, N_str_parsed = parse_differential_equation_from_full_string(full_equation_str_processed)
        
        # Buscar el factor integrante
        results = find_integrating_factor(M_str_parsed, N_str_parsed)
        
        st.markdown("---")
        st.markdown("## Factor Integrante:")
        display_results(results)
            
    except ValueError as ve:
        st.error(f"Error de formato: {str(ve)}")
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")

def main():
    """Función principal de la aplicación."""
    st.title("Análisis de Ecuaciones Diferenciales Exactas y Factores Integrantes")
    st.markdown("### Introduce la ecuación diferencial completa:")
    
    full_equation_latex_input, _ = mathfield(
        value=r"(x^2+x+y)dx+(1-x^2-y)dy=0",
        key="full_equation_input"
    )

    if st.button("Procesar"):
        process_equation(full_equation_latex_input)

if __name__ == "__main__":
    main()