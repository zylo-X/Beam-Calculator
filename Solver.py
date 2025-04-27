# solvers.py
# --------------------------------------------------------------------------------
#           Libraries
# --------------------------------------------------------------------------------

import numpy as np

# --------------------------------------------------------------------------------
#         Load Definitions (Testing Values - Later Will be User Inputs)
# --------------------------------------------------------------------------------

# --- Point Loads: [Position (m), X-Force (kN), Y-Force (kN)] ---
pointloads = np.array([[1, 2, 3],
                       [4, 6, 7]])

# --- Uniform Distributed Loads: [Start (m), End (m), Intensity (kN/m)] ---
distributedloads = np.array([[1.2, 5.2, -2]])

# --- Triangular Distributed Loads: [Start (m), End (m), Start Intensity (kN/m), End Intensity (kN/m)] ---
Triangleloads = np.empty((0, 4))  # (Fixed: Safer empty array shape)

# --- Point Moments: [Position (m), Magnitude (kNm)] ---
momentloads = np.array([[3.2, -8]])

# --- Load Presence Flags ---
Test_pointloads = len(pointloads[0])
Test_momentloads = len(momentloads[0])
Test_UDLs = len(distributedloads[0])
Test_TRLs = len(Triangleloads[0])

# --------------------------------------------------------------------------------
#         Solver Initialization Functions
# --------------------------------------------------------------------------------

def initialize_solver(beam_length, divisions=10000):
    """
    Initialize the solver with beam length and number of divisions.
    """
    Delta = beam_length / divisions
    X_Field = np.arange(0, beam_length + Delta, Delta)  # Discretized beam length
    return X_Field, Delta

def initialize_containers(X_Field):
    """
    Initialize containers for storing results during calculations.
    """
    Reactions = np.array([0.0, 0.0, 0.0])               # [Va, Ha, Vb]
    Force_Reactions_Recorder = np.empty((0, 3))
    Moment_Reactions_Recorder = np.empty((0, 2))
    UDLs_Reactions_Recorder = np.empty((0, 2))
    TRLs_Reactions_Recorder = np.empty((0, 2))
    ShearForce_Recorder = np.empty((0, len(X_Field)))
    BendingMoment_Recorder = np.empty((0, len(X_Field)))
    return (Reactions, Force_Reactions_Recorder, Moment_Reactions_Recorder,
            UDLs_Reactions_Recorder, TRLs_Reactions_Recorder,
            ShearForce_Recorder, BendingMoment_Recorder)

# --------------------------------------------------------------------------------
#         REACTION SOLVER SECTION
# --------------------------------------------------------------------------------

def Calculate_Force_Reactions(n, A, B):
    """Calculate reactions at supports due to a point force."""
    Xp = pointloads[n, 0]
    Fx = pointloads[n, 1]
    Fy = pointloads[n, 2]

    Vb = Fy * (A - Xp) / (B - A)
    Va = -Fy - Vb
    Ha = Fx

    return Va, Vb, Ha

def Calculate_Moment_Reactions(n, A, B):
    """Calculate reactions at supports due to a point moment."""
    Xm = momentloads[n, 0]
    m = momentloads[n, 1]

    Vb = m / (B - A)
    Va = -Vb

    return Va, Vb

def Calculate_UDL_Reactions(n, A, B):
    """Calculate reactions at supports due to a Uniform Distributed Load (UDL)."""
    Xstart = distributedloads[n, 0]
    Xend = distributedloads[n, 1]
    Fy = distributedloads[n, 2]

    Fy_res = Fy * (Xend - Xstart)
    X_res = Xstart + 0.5 * (Xend - Xstart)

    Vb = Fy_res * (A - X_res) / (B - A)
    Va = -Fy_res - Vb

    return Va, Vb

def Calculate_TRL_Reactions(n, A, B):
    """Calculate reactions at supports due to a Triangular Distributed Load."""
    Xstart = Triangleloads[n, 0]
    Xend = Triangleloads[n, 1]
    Fy_start = Triangleloads[n, 2]
    Fy_end = Triangleloads[n, 3]

    if abs(Fy_start) > 0:
        Fy_res = 0.5 * Fy_start * (Xend - Xstart)
        X_res = Xstart + (1/3)*(Xend - Xstart)
    else:
        Fy_res = 0.5 * Fy_end * (Xend - Xstart)
        X_res = Xstart + (2/3)*(Xend - Xstart)

    Vb = Fy_res * (A - X_res) / (B - A)
    Va = -Fy_res - Vb

    return Va, Vb

