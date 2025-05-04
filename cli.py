#!/usr/bin/env python3
"""
CLI for Zylo-X Beam Calculator
===================================
This script provides a command-line interface (CLI) for the Zylo-X Beam Calculator.
It handles project management, profile and material selection, boundary conditions,
load definitions, analysis, postprocessing, and project save/load functionalities.
"""
# modules
import json
import numpy as np
import time
from termcolor import colored, cprint

# Application modules
from Materials_database import MaterialDatabase  # Import MaterialDatabase class
from Solver import solve_simple_beam
import moi_solver
from Plotting import (Matplot_Deflection, Plotly_Deflection, Plotly_sfd_bmd, Matplot_sfd_bmd, format_loads_for_plotting, Plotly_ShearStress,Matplot_ShearStress,
                      Plotly_combined_diagrams,Matplot_combined)
from beam_plot import plot_reaction_diagram, plot_beam_schematic
from Stress_solver import (calculate_beam_deflection, first_moment_of_area_rect, calculate_shear_stress,
                         calculate_bending_stress, Factor_of_Safety)
from Menus import (main_menu_template, project_management_menu, profile_definition_menu, choose_profile,
                 material_selection_menu, boundary_conditions_menu, loads_definition_menu, analysis_simulation_menu,
                 postprocessing_menu, print_success, print_error, print_option, print_title, clear_screen)
from inputs import Beam_Length, Beam_Supports, manage_loads,Beam_Classification

# -----------------------------
# Global Storage Variables
# -----------------------------
beam_storage = []      # List to hold all saved projects
current_project = None # Dictionary holding the currently loaded project
Materials = None       # Placeholder for the materials database object
beam_length = 0.0
A = 0.0
B = 0.0
A_restraint = []
B_restraint = []
A_type = ""
B_type = ""
X_Field = np.array([])
Total_ShearForce = np.array([])
Total_BendingMoment = np.array([])
Reactions = np.array([])
loads = {}
selected_material = ''
Ix = 0.0
shape = ""
c = 0.0
b = 0.0
y_array = np.array([])
project_state = {
    "is_loaded": False,
    "profile_saved": False, 
    "material_saved": False,
    "loads_saved": False,
    "supports_saved": False,
    "has_unsaved_changes": False
}
# -----------------------------

# =============================
# Project Management Functions
# =============================
def New_Project():
    """Start a new project by resetting the current project."""
    global current_project, project_state
    current_project = None  # Reset current project data
    
    # Reset project state flags
    project_state = {
        "is_loaded": False,
        "profile_saved": False, 
        "material_saved": False,
        "loads_saved": False,
        "supports_saved": False,
        "has_unsaved_changes": False
    }
    
    print_success("Starting a new project...")
    time.sleep(0.5)

