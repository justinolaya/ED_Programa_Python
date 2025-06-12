import streamlit as st
import sympy as sp
from st_mathlive import mathfield
import re
import unicodedata

# Definir símbolos globalmente para SymPy
x, y = sp.symbols('x y')

def latex_to_sympy(latex_str: str) -> str:
    """
    Convierte una cadena LaTeX a una cadena compatible con SymPy.
    Versión corregida con mejor manejo de funciones y multiplicación.
    """
    if latex_str is None:
        return ""
    if not isinstance(latex_str, str):
        return str(latex_str)
    
    result = latex_str.strip()
    print(f"[DEBUG] Input: {result}")

    # Paso 1: Normalización de Unicode y limpieza inicial
    result = unicodedata.normalize('NFKD', result).encode('ascii', 'ignore').decode('utf-8')

    # Eliminar \left, \right, y comandos \mathrm/\text
    result = re.sub(r'\\left|\\right', '', result)
    result = re.sub(r'\\(?:mathrm|text[a-zA-Z]*|textbf|text){([^}]+)}', r'\1', result)
    result = re.sub(r'{}', '', result)

    # Paso 2: Manejar funciones trigonométricas PRIMERO
    # Convertir funciones LaTeX a SymPy antes de procesar multiplicación
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
        result = re.sub(pattern, replacement, result)
    
    # Reemplazos directos
    replacements = {
        '\\sin': 'sin', '\\cos': 'cos', '\\tan': 'tan', '\\cot': 'cot', 
        '\\sec': 'sec', '\\csc': 'csc',
        '\\arcsin': 'asin', '\\arccos': 'acos', '\\arctan': 'atan',
        '\\sinh': 'sinh', '\\cosh': 'cosh', '\\tanh': 'tanh',
        '\\exp': 'exp', '\\ln': 'log', '\\log': 'log',
        '\\pi': 'pi', '\\infty': 'oo',
        'sen': 'sin',  # Para español
        '\\cdot': '*', '\\times': '*'
    }
    for old, new in replacements.items():
        result = result.replace(old, new)

    print(f"[DEBUG] After function replacements: {result}")
    
    # Paso 3: Manejo de potencias (antes de multiplicación implícita)
    print(f"[DEBUG] Before power processing: {result}")

    # a) Potencias con llaves, base simple o con paréntesis embebido:
    #    x^{2+1} -> x**(2+1)
    #    (x+1)^{y+2} -> (x+1)**(y+2)
    result = re.sub(
    r'(\([^\)]+\)|[a-zA-Z0-9]+)\s*\^\s*\{([^}]+)\}',
    r'\1**(\2)',
    result
    )

    # b) Potencias sin llaves, exponente simple:
    #    x^2 -> x**2, e^x -> e**x
    result = re.sub(
    r'(\([^\)]+\)|[a-zA-Z0-9]+)\s*\^\s*([a-zA-Z0-9]+)',
    r'\1**(\2)',
    result
    )

    # c) Cualquier resto de '^' sin capturar potencias (por seguridad)
    result = result.replace('^', '**')

    
    print(f"[DEBUG] After power processing: {result}")
    
    # Paso 4: Manejar fracciones
    result = re.sub(r'\\frac{([^{}]+)}{([^{}]+)}', r'(\1)/(\2)', result)
    
    # Paso 5: Proteger dx y dy
    result = re.sub(r'\bdx\b', ' __DX__ ', result)
    result = re.sub(r'\bdy\b', ' __DY__ ', result)
    
    print(f"[DEBUG] After dx/dy protection: {result}")
    
    # Paso 6: Multiplicación implícita mejorada (DESPUÉS de potencias)
    result = re.sub(r'\s+', ' ', result).strip()
    
    print(f"[DEBUG] Before implicit multiplication: {result}")
    
    # IMPORTANTE: NO procesar multiplicación si ya hay ** (potencias)
    # Número seguido de variable (pero NO si hay ** en el medio)
    result = re.sub(r'(\d+)\s+([a-zA-Z])', r'\1*\2', result)
    
    # Variable seguida de paréntesis (sin espacios para evitar conflictos)
    result = re.sub(r'([a-zA-Z])\(', r'\1*(', result)
    
    # Paréntesis cerrado seguido de variable
    result = re.sub(r'\)\s*([a-zA-Z])', r')*\1', result)
    
    # Paréntesis cerrado seguido de paréntesis abierto
    result = re.sub(r'\)\s*\(', r')*(', result)
    
    # Número seguido de paréntesis
    result = re.sub(r'(\d+)\s*\(', r'\1*(', result)
    
    # Casos especiales para funciones trigonométricas
    # xsin(y) -> x*sin(y) (pero NO x**sin)
    result = re.sub(r'([a-zA-Z])(?!\*\*)([a-zA-Z]+\()', r'\1*\2', result)
    
    # sin(x)cos(y) -> sin(x)*cos(y)
    result = re.sub(r'(sin|cos|tan|log|exp)\(([^)]+)\)\s*(sin|cos|tan|log|exp)', r'\1(\2)*\3', result)
    
    # sin(x)y -> sin(x)*y (pero NO sin(x)**y)
    result = re.sub(r'(sin|cos|tan|log|exp)\(([^)]+)\)(?!\*\*)([a-zA-Z])', r'\1(\2)*\3', result)
    
    print(f"[DEBUG] After implicit multiplication: {result}")
    
    # Paso 7: Restaurar dx y dy
    result = result.replace('__DX__', 'dx')
    result = result.replace('__DY__', 'dy')
    
    # Paso 8: Limpiar multiplicaciones dobles
    # result = re.sub(r'\*+', '*', result) # Eliminado para evitar que x**2 se convierta en x*2
    
    print(f"[DEBUG] Final result: {result}")
    return result

