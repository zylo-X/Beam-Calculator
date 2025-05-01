
from termcolor import colored
import time
from Menus import print_error, print_success, print_title, print_option, clear_screen


def Beam_Length():
    """
    Prompt the user to enter the beam length.
    """
    beam_length = float(input(colored("Enter Beam Length (meters): ➔ ", 'cyan')))
    if beam_length <=0:
        print_error("Beam length must be positive.")
        time.sleep(1)
        return Beam_Length()
    print("")
    return beam_length

#==============================
def Beam_Supports():
    """
    Prompt the user to define the beam supports (positions and types).
    
    Returns:
        tuple: (A, B, A_restraint, B_restraint, A_type, B_type)
        or (None, None, None, None, None, None) if an error occurs.
    """
    try:
        A = float(input(colored("Enter Position of Pin Support A (meters): ➔ ", 'cyan')))
        A_restraint = (1, 1, 0)
        A_type = "Pin Support"
    
        B = float(input(colored("Enter Position of Roller Support B (meters): ➔ ", 'cyan')))
        B_restraint = (0, 1, 0)
        B_type = "Roller Support"
    
        if A < 0 or B < 0:
            print_error("Support positions must be positive.")
            time.sleep(1)
            print("")
            return Beam_Supports()
        if A >= B:
             print_error("Support A must be to the left of Support B.")
             print("")
             time.sleep(1)
             return Beam_Supports()  
             print("")
        print("")
        return A, B, A_restraint, B_restraint, A_type, B_type
    except ValueError as ve:
        print_error(f"Input error: {ve}")
        return None, None, None, None, None, None
#==============================
def manage_loads():
    """
    Display a submenu to manage load inputs interactively.
    
    Returns:
        dict: A dictionary with keys "pointloads", "distributedloads", 
              "momentloads", "triangleloads" containing defined loads.
    """
    loads = {
        "pointloads": [],
        "distributedloads": [],
        "momentloads": [],
        "triangleloads": []
    }
    
    while True:
        clear_screen()
        print_title("Loads Definition Submenu")
        print_option("1 - Add Point Load")
        print_option("2 - Add Distributed Load")
        print_option("3 - Add Moment Load")
        print_option("4 - Add Triangular Load")
        print_option("5 - Show Current Loads")
        print_option("6 - Remove All Loads")
        print_option("7 - Return to Main Menu")
        print("")
        choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    
        if choice == '1':
            try:
                pos = float(input("Enter position (m): ➔ "))
                print(colored("Select Point Load Type:", 'yellow'))
                print_option("1 - Vertical Load (Y-direction)")
                print_option("2 - Horizontal Load (X-direction)")
                print_option("3 - Angled Load (Force & Angle)")
                load_type = input(colored("Enter your choice (1, 2, or 3) ➔ ", 'cyan'))
                if load_type == '1':
                    y_force = float(input("Enter Y-force (N): ➔ "))
                    loads["pointloads"].append([pos, 0, y_force])
                elif load_type == '2':
                    x_force = float(input("Enter X-force (N): ➔ "))
                    loads["pointloads"].append([pos, x_force, 0])
                elif load_type == '3':
                    force_mag = float(input("Enter Force magnitude (N): ➔ "))
                    angle = float(input("Enter angle (degrees): ➔ "))
                    x_force = force_mag * np.cos(np.radians(angle))
                    y_force = force_mag * np.sin(np.radians(angle))
                    loads["pointloads"].append([pos, x_force, y_force])
                else:
                    print_error("Invalid point load type selection!")
                    time.sleep(2)
            except Exception as e:
                print_error(f"Error adding point load: {e}")
                time.sleep(2)
    
        elif choice == '2':
            try:
                start = float(input("Enter start position (m) for UDL: ➔ "))
                end = float(input("Enter end position (m) for UDL: ➔ "))
                intensity = float(input("Enter load intensity (N/m): ➔ "))
                loads["distributedloads"].append([start, end, intensity])
            except Exception as e:
                print_error(f"Error adding distributed load: {e}")
                time.sleep(2)
    
        elif choice == '3':
            try:
                pos = float(input("Enter position (m) for Moment Load: ➔ "))
                moment = float(input("Enter moment magnitude (N·m): ➔ "))
                loads["momentloads"].append([pos, moment])
            except Exception as e:
                print_error(f"Error adding moment load: {e}")
                time.sleep(2)
    
        elif choice == '4':
            try:
                start = float(input("Enter start position (m) for Triangular Load: ➔ "))
                end = float(input("Enter end position (m) for Triangular Load: ➔ "))
                intensity = float(input("Enter peak load intensity (N/m): ➔ "))
                intensityL = float(input("Enter lowest load intensity (N/m): ➔ "))
                loads["triangleloads"].append([start, end, intensity, intensityL])
            except Exception as e:
                print_error(f"Error adding triangular load: {e}")
                time.sleep(2)
    
        elif choice == '5':
            clear_screen()
            print_title("Current Loads:")
            print(colored(f"Point Loads: {loads['pointloads']}", 'white'))
            print(colored(f"Distributed Loads: {loads['distributedloads']}", 'white'))
            print(colored(f"Moment Loads: {loads['momentloads']}", 'white'))
            print(colored(f"Triangular Loads: {loads['triangleloads']}", 'white'))
            print("")
            input("Press Enter to continue...")
    
        elif choice == '6':
            confirm = input(colored("Are you sure you want to remove all loads? (Y/N): ➔ ", 'cyan'))
            if confirm.lower() == 'y':
                loads = {
                    "pointloads": [],
                    "distributedloads": [],
                    "momentloads": [],
                    "triangleloads": []
                }
                print_success("All loads have been removed!")
                time.sleep(2)
            else:
                print("No loads were removed.")
                time.sleep(2)
    
        elif choice == '7':
            break
        else:
            print_error("Invalid selection! Please try again.")
            time.sleep(2)
    
    return loads