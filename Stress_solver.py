
import numpy as np

# =============================
# Calculation Functions
# =============================
def first_moment_of_area_rect(b, y_array):
    """
    Calculate the first moment of area for a rectangular section.
    
    Args:
        b (float): Width of the section (m).
        y_array (np.ndarray): Array of vertical distances from the neutral axis.
        
    Returns:
        np.ndarray: First moment of area Q in m^3.
    """
    Q_array = b * np.abs(y_array) * (np.abs(y_array) / 2)
    return Q_array


def calculate_shear_stress(Total_ShearForce, Q_array, Ix, b):
    """
    Calculate the shear stress distribution.
    
    Args:
        Total_ShearForce (np.ndarray): Shear force distribution (N).
        Q_array (np.ndarray): First moment of area distribution (m^3).
        Ix (float): Moment of inertia (m^4).
        b (float): Width of the section (m).
        
    Returns:
        np.ndarray: Shear stress distribution (Pa).
    """
    min_len = min(len(Total_ShearForce), len(Q_array))
    tau_array = Total_ShearForce[:min_len] * Q_array[:min_len] / (Ix * b)
    return tau_array


def calculate_bending_stress(M, c, Ix):

    sigma = M * c / Ix
    return sigma


def calculate_FOS(yield_strength, sigma):
    """
    Calculate the Factor of Safety (FOS).
    
    Args:
        yield_strength (float): Yield strength (Pa).
        sigma (float): Calculated bending stress (Pa).
        
    Returns:
        float: Factor of Safety.
    """
    FOS = yield_strength / sigma
    return FOS


def Factor_of_Safety(Total_BendingMoment, c, yield_strength, Ix):

    M_max = np.max(np.abs(Total_BendingMoment))
    sigma = calculate_bending_stress(M_max, c, Ix)
    FOS = calculate_FOS(yield_strength, sigma)
    print(f"Maximum bending moment (N.m): {M_max:.2f}")
    print(f"Bending stress (Pa): {sigma:.2f}")
    print(f"Factor of Safety: {FOS:.2f}")



def calculate_beam_deflection(X_Field, moment_distribution, E, I):

    # Calculate curvature at each discrete point: curvature = M/(E*I)
    curvature = moment_distribution / (E * I)
    
    # Assume uniform discretization; compute the spacing delta
    dx = X_Field[1] - X_Field[0]
    
    # First integration: cumulative trapezoidal integration to obtain slope
    # Here we use a simple cumulative summation multiplied by dx:
    slope = np.cumsum(curvature) * dx
    
    # Second integration: cumulative summation on the slope gives deflection:
    deflection = np.cumsum(slope) * dx
    
    # For a simply supported beam, deflection at the supports should be 0.
    # We can correct our computed deflection by subtracting a linear function that forces
    # the endpoints (supports) to be zero. Here we assume support at the beginning (x=0)
    # and at the end (x = beam_length).
    correction = np.linspace(deflection[0], deflection[-1], len(deflection))
    deflection_adjusted = deflection - correction
    
    return deflection_adjusted, slope, curvature

# Example usage:
# Assuming you have calculated X_Field and Total_BendingMoment from your solver,
# and you have E (Elastic Modulus) and I (from profile, e.g., Ix) already computed:
# deflection, slope, curvature = calculate_beam_deflection(X_Field, Total_BendingMoment, elastic_modulus, Ix)