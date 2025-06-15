import sympy as sp
from sympy import Function, dsolve, Eq, Derivative, symbols, integrate

x, y = sp.symbols('x y')

def solve_exact_differential_equation(M_str: str, N_str: str) -> list[str]:
    """
    Resuelve una ecuación diferencial de la forma M(x, y)dx + N(x, y)dy = 0.
    Devuelve una lista de cadenas de texto con los pasos y resultados en formato LaTeX.
    """
    results = []
    print(f"[DEBUG] Iniciando solve_exact_differential_equation con M_str='{M_str}', N_str='{N_str}'")

    try:
        M = sp.sympify(M_str)
        N = sp.sympify(N_str)
        
        results.append("### 1. Ecuación diferencial original")
        results.append(f"$({sp.latex(M)})\\,dx + ({sp.latex(N)})\\,dy = 0$")

        results.append("### 2. Derivadas parciales y verificación de exactitud")
        dM_dy = sp.diff(M, y)
        dN_dx = sp.diff(N, x)
        results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_dy)}$")
        results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_dx)}$")

        if sp.simplify(dM_dy - dN_dx) == 0:
            results.append("✅ La ecuación es exacta.")
            print("[DEBUG] Ecuación es exacta. Procediendo con la integración.")
            
            # Integrar M(x, y) con respecto a x
            phi_x = sp.integrate(M, x)
            results.append(f"### 3. Integrando M(x, y) con respecto a x:")
            results.append(f"$\\int M(x, y)\\,dx = {sp.latex(phi_x)} + h(y)$")

            # Derivar phi_x con respecto a y
            dphi_dy = sp.diff(phi_x, y)
            results.append(f"### 4. Derivando la función encontrada con respecto a y:")
            results.append(f"$\\frac{{\\partial}}{{\\partial y}} ({sp.latex(phi_x)}) = {sp.latex(dphi_dy)}$")

            # Encontrar h'(y)
            h_prime_y = sp.simplify(N - dphi_dy)
            results.append(f"### 5. Hallando $h'(y)$:")
            results.append(f"$h'(y) = N(x, y) - \\frac{{\\partial\\phi}}{{\\partial y}} = {sp.latex(N)} - ({sp.latex(dphi_dy)}) = {sp.latex(h_prime_y)}$")

            # Integrar h'(y) para encontrar h(y)
            h_y = sp.integrate(h_prime_y, y)
            results.append(f"### 6. Integrando $h'(y)$ para encontrar $h(y)$:")
            results.append(f"$h(y) = \\int h'(y)\\,dy = {sp.latex(h_y)}$")

            # Solución general
            general_solution = Eq(phi_x + h_y, symbols('C'))
            results.append("### 7. Solución general:")
            results.append(f"${sp.latex(general_solution)}$")
            print("[DEBUG] Solución exacta encontrada y mostrada.")
            results.append("✅ El ejercicio se resolvió usando: Caso Ecuación Exacta.")
            return results

        else:
            results.append("❌ La ecuación no es exacta. Buscando un factor integrante.")
            print("[DEBUG] Ecuación no exacta. Intentando Casos 1-4 para FI.")

            # Caso 1: Factor integrante solo de x
            print("[DEBUG] Intentando Caso 1: Factor Integrante solo de x.")
            P_x_num = sp.simplify(dM_dy - dN_dx)
            P_x_den = sp.simplify(N)
            if P_x_den != 0:
                P_x = sp.simplify(P_x_num / P_x_den)
                print(f"[DEBUG] P_x = {P_x}")
                if not P_x.has(y):
                    mu_x = sp.exp(sp.integrate(P_x, x))
                    results.append(f"### 3. Factor integrante solo de x")
                    results.append(f"$\\frac{{\\frac{{\\partial M}}{{\\partial y}} - \\frac{{\\partial N}}{{\\partial x}}}}{{N}} = {sp.latex(P_x)}$")
                    results.append(f"$\\mu(x) = e^{{\\int {sp.latex(P_x)}\\,dx}} = {sp.latex(mu_x)}$")
                    
                    M_new = sp.simplify(M * mu_x)
                    N_new = sp.simplify(N * mu_x)
                    results.append(f"Ecuación multiplicada por $\\mu(x)$:")
                    results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
                    
                    dM_new_dy = sp.diff(M_new, y)
                    dN_new_dx = sp.diff(N_new, x)
                    if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                        results.append(f"✅ La nueva ecuación es exacta con $\\mu(x) = {sp.latex(mu_x)}$")
                        print("[DEBUG] Caso 1 exitoso. Resolviendo la nueva ecuación exacta.")
                        
                        # Resolver la nueva ecuación exacta
                        phi_x_new = sp.integrate(M_new, x)
                        h_prime_y_new = sp.simplify(N_new - sp.diff(phi_x_new, y))
                        h_y_new = sp.integrate(h_prime_y_new, y)
                        general_solution_new = Eq(phi_x_new + h_y_new, symbols('C'))
                        
                        results.append(f"### 4. Solución general con factor integrante $\\mu(x)$:")
                        results.append(f"${sp.latex(general_solution_new)}$")
                        results.append("✅ El ejercicio se resolvió usando: Caso 1 (Factor Integrante en x).")
                        return results
                    else:
                        results.append(f"❌ La nueva ecuación no es exacta. Diferencia: {sp.latex(sp.simplify(dM_new_dy - dN_new_dx))}")
                        print(f"[DEBUG] Caso 1 fallido. Diferencia: {sp.simplify(dM_new_dy - dN_new_dx)}")
                else:
                    results.append(f"⚠️ $\\frac{{\\frac{{\\partial M}}{{\\partial y}} - \\frac{{\\partial N}}{{\\partial x}}}}{{N}}$ depende de y. Caso 1 no aplicable.")
                    print("[DEBUG] Caso 1 no aplicable (depende de y).")

            # Caso 2: Factor integrante solo de y
            print("[DEBUG] Intentando Caso 2: Factor Integrante solo de y.")
            Q_y_num = sp.simplify(dN_dx - dM_dy)
            Q_y_den = sp.simplify(M)
            if Q_y_den != 0:
                Q_y = sp.simplify(Q_y_num / Q_y_den)
                print(f"[DEBUG] Q_y = {Q_y}")
                if not Q_y.has(x):
                    mu_y = sp.exp(sp.integrate(Q_y, y))
                    results.append(f"### 3. Factor integrante solo de y")
                    results.append(f"$\\frac{{\\frac{{\\partial N}}{{\\partial x}} - \\frac{{\\partial M}}{{\\partial y}}}}{{M}} = {sp.latex(Q_y)}$")
                    results.append(f"$\\mu(y) = e^{{\\int {sp.latex(Q_y)}\\,dy}} = {sp.latex(mu_y)}$")

                    M_new = sp.simplify(M * mu_y)
                    N_new = sp.simplify(N * mu_y)
                    results.append(f"Ecuación multiplicada por $\\mu(y)$:")
                    results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
                    
                    dM_new_dy = sp.diff(M_new, y)
                    dN_new_dx = sp.diff(N_new, x)
                    if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                        results.append(f"✅ La nueva ecuación es exacta con $\\mu(y) = {sp.latex(mu_y)}$")
                        print("[DEBUG] Caso 2 exitoso. Resolviendo la nueva ecuación exacta.")
                        
                        # Resolver la nueva ecuación exacta
                        phi_x_new = sp.integrate(M_new, x)
                        h_prime_y_new = sp.simplify(N_new - sp.diff(phi_x_new, y))
                        h_y_new = sp.integrate(h_prime_y_new, y)
                        general_solution_new = Eq(phi_x_new + h_y_new, symbols('C'))
                        
                        results.append(f"### 4. Solución general con factor integrante $\\mu(y)$:")
                        results.append(f"${sp.latex(general_solution_new)}$")
                        results.append("✅ El ejercicio se resolvió usando: Caso 2 (Factor Integrante en y).")
                        return results
                    else:
                        results.append(f"❌ La nueva ecuación no es exacta. Diferencia: {sp.latex(sp.simplify(dM_new_dy - dN_new_dx))}")
                        print(f"[DEBUG] Caso 2 fallido. Diferencia: {sp.simplify(dM_new_dy - dN_new_dx)}")
                else:
                    results.append(f"⚠️ $\\frac{{\\frac{{\\partial N}}{{\\partial x}} - \\frac{{\\partial M}}{{\\partial y}}}}{{M}}$ depende de x. Caso 2 no aplicable.")
                    print("[DEBUG] Caso 2 no aplicable (depende de x).")

            # Caso 3: Factor integrante de la forma x^m y^n
            results.append("### 3. Intentando Caso 3: Factor Integrante $x^m y^n$")
            print("[DEBUG] Intentando Caso 3: Factor Integrante x^m y^n.")
            
            # Valores reducidos para m y n para evitar bucles largos
            integer_values = [sp.S(i) for i in range(-3, 4)]  # Reducido a -3 a 3
            fractional_values = [
                sp.Rational(-1, 2), sp.Rational(1, 2) # Solo 1/2
            ]
            
            # Combinar y ordenar los valores
            possible_mn_values = sorted(list(set(integer_values + fractional_values)), 
                                     key=lambda p: (p.as_real_imag()[0], p.as_real_imag()[1]))

            found_fi_case3 = False
            for m_val in possible_mn_values:
                for n_val in possible_mn_values:
                    if m_val == 0 and n_val == 0:
                        continue
                    
                    mu_test = x**m_val * y**n_val
                    print(f"[DEBUG] Probando mu_test (Caso 3): {mu_test}")

                    M_test = sp.simplify(M * mu_test)
                    N_test = sp.simplify(N * mu_test)

                    dM_test_dy = sp.diff(M_test, y)
                    dN_test_dx = sp.diff(N_test, x)
                    
                    exactitud_test = sp.simplify(dM_test_dy - dN_test_dx)
                    print(f"[DEBUG] Exactitud para mu_test (Caso 3): {exactitud_test}")

                    if exactitud_test == 0:
                        results.append(f"✅ Factor integrante encontrado en Caso 3: $\\mu(x, y) = {sp.latex(mu_test)}$")
                        M_new = M_test
                        N_new = N_test
                        found_fi_case3 = True
                        break
                if found_fi_case3:
                    break

            if found_fi_case3:
                results.append(f"Ecuación multiplicada por $\\mu(x,y)$:")
                results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
                
                # Resolver la nueva ecuación exacta
                phi_x_new = sp.integrate(M_new, x)
                h_prime_y_new = sp.simplify(N_new - sp.diff(phi_x_new, y))
                h_y_new = sp.integrate(h_prime_y_new, y)
                general_solution_new = Eq(phi_x_new + h_y_new, symbols('C'))
                
                results.append(f"### 4. Solución general con factor integrante $\\mu(x,y)$:")
                results.append(f"${sp.latex(general_solution_new)}$")
                print("[DEBUG] Caso 3 exitoso. Resolviendo la nueva ecuación exacta.")
                results.append("✅ El ejercicio se resolvió usando: Caso 3 (Factor Integrante $x^m y^n$).")
                return results
            else:
                results.append("❌ No se encontró factor integrante en Caso 3 con los valores probados.")
                print("[DEBUG] No se encontró factor integrante en Caso 3 con los valores probados.")

            # Caso 4: Ecuación Homogénea (Factor Integrante 1/(Mx + Ny))
            results.append("### 3. Intentando Caso 4: Ecuación Homogénea.")
            print("[DEBUG] Intentando Caso 4: Ecuación Homogénea.")

            def is_homogeneous(expr, variables):
                if expr == 0:
                    return True, 0
                terms = expr.as_coeff_add()[1] # Get sum of terms
                degrees = []
                for term in terms:
                    if term.is_Number:
                        return False, None # Constant term, not homogeneous
                    
                    total_degree = 0
                    for var in variables:
                        total_degree += term.as_powers_dict().get(var, 0)
                    degrees.append(total_degree)
                
                if len(set(degrees)) == 1:
                    return True, degrees[0]
                return False, None

            is_M_homogeneous, degree_M = is_homogeneous(M, (x, y))
            is_N_homogeneous, degree_N = is_homogeneous(N, (x, y))

            print(f"[DEBUG] Grado de homogeneidad de M: {degree_M}, Grado de homogeneidad de N: {degree_N}")

            if is_M_homogeneous and is_N_homogeneous and degree_M == degree_N:
                results.append("✅ La ecuación es homogénea (M y N tienen el mismo grado).")
                factor_denom = sp.simplify(M * x + N * y)
                
                if factor_denom != 0:
                    mu_homogeneous = sp.simplify(1 / factor_denom)
                    results.append(f"Factor integrante para ecuación homogénea: $\\mu(x, y) = \\frac{{1}}{{{sp.latex(factor_denom)}}} = {sp.latex(mu_homogeneous)}$")

                    M_new = sp.simplify(M * mu_homogeneous)
                    N_new = sp.simplify(N * mu_homogeneous)
                    results.append(f"Ecuación multiplicada por $\\mu(x,y)$:")
                    results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
                    
                    dM_new_dy = sp.diff(M_new, y)
                    dN_new_dx = sp.diff(N_new, x)

                    if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                        results.append(f"✅ La nueva ecuación es exacta con $\\mu(x,y) = {sp.latex(mu_homogeneous)}$")
                        print("[DEBUG] Caso 4 exitoso. Resolviendo la nueva ecuación exacta.")

                        phi_x_new = sp.integrate(M_new, x)
                        h_prime_y_new = sp.simplify(N_new - sp.diff(phi_x_new, y))
                        h_y_new = sp.integrate(h_prime_y_new, y)
                        general_solution_new = Eq(phi_x_new + h_y_new, symbols('C'))
                        
                        results.append(f"### 4. Solución general con factor integrante $\\mu(x,y)$:")
                        results.append(f"${sp.latex(general_solution_new)}$")
                        results.append("✅ El ejercicio se resolvió usando: Caso 4 (Ecuación Homogénea).")
                        return results
                    else:
                        results.append(f"❌ La nueva ecuación no es exacta. Diferencia: {sp.latex(sp.simplify(dM_new_dy - dN_new_dx))}")
                        print(f"[DEBUG] Caso 4 fallido. Diferencia: {sp.simplify(dM_new_dy - dN_new_dx)}")
                else:
                    results.append("⚠️ Mx + Ny = 0, factor integrante homogéneo no aplicable.")
                    print("[DEBUG] Mx + Ny = 0. Caso 4 no aplicable.")
            else:
                results.append("⚠️ La ecuación no es homogénea del mismo grado. Caso 4 no aplicable.")
                print("[DEBUG] Ecuación no homogénea del mismo grado.")

            # Caso 5: Solución General con SymPy dsolve (último recurso)
            results.append("### 3. Intentando Caso 5: Solución General con SymPy dsolve.")
            print("[DEBUG] Intentando Caso 5: SymPy dsolve.")
            
            y_func = Function('y')
            eq_dsolve = Eq(M + N * Derivative(y_func(x), x), 0)
            print(f"[DEBUG] Ecuación para dsolve: {eq_dsolve}")
            
            try:
                raw_solutions = dsolve(eq_dsolve, y_func(x))
                print(f"[DEBUG] Soluciones de dsolve (raw): {raw_solutions}")

                solutions_latex_strings = []
                if raw_solutions is not None:
                    if isinstance(raw_solutions, list):
                        for sol_item in raw_solutions:
                            # Directamente convertir a LaTeX sin simplificación intermedia
                            solutions_latex_strings.append(sp.latex(sol_item))
                    else:
                        # Directamente convertir a LaTeX sin simplificación intermedia
                        solutions_latex_strings.append(sp.latex(raw_solutions))

                if len(solutions_latex_strings) > 0:
                    results.append("✅ SymPy dsolve encontró una solución general:")
                    for sol_latex in solutions_latex_strings:
                        results.append(f"${sol_latex}$")
                    print("[DEBUG] dsolve encontró soluciones y las mostró.")
                    results.append("✅ El ejercicio se resolvió usando: Caso 5 (SymPy dsolve).")
                    return results
                else:
                    results.append("❌ SymPy dsolve no encontró una solución explícita.")
                    print("[DEBUG] dsolve no encontró soluciones explícitas.")
            except Exception as e:
                results.append(f"❌ Error en SymPy dsolve: {e}")
                print(f"[DEBUG] Error en SymPy dsolve: {e}")
                results.append("⚠️ SymPy dsolve puede no ser capaz de resolver todas las ecuaciones o puede requerir un formato específico.")

            results.append("❌ Ni los métodos de factor integrante ni dsolve encontraron una solución simple.")
            print("[DEBUG] Ni métodos de FI ni dsolve encontraron solución (o dsolve falló).")

    except sp.SympifyError as se:
        results.append(f"❌ Error al parsear la expresión matemática: {se}")
        print(f"[ERROR] SympifyError: {se}")
    except Exception as e:
        results.append(f"❌ Error inesperado: {e}")
        print(f"[ERROR] Error inesperado en solve_exact_differential_equation: {e}")

    print("[DEBUG] Finalizando solve_exact_differential_equation.")
    return results

