import sympy as sp

def integrating_factor_x(M_str: str, N_str: str):
    x, y = sp.symbols('x y')
    M = sp.sympify(M_str)
    N = sp.sympify(N_str)

    dM_dy = sp.diff(M, y)
    dN_dx = sp.diff(N, x)
    expr = sp.simplify((dM_dy - dN_dx) / N)

    steps = []
    steps.append(f"Verificando si (My - Nx)/N depende solo de x: {expr}")

    if expr.free_symbols <= {x}:
        mu = sp.exp(sp.integrate(expr, x))
        steps.append(f"✅ Depende solo de x. Factor integrante: mu(x) = {sp.latex(mu)}")
        return mu, steps
    else:
        steps.append("❌ No depende solo de x. Este caso no aplica.")
        return None, steps