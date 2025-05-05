# --------------------------------------------------------------------------------
#           Libraries
# --------------------------------------------------------------------------------
import numpy as np

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
    Reactions = np.array([0.0, 0.0, 0.0])  # [Va, Ha, Vb]
    ShearForce_Recorder = np.zeros(len(X_Field))
    BendingMoment_Recorder = np.zeros(len(X_Field))
    return Reactions, ShearForce_Recorder, BendingMoment_Recorder

# --------------------------------------------------------------------------------
#         Simple Beam Reaction Solver
# --------------------------------------------------------------------------------
def calculate_all_reactions(A, B, pointloads, momentloads, distributedloads, triangleloads):
    """
    Calculate reactions at supports due to all types of loads simultaneously.
    Handles:
    - Point Loads (pointloads)
    - Point Moments (momentloads)
    - Uniform Distributed Loads (distributedloads)
    - Triangular Distributed Loads (triangleloads)
    
    Sign Convention:
    - Positive vertical forces act downward
    - Positive horizontal forces act to the right
    - Positive moments act counter-clockwise
    """
    Va, Vb, Ha = 0, 0, 0  # Initialize reactions (vertical, horizontal, and moment)

    # Point Loads
    if pointloads.shape[0] > 0:
        for n in range(pointloads.shape[0]):
            Xp, Fx, Fy = pointloads[n]
            Vb += Fy * (A - Xp) / (B - A)
            Va += -Fy - (Fy * (A - Xp) / (B - A))
            Ha += Fx

    # Point Moments
    if momentloads.shape[0] > 0:
        for n in range(momentloads.shape[0]):
            Xm, m = momentloads[n]
            Vb += m / (B - A)
            Va += -m / (B - A)

    # Uniform Distributed Loads (UDL)
    if distributedloads.shape[0] > 0:
        for n in range(distributedloads.shape[0]):
            Xstart, Xend, Fy = distributedloads[n]
            Fy_res = Fy * (Xend - Xstart)
            X_res = Xstart + 0.5 * (Xend - Xstart)
            Vb += Fy_res * (A - X_res) / (B - A)
            Va += -Fy_res - (Fy_res * (A - X_res) / (B - A))

    # Triangular Distributed Loads (TRL)
    if triangleloads.shape[0] > 0:
        for n in range(triangleloads.shape[0]):
            Xstart, Xend, Fy_start, Fy_end = triangleloads[n]
            if abs(Fy_start) > 0:
                Fy_res = 0.5 * Fy_start * (Xend - Xstart)
                X_res = Xstart + (1/3) * (Xend - Xstart)
            else:
                Fy_res = 0.5 * Fy_end * (Xend - Xstart)
                X_res = Xstart + (2/3) * (Xend - Xstart)
            Vb += Fy_res * (A - X_res) / (B - A)
            Va += -Fy_res - (Fy_res * (A - X_res) / (B - A))

    return Va, Vb, Ha  # Fixed: Return statement moved outside the loop

# --------------------------------------------------------------------------------
#         cantilever Beam Reaction Solver
# --------------------------------------------------------------------------------
def Calculate_Cantilever_Reactions(pointloads, momentloads, distributedloads, triangleloads):
    """
    Calculate reactions at the fixed support of a cantilever beam.
    
    Sign Convention:
    - Positive vertical forces act downward
    - Positive horizontal forces act to the right
    - Positive moments act counter-clockwise (clockwise is negative)
    """
    Va,Ma, Ha  = 0, 0, 0  # Initialize reactions (vertical, horizontal, and moment)

    # Point Loads
    if pointloads.shape[0] > 0:
        for n in range(pointloads.shape[0]):
            Xp, Fx, Fy = pointloads[n]
            Va += Fy
            Ha += Fx
            Ma -= Fy * Xp  # Clockwise moment is negative

    # Point Moments
    if momentloads.shape[0] > 0:
        for n in range(momentloads.shape[0]):
            Xm, M = momentloads[n]
            Ma -= M

    # Uniform Distributed Loads (UDL)
    if distributedloads.shape[0] > 0:
        for n in range(distributedloads.shape[0]):
            Xstart, Xend, Fy = distributedloads[n]
            load_length = Xend - Xstart
            Fy_res = Fy * load_length
            X_res = Xstart + 0.5 * load_length
            Va += Fy_res
            Ma -= Fy_res * X_res

    # Triangular Distributed Loads (TRL)
    if triangleloads.shape[0] > 0:
        for n in range(triangleloads.shape[0]):
            Xstart, Xend, Fy_start, Fy_end = triangleloads[n]
            if abs(Fy_start) > 0:
                Fy_res = 0.5 * Fy_start * (Xend - Xstart)
                X_res = Xstart + (1/3) * (Xend - Xstart)
            else:
                Fy_res = 0.5 * Fy_end * (Xend - Xstart)
                X_res = Xstart + (2/3) * (Xend - Xstart)

            Va += Fy_res
            Ma -= Fy_res * X_res

    return Va,Ma, Ha   # Fixed: Return statement moved outside the loop