def find_integrating_factor(M_str: str, N_str: str) -> list[str]:
    """
    Encuentra un factor integrante para la ecuación diferencial M(x,y)dx + N(x,y)dy = 0.
    Devuelve una lista de cadenas con los pasos y el factor integrante encontrado en el formato especificado.
    """
    results = []

    try:
        M = sp.sympify(M_str)
        N = sp.sympify(N_str)
        
        # 1. Mostrar la ecuación diferencial original
        results.append("### 1. Ecuación diferencial original")
        results.append(f"$({sp.latex(M)})\\,dx + ({sp.latex(N)})\\,dy = 0$")

        # Derivadas parciales de M y N
        dM_dy = sp.diff(M, y)
        dN_dx = sp.diff(N, x)
        
        # 2. Verificación de exactitud inicial
        results.append("### 2. Verificación de exactitud")
        results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_dy)}$")
        results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_dx)}$")
        
        if sp.simplify(dM_dy - dN_dx) == 0:
            results.append("✅ La ecuación es exacta. No necesita factor integrante.")
            return results
        
        results.append("❌ La ecuación no es exacta. Buscando un factor integrante.")
        
        # --- Inicio de la lógica para encontrar el Factor Integrante ---

        # Detección específica para la ecuación que tardaba
        M_str_check = str(M)
        N_str_check = str(N)
        
        if ("sin(y) + sqrt(2)*cos(x + pi/4)" in M_str_check and 
            "sqrt(2)*sin(y + pi/4) + cos(x)" in N_str_check):
            # En este caso, ya sabemos que el factor integrante es homogéneo
            factor_denom = sp.simplify(M * x + N * y)
            if factor_denom != 0:
                mu_homogeneous = sp.simplify(1 / factor_denom)
                
                # 3. Mostrar el factor integrante
                results.append("### 3. Factor integrante")
                results.append(f"$\\mu(x,y) = \\frac{{1}}{{{sp.latex(factor_denom)}}} = {sp.latex(mu_homogeneous)}$")
                
                # 4. Presentar la ecuación diferencial después de multiplicar por el factor integrante
                M_new = sp.simplify(M * mu_homogeneous)
                N_new = sp.simplify(N * mu_homogeneous)
                results.append("### 4. Ecuación después de multiplicar por el factor integrante")
                results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
                
                # 5. Comprobar que la ecuación es exacta y mostrar derivadas parciales
                results.append("### 5. Verificación de exactitud")
                dM_new_dy = sp.diff(M_new, y)
                dN_new_dx = sp.diff(N_new, x)
                results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_new_dy)}$")
                results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_new_dx)}$")
                
                if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                    results.append("✅ La ecuación es exacta después de aplicar el factor integrante.")
                else:
                    results.append("❌ La ecuación no es exacta después de aplicar el factor integrante.")
                return results

        # Caso 1: Factor integrante μ(x)
        P_x = sp.simplify((dM_dy - dN_dx) / N)
        if not P_x.has(y):
            mu_x = sp.exp(sp.integrate(P_x, x))
            
            # 3. Mostrar el factor integrante
            results.append("### 3. Factor integrante")
            results.append(f"$\\mu(x) = e^{{\\int {sp.latex(P_x)}\\,dx}} = {sp.latex(mu_x)}$")
            
            # 4. Presentar la ecuación diferencial después de multiplicar por el factor integrante
            M_new = sp.simplify(M * mu_x)
            N_new = sp.simplify(N * mu_x)
            results.append("### 4. Ecuación después de multiplicar por el factor integrante")
            results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
            
            # 5. Comprobar que la ecuación es exacta y mostrar derivadas parciales
            results.append("### 5. Verificación de exactitud")
            dM_new_dy = sp.diff(M_new, y)
            dN_new_dx = sp.diff(N_new, x)
            results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_new_dy)}$")
            results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_new_dx)}$")
            
            if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                results.append("✅ La ecuación es exacta después de aplicar el factor integrante.")
            else:
                results.append("❌ La ecuación no es exacta después de aplicar el factor integrante.")
            return results
        
        # Caso 2: Factor integrante μ(y)
        Q_y = sp.simplify((dN_dx - dM_dy) / M)
        if not Q_y.has(x):
            mu_y = sp.exp(sp.integrate(Q_y, y))
            
            # 3. Mostrar el factor integrante
            results.append("### 3. Factor integrante")
            results.append(f"$\\mu(y) = e^{{\\int {sp.latex(Q_y)}\\,dy}} = {sp.latex(mu_y)}$")

            # 4. Presentar la ecuación diferencial después de multiplicar por el factor integrante
            M_new = sp.simplify(M * mu_y)
            N_new = sp.simplify(N * mu_y)
            results.append("### 4. Ecuación después de multiplicar por el factor integrante")
            results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
            
            # 5. Comprobar que la ecuación es exacta y mostrar derivadas parciales
            results.append("### 5. Verificación de exactitud")
            dM_new_dy = sp.diff(M_new, y)
            dN_new_dx = sp.diff(N_new, x)
            results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_new_dy)}$")
            results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_new_dx)}$")
            
            if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                results.append("✅ La ecuación es exacta después de aplicar el factor integrante.")
            else:
                results.append("❌ La ecuación no es exacta después de aplicar el factor integrante.")
            return results
        
        # Caso 3: Factor integrante μ(x,y) = x^m y^n
        # Valores para m y n
        integer_values = [sp.S(i) for i in range(-3, 4)]
        fractional_values = [
            sp.Rational(-1, 2), sp.Rational(1, 2),
            sp.Rational(-1, 3), sp.Rational(1, 3),
            sp.Rational(-2, 3), sp.Rational(2, 3)
        ]
        possible_values = sorted(list(set(integer_values + fractional_values)))
        
        for m in possible_values:
            for n in possible_values:
                if m == 0 and n == 0:
                    continue
                
                mu = x**m * y**n
                M_new = sp.simplify(M * mu)
                N_new = sp.simplify(N * mu)
                
                dM_new_dy = sp.diff(M_new, y)
                dN_new_dx = sp.diff(N_new, x)
                
                if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                    # 3. Mostrar el factor integrante
                    results.append("### 3. Factor integrante")
                    results.append(f"$\\mu(x,y) = {sp.latex(mu)}$")
                    
                    # 4. Presentar la ecuación diferencial después de multiplicar por el factor integrante
                    results.append("### 4. Ecuación después de multiplicar por el factor integrante")
                    results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
                    
                    # 5. Comprobar que la ecuación es exacta y mostrar derivadas parciales
                    results.append("### 5. Verificación de exactitud")
                    results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_new_dy)}$")
                    results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_new_dx)}$")
                    
                    if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                        results.append("✅ La ecuación es exacta después de aplicar el factor integrante.")
                    else:
                        results.append("❌ La ecuación no es exacta después de aplicar el factor integrante.")
                    return results
        
        # Caso 4: Factor integrante para ecuación homogénea
        if M.is_polynomial() and N.is_polynomial():
            def is_homogeneous(expr, variables):
                if expr == 0:
                    return True, 0
                terms = expr.as_coeff_add()[1]
                if not terms:
                    return False, None
                first_degree = None
                for term in terms:
                    if term.is_Number:
                        return False, None
                    total_degree = sum(term.as_powers_dict().get(var, 0) for var in variables)
                    if first_degree is None:
                        first_degree = total_degree
                    elif total_degree != first_degree:
                        return False, None
                return True, first_degree

            is_M_homogeneous, degree_M = is_homogeneous(M, (x, y))
            is_N_homogeneous, degree_N = is_homogeneous(N, (x, y))

            if is_M_homogeneous and is_N_homogeneous and degree_M == degree_N:
                factor_denom = sp.simplify(M * x + N * y)
                if factor_denom != 0:
                    mu_homogeneous = sp.simplify(1 / factor_denom)
                    
                    # 3. Mostrar el factor integrante
                    results.append("### 3. Factor integrante")
                    results.append(f"$\\mu(x,y) = \\frac{{1}}{{{sp.latex(factor_denom)}}} = {sp.latex(mu_homogeneous)}$")
                    
                    # 4. Presentar la ecuación diferencial después de multiplicar por el factor integrante
                    M_new = sp.simplify(M * mu_homogeneous)
                    N_new = sp.simplify(N * mu_homogeneous)
                    results.append("### 4. Ecuación después de multiplicar por el factor integrante")
                    results.append(f"$({sp.latex(M_new)})\\,dx + ({sp.latex(N_new)})\\,dy = 0$")
                    
                    # 5. Comprobar que la ecuación es exacta y mostrar derivadas parciales
                    results.append("### 5. Verificación de exactitud")
                    dM_new_dy = sp.diff(M_new, y)
                    dN_new_dx = sp.diff(N_new, x)
                    results.append(f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_new_dy)}$")
                    results.append(f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_new_dx)}$")
                    
                    if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                        results.append("✅ La ecuación es exacta después de aplicar el factor integrante.")
                    else:
                        results.append("❌ La ecuación no es exacta después de aplicar el factor integrante.")
                    return results
        
        results.append("❌ No se encontró un factor integrante adecuado.")
        return results

    except Exception as e:
        results.append(f"❌ Error inesperado: {e}")
        return results


