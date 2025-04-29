# cli.py

from termcolor import colored
import json
import numpy as np

# Import application modules
import Solver
import Plotting
import moi_solver
import beam_plot

# ================================
# Global Storage
# ================================
beam_storage = []      # List to hold all projects
current_project = None # Dictionary to hold the currently loaded project

# ================================
# Startup Menu Functions
# ================================

def project_startup():
    """
    Display the startup menu and load or create a new project.
    """
    global current_project

    print_title("Zylo-X Beam Calculator Startup ⚙️")
    print_option("1) Start New Project")
    print_option("2) Load Existing Project")
    print("")  # Blank line for spacing

    choice = input(colored("Enter your choice ➔ ", 'cyan'))

    if choice == '1':
        current_project = None  # New empty project
        print_success("Starting a new project...")
        print("")
    elif choice == '2':
        load_projects_from_disk()
        if not beam_storage:
            print_error("No saved projects available! Starting new project instead.")
            current_project = None
        else:
            print(colored("\nAvailable Projects:", 'yellow'))
            for idx, proj in enumerate(beam_storage):
                print(f" {idx+1}) {proj['name']}")
            print("")
            try:
                proj_choice = int(input(colored("Enter the number of the project you want to load ➔ ", 'cyan')))
                current_project = beam_storage[proj_choice - 1]
                print_success(f"Project '{current_project['name']}' loaded successfully!")
                print("")
            except (IndexError, ValueError):
                print_error("Invalid choice! Starting new project instead.")
                current_project = None
    else:
        print_error("Invalid choice! Starting new project by default.")
        current_project = None


# ================================
# Data Saving and Loading Functions
# ================================

def save_project(beam_length, A, B, A_restraint, B_restraint,
                 X_Field, Total_ShearForce, Total_BendingMoment, Reactions):
    """
    Save the current project data.
    """
    global beam_storage, current_project

    project_name = input(colored("Enter a name for this project ➔ ", 'cyan'))

    project_data = {
        'name': project_name,
        'beam_length': beam_length,
        'support_A_pos': A,
        'support_B_pos': B,
        'support_A_restraint': list(A_restraint),
        'support_B_restraint': list(B_restraint),
        'X_Field': safe_serialize(X_Field),
        'Total_ShearForce': safe_serialize(Total_ShearForce),
        'Total_BendingMoment': safe_serialize(Total_BendingMoment),
        'Reactions': safe_serialize(Reactions)
    }

    beam_storage.append(project_data)
    print_success(f"Project '{project_name}' saved successfully! 📂")
    print("")


