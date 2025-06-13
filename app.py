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

    # Reglas en orden de precedencia y especificidad
    # 1. Función seguida de función (e.g., sin(x)cos(y))
    result = re.sub(r'(sin|cos|tan|log|exp|sqrt)\(([^)]+)\)\s*(sin|cos|tan|log|exp|sqrt)', r'\1(\2)*\3', result)

    # 2. Variable seguida de función (e.g., xsin(y))
    result = re.sub(r'([a-zA-Z])\s*(sin|cos|tan|log|exp|sqrt)\(([^)]+)\)', r'\1*\2(\3)', result)

    # 3. Función seguida de variable (e.g., sin(x)y)
    result = re.sub(r'(sin|cos|tan|log|exp|sqrt)\(([^)]+)\)\s*([a-zA-Z])', r'\1(\2)*\3', result)

    # 4. Número seguido de variable (e.g., 2x)
    result = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', result)

    # 5. Número seguido de paréntesis (e.g., 2(x+y))
    result = re.sub(r'(\d+)\s*\(', r'\1*(', result)

    # 6. Paréntesis cerrado seguido de variable (e.g., (x+y)z)
    result = re.sub(r'\)\s*([a-zA-Z])', r')*\1', result)

    # 7. Paréntesis cerrado seguido de paréntesis abierto (e.g., (x+y)(a+b))
    result = re.sub(r'\)\s*\(', r')*(', result)

    # 8. Variable seguida de paréntesis (e.g., x(y+z)), solo si no es un nombre de función ya reconocido
    # Usamos una función de reemplazo para evitar falsos positivos con nombres de funciones
    result = re.sub(
        r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
        lambda m: m.group(1) + '*(' if m.group(1) not in ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt'] else m.group(0),
        result
    )

    print(f"[DEBUG] After implicit multiplication: {result}")

    # Paso 7: Restaurar dx y dy -- ELIMINADO de aquí, se maneja en el parser
    # result = result.replace('__DX__', 'dx')
    # result = result.replace('__DY__', 'dy')

    # Paso 8: Limpiar multiplicaciones dobles (solo si no forman parte de potencias)
    result = re.sub(r'\*{2,}', '**', result) # Conservar ** para potencias

    print(f"[DEBUG] Final result from latex_to_sympy: {result}")
    return result

def parse_differential_equation_from_full_string(equation_str: str) -> tuple[str, str]:
    """
    Parsea la cadena de la ecuación diferencial para extraer M(x,y) y N(x,y).
    Maneja diferentes formatos de ecuaciones diferenciales utilizando SymPy.
    """
    print(f"[DEBUG] Parsing full equation string: {equation_str}")

    # Paso 1: Normalizar la ecuación a la forma LadoIzquierdo = 0
    # Asegurarse de que __DX__ y __DY__ ya estén presentes desde latex_to_sympy
    normalized_eq_str = equation_str.strip()

    if '=' in normalized_eq_str:
        left_side, right_side = normalized_eq_str.split('=', 1)
        # Aseguramos que el lado derecho se reste correctamente
        normalized_eq_str = f"({left_side}) - ({right_side})"
    else:
        # Si no hay =, asumimos que ya es el lado izquierdo (Mdx + Ndy)
        normalized_eq_str = f"({normalized_eq_str})"
    
    print(f"[DEBUG] Normalized equation for SymPy parsing: {normalized_eq_str}")

    # Paso 2: Usar símbolos temporales de SymPy para extraer coeficientes
    # Definir los símbolos temporales para dx y dy
    _dx_temp, _dy_temp = sp.symbols('__dx_temp__ __dy_temp__')
    
    # Reemplazar los marcadores __DX__ y __DY__ con los símbolos temporales de SymPy.
    # Aseguramos que se interpreten como multiplicación (ej. x * _dx_temp).
    # Usamos re.sub con una función de reemplazo para añadir el '*' si es necesario.

    # Primero, asegúrate de que haya un '*' antes de __DX__ o __DY__ si hay una variable o número
    # justo antes. Esto es crucial para la multiplicación implícita que SymPy necesita.
    temp_expr_str = re.sub(r'([a-zA-Z0-9)])\s*__DX__', r'\1*__dx_temp__', normalized_eq_str)
    temp_expr_str = re.sub(r'([a-zA-Z0-9)])\s*__DY__', r'\1*__dy_temp__', temp_expr_str)

    # Luego, reemplaza los marcadores remanentes (ej. si el término empieza con __DX__ o después de un operador)
    temp_expr_str = temp_expr_str.replace('__DX__', str(_dx_temp))
    temp_expr_str = temp_expr_str.replace('__DY__', str(_dy_temp))


    print(f"[DEBUG] Expression for sympify coefficient extraction: {temp_expr_str}")
    
    try:
        # Convertir la expresión a un objeto SymPy
        # Añadimos los símbolos temporales al namespace para sympify
        sym_expr = sp.sympify(temp_expr_str, locals={'x': x, 'y': y, 
                                                    'sin': sp.sin, 'cos': sp.cos, 
                                                    'tan': sp.tan, 'log': sp.log, 
                                                    'exp': sp.exp, 'pi': sp.pi, 
                                                    'sqrt': sp.sqrt,
                                                    str(_dx_temp): _dx_temp,
                                                    str(_dy_temp): _dy_temp})
        print(f"[DEBUG] Sympified expression: {sym_expr}")

        # Expandir la expresión para asegurar que los coeficientes se extraigan correctamente
        sym_expr = sp.expand(sym_expr)
        print(f"[DEBUG] Expanded expression: {sym_expr}")

        # Extraer los coeficientes de _dx_temp y _dy_temp
        M_sym = sp.simplify(sym_expr.coeff(_dx_temp, 1))
        N_sym = sp.simplify(sym_expr.coeff(_dy_temp, 1))
        
        # Convertir a cadena y asegurar que no haya marcadores temporales o símbolos de SymPy
        M_str_final = str(M_sym).replace(str(_dx_temp), '').replace(str(_dy_temp), '').strip()
        N_str_final = str(N_sym).replace(str(_dx_temp), '').replace(str(_dy_temp), '').strip()

        # Manejar el caso de que el coeficiente sea '0' en SymPy
        if M_sym == 0: M_str_final = '0'
        if N_sym == 0: N_str_final = '0'

        # Verificar si la ecuación tiene sentido
        if M_sym == 0 and N_sym == 0 and sym_expr != 0:
             # Si la expresión completa no es cero, pero los coeficientes son cero,
             # significa que no se encontraron términos con dx o dy.
             raise ValueError("La ecuación no parece tener términos dx o dy válidos.")

        print(f"[DEBUG] Extracted M_str: {M_str_final}, N_str: {N_str_final}")
        
        return M_str_final, N_str_final

    except Exception as e:
        print(f"[ERROR] Error in sympify during parse_differential_equation_from_full_string: {e}")
        raise ValueError(f"No se pudo parsear la ecuación diferencial compleja: '{equation_str}'. Error: {e}")


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