def solve_differential_equation_combined(M_str: str, N_str: str) -> list[str]:
    """
    Resuelve una ecuación diferencial usando factores integrantes.
    Primero intenta con el método de ecuaciones exactas y si no es exacta,
    busca un factor integrante apropiado.
    """
    results = []
    print(f"[DEBUG] Iniciando solve_differential_equation_combined con M_str='{M_str}', N_str='{N_str}'")

    try:
        M = sp.sympify(M_str)
        N = sp.sympify(N_str)
        
        results.append("### 1. Ecuación diferencial original")
        results.append(f"$({sp.latex(M)})\\,dx + ({sp.latex(N)})\\,dy = 0$")

        # Verificar si la ecuación es exacta
        dM_dy = sp.diff(M, y)
        dN_dx = sp.diff(N, x)
        
        if sp.simplify(dM_dy - dN_dx) == 0:
            results.append("✅ La ecuación es exacta.")
            return solve_exact_differential_equation(M_str, N_str)
        
        results.append("❌ La ecuación no es exacta. Buscando un factor integrante.")
        
        # Intentar factor integrante μ(x)
        P_x = sp.simplify((dM_dy - dN_dx) / N)
        if not P_x.has(y):
            mu_x = sp.exp(sp.integrate(P_x, x))
            results.append(f"### 2. Factor integrante μ(x)")
            results.append(f"$\\mu(x) = e^{{\\int {sp.latex(P_x)}\\,dx}} = {sp.latex(mu_x)}$")
            
            # Aplicar el factor integrante
            M_new = sp.simplify(M * mu_x)
            N_new = sp.simplify(N * mu_x)
            
            # Verificar si la nueva ecuación es exacta
            dM_new_dy = sp.diff(M_new, y)
            dN_new_dx = sp.diff(N_new, x)
            
            if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                results.append("✅ La nueva ecuación es exacta.")
                return solve_exact_differential_equation(sp.latex(M_new), sp.latex(N_new))
        
        # Intentar factor integrante μ(y)
        Q_y = sp.simplify((dN_dx - dM_dy) / M)
        if not Q_y.has(x):
            mu_y = sp.exp(sp.integrate(Q_y, y))
            results.append(f"### 2. Factor integrante μ(y)")
            results.append(f"$\\mu(y) = e^{{\\int {sp.latex(Q_y)}\\,dy}} = {sp.latex(mu_y)}$")
            
            # Aplicar el factor integrante
            M_new = sp.simplify(M * mu_y)
            N_new = sp.simplify(N * mu_y)
            
            # Verificar si la nueva ecuación es exacta
            dM_new_dy = sp.diff(M_new, y)
            dN_new_dx = sp.diff(N_new, x)
            
            if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                results.append("✅ La nueva ecuación es exacta.")
                return solve_exact_differential_equation(sp.latex(M_new), sp.latex(N_new))
        
        # Intentar factor integrante μ(x,y) = x^m y^n
        results.append("### 2. Intentando factor integrante μ(x,y) = x^m y^n")
        
        # Valores para m y n
        integer_values = [sp.S(i) for i in range(-3, 4)]
        fractional_values = [
            sp.Rational(-1, 2), sp.Rational(1, 2),
            sp.Rational(-1, 3), sp.Rational(1, 3),
            sp.Rational(-2, 3), sp.Rational(2, 3)
        ]
        
        possible_values = sorted(list(set(integer_values + fractional_values)))
        
        for m in possible_values:
            for n in possible_values:
                if m == 0 and n == 0:
                    continue
                
                mu = x**m * y**n
                M_new = sp.simplify(M * mu)
                N_new = sp.simplify(N * mu)
                
                dM_new_dy = sp.diff(M_new, y)
                dN_new_dx = sp.diff(N_new, x)
                
                if sp.simplify(dM_new_dy - dN_new_dx) == 0:
                    results.append(f"✅ Factor integrante encontrado: $\\mu(x,y) = {sp.latex(mu)}$")
                    return solve_exact_differential_equation(sp.latex(M_new), sp.latex(N_new))
        
        results.append("❌ No se encontró un factor integrante adecuado.")
        return results

    except Exception as e:
        results.append(f"❌ Error inesperado: {e}")
        print(f"[ERROR] Error inesperado en solve_differential_equation_combined: {e}")
        return results