def parse_differential_equation_from_full_string(equation_str: str) -> tuple[str, str]:
    """
    Parser mejorado para ecuaciones diferenciales.
    """
    equation_str = equation_str.strip()
    print(f"[DEBUG] Parsing equation: {equation_str}")

    # Normalizar la ecuación para el parsing
    temp_equation_str = re.sub(r'\bdx\b', '__DX__', equation_str)
    temp_equation_str = re.sub(r'\bdy\b', '__DY__', temp_equation_str)
    
    print(f"[DEBUG] After dx/dy substitution: {temp_equation_str}")

    # Patrón 1: (M)dx + (N)dy = 0 o (M)dx - (N)dy = 0
    pattern1 = r'^(.*?)\s*__DX__\s*([+\-])\s*(.*?)\s*__DY__\s*=\s*0\s*$'
    match1 = re.match(pattern1, temp_equation_str, re.IGNORECASE)
    if match1:
        M_str = match1.group(1).strip()
        sign = match1.group(2)
        N_str = match1.group(3).strip()
        
        # Manejar coeficientes implícitos de 1
        if not M_str: M_str = '1'
        if not N_str: N_str = '1'
        
        print(f"[DEBUG] Pattern 1 matched - M: {M_str}, sign: {sign}, N: {N_str}")
        
        M_str = clean_outer_parentheses(M_str)
        N_str = clean_outer_parentheses(N_str)
        
        if sign == '-':
            N_str = f"-({N_str})"
        
        return M_str, N_str

    # Patrón 2: (M)dx + (N)dy (sin =0)
    pattern2 = r'^(.*?)\s*__DX__\s*([+\-])\s*(.*?)\s*__DY__\s*$'
    match2 = re.match(pattern2, temp_equation_str, re.IGNORECASE)
    if match2:
        M_str = match2.group(1).strip()
        sign = match2.group(2)
        N_str = match2.group(3).strip()
        
        # Manejar coeficientes implícitos de 1
        if not M_str: M_str = '1'
        if not N_str: N_str = '1'
        
        M_str = clean_outer_parentheses(M_str)
        N_str = clean_outer_parentheses(N_str)
        
        if sign == '-':
            N_str = f"-({N_str})"
        
        return M_str, N_str

    # Patrón 3: Mdx = Ndy
    pattern3 = r'^(.*?)\s*__DX__\s*=\s*(.*?)\s*__DY__\s*$'
    match3 = re.match(pattern3, temp_equation_str, re.IGNORECASE)
    if match3:
        M_str = match3.group(1).strip()
        N_str = match3.group(2).strip()
        
        # Manejar coeficientes implícitos de 1
        if not M_str: M_str = '1'
        if not N_str: N_str = '1'
        
        M_str = clean_outer_parentheses(M_str)
        N_str = clean_outer_parentheses(N_str)
        
        return M_str, f"-({N_str})"

    print(f"[DEBUG] No pattern matched for: {temp_equation_str}")
    raise ValueError(f"No se pudo parsear la ecuación: '{equation_str}'. Formatos soportados: (M)dx + (N)dy = 0, Mdx = Ndy, etc.")

