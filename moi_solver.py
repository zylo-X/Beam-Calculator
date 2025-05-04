
# --------------------------------------------------------------------------------
#            Moment of Inertia (MOI) Solver with Neutral Axis Distance (c) & Width (b)
# --------------------------------------------------------------------------------
import numpy as np
from termcolor import cprint, colored

# --- Functions for Different Cross-Sections ---

def inertia_moment_ibeam():
    try:
        print("\nEnter dimensions for a symmetric I-beam (in meters):")
        bf = float(input("Flange width, bf: "))
        tf = float(input("Flange height, tf: "))
        hw = float(input("Web height, hw: "))
        tw = float(input("Web thickness, tw: "))
    except Exception as e:
        print("Invalid input. Please enter numeric values.")
        return None

    H = 2 * tf + hw
    c = H / 2
    d = c - tf / 2

    I_flange = (bf * tf**3) / 12
    I_flange_total = I_flange + bf * tf * (d**2)
    I_web = (tw * hw**3) / 12
    Ix_total = 2 * I_flange_total + I_web
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(f"\nCalculated Ix for I-beam: {Ix_total:.6e} m^4")
    print("")
    print(f"Distance c from neutral axis to extreme fiber: {c:.4f} m")
    return Ix_total, "I-beam", c, tw,y_array  # Web width as representative width

def inertia_moment_tbeam():
    try:
        print("\nEnter dimensions for a T-beam (in meters):")
        bf = float(input("Flange width, bf: "))
        tf = float(input("Flange thickness, tf: "))
        hw = float(input("Web height, hw: "))
        tw = float(input("Web thickness, tw: "))
    except Exception as e:
        print("Invalid input. Please enter numeric values.")
        return None

    A_flange = bf * tf
    A_web = tw * hw
    y_flange = tf / 2
    y_web = tf + hw / 2
    A_total = A_flange + A_web
    y_bar = (A_flange * y_flange + A_web * y_web) / A_total
    c = max(y_bar, tf + hw - y_bar)
    I_flange = (bf * tf**3) / 12
    I_web = (tw * hw**3) / 12
    I_flange_total = I_flange + A_flange * (y_bar - y_flange)**2
    I_web_total = I_web + A_web * (y_web - y_bar)**2
    Ix_total = I_flange_total + I_web_total
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(f"\nCalculated Ix for T-beam: {Ix_total:.6e} m^4")
    print("")
    print(f"Distance c from neutral axis to extreme fiber: {c:.4f} m")
    print("")
    return Ix_total, "T-beam", c, tw,y_array

def inertia_moment_circle():
    try:
        diameter = float(input(colored("Enter the diameter of the circle (in meters): ", 'cyan')))
    except Exception as e:
        print("Invalid input. Please enter a numeric value.")
        return None

    r = diameter / 2.0
    c = r
    Ix_total = (np.pi * (r**4)) / 4
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(colored(f"Calculated Ix for a solid circle: {Ix_total:.6e} m^4", 'green'))
    print("")
    print(colored(f"Distance c from neutral axis to extreme fiber: {c:.4f} m", 'yellow'))
    print("")
    return Ix_total, "Circle", c, diameter,y_array # Diameter as effective width

def inertia_moment_rectangle():
    try:
        b = float(input(colored("Enter the base (width) of the rectangle (in meters): ", 'cyan')))
        h = float(input(colored("Enter the height of the rectangle (in meters): ", 'cyan')))
    except Exception as e:
        print("Invalid input. Please enter numeric values.")
        return None

    c = h / 2
    Ix_total = b * h**3 / 12
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(colored(f"Calculated Ix for a rectangle: {Ix_total:.6e} m^4", 'green'))
    print("")
    print(colored(f"Distance c from neutral axis to extreme fiber: {c:.4f} m", 'yellow'))
    print("")
    return Ix_total, "Rectangle", c, b,y_array

def inertia_moment_square():
    try:
        a = float(input(colored("Enter the side length of the square (in meters): ", 'cyan')))
    except Exception as e:
        print("Invalid input. Please enter a numeric value.")
        return None

    c = a / 2
    Ix_total = a**4 / 12
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(colored(f"Calculated Ix for a square: {Ix_total:.6e} m^4", 'green'))
    print("")
    print(colored(f"Distance c from neutral axis to extreme fiber: {c:.4f} m", 'yellow'))
    print("")
    return Ix_total, "Square", c, a,y_array

def inertia_moment_hollow_circle():
    try:
        outer_diameter = float(input(colored("Enter the outer diameter of the hollow circle (in meters): ", 'cyan')))
        inner_diameter = float(input(colored("Enter the inner diameter of the hollow circle (in meters): ", 'cyan')))
    except Exception as e:
        print("Invalid input. Please enter numeric values.")
        return None

    r_outer = outer_diameter / 2.0
    r_inner = inner_diameter / 2.0
    c = r_outer
    Ix_total = (np.pi * (r_outer**4 - r_inner**4)) / 4
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(colored(f"Calculated Ix for a hollow circle: {Ix_total:.6e} m^4", 'green'))
    print("")
    print(colored(f"Distance c from neutral axis to extreme fiber: {c:.4f} m", 'yellow'))
    print("")
    return Ix_total, "Hollow Circle", c, outer_diameter,y_array

def inertia_moment_hollow_square():
    try:
        outer_width = float(input(colored("Enter the outer side length of the hollow square (in meters): ", 'cyan')))
        inner_width = float(input(colored("Enter the inner side length of the hollow square (in meters): ", 'cyan')))
    except Exception as e:
        print("Invalid input. Please enter numeric values.")
        return None

    c = outer_width / 2
    Ix_total = (outer_width**4 - inner_width**4) / 12
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(colored(f"Calculated Ix for a hollow square: {Ix_total:.6e} m^4", 'green'))
    print("")
    print(colored(f"Distance c from neutral axis to extreme fiber: {c:.4f} m", 'yellow'))
    print("")
    return Ix_total, "Hollow Square", c, outer_width,y_array

def inertia_moment_hollow_rectangle():
    try:
        outer_b = float(input(colored("Enter the outer base (width) of the hollow rectangle (in meters): ", 'cyan')))
        outer_h = float(input(colored("Enter the outer height of the hollow rectangle (in meters): ", 'cyan')))
        inner_b = float(input(colored("Enter the inner base (width) of the hollow rectangle (in meters): ", 'cyan')))
        inner_h = float(input(colored("Enter the inner height of the hollow rectangle (in meters): ", 'cyan')))
    except Exception as e:
        print("Invalid input. Please enter numeric values.")
        return None

    c = outer_h / 2
    I_outer = outer_b * (outer_h**3) / 12
    I_inner = inner_b * (inner_h**3) / 12
    Ix_total = I_outer - I_inner
    y_array = np.linspace(-c, c, 10001)
    print("")
    print(colored(f"Calculated Ix for a hollow rectangle: {Ix_total:.6e} m^4", 'green'))
    print("")
    print(colored(f"Distance c from neutral axis to extreme fiber: {c:.4f} m", 'yellow'))
    print("")
    return Ix_total, "Hollow Rectangle", c, outer_b,y_array