# =============================
def safe_serialize(obj):
    """
    Convert non-JSON serializable objects to JSON-friendly types.
    
    Args:
        obj: Any object (e.g., numpy array, tuple).
    
    Returns:
        A list if object is numpy.ndarray or tuple; otherwise, returns object as is.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, tuple):
        return list(obj)
    return obj

# =============================
def load_project():
    """Load a project from storage into the current session."""
    global current_project, beam_length, A, B, A_restraint, B_restraint, A_type, B_type
    global X_Field, Total_ShearForce, Total_BendingMoment, Reactions, loads
    global Ix, shape, c, b, y_array, project_state
    global elastic_modulus, selected_material, density, yield_strength, ultimate_strength, poisson_ratio, shear_yield_strength
    global pointloads, distributedloads, momentloads, triangleloads

    load_projects_from_disk()

    if not beam_storage:
        print_error("No saved projects available! Starting a new project instead.")
        current_project = None
        time.sleep(2)
        return

    print(colored("\nAvailable Projects:", 'yellow'))
    for idx, proj in enumerate(beam_storage):
        print(f" {idx+1}) {proj['name']}")
    print("")

    try:
        proj_choice = int(input(colored("Enter the number of the project you want to load ➔ ", 'cyan')))
        current_project = beam_storage[proj_choice - 1]
        print_success(f"Project '{current_project['name']}' loaded successfully!")
        time.sleep(1)

        # Apply loaded project data to current state
        beam_length = current_project.get('beam_length', 0)
        A = current_project.get('support_A_pos', 0)
        B = current_project.get('support_B_pos', 0)
        A_restraint = current_project.get('support_A_restraint', [])
        B_restraint = current_project.get('support_B_restraint', [])
        A_type = current_project.get('support_A_type', '')
        B_type = current_project.get('support_B_type', '')

        # Load analysis data
        X_Field = np.array(current_project.get('X_Field', []))
        Total_ShearForce = np.array(current_project.get('Total_ShearForce', []))
        Total_BendingMoment = np.array(current_project.get('Total_BendingMoment', []))
        Reactions = np.array(current_project.get('Reactions', []))
        
        # Load and assign loads
        loads = current_project.get('loads', {})
        pointloads = loads.get("pointloads", [])
        distributedloads = loads.get("distributedloads", [])
        momentloads = loads.get("momentloads", [])
        triangleloads = loads.get("triangleloads", [])

        # Load profile data
        profile_data = current_project.get('profile', {})
        Ix = profile_data.get('Ix', 0)
        shape = profile_data.get('shape', '')
        c = profile_data.get('c', 0)
        b = profile_data.get('b', 0)
        y_array = np.array(profile_data.get('y_array', []))

        # Load material data
        material_data = current_project.get('material', {})
        if material_data and 'material' in material_data:
            selected_material = material_data.get('material', {})
            if selected_material:
                density = float(selected_material.get("Density", 0))
                yield_strength = float(selected_material.get("Yield Strength", 0)) * 1e6
                ultimate_strength = float(selected_material.get("Ultimate Strength", 0)) * 1e6
                elastic_modulus = float(selected_material.get("Elastic Modulus", 0)) * 1e9
                poisson_ratio = float(selected_material.get("Poisson Ratio", 0))
                shear_yield_strength = 0.55 * yield_strength
        else:
            selected_material = {}

        # Update project state flags
        project_state["is_loaded"] = True
        project_state["profile_saved"] = bool(shape) and Ix > 0
        project_state["material_saved"] = bool(selected_material)
        project_state["loads_saved"] = bool(loads)
        project_state["supports_saved"] = bool(A_type) and bool(B_type)
        project_state["has_unsaved_changes"] = False

        # Optional: Show confirmation summary
        print_loaded_project_summary()

    except (IndexError, ValueError):
        print_error("Invalid choice! Starting a new project instead.")
        current_project = None
        time.sleep(1)

# =============================
def print_loaded_project_summary():
    """Display a summary of the loaded project."""
    print(colored(f"\nLoaded Project Summary:", 'green'))
    print(f"Beam Length: {beam_length} m")
    print(f"Supports: A : {A} m ({A_type}), B : {B} m ({B_type})")
    
    # Enhanced profile information
    if shape:
        print(f"Profile: {shape} | Ix = {Ix:.2e} m⁴")
    else:
        print("Profile: Not defined")
        
    # Enhanced material information
    if selected_material:
        print(f"Material: {selected_material.get('Material')} | E = {elastic_modulus:.2e} Pa")
    else:
        print("Material: Not defined")
        
    # Show load information if available
    if loads:
        total_load_count = (len(loads.get("pointloads", [])) + 
                          len(loads.get("distributedloads", [])) + 
                          len(loads.get("momentloads", [])) + 
                          len(loads.get("triangleloads", [])))
        print(f"Loads: {total_load_count} total loads defined")
    else:
        print("Loads: None defined")
        
    print("")
    input(colored("Press Enter to continue...", 'cyan'))

# =============================
def modify_loaded_project_data():
    """Allow the user to modify specific aspects of a loaded project."""
    global project_state
    
    if not project_state["is_loaded"]:
        print_error("No project is currently loaded!")
        time.sleep(1)
        return
        
    while True:
        clear_screen()
        print_title("Modify Loaded Project Data")
        print_option("1. Edit profile data")
        print_option("2. Edit material selection")
        print_option("3. Edit boundary conditions")
        print_option("4. Edit loads")
        print_option("5. Return to project management")
        print("")
        
        choice = input(colored("Enter your choice ➔ ", 'cyan'))
        
        if choice == '1':
            project_state["profile_saved"] = False
            project_state["has_unsaved_changes"] = True
            print_success("Profile data can now be modified.")
            time.sleep(1)
            return
            
        elif choice == '2':
            project_state["material_saved"] = False
            project_state["has_unsaved_changes"] = True
            print_success("Material selection can now be modified.")
            time.sleep(1)
            return
            
        elif choice == '3':
            project_state["supports_saved"] = False
            project_state["has_unsaved_changes"] = True
            print_success("Boundary conditions can now be modified.")
            time.sleep(1)
            return
            
        elif choice == '4':
            project_state["loads_saved"] = False
            project_state["has_unsaved_changes"] = True
            print_success("Loads can now be modified.")
            time.sleep(1)
            return
            
        elif choice == '5':
            return
            
        else:
            print_error("Invalid selection! Please try again.")
            time.sleep(1)

# =============================
def delete_project():
    """
    Delete an existing project from storage.
    Lists the projects, asks for confirmation, and updates the JSON file.
    """
    global beam_storage
    load_projects_from_disk()
    
    if not beam_storage:
        print_error("No saved projects available to delete!")
        input("Press Enter to return to the Project Management menu...")
        return

    print_title("Delete Project")
    print_option("Select a project to delete:")
    for idx, project in enumerate(beam_storage):
        print_option(f"  {idx+1}. {project['name']}")
    print("")
    
    try:
        selection = int(input(colored("Enter the project number you want to delete ➔ ", 'cyan')))
        if selection < 1 or selection > len(beam_storage):
            print_error("Invalid project number. Operation cancelled.")
            input("Press Enter to return to the Project Management menu...")
            return
        
        project_to_delete = beam_storage[selection - 1]
        confirmation = input(colored(f"Are you sure you want to delete project '{project_to_delete['name']}'? (Y/N): ", 'cyan'))
        if confirmation.lower() == 'y':
            del beam_storage[selection - 1]
            try:
                with open('beam_projects.json', 'w') as file:
                    json.dump(beam_storage, file, indent=4)
                print_success(f"Project '{project_to_delete['name']}' deleted successfully!")
            except Exception as e:
                print_error(f"Error saving updated project file: {e}")
        else:
            print("Deletion cancelled.")
    except ValueError:
        print_error("Invalid input! Please enter a valid number.")

    print("")
    input("Press Enter to return to the Project Management menu...")

# =============================
# Save/Load Project Functions (To Disk)
# =============================
def save_project():
    """
    Save or update a project in memory, and persist later to disk.
    """
    global beam_storage, current_project, project_state
    
    project_name = input(colored("Enter a name for this project ➔ ", 'cyan')).strip()
    
    if not project_name:
        print_error("Project name cannot be empty!")
        return False

    # Create proper profile data structure
    profile_data = {
        'Ix': Ix,
        'shape': shape,
        'c': c,
        'b': b,
        'y_array': safe_serialize(y_array)
    }
    
    # Create proper material data structure
    material_data = {
        'material': selected_material
    }
    
    # Create project data dictionary
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
        'Reactions': safe_serialize(Reactions),
        'loads': loads if loads is not None else {},
        'profile': profile_data,
        'material': material_data
    }

    # Check if project with this name already exists
    for idx, proj in enumerate(beam_storage):
        if proj['name'].lower() == project_name.lower():
            confirmation = input(colored(f"Project '{project_name}' already exists. Overwrite? (Y/N): ", 'cyan'))
            if confirmation.lower() == 'y':
                beam_storage[idx] = project_data
                print_success(f"Project '{project_name}' updated successfully!")
                current_project = project_data
                project_state["has_unsaved_changes"] = False
                return True
            else:
                print("Save cancelled.")
                return False

    # Add new project
    beam_storage.append(project_data)
    print_success(f"Project '{project_name}' saved successfully!")
    current_project = project_data
    project_state["has_unsaved_changes"] = False
    return True

# =============================
def save_projects_to_disk():
    """
    Save all global projects to disk as a JSON file.
    Uses indentation for human readability.
    """
    global beam_storage
    try:
        with open('beam_projects.json', 'w') as file:
            json.dump(beam_storage, file, indent=4)
        print_success("All projects saved to disk successfully!")
        return True
    except Exception as e:
        print_error(f"Error saving projects to disk: {e}")
        return False

# =============================
def load_projects_from_disk():
    """
    Load projects from the JSON file into the global beam_storage.
    Initializes an empty storage if the file is not found or an error occurs.
    """
    global beam_storage
    try:
        with open('beam_projects.json', 'r') as file:
            beam_storage = json.load(file)
        print_success("Projects loaded from disk successfully!")
    except FileNotFoundError:
        print_error("No saved project file found. Starting with empty storage.")
        beam_storage = []
    except json.JSONDecodeError:
        print_error("Error loading projects from disk. Starting with empty storage.")
        beam_storage = []

# =============================
# Material Database Functions
# =============================
def load_material_database():
    """
    Load the material database from 'Materials.json' into the global variable.
    """
    global Materials
    json_filename = "Materials.json"
    try:
        Materials = MaterialDatabase(json_filename)
    except Exception as e:
        print_error(f"Error loading the materials database: {e}")
        time.sleep(3)

# =============================
def select_material():
    """
    List all materials from the loaded database, prompt for a selection,
    and return key properties of the selected material.
    
    Returns:
        dict: Selected material properties or None if input is invalid.
    """
    global Materials, project_state
    if Materials is None:
        print_error("Materials database is not loaded!")
        return None

    materials_list = Materials.materials
    print_title("Select a Material")
    cprint("-------------------------------------------------------------------------------------------------------------", "red")
    cprint("Density (kg/m³), Yield Strength (MPa), Ultimate Strength (MPa), Elastic Modulus (GPa), Poisson Ratio", "white")
    cprint("-------------------------------------------------------------------------------------------------------------", "red")
    print("")
    for index, material in enumerate(materials_list):
        properties_line = ", ".join([f"{key}: {value}" for key, value in material.items() if key != "Material"])
        print(colored(f"{index + 1} - {material['Material']}", "light_yellow"))
        print(colored(f"{properties_line}", 'white'))
        print("")
    selection = input(colored("Enter the number of the material you want to select ➔ ", 'cyan'))
    try:
        idx = int(selection) - 1
        if idx < 0 or idx >= len(materials_list):
            print_error("Invalid selection!")
            return None
        selected_material = materials_list[idx]
        print_success(f"You selected: {selected_material['Material']}")
        
        # Mark material as changed
        project_state["material_saved"] = True
        project_state["has_unsaved_changes"] = True
        
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

# =============================
def check_unsaved_changes():
    """Check if there are unsaved changes and prompt user to save."""
    global project_state
    
    if project_state["has_unsaved_changes"]:
        confirmation = input(colored("You have unsaved changes. Would you like to save them? (Y/N): ", 'cyan'))
        if confirmation.lower() == 'y':
            if save_project():
                save_projects_to_disk()
                return True
    return False

# =============================
def run_extended_menu():
    global current_project, project_state
    global beam_length, A, B, A_restraint, B_restraint, A_type, B_type
    global Ix, shape, c, b, y_array
    global selected_material, density, yield_strength, ultimate_strength, elastic_modulus, poisson_ratio, shear_yield_strength
    global pointloads, distributedloads, momentloads, triangleloads, loads
    global support_types

    load_material_database()
    load_projects_from_disk()

    while True:
        selection = main_menu_template()

        if selection == '1':  # Project Management
            while True:
                sub_choice = project_management_menu()
                if sub_choice == '5':  # Back to main menu
                    break
                elif sub_choice == '1':  # New project
                    if project_state["has_unsaved_changes"]:
                        check_unsaved_changes()
                    New_Project()
                    break
                elif sub_choice == '2':  # Load project
                    if project_state["has_unsaved_changes"]:
                        check_unsaved_changes()
                    load_project()
                    break
                elif sub_choice == '3':  # Modify project
                    modify_loaded_project_data()
                elif sub_choice == '4':  # Delete project
                    delete_project()
                else:
                    print_error("Invalid selection! Please try again.")
                    time.sleep(1)

        elif selection == '2':  # Define Beam Type
            while True:
                beam_type = Beam_Classification()
                if beam_type == "Simple" or beam_type == "Cantilever":
                    clear_screen()
                    cprint("==========================================================", 'red')
                    cprint(f"Beam Classification is {beam_type} Beam:",'white')
                    cprint("==========================================================", 'red')
                    time.sleep(1)
                    break
                else:
                    print_error("Invalid Beam Classification Please try again.")
                    time.sleep(1)
                    continue

        elif selection == '3':  # Profile Definition
            while True:
                sub_choice = profile_definition_menu()
                if sub_choice == '4':  # Back to main menu
                    break
                elif sub_choice == '1':  # Define beam length
                    if project_state["is_loaded"] and project_state["profile_saved"]:
                        confirmation = input(colored("Project already has a beam length defined. Modify? (Y/N): ", 'cyan'))
                        if confirmation.lower() != 'y':
                            continue
                            
                    beam_length = Beam_Length()
                    project_state["has_unsaved_changes"] = True
                    print("")
                    cprint("==========================================================", 'red')
                    cprint(f"Beam Length is set to: {beam_length} m",'white')
                    cprint("==========================================================", 'red')
                    time.sleep(1)
                    
                elif sub_choice == '2':  # Choose profile
                    if project_state["is_loaded"] and project_state["profile_saved"]:
                        confirmation = input(colored("Project already has a profile defined. Modify? (Y/N): ", 'cyan'))
                        if confirmation.lower() != 'y':
                            continue
                            
                    clear_screen()
                    profile_choice = choose_profile()
                    print("")
                    
                    # Moment of Inertia (MOI) Solver
                    if beam_type is None:
                        cprint("----------------------------------------------","white")
                        print_error("Note: Please define beam type !!!!")
                        cprint("----------------------------------------------","white")
                        print("")
                    if profile_choice == '1':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_ibeam()
                    elif profile_choice == '2':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_tbeam()
                    elif profile_choice == '3':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_circle()
                    elif profile_choice == '4':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_circle()
                    elif profile_choice == '5':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_square()
                    elif profile_choice == '6':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_hollow_square()
                    elif profile_choice == '7':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_rectangle()
                    elif profile_choice == '8':
                        Ix, shape, c, b, y_array = moi_solver.inertia_moment_hollow_rectangle()
                    else:
                        print_error("Invalid choice! Please try again.")
                        continue
                        
                    project_state["profile_saved"] = True
                    project_state["has_unsaved_changes"] = True
                    print_success("Profile defined successfully!")
                    time.sleep(2)
                    
                elif sub_choice == '3':  # View profile info
                    if not project_state["profile_saved"] and not shape:
                        print_error("No profile defined yet!")
                        time.sleep(2)
                        continue
                        
                    clear_screen()
                    cprint("==========================================================", 'red')
                    cprint("                    Profile Information     ", 'light_yellow')
                    cprint("==========================================================", 'red')
                    cprint(f"Beam Length is set to: {beam_length} m",'white')
                    print("")
                    cprint(f"\nCurrent Profile: {shape}",'white')
                    print("")
                    cprint(f"Ix = {Ix:.6e} m⁴", "white")
                    print("")
                    cprint(f"Distance c from neutral axis to extreme fiber: {c:.4f} m",'white')
                    print("")
                    cprint(f"effective width b from neutral axis to extreme fiber: {b:.4f} m",'white')
                    cprint("==========================================================", 'red')
                    print()
                    input("Press Enter to return to the Profile menu...")

        elif selection == '4':  # Material Selection
            while True:
                sub_choice = material_selection_menu()
                if sub_choice == '3':  # Back to main menu
                    break
                elif sub_choice == '1':  # Select material
                    if project_state["is_loaded"] and project_state["material_saved"]:
                        confirmation = input(colored("Project already has a material defined. Modify? (Y/N): ", 'cyan'))
                        if confirmation.lower() != 'y':
                            continue
                            
                    selected_material = select_material()
                    if selected_material:
                        density = float(selected_material["Density"])
                        yield_strength = float(selected_material["Yield Strength"]) * 1e6
                        ultimate_strength = float(selected_material["Ultimate Strength"]) * 1e6
                        elastic_modulus = float(selected_material["Elastic Modulus"]) * 1e9
                        poisson_ratio = float(selected_material["Poisson Ratio"])
                        shear_yield_strength = 0.55 * yield_strength
                        project_state["material_saved"] = True
                        project_state["has_unsaved_changes"] = True
                        
                        cprint("==========================================================", 'red')
                        cprint("       Units Automatically Converted To Metric Units    ",'green')
                        cprint("==========================================================", 'red')
                        time.sleep(1)

                elif sub_choice == '2':  # View material info
                    if not project_state["material_saved"] and not selected_material:
                        print_error("No material selected yet.")
                        time.sleep(2)
                        continue
                        
                    clear_screen()
                    cprint("==========================================================", 'red')
                    cprint("                       Custom Units                                   ",'white')
                    cprint("==========================================================", 'red')
                    print(f"\nMaterial: {selected_material['Material']}")
                    print(f"\nDensity: {selected_material['Density']} kg/m³")
                    print(f"\nYield Strength: {selected_material['Yield Strength']} MPa")
                    print(f"\nUltimate Strength: {selected_material['Ultimate Strength']} MPa")
                    print(f"\nElastic Modulus: {selected_material['Elastic Modulus']} GPa")
                    print(f"\nPoisson Ratio: {selected_material['Poisson Ratio']}")
                    cprint("==========================================================", 'red')
                    cprint("                       Metric Units                                   ",'white')
                    cprint("==========================================================", 'red')
                    print(f"\nMaterial: {selected_material['Material']}")
                    print(f"\nDensity: {density} kg/m³")
                    print(f"\nYield Strength: {yield_strength} Pa")
                    print(f"\nUltimate Strength: {ultimate_strength} Pa")
                    print(f"\nElastic Modulus: {elastic_modulus} Pa")
                    print(f"\nPoisson Ratio: {poisson_ratio}")

                    input("Press Enter to return to the Material Selection menu...")

        elif selection == '5':  # Boundary Conditions

            if beam_type == "Cantilever":
                print_error("Cantilever beams Boundary Conditions Already Defined !!!!")
                time.sleep(2)
                break

            elif beam_type == "Simple":
                while True:
                    sub_choice = boundary_conditions_menu()
                    if sub_choice == '3':  # Back to main menu
                        break
                    elif sub_choice == '1':  # Define supports
                        if project_state["is_loaded"] and project_state["supports_saved"]:
                            confirmation = input(colored("Project already has supports defined. Modify? (Y/N): ", 'cyan'))
                            if confirmation.lower() != 'y':
                                continue
                            
                        A, B, A_restraint, B_restraint, A_type, B_type = Beam_Supports()
                        project_state["supports_saved"] = True
                        project_state["has_unsaved_changes"] = True
                        support_types = ("pin", "roller")
                    
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                Selected Support Positions                                 ", 'light_yellow')
                        cprint("==========================================================", 'red')
                        print(f"Pin Support Position(A): {A} m")
                        print("")
                        print(f"Roller Support Position(B): {B} m")
                        cprint("==========================================================", 'red')
                        print("")                        
                        input("Press Enter to return to the menu...")
                    
                    elif sub_choice == '2':  # View supports
                        if not project_state["supports_saved"] and not A_type and not B_type:
                            print_error("No supports defined yet!")
                            time.sleep(2)
                            continue
                        
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                Selected Support Positions                                 ", 'light_yellow')
                        cprint("==========================================================", 'red')
                        cprint(f"Pin Support Position(A): {A} m","white")
                        print("")
                        cprint(f"Roller Support Position(B): {B} m",'white')
                        cprint("==========================================================", 'red')
                        print("")
                        input("Press Enter to return to the menu...")
            else:
                print_error("Please define Beam Classification first !!!! ")
                time.sleep(2)
                continue

        elif selection == '6':  # Loads Definition
            if beam_type is None:
                print_error("Beam Classificatione is not defined yet!")
                time.sleep(2)
                continue
            else:
                while True:
                    sub_choice = loads_definition_menu()
                    if sub_choice == '4':  # Back to main menu
                        break
                    elif sub_choice == '1':  # Define loads
                        if project_state["is_loaded"] and project_state["loads_saved"]:
                            confirmation = input(colored("Project already has loads defined. Modify? (Y/N): ", 'cyan'))
                            if confirmation.lower() != 'y':
                                continue
                    
                        print("Define Loads:")
                        loads_dict = manage_loads()
                        pointloads = loads_dict.get("pointloads", [])
                        distributedloads = loads_dict.get("distributedloads", [])
                        momentloads = loads_dict.get("momentloads", [])
                        triangleloads = loads_dict.get("triangleloads", [])
                        loads = loads_dict  # Store the complete dictionary for later use
                    
                        # Update project state
                        project_state["loads_saved"] = True
                        project_state["has_unsaved_changes"] = True
                    
                        print("")
                        print_success("Loads defined successfully!")
                        time.sleep(1)
                    
                    elif sub_choice == '2':  # View loads
                        if not project_state["loads_saved"] and not loads:
                            print_error("No loads defined yet!")
                            time.sleep(2)
                            continue
                        
                        clear_screen()
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                    Defined Loads:                        ", 'light_yellow')
                        cprint("==========================================================", 'red')                    
                        print_title("Current Loads:")
                        print(colored(f"\nPoint Loads: {loads.get('pointloads', [])}", 'white'))
                        print(colored(f"\nDistributed Loads: {loads.get('distributedloads', [])}", 'white'))
                        print(colored(f"\nMoment Loads: {loads.get('momentloads', [])}", 'white'))
                        print(colored(f"\nTriangular Loads: {loads.get('triangleloads', [])}", 'white'))
                        print("")
                        input("Press Enter to continue...")
                    
                    elif sub_choice == '3':  # Plot beam schematic
                        if not project_state["loads_saved"] or not project_state["supports_saved"]:
                            print_error("Both loads and supports must be defined before plotting!")
                            time.sleep(2)
                            continue
                        
                        try:
                            support_types = ("pin", "roller")  # Use actual support types from project data
                            formatted_loads = format_loads_for_plotting(loads_dict)
                            plot_beam_schematic(beam_length, A, B, support_types, formatted_loads)
                        except Exception as e:
                            print_error(f"Error plotting schematic: {e}")
                            time.sleep(2)
                    else:
                        print_error("Invalid selection! Please try again.")
                        time.sleep(2)
                    
        elif selection == '7':  # Show Beam Schematic (Standalone)
            if not project_state["loads_saved"] or not project_state["supports_saved"]:
                print_error("Both loads and supports must be defined before plotting!")
                time.sleep(2)
                continue
                
            try:
                support_types = ("pin", "roller")
                formatted_loads = format_loads_for_plotting(loads_dict)
                plot_beam_schematic(beam_length, A, B, support_types, formatted_loads)
            except Exception as e:
                print_error(f"Error plotting beam schematic: {e}")
                time.sleep(2)

        elif selection == '8':  # Analysis/Simulation
            while True:
                sub_choice = analysis_simulation_menu()
                if sub_choice == '5':  # Back to main menu
                    break
                    
                # Check if all required data is available for analysis
                if not project_state["profile_saved"] or not project_state["material_saved"] or \
                   not project_state["loads_saved"] or not project_state["supports_saved"]:
                    print_error("Analysis requires profile, material, supports and loads to be defined!")
                    time.sleep(2)
                    continue
                
                if sub_choice == '1':  # Run analysis
                    try:
                        clear_screen()
                        cprint("==========================================================", 'red')
                        cprint("                     Solver Information:                 ", "white")
                        cprint("==========================================================", 'red')
                        cprint("Used Solver: Simple Determined Beams Solver", 'white')
                        cprint("Solver Version: 1.02 Stable", 'white')
                        cprint("Solver Accuracy: Preferred High Accuracy", 'white')
                        cprint("Estimated Solve Time: 0.3 Sec", 'white')
                        cprint("Number of Divisions = 10000 part", 'white')
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                     Profile Properties                  ", "light_yellow")
                        cprint("==========================================================", 'red')
                        print(f"Beam Length: {beam_length} m")
                        print(f"\nCurrent Profile: {shape}")
                        print(f"\nMaterial: {selected_material['Material']}")
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                           Supports                      ", "light_red")
                        cprint("==========================================================", 'red')
                        print(f"Support A Position ({A_type}): {A} m")
                        print(f"Support B Position ({B_type}): {B} m")
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                          Applied Loads                  ", "light_green")
                        cprint("==========================================================", 'red')
                        print(f"Point Loads: {pointloads} (position in m and magnitude in N)")
                        print(f"Distributed Loads: {distributedloads} (start, end in m and intensity in N/m)")
                        print(f"Moment Loads: {momentloads} (position in m and moment in N·m)")
                        print(f"Triangular Loads: {triangleloads} (position and magnitude)")
                        print("")
                        cprint("==========================================================", 'red')
                        print("")
                        print("Solving....................")
                        time.sleep(0.2)
                        
                        # Extract loads for solver
                        pointloads_in = loads.get("pointloads", [])
                        distributedloads_in = loads.get("distributedloads", [])
                        momentloads_in = loads.get("momentloads", [])
                        triangleloads_in = loads.get("triangleloads", [])
                        
                        # Perform the analysis with proper arguments
                        X_Field, Total_ShearForce, Total_BendingMoment, Reactions = solve_simple_beam(
                            beam_length, A=A, B=B,
                            pointloads_in=pointloads_in, 
                            distributedloads_in=distributedloads_in,
                            momentloads_in=momentloads_in, 
                            triangleloads_in=triangleloads_in,
                            beam_type=beam_type
                        )
                        
                        # Mark results as available for use in other menus
                        project_state["analysis_complete"] = True
                        project_state["has_unsaved_changes"] = True
                        
                        # Extract and display key results
                        if beam_type=="Simple":
                            Va = Reactions[0]
                            Ha = Reactions[2]
                            Vb = Reactions[1]
                        else:
                            Va = Reactions[0]
                            Ha = Reactions[1]
                            Vb = Reactions[2]
                        max_shear = round(np.max(Total_ShearForce), 3)
                        min_shear = round(np.min(Total_ShearForce), 3)
                        max_bending = round(np.max(Total_BendingMoment), 3)
                        min_bending = round(np.min(Total_BendingMoment), 3)
                        
                        print("")
                        cprint("==========================================================", 'white')
                        cprint("            Beam analysis completed successfully!        ", 'green')
                        cprint("==========================================================", 'white')
                        print("")
                        input("Press Enter to return to the Analysis/Simulation menu...")
                        
                    except Exception as e:
                        print_error(f"Error solving beam: {e}")
                        time.sleep(2)
                        continue

                elif sub_choice == '2':  # View analysis results
                    if not project_state.get("analysis_complete", False):
                        print_error("No analysis results available yet! Please run analysis first.")
                        time.sleep(2)
                        continue
                        
                    try:
                        clear_screen()
                        cprint("                  Analysis Results:","light_green")
                        cprint("==========================================================", 'white')
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                  Reactions Forces                       ", "white")
                        cprint("==========================================================", 'red')
                        print(colored(f"Support A Reaction Force: RA: {Va} N", "white"))
                        print(colored(f"Support B Reaction Force: RB: {Vb} N", "white"))
                        print("")
                        cprint("==========================================================", 'red')
                        cprint("                 Max/Min Shear Force                     ", "white")
                        cprint("==========================================================", 'red')      
                        print(colored(f"Maximum Shear Force Value: {max_shear} N", "white"))
                        print(f"Minimum Shear Force Value: {min_shear} N")
                        print("")
                        cprint("==========================================================", 'red')      
                        cprint("                 Max/Min Bending Moment                  ", "white")
                        cprint("==========================================================", 'red')         
                        print(colored(f"Maximum Bending Moment: {max_bending} N·m", "white"))
                        print(colored(f"Minimum Bending Moment: {min_bending} N·m", "white"))
                        cprint("==========================================================", 'red')
                        input("Press Enter to return to the Analysis/Simulation menu...")
                        
                    except Exception as e:
                        print_error(f"Error displaying analysis results: {e}")
                        time.sleep(2)
                        continue

                elif sub_choice == '3':  # Calculate deflection
                    if not project_state.get("analysis_complete", False):
                        print_error("Please run the analysis first!")
                        time.sleep(2)
                        continue
                        
                    try:
                        clear_screen()
                        cprint("==========================================================", 'red')       
                        print("                 Calculating deflection...")                         
                        cprint("==========================================================", 'red')       
                        Deflection, Slope, curv = calculate_beam_deflection(X_Field, Total_BendingMoment, elastic_modulus, Ix)
                        print("")
                        print_success("Deflection calculations completed successfully!")
                        
                        # Update project state to mark deflection as calculated
                        project_state["deflection_calculated"] = True
                        project_state["has_unsaved_changes"] = True
                        
                        # Show max deflection
                        max_deflection = round(np.max(np.abs(Deflection)), 6)
                        print(f"Maximum deflection: {max_deflection} m")
                        cprint("==========================================================", 'red')  
                        time.sleep(1)
                        input("Press Enter to return to the Analysis/Simulation menu...")
                        
                    except Exception as e:
                        print_error(f"Error calculating deflection: {e}")
                        time.sleep(2)
                        continue

                elif sub_choice == '4':  # Calculate stress and FOS
                    if not project_state.get("analysis_complete", False):
                        print_error("Please run the analysis first!")
                        time.sleep(2)
                        continue
                        
                    try:
                        clear_screen()
                        cprint("==========================================================", 'red')       
                        print("                 Calculating stresses...")                         
                        cprint("==========================================================", 'red')
                        
                        # Calculate shear and bending stresses
                        # Shear stress
                        Q_array = first_moment_of_area_rect(b, y_array)
                        calculate_shear_stress(Total_ShearForce, Q_array, Ix, b)
                        Shear_stress = calculate_shear_stress(Total_ShearForce, Q_array, Ix, b)
                        Max_Shear_stress = np.max(Shear_stress)

                        # Bending stress

                        bending_stress =calculate_bending_stress(Total_BendingMoment, c, Ix)
                        Max_bending_stress = np.max(np.abs(bending_stress))
                        
                        # Calculate and display Factor of Safety
                        FOS = Factor_of_Safety(Total_BendingMoment, c, yield_strength, Ix)
                        
                        # Update project state
                        project_state["stress_calculated"] = True
                        project_state["has_unsaved_changes"] = True
                        print_success("Stress and Factor of Safety calculations completed successfully!")
                        cprint("=================================================================", 'red')
                        print("")
                        time.sleep(1)
                        print(f"For the shear stress, the maximum value is: {Max_Shear_stress:.2e} Pa")
                        print("")
                        print(f"For the bending stress, the maximum value is: {Max_bending_stress:.2e} Pa")
                        cprint("=================================================================", 'red')
                        print("")
                        print(f"Factor of Safety against yielding: {FOS:.2f}")
                        print("")
                        if FOS > 1:
                            print(colored("The beam is safe!", 'green'))
                        elif FOS == 1:
                            print(colored("The beam is at the limit of safety!", 'yellow'))
                        else:
                            print(colored("The beam is not safe!", 'red'))
                        print("")
                        print("---------------------------------------------------------")
                        input("Press Enter to return to the Analysis/Simulation menu...")
                        
                    except Exception as e:
                        print_error(f"Error in stress/F.O.S calculations: {e}")
                        time.sleep(2)
                        continue

        elif selection == '9':  # Postprocessing/Visualization
            while True:
                sub_choice = postprocessing_menu()
                if sub_choice == '6':  # Back to main menu
                    break
                    
                # Check if analysis has been completed before allowing visualization
                if not project_state.get("analysis_complete", False):
                    print_error("Please complete an analysis before attempting visualization!")
                    time.sleep(2)
                    continue
                    
                if sub_choice == '1':  # Reaction forces schematic
                    try:
                        print_success("Processing Reactions Forces Schematic Plots (Plotly-only):")
                        support_types = ("pin", "roller")
                        plot_reaction_diagram(A, B, Reactions, support_types)
                    except Exception as e:
                        print_error(f"Error plotting reaction diagram: {e}")
                        time.sleep(2)
                        continue
                        
                elif sub_choice == '2':  # SFD/BMD (Matplotlib)
                    try:
                        style = input(colored("Choose a style (1 for Matplotlib, 2 for Plotly) ➔ ", 'cyan'))
                        if style == '1':
                            print_success("Processing Shear Force/Bending Moment Plots (Matplotlib):")
                            Matplot_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment)
                        elif style == '2':
                                print_success("Processing Shear Force/Bending Moment Plots (Plotly):")
                                Plotly_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment, beam_length)
                        
                    except Exception as e:
                        print_error(f"Error in Plotting !!! : {e}")
                        time.sleep(2)
                        continue
                        
                elif sub_choice == '5':  # Combined (Plotly)
                    try:
                        style = input(colored("Choose a style (1 for Matplotlib, 2 for Plotly) ➔ ", 'cyan'))
                        if style == '1':
                            print_success("Processing Combined Plots (Matplotlib):")
                            Matplot_combined(X_Field, Total_ShearForce, Total_BendingMoment, Deflection=Deflection, ShearStress=Shear_stress)
                        elif style == '2':
                                print_success("Processing Combined Plots (Plotly):")
                                Plotly_combined_diagrams(X_Field, Total_ShearForce, Total_BendingMoment, beam_length, Deflection=Deflection, ShearStress=Shear_stress)
                        
                    except Exception as e:
                        print_error(f"Error in Plotting !!! : {e}")
                        time.sleep(2)
                        continue

                elif sub_choice == '3':  # Deflection plot
                    if not project_state.get("deflection_calculated", False):
                        print_error("Please calculate deflection first (in Analysis menu)!")
                        time.sleep(2)
                        continue
                        
                    try:
                        style = input(colored("Choose a style (1 for Matplotlib, 2 for Plotly) ➔ ", 'cyan'))
                        if style == '1':
                            print_success("Processing Deflection/Displacement Plots (Matplotlib):")
                            Matplot_Deflection(X_Field, Deflection)
                        elif style == '2':
                            print_success("Processing Deflection/Displacement Plots (Plotly):")
                            Plotly_Deflection(X_Field, Deflection, beam_length)
                        else:
                            print_error("Invalid style selection!")
                            time.sleep(2)
                            continue
                    except Exception as e:
                        print_error(f"Error plotting Deflection Plot: {e}")
                        time.sleep(2)
                        continue

                elif sub_choice == '4':  # Stress contours
                    #if not project_state.get("stress_calculated", False):
                        try:
                            style = input(colored("Choose a style (1 for Matplotlib, 2 for Plotly) ➔ ", 'cyan'))
                            if style == '1':
                                print_success("Processing shear-Stress Plots (Matplotlib):")
                                Matplot_ShearStress(X_Field,Shear_stress)
                            elif style == '2':
                                print_success("Processing shear-Stress Plots (Plotly):")
                                Plotly_ShearStress(X_Field,Shear_stress,beam_length)
                            else:
                                print_error("Invalid style selection!")
                                time.sleep(2)
                                continue
                        except Exception as e:
                            print_error(f"Error plotting shear-Stress Plot: {e}")
                            time.sleep(2)


                                
        elif selection == '10':  # Save Project
            if not project_state["profile_saved"] or not project_state["material_saved"] or \
               not project_state["supports_saved"] or not project_state["loads_saved"]:
                print_error("You must define profile, material, supports and loads before saving!")
                time.sleep(2)
                continue
                
            try:
                save_decision = input(colored("Do you want to save this project? (Y/N) ➔ ", 'cyan'))
                print("")
                
                if save_decision.lower() == 'y':
                    if save_project():  # Use the new save_project function that takes no arguments
                        save_projects_to_disk()
                        print_success("Project saved to disk successfully!")
                    else:
                        print_error("Failed to save project!")
                else:
                    print(colored("Project not saved. Continuing...", 'yellow'))
                    print("")
                
                time.sleep(2)
                
            except Exception as e:
                print_error(f"Error saving project: {e}")
                time.sleep(2)
                
        elif selection == '0':  # Exit
            if project_state["has_unsaved_changes"]:
                check_unsaved_changes()
            
            print_success("Thank you for using the Zylo-X Beam Calculator!")
            break
            
        else:
            print_error("Invalid selection! Please try again.")
            time.sleep(1)

def init():
    global project_state

    project_state = {
        "is_loaded": False,
        "profile_saved": False, 
        "material_saved": False,
        "loads_saved": False,
        "supports_saved": False,
        "analysis_complete": False,
        "deflection_calculated": False,
        "stress_calculated": False,
        "has_unsaved_changes": False
    }
# =============================
# Main Program Execution
# =============================
if __name__ == "__main__":
    # Initialize global variables for proper tracking
    init()
    # Start the extended menu-driven application
    run_extended_menu()