# Solver.py  (extended for simple supported, cantilever and fixed-fixed beams)
import numpy as np

def solve_simple_beam(beam_length, A, B,
                      pointloads_in=None,
                      distributedloads_in=None,
                      momentloads_in=None,
                      triangleloads_in=None,
                      divisions=10000):
    """
    Pin at A, Roller at B (statically determinate simply-supported beam).
    Returns X_Field, SF, BM, [Va, Ha, Vb]
    """
    # Discretization
    Delta = beam_length / divisions
    X_Field = np.arange(0, beam_length + Delta, Delta)

    # Reaction forces: vertical at A and B
    # Sum vertical loads = Va + Vb
    # Sum moments about A = Vb*(B-A) - sum(Fy_i * (pos_i - A)) - sum(M_i) = 0
    F_sum = 0.0
    M_A = 0.0
    # point loads
    if pointloads_in:
        for pos, Fx, Fy in pointloads_in:
            F_sum += Fy
            M_A += Fy * (pos - A)
    # UDL
    if distributedloads_in:
        for start, end, w in distributedloads_in:
            L = end - start
            F = w * L
            x_cent = (start + end) / 2
            F_sum += F
            M_A += F * (x_cent - A)
    # moments
    if momentloads_in:
        for pos, M in momentloads_in:
            M_A += M
    # Solve
    Vb = M_A / (B - A)
    Va = F_sum - Vb
    Ha = 0.0  # horizontal not handled here

    # Build shear force (SF) and bending moment (BM)
    SF = np.zeros_like(X_Field)
    BM = np.zeros_like(X_Field)

    # Superpose reactions
    for i, x in enumerate(X_Field):
        if x >= A:
            SF[i] += Va
            BM[i] += Va * (x - A)
        if x >= B:
            SF[i] -= Vb
            BM[i] -= Vb * (x - B)

    # Superpose point loads
    if pointloads_in:
        for pos, Fx, Fy in pointloads_in:
            for i, x in enumerate(X_Field):
                if x >= pos:
                    SF[i] -= Fy
                    BM[i] -= Fy * (x - pos)
    # Superpose UDLs
    if distributedloads_in:
        for start, end, w in distributedloads_in:
            for i, x in enumerate(X_Field):
                if x >= start:
                    x_eff = min(x, end) - start
                    SF[i] -= w * x_eff
                    BM[i] -= w * x_eff * (x - start - x_eff/2)
    # Superpose moments
    if momentloads_in:
        for pos, M in momentloads_in:
            for i, x in enumerate(X_Field):
                if x >= pos:
                    BM[i] -= M

    return X_Field, SF, BM, [Va, Ha, Vb]

# Cantilever (fixed at A, free at B)
def solve_cantilever(beam_length, A,
                     pointloads_in=None,
                     distributedloads_in=None,
                     momentloads_in=None,
                     divisions=10000):
    """
    Fixed support at A: unknown shear Va and moment Ma.
    Free at B: no reactions.
    Returns X_Field, SF, BM, [Va, Ma]
    """
    Delta = beam_length / divisions
    X_Field = np.arange(0, beam_length + Delta, Delta)

    # Compute reaction via equilibrium
    V_total = 0.0
    M_total = 0.0
    if pointloads_in:
        for pos, Fx, Fy in pointloads_in:
            V_total += Fy
            M_total += Fy * (pos - A)
    if distributedloads_in:
        for start, end, w in distributedloads_in:
            L = end - start
            F = w * L
            x_bar = (start + end) / 2
            V_total += F
            M_total += F * (x_bar - A)
    if momentloads_in:
        for pos, M in momentloads_in:
            M_total += M
    Va = V_total
    Ma = M_total

    SF = np.zeros_like(X_Field)
    BM = np.zeros_like(X_Field)

    # Superpose fixed reactions at A
    for i, x in enumerate(X_Field):
        if x >= A:
            SF[i] += Va
            BM[i] += Ma + Va * (x - A)

    # Superpose point loads
    if pointloads_in:
        for pos, Fx, Fy in pointloads_in:
            for i, x in enumerate(X_Field):
                if x >= pos:
                    SF[i] -= Fy
                    BM[i] -= Fy * (x - pos)
    # Superpose UDLs
    if distributedloads_in:
        for start, end, w in distributedloads_in:
            for i, x in enumerate(X_Field):
                if x >= start:
                    x_eff = min(x, end) - start
                    SF[i] -= w * x_eff
                    BM[i] -= w * x_eff * (x - start - x_eff/2)
    # Superpose moments
    if momentloads_in:
        for pos, M in momentloads_in:
            for i, x in enumerate(X_Field):
                if x >= pos:
                    BM[i] -= M

    return X_Field, SF, BM, [Va, Ma]

# Fixed-Fixed (fixed supports at A and B)
def solve_fixed_fixed(beam_length, A, B,
                      pointloads_in=None,
                      distributedloads_in=None,
                      momentloads_in=None,
                      divisions=10000):
    """
    Fixed at A and B: unknown Va, Vb, Ma.
    Returns X_Field, SF, BM, [Va, Vb, Ma]
    """
    Delta = beam_length / divisions
    X_Field = np.arange(0, beam_length + Delta, Delta)

    # Equilibrium sums
    F_sum = 0.0
    M_A = 0.0
    M_B = 0.0
    if pointloads_in:
        for pos, Fx, Fy in pointloads_in:
            F_sum += Fy
            M_A += Fy * (pos - A)
            M_B += Fy * (B - pos)
    if distributedloads_in:
        for start, end, w in distributedloads_in:
            L = end - start
            F = w * L
            x_cent = (start + end) / 2
            F_sum += F
            M_A += F * (x_cent - A)
            M_B += F * (B - x_cent)
    if momentloads_in:
        for pos, M in momentloads_in:
            M_A += M
            M_B += M
    # Solve 3x3: [Va, Vb, Ma]
    K = np.array([[1, 1, 0],
                  [0, (B - A), 1],
                  [(B - A), 0, 1]], dtype=float)
    b = np.array([F_sum, M_A, M_B], dtype=float)
    Va, Vb, Ma = np.linalg.solve(K, b)

    SF = np.zeros_like(X_Field)
    BM = np.zeros_like(X_Field)

    # Reactions superposition
    for i, x in enumerate(X_Field):
        if x >= A:
            SF[i] += Va
            BM[i] += Va * (x - A) + Ma
        if x >= B:
            SF[i] += Vb
            BM[i] += Vb * (x - B)
    # Point loads
    if pointloads_in:
        for pos, Fx, Fy in pointloads_in:
            for i, x in enumerate(X_Field):
                if x >= pos:
                    SF[i] -= Fy
                    BM[i] -= Fy * (x - pos)
    # UDLs
    if distributedloads_in:
        for start, end, w in distributedloads_in:
            for i, x in enumerate(X_Field):
                if x >= start:
                    x_eff = min(x, end) - start
                    SF[i] -= w * x_eff
                    BM[i] -= w * x_eff * (x - start - x_eff/2)
    # Moments
    if momentloads_in:
        for pos, M in momentloads_in:
            for i, x in enumerate(X_Field):
                if x >= pos:
                    BM[i] -= M

    return X_Field, SF, BM, [Va, Vb, Ma]