def Calculate_Reactions(A, B,
                         Reactions,
                         Force_Reactions_Recorder,
                         Moment_Reactions_Recorder,
                         UDLs_Reactions_Recorder,
                         TRLs_Reactions_Recorder):
    """
    Calculate all reactions at supports due to all types of loads.
    """
    if Test_pointloads > 0:
        for n, _ in enumerate(pointloads):
            Va, Vb, Ha = Calculate_Force_Reactions(n, A, B)
            new_reaction = np.array([[Va, Ha, Vb]])
            Force_Reactions_Recorder = np.vstack([Force_Reactions_Recorder, new_reaction])
            Reactions[0] += Va
            Reactions[1] += Ha
            Reactions[2] += Vb

    if Test_momentloads > 0:
        for n, _ in enumerate(momentloads):
            Va, Vb = Calculate_Moment_Reactions(n, A, B)
            new_reaction = np.array([[Va, Vb]])
            Moment_Reactions_Recorder = np.vstack([Moment_Reactions_Recorder, new_reaction])
            Reactions[0] += Va
            Reactions[2] += Vb

    if Test_UDLs > 0:
        for n, _ in enumerate(distributedloads):
            Va, Vb = Calculate_UDL_Reactions(n, A, B)
            new_reaction = np.array([[Va, Vb]])
            UDLs_Reactions_Recorder = np.vstack([UDLs_Reactions_Recorder, new_reaction])
            Reactions[0] += Va
            Reactions[2] += Vb

    if Test_TRLs > 0:
        for n, _ in enumerate(Triangleloads):
            Va, Vb = Calculate_TRL_Reactions(n, A, B)
            new_reaction = np.array([[Va, Vb]])
            TRLs_Reactions_Recorder = np.vstack([TRLs_Reactions_Recorder, new_reaction])
            Reactions[0] += Va
            Reactions[2] += Vb

    return (Reactions,
            Force_Reactions_Recorder,
            Moment_Reactions_Recorder,
            UDLs_Reactions_Recorder,
            TRLs_Reactions_Recorder)

# --------------------------------------------------------------------------------
#         SHEAR FORCE AND BENDING MOMENT SOLVER SECTION
# --------------------------------------------------------------------------------

def Calculate_SF_BM_Force(n, A, B, X_Field, Force_Reactions_Recorder):
    """Calculate SF and BM from a Point Load."""
    Xp = pointloads[n, 0]
    Fy = pointloads[n, 2]
    Va = Force_Reactions_Recorder[n, 0]
    Vb = Force_Reactions_Recorder[n, 2]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)
        if x > Xp:
            shear += Fy
            moment -= Fy * (x - Xp)
        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

def Calculate_SF_BM_Moment(n, A, B, X_Field, Moment_Reactions_Recorder):
    """Calculate SF and BM from a Point Moment."""
    Xm = momentloads[n, 0]
    m = momentloads[n, 1]
    Va = Moment_Reactions_Recorder[n, 0]
    Vb = Moment_Reactions_Recorder[n, 1]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)
        if x > Xm:
            moment -= m
        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

def Calculate_SF_BM_UDL(n, A, B, X_Field, UDLs_Reactions_Recorder):
    """Calculate SF and BM from a Uniform Distributed Load."""
    Xstart = distributedloads[n, 0]
    Xend = distributedloads[n, 1]
    Fy = distributedloads[n, 2]
    Va = UDLs_Reactions_Recorder[n, 0]
    Vb = UDLs_Reactions_Recorder[n, 1]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)

        if Xstart < x <= Xend:
            shear += Fy * (x - Xstart)
            moment -= Fy * (x - Xstart) * 0.5 * (x - Xstart)
        elif x > Xend:
            shear += Fy * (Xend - Xstart)
            moment -= Fy * (Xend - Xstart) * (x - Xstart - 0.5 * (Xend - Xstart))

        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

