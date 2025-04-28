# cli.py
from termcolor import colored
import json
# Import your modules
import Solver
import Plotting
import moi_solver
import numpy as np
import beam_plot
# ================================
#    GLOBAL STORAGE
# ================================

beam_storage = []  # List to hold all projects
current_project = None  # Dict to hold the currently loaded project
#================
#Startup Menu :
#================
def project_startup():
    global current_project

    print_title("Zylo-X Beam Calculator Startup ⚙️")

    print_option("1) Start New Project")
    print_option("2) Load Existing Project")
    
    choice = input(colored("\nEnter your choice ➔ ", 'cyan'))

    if choice == '1':
        current_project = None  # New empty project
        print_success("Starting a new project...")

    elif choice == '2':
        load_projects_from_disk()
        if not beam_storage:
            print_error("No saved projects available! Starting new project instead.")
            current_project = None

        else:
            print(colored("\nAvailable Projects:", 'yellow'))
            for idx, proj in enumerate(beam_storage):
                print(f" {idx+1}) {proj['name']}")

            try:
                proj_choice = int(input(colored("\nEnter the number of the project you want to load ➔ ", 'cyan')))
                current_project = beam_storage[proj_choice-1]
                print_success(f"Project '{current_project['name']}' loaded successfully!")
            except (IndexError, ValueError):
                print_error("Invalid choice! Starting new project instead.")
                current_project = None
    else:
        print_error("Invalid choice! Starting new project by default.")
        current_project = None
# ================================
#    Data Saving and Loading
# ================================
def save_project(beam_length, A, B, A_restraint, B_restraint, X_Field, Total_ShearForce, Total_BendingMoment, Reactions):
    global beam_storage
    global current_project
    project_name = input(colored("\nEnter a name for this project ➔ ", 'cyan'))

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

    
# ================================
#    HELPER FUNCTIONS
# ================================

