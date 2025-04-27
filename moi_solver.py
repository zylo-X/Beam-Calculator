# --------------------------------------------------------------------------------
#            Moment of Inertia (MOI) Solver
# --------------------------------------------------------------------------------
import numpy as np

# --- Functions for Different Cross-Sections ---

def inertia_moment_ibeam(bf, tf, hw, tw):
    """Calculate moment of inertia for an I-Beam."""
    Ix = (bf * tf**3 / 12) + (bf * tf * (hw/2 - tf/2)**2) + (tw * hw**3 / 12)
    return Ix

def inertia_moment_tbeam(bf, tf, hw, tw):
    """
    Calculate Moment of Inertia (Ix) for a T-Beam cross-section.

    Parameters:
    - bf: Flange width (m)
    - tf: Flange thickness (m)
    - hw: Web height (m) (without flange thickness)
    - tw: Web thickness (m)

    Returns:
    - Ix: Moment of Inertia (m^4)
    """
    # Area and centroid calculation first
    A_flange = bf * tf
    A_web = tw * hw

    # Distance between top and overall centroid
    y_flange = tf / 2
    y_web = tf + hw / 2

    # Total Area
    A_total = A_flange + A_web

    # Centroid (from bottom)
    y_bar = (A_flange * y_flange + A_web * y_web) / A_total

    # Moment of inertia for each part (about its own centroid)
    I_flange = (bf * tf**3) / 12
    I_web = (tw * hw**3) / 12

    # Use parallel axis theorem
    I_flange_total = I_flange + A_flange * (y_bar - y_flange)**2
    I_web_total = I_web + A_web * (y_web - y_bar)**2

    # Total Ix
    Ix_total = I_flange_total + I_web_total

    return Ix_total





def inertia_moment_circle(diameter):
    """Calculate moment of inertia for a circle."""
    r = diameter / 2
    return (np.pi * r**4) / 4

def inertia_moment_rectangle(b, h):
    """Calculate moment of inertia for a rectangle."""
    return b * h**3 / 12

def inertia_moment_square(a):
    """Calculate moment of inertia for a square."""
    return a**4 / 12

def inertia_moment_hollow_circle(outer_diameter, inner_diameter):
    """Calculate moment of inertia for a hollow circle."""
    r_outer = outer_diameter / 2
    r_inner = inner_diameter / 2
    return (np.pi * (r_outer**4 - r_inner**4)) / 4

def inertia_moment_hollow_square(outer_width, inner_width):
    """Calculate moment of inertia for a hollow square."""
    return (outer_width**4 - inner_width**4) / 12

def inertia_moment_hollow_rectangle(outer_b, outer_h, inner_b, inner_h):
    """Calculate moment of inertia for a hollow rectangle."""
    return (outer_b * outer_h**3 / 12) - (inner_b * inner_h**3 / 12)
