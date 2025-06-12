import sympy as sp

def integrating_factor_mn(M_str: str, N_str: str):
    x, y, m, n = sp.symbols('x y m n')
    M = sp.sympify(M_str)
    N = sp.sympify(N_str)

    dM_dy = sp.diff(M, y)
    dN_dx = sp.diff(N, x)
    eq = sp.simplify((dM_dy - dN_dx) - m*N/x + n*M/y)

    steps = []
    steps.append("Ecuación planteada para encontrar m y n:")
    steps.append(f"(My - Nx) - m(N/x) + n(M/y) = {sp.latex(eq)}")

    try:
        sol = sp.solve(eq, (m, n), dict=True)
        if sol:
            m_val = sol[0].get(m)
            n_val = sol[0].get(n)
            mu = x**m_val * y**n_val
            steps.append(f"✅ Se encontraron valores: m = {m_val}, n = {n_val}")
            steps.append(f"Factor integrante: mu(x, y) = {sp.latex(mu)}")
            return mu, steps
        else:
            steps.append("❌ No se encontraron soluciones simples para m y n.")
            return None, steps
    except Exception as e:
        steps.append(f"⚠️ Error al resolver: {str(e)}")
        return None, steps