def Calculate_SF_BM_TRL(n, A, B, X_Field, TRLs_Reactions_Recorder):
    """Calculate SF and BM from a Triangular Distributed Load."""
    Xstart = Triangleloads[n, 0]
    Xend = Triangleloads[n, 1]
    Fy_start = Triangleloads[n, 2]
    Fy_end = Triangleloads[n, 3]
    Va = TRLs_Reactions_Recorder[n, 0]
    Vb = TRLs_Reactions_Recorder[n, 1]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)

        if Xstart < x <= Xend:
            if abs(Fy_start) > 0:
                Xbase = x - Xstart
                F_cut = Fy_start - Xbase * (Fy_start / (Xend - Xstart))
                R1 = 0.5 * Xbase * (Fy_start - F_cut)
                R2 = Xbase * F_cut
                shear += R1 + R2
                moment -= R1 * (2/3) * Xbase + R2 * 0.5 * Xbase
            else:
                Xbase = x - Xstart
                F_cut = Fy_end * (Xbase / (Xend - Xstart))
                R = 0.5 * Xbase * F_cut
                shear += R
                moment -= R * (1/3) * Xbase
        elif x > Xend:
            if abs(Fy_start) > 0:
                R = 0.5 * Fy_start * (Xend - Xstart)
                Xr = Xstart + (1/3)*(Xend - Xstart)
                shear += R
                moment -= R * (x - Xr)
            else:
                R = 0.5 * Fy_end * (Xend - Xstart)
                Xr = Xstart + (2/3)*(Xend - Xstart)
                shear += R
                moment -= R * (x - Xr)

        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

def Calculate_SF_BM(X_Field, A, B,
                    Force_Reactions_Recorder,
                    ShearForce_Recorder,
                    BendingMoment_Recorder,
                    Moment_Reactions_Recorder,
                    UDLs_Reactions_Recorder,
                    TRLs_Reactions_Recorder):
    """
    Calculate total Shear Force and Bending Moment for the entire beam.
    """
    if Test_pointloads > 0:
        for n, _ in enumerate(pointloads):
            Shear, Moment = Calculate_SF_BM_Force(n, A, B, X_Field, Force_Reactions_Recorder)
            ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])
            BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])

    if Test_momentloads > 0:
        for n, _ in enumerate(momentloads):
            Shear, Moment = Calculate_SF_BM_Moment(n, A, B, X_Field, Moment_Reactions_Recorder)
            ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])
            BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])

    if Test_UDLs > 0:
        for n, _ in enumerate(distributedloads):
            Shear, Moment = Calculate_SF_BM_UDL(n, A, B, X_Field, UDLs_Reactions_Recorder)
            ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])
            BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])

    if Test_TRLs > 0:
        for n, _ in enumerate(Triangleloads):
            Shear, Moment = Calculate_SF_BM_TRL(n, A, B, X_Field, TRLs_Reactions_Recorder)
            ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])
            BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])

    Total_ShearForce = np.sum(ShearForce_Recorder, axis=0)
    Total_BendingMoment = -np.sum(BendingMoment_Recorder, axis=0)

    return Total_ShearForce, Total_BendingMoment

def solve_simple_beam(beam_length, A, B):
    """
    High-level function to solve a simple beam completely.
    
    Parameters:
    - beam_length: Length of beam (meters)
    - A: Position of Pin Support (meters)
    - B: Position of Roller Support (meters)
    
    Returns:
    - X_Field: Array of x-positions
    - Total_ShearForce: Shear Force at each x-position
    - Total_BendingMoment: Bending Moment at each x-position
    """

    # Initialize Solver
    X_Field, Delta = initialize_solver(beam_length)

    # Initialize Containers
    (Reactions, Force_Reactions_Recorder, Moment_Reactions_Recorder,
     UDLs_Reactions_Recorder, TRLs_Reactions_Recorder,
     ShearForce_Recorder, BendingMoment_Recorder) = initialize_containers(X_Field)

    # Solve Reactions
    (Reactions,
     Force_Reactions_Recorder,
     Moment_Reactions_Recorder,
     UDLs_Reactions_Recorder,
     TRLs_Reactions_Recorder) = Calculate_Reactions(A, B,
                                                     Reactions,
                                                     Force_Reactions_Recorder,
                                                     Moment_Reactions_Recorder,
                                                     UDLs_Reactions_Recorder,
                                                     TRLs_Reactions_Recorder)

    # Solve Shear Force and Bending Moment
    Total_ShearForce, Total_BendingMoment = Calculate_SF_BM(X_Field, A, B,
                                                            Force_Reactions_Recorder,
                                                            ShearForce_Recorder,
                                                            BendingMoment_Recorder,
                                                            Moment_Reactions_Recorder,
                                                            UDLs_Reactions_Recorder,
                                                            TRLs_Reactions_Recorder)

    # DONE
    return X_Field, Reactions, Total_ShearForce, Total_BendingMoment
