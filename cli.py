# cli.py

from calendar import c
from termcolor import colored,cprint
import json
import numpy as np
import os
import time     
# Import application modules
from Materials_database import MaterialDatabase  # Import the MaterialDatabase class
import Solver
import Plotting
import moi_solver
import beam_plot
# ================================
# Global Storage
# ================================
beam_storage = []      # List to hold all projects
current_project = None # Dictionary to hold the currently loaded project
Materials = None # Placeholder for the materials database object
# ================================
# Startup Menu Functions
# ================================
# ----------------------------------------------------------------
# Sub-Menu: Project Management
# ----------------------------------------------------------------
def project_management_menu():
    clear_screen()
    print_title("_________ Project Management _________")
    print_option("1 - New Project")
    print_option("2 - Load Project")
    print_option("3 - Delete Project")
    print_option("4 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice
# ----------------------------------------------------------------
def New_Project():
    global current_project
    # Start a new project
    current_project = None  # New empty project
    print_success("Starting a new project...")
    time.sleep(2)   # Pause for 2 second
            
def load_project():
    global current_project
    # Load an existing project
    load_projects_from_disk()

    if not beam_storage:
        print_error("No saved projects available! Starting new project instead.")
        current_project = None
        time.sleep(2)   # Pause for 2 second
    else:
        print(colored("\nAvailable Projects:", 'yellow'))
        for idx, proj in enumerate(beam_storage):
            print(f" {idx+1}) {proj['name']}")
        print("")
        try:
            proj_choice = int(input(colored("Enter the number of the project you want to load ➔ ", 'cyan')))
            current_project = beam_storage[proj_choice - 1]
            print_success(f"Project '{current_project['name']}' loaded successfully!")
            time.sleep(2)   # Pause for 2 second
        except (IndexError, ValueError):
            print_error("Invalid choice! Starting new project instead.")
            current_project = None
            time.sleep(2)   # Pause for 2 second


def delete_project():
    """
    Delete an existing project from global storage and update the JSON file.
    After performing the deletion (or cancellation), the user will be prompted to
    return to the Project Management menu.
    """
    global beam_storage

    # Load the latest projects from disk
    load_projects_from_disk()
    
    if not beam_storage:
        print_error("No saved projects available to delete!")
        input("Press Enter to return to the Project Management menu...")
        return

    # List available projects
    print_title("Delete Project")
    print_option("Select a project to delete:")
    
    for idx, project in enumerate(beam_storage):
        print_option(f"  {idx + 1}. {project['name']}")
    
    print("")  # Blank line for spacing
    
    try:
        selection = int(input(colored("Enter the project number you want to delete ➔ ", 'cyan')))
        if selection < 1 or selection > len(beam_storage):
            print_error("Invalid project number. Operation cancelled.")
            input("Press Enter to return to the Project Management menu...")
            return
        
        # Retrieve the selected project and confirm deletion
        project_to_delete = beam_storage[selection - 1]
        confirmation = input(colored(f"Are you sure you want to delete project '{project_to_delete['name']}'? (Y/N): ", 'cyan'))
        
        if confirmation.lower() == 'y':
            # Remove the project from storage
            del beam_storage[selection - 1]
            
            # Write the updated list back to the JSON file
            with open('beam_projects.json', 'w') as file:
                json.dump(beam_storage, file)
            
            print_success(f"Project '{project_to_delete['name']}' deleted successfully!")
        else:
            print("Deletion cancelled.")
    
    except ValueError:
        print_error("Invalid input! Please enter a valid number.")

    print("")
    input("Press Enter to return to the Project Management menu...")
# ----------------------------------------------------------------
# Sub-Menu: Profile Definition
# ----------------------------------------------------------------
def profile_definition_menu():
    clear_screen()
    print_title("_________ Profile Definition _________")
    print_option("1 - Enter Beam Length (m)")
    print_option("2 - Define Profile")
    print_option("3 - View Current Profile")
    print_option("4 - Return to Main Menu")
    print("")       
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice
# ----------------------------------------------------------------
def choose_profile():
    """
    Display the available profile options in a neat style and prompt
    the user to select their preferred profile by number.
    
    Returns:
        profile_choice (str): The number representing the chosen profile.
    """
    print_title("Available Profiles")
    print_option("1 - I-beam")
    print_option("2 - T-beam")
    print_option("3 - Solid Circle")
    print_option("4 - Hollow Circle")
    print_option("5 - Square")
    print_option("6 - Hollow Square")
    print_option("7 - Rectangle")
    print_option("8 - Hollow Rectangle")
    print("")  # Blank line for spacing
    profile_choice = input(colored("Enter your preferred profile number ➔ ", 'cyan'))
    return profile_choice
# ----------------------------------------------------------------
# Sub-Menu: Material Selection
# ----------------------------------------------------------------
def material_selection_menu():
    load_material_database()
    clear_screen()
    print_title("_________ Material Selection _________")
    print_option("1 - Select Material")
    print_option("2 - View Current Material Details")
    print_option("3 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice
# ----------------------------------------------------------------
def load_material_database():
    """
    Initialize and load the material database, storing it in the global variable 'Materials'.
    """
    global Materials
    json_filename = "Materials.json" 
    try:
        Materials = MaterialDatabase(json_filename)
    except Exception as e:
        print_error(f"Error loading the materials database: {e}")
        time.sleep(3)   # Pause for 1 second
# ----------------------------------------------------------------
def select_material():
    """
    Print all materials from the loaded Materials database in one-line format
    and allow the user to select one by entering the corresponding number.
    
    Returns:
        dict: The selected material dictionary, or None if invalid input.
    """
    global Materials
    if Materials is None:
        print_error("Materials database is not loaded!")
        return None

    # Get the full materials list from the database.
    materials_list = Materials.materials
    print_title("Select a Material")
    cprint("-------------------------------------------------------------------------------------------------------------","red")
    cprint("Density (kg/m³), Yield Strength (MPa), Ultimate Strength (MPa), Elastic Modulus (GPa), Poisson Ratio","white")
    cprint("-------------------------------------------------------------------------------------------------------------","red")
    print("")  # Blank line for spacing
    for index, material in enumerate(materials_list):
        properties_line = ", ".join(
        [f"{key}: {value}" for key, value in material.items() if key != "Material"]
        )
        # Print index, material name, and its properties all in one line.
        print(colored(f"{index + 1} - {material['Material']}","light_yellow"))  
        print(colored(f"{properties_line}", 'white'))
        print("")  # Blank line for spacing

    # Prompt the user for selection
    selection = input(colored("Enter the number of the material you want to select ➔ ", 'cyan'))
    try:
        idx = int(selection) - 1
        if idx < 0 or idx >= len(materials_list):
            print_error("Invalid selection!")
            return None
        selected_material = materials_list[idx]
        print_success(f"You selected: {selected_material['Material']}")
        # Extract only the required properties.
        key_props = {
            "Material": selected_material.get("Material"),
            "Density": selected_material.get("Density"),
            "Yield Strength": selected_material.get("Yield Strength"),
            "Ultimate Strength": selected_material.get("Ultimate Strength"),
            "Elastic Modulus": selected_material.get("Elastic Modulus"),
            "Poisson Ratio": selected_material.get("Poisson Ratio"),
        }

        return key_props

    except ValueError:
        print_error("Invalid input. Please enter a valid number.")
        return None
# ----------------------------------------------------------------
# Sub-Menu: Boundary Conditions
# ----------------------------------------------------------------
def boundary_conditions_menu():
    clear_screen()
    print_title("_________ Boundary Conditions _________")
    print_option("1 - Define Supports")
    print_option("2 - View Supports")
    print_option("3 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice

# ----------------------------------------------------------------
# Sub-Menu: Loads Definition
# ----------------------------------------------------------------
def loads_definition_menu():
    clear_screen()
    print_title("_________ Loads Definition _________")
    print_option("1 - Define Loads")
    print_option("2 - View Loads")
    print_option("3 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice

# ----------------------------------------------------------------
# Sub-Menu: Analysis/Simulation
# ----------------------------------------------------------------
def analysis_simulation_menu():
    clear_screen()
    print_title("_________ Analysis/Simulation _________")
    print_option("1 - Solve Beam")
    print_option("2 - View Analysis Results")
    print_option("3 - Calculate Stress and F.O.S")
    print_option("4 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice
#__________________________________________________________

def first_moment_of_area_rect(b, y_array):
    """
    b: Width of the section (m)
    y: Vertical distance from neutral axis to point of interest (m)
    Returns Q in m^3
    """
    Q_array = b * np.abs(y_array) * (np.abs(y_array) / 2)
    return Q_array

def calculate_shear_stress(Total_ShearForce, Q_array, Ix, b):
    """
    V: Shear force at point (N)
    Q: First moment of area above/below point (m^3)
    I: Moment of inertia (m^4)
    b: Width of the section at point (m)
    Returns shear stress (Pa)
    """
    tau_array = Total_ShearForce * Q_array / (Ix * b)
    return tau_array


def calculate_bending_stress(M, c, Ix):
    """
    M: Bending moment (N·m)
    c: Distance from neutral axis to outermost fiber (m)
    Ix: Moment of inertia (m^4)
    Returns bending stress (Pa)
    """
    sigma = M * c / Ix
    return sigma

def calculate_FOS(yield_strength, sigma):
    """
    yield_strength: Yield strength of the material (MPa)
    sigma: Bending stress (Pa)
    Returns Factor of Safety (FOS)
    """
    FOS = yield_strength / sigma
    return FOS

def Factor_of_Safety(Total_BendingMoment, c,yield_strength,Ix):

    M_max_kNm = np.max(np.abs(Total_BendingMoment))
    M_max = M_max_kNm * 1000    # Convert to N·m
    sigma_Pa = calculate_bending_stress(M_max, c, Ix)
    sigma_MPa = sigma_Pa / 1e6  # Convert to MPa if desired
    yield_strength_MPa = yield_strength
    FOS = calculate_FOS(yield_strength_MPa, sigma_MPa)
    print(f"Maximum bending moment (N·m): {M_max:.2f}")
    print(f"Bending stress (MPa): {sigma_MPa:.2f}")
    print(f"Factor of Safety: {FOS:.2f}")

# ================================
# Data Saving and Loading Functions
# ================================

def save_project(beam_length, A, B, A_restraint, B_restraint,
                 X_Field, Total_ShearForce, Total_BendingMoment, Reactions,A_type,B_type):
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
        'support_A_type': A_type,
        'support_B_type': B_type,
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
    A_type = ""
    B_type = ""
    if A_type_choice == '1':
        A_restraint = (1, 1, 0)
        A_type ="Pin Support" 
    else :
        A_restraint = (0, 1, 0)
        A_type ="Roller Support" 
     
    B = float(input(colored("Enter Position of Support B (meters): ➔ ", 'cyan')))
    print(colored("Choose Support B Type:", 'yellow'))
    print(colored("  1) Pin Support", 'yellow'))
    print(colored("  2) Roller Support", 'yellow'))
    B_type_choice = input(colored("Enter your choice (1 or 2) ➔ ", 'cyan'))
    if B_type_choice == '1':
        B_restraint = (1, 1, 0)
        B_type ="Pin Support" 
    else :
        B_restraint = (0, 1, 0)
        B_type ="Roller Support" 

    if A <= 0 or B <= 0:
        raise ValueError("Support positions must be positive.")
    if A >= B:
        raise ValueError("Support A must be to the left of Support B.")
    
    print("")
    return A, B, A_restraint, B_restraint, A_type, B_type


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

# ----------------------------------------------------------------
# Utility Function: Clear the Terminal Screen
# ----------------------------------------------------------------
def clear_screen():
    """
    Clear the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# ----------------------------------------------------------------
# Extended Main Menu Template
# ----------------------------------------------------------------
def main_menu_template():
    """
    Display the extended main menu and return the user's selection.
    """
    clear_screen()
    print_title("Main Menu")
    print_option("1 - Project Management")
    print_option("2 - Profile Definition")
    print_option("3 - Material Selection")
    print_option("4 - Boundary Conditions")
    print_option("5 - Loads Definition")
    print_option("6 - Analysis/Simulation")
    print_option("7 - Postprocessing/Visualization")
    print_option("8 - Save Project")
    print("")
    selection = input(colored("Enter your selection: ➔ ", 'cyan'))
    return selection


# ----------------------------------------------------------------
# Sub-Menu: Postprocessing/Visualization
# ----------------------------------------------------------------
def postprocessing_menu():
    clear_screen()
    print_title("_________ Postprocessing/Visualization _________")
    print_option("1 - SFD/BMD Plots (Matplotlib)")
    print_option("2 - SFD/BMD Plots (Plotly)")
    print_option("3 - Stress/F.O.S Contours")
    print_option("4 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice


# ----------------------------------------------------------------
# Sub-Menu: Save Project
# ----------------------------------------------------------------
def save_project_menu():
    clear_screen()
    print_title("_________ Save Project _________")
    print_option("1 - Save Current Project")
    print_option("2 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice


# ----------------------------------------------------------------
# Extended Main Menu Runner
# ----------------------------------------------------------------
def run_extended_menu():
    global current_project
    load_material_database()
    Support_defined = False
    """
    Run the extended main menu. Depending on the user's selection,
    display the corresponding sub-menu (or a placeholder for future functions).
    """
    while True:
        selection = main_menu_template()
        if selection == '1':
             while True:
    
                sub_choice = project_management_menu()
                if sub_choice == '4':  # Return to main menu
                    break
                else:

                    # based on the sub_choice
                    if sub_choice == '1':
                            # Start a new project
                            New_Project()
                            break

                    elif sub_choice == '2':
                        # Load an existing project
                        load_project()
                        break

                    elif sub_choice == '3':
                        delete_project()
                    else:
                     print_error("Invalid selection! Please try again.")
                     time.sleep(1)   # Pause for 1 second

        elif selection == '2':
            while True:
                sub_choice = profile_definition_menu()
                if sub_choice == '4':  # Return to main menu
                    break
                else:
                    if sub_choice == '1':  # Enter Beam Length
                        beam_length = Beam_Length()

                    elif sub_choice == '2':  # Define Profile   b: Width of the section at point (m) - C: Neutral Axis Distance (m)
                        profile_choice = choose_profile()
                        if profile_choice == '1':
                            print("I-beam profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_ibeam()
                            time.sleep(2)   # Pause for 2 second
                        elif profile_choice == '2':
                            print("T-beam profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_tbeam()
                            time.sleep(2)   # Pause for 2 second
                        elif profile_choice == '3':
                            print("Solid Circle profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_circle()
                            time.sleep(2)   # Pause for 2 second
                        elif profile_choice == '4':
                            print("Hollow Circle profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_circle()
                            time.sleep(2)   # Pause for 2 second
                        elif profile_choice == '5':
                            print("Square profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_square()
                            time.sleep(2)   # Pause for 2 second
                        elif profile_choice == '6':
                            print("Hollow Square profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_hollow_square()
                            time.sleep(2)   # Pause for 2 second
                        elif profile_choice == '7':
                            print("Rectangle profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_rectangle()
                            time.sleep(2)   # Pause for 2 second
                        elif profile_choice == '8':
                            print("Hollow Rectangle profile selected.")
                            Ix,shape,c,b,y_array = moi_solver.inertia_moment_hollow_rectangle()
                            time.sleep(2)
                        else:
                            print_error("Invalid choice! Please try again.")

                    else:
                        print("")
                        print(f'{shape} profile is selected')
                        print("Current Profile Details: ")
                        print("")
                        print(colored(f"Calculated Ix for {shape} Profile is : {Ix:.6e} m^4", 'green'))
                        print("----------------------------------------------------------------------")
                        input("Press Enter to return to the Profile Definition menu...")
                        
        elif selection == '3':
            while True:
                sub_choice = material_selection_menu()
                if sub_choice == '3':
                    break
                else:
                    if sub_choice == '1':
                        selected_material = select_material()
                        if selected_material:
                            density = float(selected_material["Density"])
                            yield_strength = float(selected_material["Yield Strength"])
                            ultimate_strength = float(selected_material["Ultimate Strength"])
                            elastic_modulus = float(selected_material["Elastic Modulus"])
                            poisson_ratio = float(selected_material["Poisson Ratio"])
                            shear_yield_strength = float(0.55 * yield_strength)
                            time.sleep(1)
                    elif sub_choice == '2':
                        print(f"Current Material Details :")
                        print("")
                        print(f"Material Name: {selected_material['Material']}")
                        print(f"The Density is: {density},kg/m³")
                        print(f"The Yield Strength is: {yield_strength},MPa")
                        print(f"The Ultimate Strength is: {ultimate_strength},MPa")
                        print(f"The Elastic Modulus is: {elastic_modulus},GPa")
                        print(f"The Poisson Ratio is: {poisson_ratio}")
                        print(f"The Shear Yield Strength is: {shear_yield_strength},MPa")
                        print("")
                        print("----------------------------------------------------------------------")
                        input("Press Enter to return to the Material Selection menu...")

                    else:
                        print_error("Invalid selection! Please try again.")
                        time.sleep(2)

        elif selection == '4':
            while True:
                sub_choice = boundary_conditions_menu()
                if sub_choice == '3':
                    break
                else:
                    if sub_choice == '1':
                        A, B, A_restraint, B_restraint, A_type, B_type = Beam_Supports()
                        print(f"Support A: {A} m, Type: {A_type}")
                        print(f"Support B: {B} m, Type: {B_type}")
                        print("")
                        input("Press Enter to return to the Boundary Conditions menu...")
                        Support_defined = True
                    elif sub_choice == '2':
                        if Support_defined == False:
                            print_error("No supports defined yet!")
                            time.sleep(2)
                        else:
                            print(f"Current Support Details:")
                            print("")
                            print(f"Support A: {A} m, Type: {A_type},restraint :{A_restraint}")
                            print(f"Support B: {B} m, Type: {B_type},restraint :{B_restraint}")                            
                        print("")
                        input("Press Enter to return to the Boundary Conditions menu...")

                    else:
                        print_error("Invalid selection! Please try again.")
                        time.sleep(2)


        elif selection == '5':
            while True:   
                sub_choice = loads_definition_menu()
                if sub_choice == '3':
                    break
                else:
                    if sub_choice== '1':
                        print("Define Loads:")
                        loads_dict = get_user_loads()
                        # Extract load lists for the solver
                        pointloads = loads_dict["pointloads"]
                        distributedloads = loads_dict["distributedloads"]
                        momentloads = loads_dict["momentloads"]
                        triangleloads = loads_dict["triangleloads"]
                        print("Loads defined successfully!")
                        time.sleep(2)

                    elif sub_choice == '2':
                        try:
                            print("Current Loads:")
                            print("")
                            print(f"Point Loads: {pointloads}")
                            print(f"Distributed Loads: {distributedloads}")
                            print(f"Moment Loads: {momentloads}")
                            print(f"Triangle Loads: {triangleloads}")
                            print("")
                        except :
                            print_error("No loads defined yet!")
                            time.sleep(2)
                            continue

                        input("Press Enter to return to the Loads Definition menu...")
                    else:
                        print_error("Invalid selection! Please try again.")
                        time.sleep(2)

        elif selection == '6':
            while True:
                
                sub_choice = analysis_simulation_menu()
                if sub_choice == '4':
                    break
                else:
                    if sub_choice == '1':
                         print("Solver informations : ")
                         print("")
                         print("Beam Length: ", beam_length)
                         print("Number of Divisions = 10000")
                         print("Support A Position: ", A)
                         print("Support B Position: ", B)
                         print("Support A Type: ", A_type)
                         print("Support B Type: ", B_type)
                         print("Point Loads: ", pointloads)
                         print("Distributed Loads: ", distributedloads)
                         print("Moment Loads: ", momentloads)
                         print("Triangle Loads: ", triangleloads)
                         print("")
                         cprint("---------------------------------------------------------", 'red')
                         print("Calculating reactions, shear force, and bending moment...")
                            # --- Solve the beam problem ---
                            # Call the solver function with the defined parameters
                         X_Field, Total_ShearForce, Total_BendingMoment, Reactions = Solver.solve_simple_beam(
                            beam_length, A, B,
                            pointloads_in = pointloads,
                            distributedloads_in = distributedloads,
                            momentloads_in = momentloads,
                            triangleloads_in = triangleloads)
                         # --- Print Calculated Reactions ---
                         Va = Reactions[0]
                         Ha = Reactions[1]
                         Vb = Reactions[2]
                         max_shear = round(np.max(Total_ShearForce), 3)
                         min_shear = round(np.min(Total_ShearForce), 3)
                         max_bending = round(np.max(Total_BendingMoment), 3)
                         min_bending = round(np.min(Total_BendingMoment), 3)

                         print("Beam analysis completed successfully!")
                         time.sleep(2)

                    elif sub_choice == '2':
                        if Reactions is None:
                            print_error("No analysis results available yet!")
                            time.sleep(2)
                        else:
                            print("Analysis Results:")
                            cprint("---------------------------------------------------------", 'red')
                            print("")
                            print(f"Reactions: Rv-A : {Va}")
                            print(f"Reactions: Rh-A : {Ha}")
                            print(f"Reactions: Rv-B : {Vb}")
                            print(f"Max Shear Force: {max_shear} kN")
                            print(f"Min Shear Force: {min_shear} kN")
                            print(f"Max Bending Moment: {max_bending} kNm")
                            print(f"Min Bending Moment: {min_bending} kNm")
                            print("")   
                            print("---------------------------------------------------------")
                    elif sub_choice =='3':
                            Q_array=first_moment_of_area_rect(b, y_array)
                            Total_stress = calculate_shear_stress(Total_ShearForce, Q_array, Ix, b)
                            Max_stress = np.max(Total_stress)
                        # Calculate Stress and F.O.S

        elif selection == '7':
            sub_choice = postprocessing_menu()
            if sub_choice == '4':
                continue
            else:
                print(f"Postprocessing/Visualization Option {sub_choice} selected. (Functionality placeholder)")
                input("Press Enter to return to the main menu...")
        elif selection == '8':
            sub_choice = save_project_menu()
            if sub_choice == '2':
                continue
            else:
                print(f"Save Project Option {sub_choice} selected. (Functionality placeholder)")
                input("Press Enter to return to the main menu...")
        else:
            print_error("Invalid selection! Please try again.")
            input("Press Enter to return to the main menu...")


# ================================
# Main Program Execution
# ================================

if __name__ == "__main__":
    # You can call run_extended_menu() here to use the new template.
    run_extended_menu()