import sympy as sp

x, y = sp.symbols('x y')

def solve_exact_differential_equation(M_str: str, N_str: str) -> list[str]:
    """
    Resuelve una ecuación diferencial de la forma M(x, y)dx + N(x, y)dy = 0.
    Devuelve una lista de cadenas de texto con los pasos y resultados en formato LaTeX.
    """
    results = []
    try:
        M = sp.sympify(M_str)
        N = sp.sympify(N_str)
        
        results.append("### 1. Ecuación diferencial original")
        results.append(f"$({sp.latex(M)})\,dx + ({sp.latex(N)})\,dy = 0$")

        results.append("### 2. Derivadas parciales y verificación de exactitud")
        dM_dy = sp.diff(M, y)
        dN_dx = sp.diff(N, x)
        results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_dy)}$")
        results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_dx)}$")
        
        if sp.simplify(dM_dy - dN_dx) == 0:
            results.append("✅ La ecuación es exacta.")
        else:
            results.append("❌ La ecuación NO es exacta.")
            results.append("### 3. Búsqueda de factor integrante")
            
            mu_found = False

            # Caso 1: Factor integrante función de x (según tu imagen)
            # Si (My - Nx) / N es función solamente de x
            p_x_candidate = sp.simplify((dM_dy - dN_dx) / N)
            if p_x_candidate.free_symbols <= {x}:
                mu = sp.exp(sp.integrate(p_x_candidate, x))
                results.append(f"**Caso 1:** Factor integrante dependiente de x: $\\mu(x) = {sp.latex(mu)}$")
                mu_found = True
            
            # Caso 2: Factor integrante función de y (según tu imagen)
            # Si (Nx - My) / M es función solamente de y
            elif (p_y_candidate := sp.simplify((dN_dx - dM_dy) / M)).free_symbols <= {y}:
                mu = sp.exp(sp.integrate(p_y_candidate, y))
                results.append(f"**Caso 2:** Factor integrante dependiente de y: $\\mu(y) = {sp.latex(mu)}$")
                mu_found = True
            
            # Caso 3: Factor integrante de la forma x^m y^n
            elif not mu_found:
                results.append("**Caso 3:** Factor integrante de la forma $\\mu(x,y) = x^m y^n$")
                m, n = sp.symbols('m n')
                
                # M_prime = M * x**m * y**n
                # N_prime = N * x**m * y**n
                # Condición de exactitud: d(M_prime)/dy = d(N_prime)/dx
                # Esto lleva a: (My - Nx) = m*N/x - n*M/y  (después de dividir por x^m y^n)
                # O lo que es lo mismo: (My - Nx) - m*N/x + n*M/y = 0
                
                equation_for_mn_display = sp.Eq(dM_dy - dN_dx, m*N/x - n*M/y)
                results.append(f"Ecuación a resolver para m y n (deriva de $\\frac{{\\partial (M x^m y^n)}}{{\\partial y}} = \\frac{{\\partial (N x^m y^n)}}{{\\partial x}}$): ${sp.latex(equation_for_mn_display)}$")

                equation_for_mn_solve = sp.simplify((dM_dy - dN_dx) - m*N/x + n*M/y)
                results.append(f"Intentando resolver: ${sp.latex(equation_for_mn_solve)} = 0$")
                
                solutions = sp.solve(equation_for_mn_solve, (m, n))
                
                if solutions and isinstance(solutions, dict) and m in solutions and n in solutions:
                    m_val = solutions[m]
                    n_val = solutions[n]

                    if m_val.is_number and n_val.is_number:
                        mu = x**m_val * y**n_val
                        results.append(f"Se encontraron soluciones: $m = {sp.latex(m_val)}$, $n = {sp.latex(n_val)}$")
                        results.append(f"Factor integrante encontrado: $\\mu(x,y) = x^{{ {sp.latex(m_val)} }} y^{{ {sp.latex(n_val)} }}$")
                        mu_found = True
                    else:
                        results.append(f"SymPy encontró soluciones simbólicas para m y n: $m={sp.latex(m_val)}$, $n={sp.latex(n_val)}$. No es una solución numérica simple para este caso.")
                else:
                    results.append("SymPy no encontró soluciones numéricas simples para m y n.")

            if mu_found:
                results.append("### 4. Ecuación multiplicada por el factor integrante")
                M_new = sp.simplify(mu * M)
                N_new = sp.simplify(mu * N)
                results.append(f"${sp.latex(M_new)}\,dx + {sp.latex(N_new)}\,dy = 0$")
                results.append("### 5. Derivadas parciales de la nueva ecuación y verificación de exactitud")
                dM_new_dy = sp.diff(M_new, y)
                dN_new_dx = sp.diff(N_new, x)
                if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                    # Si son iguales, mostrar la forma expandida para que se vea claro
                    simplified_partial_deriv = sp.expand(dM_new_dy) # O dN_new_dx, serán iguales
                    results.append(f"$\\frac{{\\partial M_{{nuevo}}}}{{\\partial y}} = {sp.latex(simplified_partial_deriv)}$")
                    results.append(f"$\\frac{{\\partial N_{{nuevo}}}}{{\\partial x}} = {sp.latex(simplified_partial_deriv)}$")
                    results.append("✅ La nueva ecuación ES exacta con el factor integrante.")
                else:
                    # Si no son iguales, mostrar las expresiones originales como estaban
                    results.append(f"$\\frac{{\\partial M_{{nuevo}}}}{{\\partial y}} = {sp.latex(dM_new_dy)}$")
                    results.append(f"$\\frac{{\\partial N_{{nuevo}}}}{{\\partial x}} = {sp.latex(dN_new_dx)}$")
                    results.append("❌ La nueva ecuación NO es exacta con el factor integrante.")
            else:
                results.append("⚠️ No se pudo encontrar un factor integrante simple dependiente solo de x o y (Casos 1 y 2). El Caso 3 (\\(x^m y^n\\)) no arrojó una solución simple para m y n.\n")
    except Exception as e:
        results.append(f"Error: {str(e)}")
    return results 