def safe_serialize(obj):
    """Convert non-JSON serializable objects like numpy arrays to lists."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, tuple):
        return list(obj)
    else:
        return obj
# ================================
#    Save to JSON

def save_projects_to_disk():    
    global beam_storage
    with open('beam_projects.json', 'w') as file:
        json.dump(beam_storage, file)
    print_success("All projects saved to disk successfully! 📂")
# ================================
#    Load from JSON
def load_projects_from_disk():
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


def print_title(title):
    print(colored(f"\n=== {title} ===\n", 'cyan', attrs=['bold']))

def print_option(option):
    print(colored(option, 'yellow'))

def print_error(error_msg):
    print(colored(error_msg, 'red', attrs=['bold']))

def print_success(msg):
    print(colored(msg, 'green'))

def main_menu():
    print_title("Welcome to Zylo-X Beam Calculator 🏗️")

    print_option("1) Solve Simple Beam (Reactions, SFD, BMD)")
    print_option("2) Plot Diagrams (Matplotlib / Plotly)")
    print_option("3) Calculate Moment of Inertia (MOI)")
    print_option("0) Exit")

    choice = input(colored("\nEnter your choice ➔ ", 'cyan'))
    return choice

# ===================================================================================
#Input Data
def Beam_Length():
    beam_length = float(input(colored("Enter Beam Length (meters): ➔ ", 'cyan')))
    if beam_length <= 0:
        raise ValueError("Beam length must be positive.")
    return beam_length

def Beam_Supports():
    A = float(input(colored("\nEnter Position of Support A (meters): ➔ ", 'cyan')))
    print(colored("Choose Support A Type:", 'yellow'))
    print(colored("  1) Pin Support", 'yellow'))
    print(colored("  2) Roller Support", 'yellow'))
    A_type_choice = input(colored("Enter your choice (1 or 2) ➔ ", 'cyan'))
    A_restraint = (1, 1, 0) if A_type_choice == '1' else (0, 1, 0)
    B = float(input(colored("\nEnter Position of Support B (meters): ➔ ", 'cyan')))
    print(colored("Choose Support B Type:", 'yellow'))
    print(colored("  1) Pin Support", 'yellow'))
    print(colored("  2) Roller Support", 'yellow'))
    B_type_choice = input(colored("Enter your choice (1 or 2) ➔ ", 'cyan'))
    B_restraint = (0, 1, 0) if B_type_choice == '1' else (1, 1, 0) 
    if A <= 0 or B <= 0:
        raise ValueError("Support positions must be positive.")
    if A >= B:
        raise ValueError("Support A must be to the left of Support B.")
    return A, B , A_restraint, B_restraint
# ===================================================================================
# MAIN PROGRAM START
# ===================================================================================

if __name__ == "__main__":
    print(colored("Welcome to Zylo-X Beam Calculator! 🚀", 'cyan', attrs=['bold'])
          )
    project_startup()
    if current_project:
        # --- Load Existing Beam Data ---
        print_title(f"Loading Project: {current_project['name']}")
        beam_length = current_project['beam_length']
        A = current_project['support_A_pos']
        B = current_project['support_B_pos']
        A_restraint = current_project['support_A_restraint']
        B_restraint = current_project['support_B_restraint']
        X_Field =  np.array(current_project['X_Field'])
        Total_ShearForce =  np.array(current_project['Total_ShearForce'])
        Total_BendingMoment =  np.array(current_project['Total_BendingMoment'])
        Reactions = np.array(current_project['Reactions'])
        print_success(f"Loaded project '{current_project['name']}' successfully!")

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
                  # --- Get Beam Length ---
                beam_length = Beam_Length()
                                
                # --- Get Support A ---
                A, B, A_restraint, B_restraint = Beam_Supports()

                # --- Call Solver ---
                X_Field, Total_ShearForce, Total_BendingMoment, Reactions  = Solver.solve_simple_beam(beam_length, A, B)    
                # --- Print Reactions ---
                Va = Reactions[0]
                Ha = Reactions[1]
                Vb = Reactions[2]    

                print_success("\nBeam Solved Successfully! 🚀")
                print(colored(f"Support Reactions:", 'cyan'))
                print(colored(f"  Va = {Va:.2f} kN", 'green'))
                print(colored(f"  Ha = {Ha:.2f} kN", 'green'))
                print(colored(f"  Vb = {Vb:.2f} kN", 'green'))

            # --- Plot Beam Schematic Automatically ---
                # Dummy Loads for Now: (Later we let user input them too!)
                loads = [
                    ("point_load", 2.5, -8),  # Example: 8kN downward at 2.5 meters
                    ("udl", 1.5, 4.5, -2),    # Example: 2kN/m UDL from 1.5m to 4.5m
                    ("moment", 5.0, 15)       # Example: 15kNm clockwise at 5m
                ]

                support_types = ("pin", "roller")  # For now, fixed

                beam_plot.plot_beam_schematic(
                    X_Field=X_Field,
                    beam_length=beam_length,
                    A=A,
                    B=B,
                    support_types=support_types,
                    loads=loads,
                    reactions=[Va, Ha, Vb]
                )




                save_decision = input(colored("\nDo you want to save this solved beam? (Y/N) ➔ ", 'cyan'))
                if save_decision.lower() == 'y':
                    save_project(beam_length, A, B, A_restraint, B_restraint, X_Field, Total_ShearForce, Total_BendingMoment, Reactions)
                    save_projects_to_disk()
                else:
                    print(colored("Beam not saved. Continuing...", 'yellow'))                                      
            except Exception as e:
                print_error(f"Error: {str(e)}")
                continue
            
        elif choice == '2':
            print_title("Plotting Diagrams 📊")

            if X_Field is None or Total_ShearForce is None or Total_BendingMoment is None:
                print_error("No solved beam found! Please solve a beam first before plotting.")
                continue

            Style = input(colored("\nSelect Ploting Style (M/Matplotlib - P/Plotly) ➔ ", 'cyan'))
            if Style.lower() == 'm':
                Plotting.Matplot_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment)
            elif Style.lower() == 'p':
                Plotting.Plotly_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment, beam_length)
            else:
                print_error("Invalid choice! Please select either 'M' or 'P'.")
                continue

        elif choice == '3':
            print_title("Moment of Inertia (MOI) Calculator 📏")
            moi_solver.inertia_moment_square(2)

        elif choice == '0':
            print_success("Thanks for using Zylo-X Beam Calculator! Goodbye 🚀")
            break
        else:
            print_error("Invalid choice! Please select a valid option.")