# --------------------------------------------------------------------------------
#         Simple Beam Shear Force and Bending Moment Solver
# --------------------------------------------------------------------------------
def calculate_sf_bm(X_Field, A, B, pointloads, momentloads, distributedloads, triangleloads, reactions):
    """
    Calculate Shear Force and Bending Moment at every point along the beam.
    Handles:
    - Point Loads (pointloads)
    - Point Moments (momentloads)
    - Uniform Distributed Loads (distributedloads)
    - Triangular Distributed Loads (triangleloads)

    Returns:
    - Total Shear Force and Bending Moment arrays
    
    Sign Convention:
    - Positive shear force causes clockwise rotation
    - Positive bending moment causes compression in the top fibers
    """
    Va, Vb, Ha  = reactions  # Reactions from supports
    ShearForce = np.zeros(len(X_Field))  # Initialize SF array
    BendingMoment = np.zeros(len(X_Field))  # Initialize BM array

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0

        # Reaction Forces
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)

        # Point Loads
        if pointloads.shape[0] > 0:
            for n in range(pointloads.shape[0]):
                Xp, Fx, Fy = pointloads[n]
                if x > Xp:
                    shear += Fy
                    moment -= Fy * (x - Xp)

        # Point Moments
        if momentloads.shape[0] > 0:
            for n in range(momentloads.shape[0]):
                Xm, m = momentloads[n]
                if x > Xm:
                    moment -= m

        # Uniform Distributed Loads (UDL)
        if distributedloads.shape[0] > 0:
            for n in range(distributedloads.shape[0]):
                Xstart, Xend, Fy = distributedloads[n]
                if Xstart < x <= Xend:
                    shear += Fy * (x - Xstart)
                    moment -= Fy * (x - Xstart) * 0.5 * (x - Xstart)
                elif x > Xend:
                    shear += Fy * (Xend - Xstart)
                    moment -= Fy * (Xend - Xstart) * (x - Xstart - 0.5 * (Xend - Xstart))

        # Triangular Distributed Loads (TRL)
        if triangleloads.shape[0] > 0:
            for n in range(triangleloads.shape[0]):
                Xstart, Xend, Fy_start, Fy_end = triangleloads[n]
                if Xstart < x <= Xend:
                    if abs(Fy_start) > 0:
                        Xbase = x - Xstart
                        F_cut = Fy_start - Xbase * (Fy_start / (Xend - Xstart))
                        R1 = 0.5 * Xbase * (Fy_start - F_cut)
                        R2 = Xbase * F_cut
                        shear += R1 + R2
                        moment -= R1 * (2 / 3) * Xbase + R2 * 0.5 * Xbase
                    else:
                        Xbase = x - Xstart
                        F_cut = Fy_end * (Xbase / (Xend - Xstart))
                        R = 0.5 * Xbase * F_cut
                        shear += R
                        moment -= R * (1 / 3) * Xbase
                elif x > Xend:
                    if abs(Fy_start) > 0:
                        R = 0.5 * Fy_start * (Xend - Xstart)
                        Xr = Xstart + (1 / 3) * (Xend - Xstart)
                        shear += R
                        moment -= R * (x - Xr)
                    else:
                        R = 0.5 * Fy_end * (Xend - Xstart)
                        Xr = Xstart + (2 / 3) * (Xend - Xstart)
                        shear += R
                        moment -= R * (x - Xr)

        # Store results
        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, -BendingMoment