def clean_outer_parentheses(expr_str: str) -> str:
    """
    Elimina paréntesis externos innecesarios si están balanceados.
    """
    expr_str = expr_str.strip()
    if expr_str.startswith('(') and expr_str.endswith(')'):
        count = 0
        for i, char in enumerate(expr_str):
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            if count == 0 and i < len(expr_str) - 1:
                return expr_str
        return expr_str[1:-1]
    return expr_str

def safe_sympify(expr_str: str):
    """
    Versión segura de sympify que maneja mejor los errores.
    """
    try:
        # Limpiar la expresión antes de pasarla a sympify
        cleaned = expr_str.strip()
        # Asegurar que las funciones estén bien formateadas
        cleaned = re.sub(r'([a-zA-Z]+)\*\*', r'(\1)**', cleaned)
        
        # Convertir usando el namespace local con símbolos definidos
        return sp.sympify(cleaned, locals={'x': x, 'y': y, 'sin': sp.sin, 'cos': sp.cos, 
                                          'tan': sp.tan, 'log': sp.log, 'exp': sp.exp, 
                                          'pi': sp.pi, 'sqrt': sp.sqrt})
    except Exception as e:
        print(f"[ERROR] Error in sympify for '{expr_str}': {e}")
        raise ValueError(f"No se pudo convertir la expresión '{expr_str}' a SymPy: {e}")

