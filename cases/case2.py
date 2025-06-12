import sympy as sp

def integrating_factor_y(M_str: str, N_str: str):
    x, y = sp.symbols('x y')
    M = sp.sympify(M_str)
    N = sp.sympify(N_str)

    dM_dy = sp.diff(M, y)
    dN_dx = sp.diff(N, x)
    expr = sp.simplify((dN_dx - dM_dy) / M)

    steps = []
    steps.append(f"Verificando si (Nx - My)/M depende solo de y: {expr}")

    if expr.free_symbols <= {y}:
        mu = sp.exp(sp.integrate(expr, y))
        steps.append(f"✅ Depende solo de y. Factor integrante: mu(y) = {sp.latex(mu)}")
        return mu, steps
    else:
        steps.append("❌ No depende solo de y. Este caso no aplica.")
        return None, steps