def safe_serialize(obj):
    """
    Convert non-JSON serializable objects (like numpy arrays) to lists.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, tuple):
        return list(obj)
    else:
        return obj


def save_projects_to_disk():
    """
    Save all projects from global storage to disk in JSON format.
    """
    global beam_storage
    with open('beam_projects.json', 'w') as file:
        json.dump(beam_storage, file)
    print_success("All projects saved to disk successfully! 📂")
    print("")


def load_projects_from_disk():
    """
    Load projects from the JSON file into global storage.
    """
    global beam_storage
    try:
        with open('beam_projects.json', 'r') as file:
            beam_storage = json.load(file)
        print_success("Projects loaded from disk successfully! 📂")
    except FileNotFoundError:
        print_error("No saved project file found. Starting with empty storage.")
        beam_storage = []
    except json.JSONDecodeError:
        print_error("Error loading projects from disk. Starting with empty storage.")
        beam_storage = []


# ================================
# Printing Helper Functions
# ================================

def print_title(title):
    """
    Print a formatted title.
    """
    print(colored(f"\n=== {title} ===\n", 'cyan', attrs=['bold']))


def print_option(option):
    """
    Print a formatted option.
    """
    print(colored(option, 'yellow'))


def print_error(error_msg):
    """
    Print an error message.
    """
    print(colored(error_msg, 'red', attrs=['bold']))


def print_success(msg):
    """
    Print a success message.
    """
    print(colored(msg, 'green'))


def main_menu():
    """
    Display the main menu and return the user's choice.
    """
    print_title("Welcome to Zylo-X Beam Calculator 🏗️")
    print_option("1) Solve Simple Beam (Reactions, SFD, BMD)")
    print_option("2) Plot Diagrams (Matplotlib / Plotly)")
    print_option("3) Calculate Moment of Inertia (MOI)")
    print_option("0) Exit")
    print("")
    choice = input(colored("Enter your choice ➔ ", 'cyan'))
    return choice


# ================================
# Input Data Functions
# ================================

def Beam_Length():
    """
    Prompt the user to enter the beam length.
    """
    beam_length = float(input(colored("Enter Beam Length (meters): ➔ ", 'cyan')))
    if beam_length <= 0:
        raise ValueError("Beam length must be positive.")
    print("")
    return beam_length


def Beam_Supports():
    """
    Prompt the user to enter the positions and types of supports.
    """
    A = float(input(colored("Enter Position of Support A (meters): ➔ ", 'cyan')))
    print(colored("Choose Support A Type:", 'yellow'))
    print(colored("  1) Pin Support", 'yellow'))
    print(colored("  2) Roller Support", 'yellow'))
    A_type_choice = input(colored("Enter your choice (1 or 2) ➔ ", 'cyan'))
    A_restraint = (1, 1, 0) if A_type_choice == '1' else (0, 1, 0)

    B = float(input(colored("Enter Position of Support B (meters): ➔ ", 'cyan')))
    print(colored("Choose Support B Type:", 'yellow'))
    print(colored("  1) Pin Support", 'yellow'))
    print(colored("  2) Roller Support", 'yellow'))
    B_type_choice = input(colored("Enter your choice (1 or 2) ➔ ", 'cyan'))
    B_restraint = (0, 1, 0) if B_type_choice == '1' else (1, 1, 0)

    if A <= 0 or B <= 0:
        raise ValueError("Support positions must be positive.")
    if A >= B:
        raise ValueError("Support A must be to the left of Support B.")
    
    print("")
    return A, B, A_restraint, B_restraint


def get_user_loads():
    """
    Prompt the user to input various load types:
      - Point loads (with sub-types: Vertical, Horizontal, or Angled)
      - Distributed loads (UDL)
      - Moment loads
      - Triangular loads (currently unused)
      
    Returns a dictionary with keys:
      "pointloads", "distributedloads", "momentloads", "triangleloads"
    """
    pointload_list = []
    distributedload_list = []
    momentload_list = []
    triangleload_list = []  # Reserved for triangular loads

    # --- Point Loads ---
    num_point = int(input("How many point loads do you want to input? ➔ "))
    for i in range(num_point):
        print(f"\n--- Point Load {i+1} ---")
        pos = float(input("Enter position (m): ➔ "))

        print(colored("Select Point Load Type:", 'yellow'))
        print(colored("  1) Vertical Load (Y-direction)", 'yellow'))
        print(colored("  2) Horizontal Load (X-direction)", 'yellow'))
        print(colored("  3) Angled Load (Force & Angle)", 'yellow'))
        load_type = input(colored("Enter your choice (1, 2, or 3) ➔ ", 'cyan'))

        if load_type == '1':  # Vertical load: only Y-force provided
            y_force = float(input("Enter Y-force (kN): ➔ "))
            pointload_list.append([pos, 0, y_force])
        elif load_type == '2':  # Horizontal load: only X-force provided
            x_force = float(input("Enter X-force (kN): ➔ "))
            pointload_list.append([pos, x_force, 0])
        elif load_type == '3':  # Angled load: convert force to components
            force_mag = float(input("Enter Force magnitude (kN): ➔ "))
            angle = float(input("Enter angle (degrees): ➔ "))
            x_force = force_mag * np.cos(np.radians(angle))
            y_force = force_mag * np.sin(np.radians(angle))
            pointload_list.append([pos, x_force, y_force])
        else:
            print_error("Invalid choice! Please enter 1, 2, or 3.")
            continue

    # --- Distributed Loads (UDL) ---
    num_udl = int(input("\nHow many UDL loads do you want to input? ➔ "))
    for i in range(num_udl):
        print(f"\n--- UDL {i+1} ---")
        start = float(input("Enter start position (m): ➔ "))
        end = float(input("Enter end position (m): ➔ "))
        intensity = float(input("Enter load intensity (kN/m): ➔ "))
        distributedload_list.append([start, end, intensity])

    # --- Moment Loads ---
    num_mom = int(input("\nHow many point moments do you want to input? ➔ "))
    for i in range(num_mom):
        print(f"\n--- Moment Load {i+1} ---")
        pos = float(input("Enter position (m): ➔ "))
        moment = float(input("Enter moment magnitude (kNm): ➔ "))
        momentload_list.append([pos, moment])
    
    # --- Triangular Loads (unused currently) ---
    triangleload_list = []

    print("")
    return {
        "pointloads": pointload_list,
        "distributedloads": distributedload_list,
        "momentloads": momentload_list,
        "triangleloads": triangleload_list
    }


# ================================
# Main Program Execution
# ================================

if __name__ == "__main__":
    print(colored("Welcome to Zylo-X Beam Calculator! 🚀", 'cyan', attrs=['bold']))
    print("")
    
    project_startup()

    if current_project:
        # --- Load Existing Beam Data ---
        print_title(f"Loading Project: {current_project['name']}")
        beam_length = current_project['beam_length']
        A = current_project['support_A_pos']
        B = current_project['support_B_pos']
        A_restraint = current_project['support_A_restraint']
        B_restraint = current_project['support_B_restraint']
        X_Field = np.array(current_project['X_Field'])
        Total_ShearForce = np.array(current_project['Total_ShearForce'])
        Total_BendingMoment = np.array(current_project['Total_BendingMoment'])
        Reactions = np.array(current_project['Reactions'])
        
        print_success(f"Loaded project '{current_project['name']}' successfully!")
        print("")
    else:
        # --- Initialize Empty Beam Data ---
        beam_length = None
        A = None
        B = None
        A_restraint = None
        B_restraint = None
        X_Field = None
        Total_ShearForce = None
        Total_BendingMoment = None
        Reactions = None

    while True:
        choice = main_menu()

        if choice == '1':
            print_title("Simple Beam Solver 🏗️")
            try:
                # --- Get Beam and Support Data ---
                beam_length = Beam_Length()
                A, B, A_restraint, B_restraint = Beam_Supports()

                # --- Get Load Data from the User ---
                loads_dict = get_user_loads()
                # Format loads for plotting
                loads = Plotting.format_loads_for_plotting(loads_dict)

                # Extract load lists for the solver
                pointloads = loads_dict["pointloads"]
                distributedloads = loads_dict["distributedloads"]
                momentloads = loads_dict["momentloads"]
                triangleloads = loads_dict["triangleloads"]

                # --- Call the Solver with Dynamic Loads ---
                X_Field, Total_ShearForce, Total_BendingMoment, Reactions = Solver.solve_simple_beam(
                    beam_length, A, B,
                    pointloads_in = pointloads,
                    distributedloads_in = distributedloads,
                    momentloads_in = momentloads,
                    triangleloads_in = triangleloads
                )

                # --- Print Calculated Reactions ---
                Va = Reactions[0]
                Ha = Reactions[1]
                Vb = Reactions[2]

                print_success("\nBeam Solved Successfully! 🚀")
                print(colored("Support Reactions:", 'cyan'))
                print(colored(f"  Va = {Va:.2f} kN", 'green'))
                print(colored(f"  Ha = {Ha:.2f} kN", 'green'))
                print(colored(f"  Vb = {Vb:.2f} kN", 'green'))
                print("")

                # --- Define Support Types (for now, fixed) ---
                support_types = ("pin", "roller")

                # --- Call the Plotting Functions ---
                beam_plot.plot_beam_schematic(beam_length, A, B, support_types, loads)
                beam_plot.plot_reaction_diagram(A, B, [Va, Ha, Vb],support_types)
                print("")

                # --- Save the Project if Desired ---
                save_decision = input(colored("Do you want to save this solved beam? (Y/N) ➔ ", 'cyan'))
                print("")
                if save_decision.lower() == 'y':
                    save_project(beam_length, A, B, A_restraint, B_restraint,
                                 X_Field, Total_ShearForce, Total_BendingMoment, Reactions)
                    save_projects_to_disk()
                else:
                    print(colored("Beam not saved. Continuing...", 'yellow'))
                    print("")

            except Exception as e:
                print_error(f"Error: {str(e)}")
                print("")
                continue

        elif choice == '2':
            print_title("Plotting Diagrams 📊")
            if X_Field is None or Total_ShearForce is None or Total_BendingMoment is None:
                print_error("No solved beam found! Please solve a beam first before plotting.")
                print("")
                continue

            Style = input(colored("Select Plotting Style (M/Matplotlib - P/Plotly) ➔ ", 'cyan'))
            print("")
            if Style.lower() == 'm':
                Plotting.Matplot_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment)
            elif Style.lower() == 'p':
                Plotting.Plotly_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment, beam_length)
            else:
                print_error("Invalid choice! Please select either 'M' or 'P'.")
                print("")
                continue

        elif choice == '3':
            print_title("Moment of Inertia (MOI) Calculator 📏")
            moi_solver.inertia_moment_square(2)
            print("")

        elif choice == '0':
            print_success("Thanks for using Zylo-X Beam Calculator! Goodbye 🚀")
            print("")
            break

        else:
            print_error("Invalid choice! Please select a valid option.")
            print("")