# --------------------------------------------------------------------------------
#         cantilever Beam Shear Force and Bending Moment Solver
# --------------------------------------------------------------------------------
def Calculate_SF_BM_Cantilever(X_Field,Va,Ma,Ha,
                               pointloads, momentloads, distributedloads, triangleloads):
    """
    Calculate Shear Force and Bending Moment for a cantilever beam.
    
    Sign Convention:
    - Positive shear force causes clockwise rotation
    - Positive bending moment causes compression in the top fibers
    - Fixed support is at X=0
    """
    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = Va
        moment = Ma

        # Point Loads
        if pointloads.shape[0] > 0:
            for n in range(pointloads.shape[0]):
                Xp, Fx, Fy = pointloads[n]
                if x >= Xp:
                    shear -= Fy
                    moment -= Fy * (x - Xp)

        # Point Moments
        if momentloads.shape[0] > 0:
            for n in range(momentloads.shape[0]):
                Xm, M = momentloads[n]
                if x >= Xm:
                    moment -= M

        # Uniform Distributed Loads (UDL)
        if distributedloads.shape[0] > 0:
            for n in range(distributedloads.shape[0]):
                Xstart, Xend, Fy = distributedloads[n]
                if x >= Xstart:
                    if x <= Xend:
                        load_length = x - Xstart
                        Fy_res = Fy * load_length
                        shear -= Fy_res
                        moment -= Fy_res * (load_length * 0.5)
                    else:
                        load_length = Xend - Xstart
                        Fy_res = Fy * load_length
                        shear -= Fy_res
                        moment -= Fy_res * (load_length * 0.5 + (x - Xend))

        # Triangular Distributed Loads (TRL)
        if triangleloads.shape[0] > 0:
            for n in range(triangleloads.shape[0]):
                Xstart, Xend, Fy_start, Fy_end = triangleloads[n]
                if x >= Xstart:
                    if x <= Xend:
                        if abs(Fy_start) > 0:
                            Xbase = x - Xstart
                            F_cut = Fy_start - Xbase * (Fy_start / (Xend - Xstart))
                            R1 = 0.5 * Xbase * (Fy_start - F_cut)
                            R2 = Xbase * F_cut
                            shear -= R1 + R2
                            moment -= R1 * (2/3) * Xbase + R2 * 0.5 * Xbase
                        else:
                            Xbase = x - Xstart
                            F_cut = Fy_end * (Xbase / (Xend - Xstart))
                            R = 0.5 * Xbase * F_cut
                            shear -= R
                            moment -= R * (1/3) * Xbase
                    else:
                        if abs(Fy_start) > 0:
                            R = 0.5 * Fy_start * (Xend - Xstart)
                            Xr = Xstart + (1/3)*(Xend - Xstart)
                            shear -= R
                            moment -= R * (x - Xr)
                        else:
                            R = 0.5 * Fy_end * (Xend - Xstart)
                            Xr = Xstart + (2/3)*(Xend - Xstart)
                            shear -= R
                            moment -= R * (x - Xr)

        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

# --------------------------------------------------------------------------------
#         High-Level Solver
# --------------------------------------------------------------------------------
def solve_simple_beam(beam_length, A=None, B=None,
                      pointloads_in=None, distributedloads_in=None,
                      momentloads_in=None, triangleloads_in=None,
                      beam_type="Simple"):
    """
    High-level function to solve a beam completely.
    Supports simple beams (with two supports) and cantilever beams.

    Parameters:
        beam_length : float : Length of the beam
        A, B        : float : Support positions (only for simple beams)
        beam_type   : str   : "simple" or "cantilever"
        
    Returns:
        X_Field     : ndarray : Beam position points
        ShearForce  : ndarray : Shear force values along the beam
        BendingMoment : ndarray : Bending moment values along the beam
        Reactions   : ndarray : Support reactions [Va, Ha, Vb/Ma]
    """
    if pointloads_in is None:
        pointloads = np.empty((0, 3))
    else:
        pointloads = np.array(pointloads_in)

    if distributedloads_in is None:
        distributedloads = np.empty((0, 3))
    else:
        distributedloads = np.array(distributedloads_in)

    if momentloads_in is None:
        momentloads = np.empty((0, 2))
    else:
        momentloads = np.array(momentloads_in)

    if triangleloads_in is None:
        triangleloads = np.empty((0, 4))
    else:
        triangleloads = np.array(triangleloads_in)

    # Initialize Solver
    X_Field, Delta = initialize_solver(beam_length)

    if beam_type == "Simple":
        # Ensure supports are defined for simple beam
        if A is None or B is None:
            raise ValueError("Support positions A and B must be provided for simple beam")
            
        # Solve Reactions
        Reactions = calculate_all_reactions(A, B, pointloads, momentloads, 
                                           distributedloads, triangleloads)
        
        # Solve SF and BM
        Total_ShearForce, Total_BendingMoment = calculate_sf_bm(
            X_Field, A, B, pointloads, momentloads, 
            distributedloads, triangleloads, Reactions)
            
        # Fixed: Add return statement for simple beam
        return X_Field, Total_ShearForce, Total_BendingMoment, Reactions

    elif beam_type == "Cantilever":
        # --- Solve Reactions ---
        Va,Ma,Ha = Calculate_Cantilever_Reactions(
            pointloads, momentloads, distributedloads, triangleloads)

        # --- Solve Shear Force and Bending Moment ---
        Total_ShearForce, Total_BendingMoment = Calculate_SF_BM_Cantilever(
            X_Field, Va,Ma, Ha , pointloads, momentloads, 
            distributedloads, triangleloads)

        Reactions = np.array([Va,Ma,Ha])
        return X_Field, Total_ShearForce, Total_BendingMoment, Reactions

    else:
        raise ValueError("Invalid beam_type. Choose 'simple' or 'cantilever'.")