def solve_exact_differential_equation(M_str: str, N_str: str) -> list[str]:
    """
    Resuelve una ecuación diferencial exacta con manejo mejorado de errores.
    """
    results = []
    try:
        # Convertir strings a expresiones SymPy usando la función segura
        M = safe_sympify(M_str)
        N = safe_sympify(N_str)
        
        results.append("### 1. Ecuación diferencial original")
        results.append(f"$({sp.latex(M)})\,dx + ({sp.latex(N)})\,dy = 0$")

        results.append("### 2. Derivadas parciales y verificación de exactitud")
        dM_dy = sp.diff(M, y)
        dN_dx = sp.diff(N, x)
        results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_dy)}$")
        results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_dx)}$")
        
        if sp.simplify(dM_dy - dN_dx) == 0:
            results.append("✅ La ecuación es exacta.")
            results.append("### 3. Solución general de la ecuación exacta")
            
            # Integrar M con respecto a x
            Fx_y = sp.integrate(M, x)
            results.append(f"Integramos $M(x,y)$ con respecto a $x$: $F(x,y) = \\int M(x,y) dx = {sp.latex(Fx_y)} + g(y)$")
            
            # Derivar F(x,y) parcialmente con respecto a y y comparar con N(x,y)
            dF_dy = sp.diff(Fx_y, y)
            
            # Calcular g'(y)
            g_prime_y_expr = sp.simplify(N - dF_dy)
            
            results.append(f"Comparamos con $N(x,y)$: $g'(y) = N(x,y) - \\frac{{\\partial F}}{{\\partial y}} = {sp.latex(N)} - ({sp.latex(dF_dy)}) = {sp.latex(g_prime_y_expr)}$")
            
            # Verificar si g_prime_y_expr contiene 'x'
            if g_prime_y_expr.free_symbols and x in g_prime_y_expr.free_symbols:
                results.append(f"**Advertencia**: $g'(y)$ aún contiene $x$: ${sp.latex(g_prime_y_expr)}$")

            # Integrar g'(y) para encontrar g(y)
            g_y = sp.integrate(g_prime_y_expr, y)
            results.append(f"Integramos $g'(y)$ con respecto a $y$: $g(y) = \\int g'(y) dy = {sp.latex(g_y)}$")
            
            # Solución general
            general_solution = sp.simplify(Fx_y + g_y)
            results.append(f"La solución general es $F(x,y) = C$: ${sp.latex(general_solution)} = C$")

        else:
            results.append("❌ La ecuación NO es exacta.")
            results.append("### 3. Búsqueda de factor integrante")
            
            mu_found = False

            # Caso 1: Factor integrante función de x
            try:
                if N != 0:
                    p_x_candidate = sp.simplify((dM_dy - dN_dx) / N)
                    if p_x_candidate.free_symbols <= {x}:
                        mu = sp.exp(sp.integrate(p_x_candidate, x))
                        results.append(f"**Caso 1:** Factor integrante dependiente de x: $\\mu(x) = {sp.latex(mu)}$")
                        mu_found = True
                        
                        # Aplicar el factor integrante y resolver
                        M_new = sp.simplify(mu * M)
                        N_new = sp.simplify(mu * N)
                        
                        results.append("### 4. Ecuación multiplicada por el factor integrante")
                        results.append(f"${sp.latex(M_new)}\,dx + {sp.latex(N_new)}\\,dy = 0$")
                        
                        # Continuar con la solución...
                        dM_new_dy = sp.diff(M_new, y)
                        dN_new_dx = sp.diff(N_new, x)
                        
                        if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                            results.append("✅ La nueva ecuación ES exacta.")
                            
                            F_new_x_y = sp.integrate(M_new, x)
                            dF_new_dy = sp.diff(F_new_x_y, y)
                            h_prime_y_expr = sp.simplify(N_new - dF_new_dy)
                            h_y = sp.integrate(h_prime_y_expr, y)
                            general_solution_new = sp.simplify(F_new_x_y + h_y)
                            results.append(f"**Solución general**: ${sp.latex(general_solution_new)} = C$")
            except Exception as e:
                results.append(f"Error en factor integrante de x: {e}")
            
            # Caso 2: Factor integrante función de y
            if not mu_found:
                try:
                    if M != 0:
                        p_y_candidate = sp.simplify((dN_dx - dM_dy) / M)
                        if p_y_candidate.free_symbols <= {y}:
                            mu = sp.exp(sp.integrate(p_y_candidate, y))
                            results.append(f"**Caso 2:** Factor integrante dependiente de y: $\\mu(y) = {sp.latex(mu)}$")
                            mu_found = True
                            
                            # Similar proceso para factor integrante de y...
                            M_new = sp.simplify(mu * M)
                            N_new = sp.simplify(mu * N)
                            
                            results.append("### 4. Ecuación multiplicada por el factor integrante")
                            results.append(f"${sp.latex(M_new)}\,dx + {sp.latex(N_new)}\\,dy = 0$")
                            
                            dM_new_dy = sp.diff(M_new, y)
                            dN_new_dx = sp.diff(N_new, x)
                            
                            if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                                results.append("✅ La nueva ecuación ES exacta.")
                                
                                F_new_x_y = sp.integrate(M_new, x)
                                dF_new_dy = sp.diff(F_new_x_y, y)
                                h_prime_y_expr = sp.simplify(N_new - dF_new_dy)
                                h_y = sp.integrate(h_prime_y_expr, y)
                                general_solution_new = sp.simplify(F_new_x_y + h_y)
                                results.append(f"**Solución general**: ${sp.latex(general_solution_new)} = C$")
                except Exception as e:
                    results.append(f"Error en factor integrante de y: {e}")

            if not mu_found:
                results.append("⚠️ No se pudo encontrar un factor integrante simple.")
                
    except Exception as e:
        results.append(f"**Error**: {str(e)}")
        import traceback
        results.append(f"**Traceback**: {traceback.format_exc()}")
    
    return results

# Código Streamlit
st.title("Análisis de Ecuaciones Diferenciales Exactas y Factores Integrantes")

st.markdown("### Introduce la ecuación diferencial completa:")
full_equation_latex_input, _ = mathfield(
    value=r"(x^2+x+y)dx+(1-x^2-y)dy=0",
    key="full_equation_input"
)

if st.button("Procesar"):
    try:
        st.write("**Debug Info:**")
        st.write(f"Input LaTeX: {full_equation_latex_input}")
        
        full_equation_str_processed = latex_to_sympy(full_equation_latex_input) if full_equation_latex_input else ""
        st.write(f"Procesado por latex_to_sympy: `{full_equation_str_processed}`")
        
        M_str_parsed, N_str_parsed = parse_differential_equation_from_full_string(full_equation_str_processed)
        
        st.write(f"M parseado: `{M_str_parsed}`")
        st.write(f"N parseado: `{N_str_parsed}`")
        
        # Resolver la ecuación
        results = solve_exact_differential_equation(M_str_parsed, N_str_parsed)
        
        st.markdown("---")
        st.markdown("## Solución:")
        
        for line in results:
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
                
    except ValueError as ve:
        st.error(f"Error de formato: {str(ve)}")
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        import traceback
        st.code(traceback.format_exc())