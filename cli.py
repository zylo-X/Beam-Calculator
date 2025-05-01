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
import Solver
import moi_solver
import Plotting
import beam_plot
from Stress_solver import (calculate_beam_deflection,first_moment_of_area_rect, calculate_shear_stress,calculate_bending_stress,Factor_of_Safety)
from Menus import (main_menu_template,project_management_menu,profile_definition_menu,choose_profile,
material_selection_menu,boundary_conditions_menu,loads_definition_menu,analysis_simulation_menu,postprocessing_menu,
print_success,print_error,print_option,print_title)
from inputs import Beam_Length,Beam_Supports,manage_loads

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
project_loaded = False
profile_loaded = False
material_loaded = False
loads_loaded = False

# -----------------------------

# =============================
# Project Management Functions
# =============================
def New_Project():
    """Start a new project by resetting the current project."""
    global current_project
    current_project = None  # Reset current project data
    print_success("Starting a new project...")
    time.sleep(0.5)
# =============================
def load_project():
    global current_project, beam_length, A, B, A_restraint, B_restraint, A_type, B_type
    global X_Field, Total_ShearForce, Total_BendingMoment, Reactions, loads
    global Ix, shape, c, b, y_array
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

        # 🧠 Apply loaded project data to current state
        beam_length = current_project.get('beam_length', 0)
        A = current_project.get('support_A_pos', 0)
        B = current_project.get('support_B_pos', 0)
        A_restraint = current_project.get('support_A_restraint', [])
        B_restraint = current_project.get('support_B_restraint', [])
        A_type = current_project.get('support_A_type', '')
        B_type = current_project.get('support_B_type', '')

        X_Field = np.array(current_project.get('X_Field', []))
        Total_ShearForce = np.array(current_project.get('Total_ShearForce', []))
        Total_BendingMoment = np.array(current_project.get('Total_BendingMoment', []))
        Reactions = np.array(current_project.get('Reactions', []))
        loads = current_project.get('loads', {})

        # Load and reassign load components for analysis use
        pointloads = loads.get("pointloads", [])
        distributedloads = loads.get("distributedloads", [])
        momentloads = loads.get("momentloads", [])
        triangleloads = loads.get("triangleloads", [])

        profile_data = current_project.get('profile', {})
        Ix = profile_data.get('Ix', 0)
        shape = profile_data.get('shape', '')
        c = profile_data.get('c', 0)
        b = profile_data.get('b', 0)
        y_array = np.array(profile_data.get('y_array', []))

        material_data = current_project.get('material', {}).get('material', {})
        if material_data:
            selected_material = material_data
            density = float(material_data.get("Density", 0))
            yield_strength = float(material_data.get("Yield Strength", 0)) * 1e6
            ultimate_strength = float(material_data.get("Ultimate Strength", 0)) * 1e6
            elastic_modulus = float(material_data.get("Elastic Modulus", 0)) * 1e9
            poisson_ratio = float(material_data.get("Poisson Ratio", 0))
            shear_yield_strength = 0.55 * yield_strength
        else:
            selected_material = None

        # ✅ Optional: Show confirmation summary
        print(colored(f"\n✔ Loaded Project Summary:", 'green'))
        print(f"Beam Length: {beam_length} m")
        print(f"Supports: A @ {A} m ({A_type}), B @ {B} m ({B_type})")
        print(f"Profile: {shape} | Ix = {Ix:.2e} m⁴")
        if selected_material:
            print(f"Material: {selected_material.get('Material')} | E = {elastic_modulus:.2e} Pa")
        print("")

    except (IndexError, ValueError):
        print_error("Invalid choice! Starting a new project instead.")
        current_project = None
        time.sleep(1)

# ====================================
def apply_loaded_project():
    global beam_length, A, B, A_restraint, B_restraint, A_type, B_type
    global Ix, shape, c, b, y_array
    global elastic_modulus, selected_material, density, yield_strength, ultimate_strength, poisson_ratio, shear_yield_strength
    global X_Field, Total_ShearForce, Total_BendingMoment, Reactions, loads
    global pointloads, distributedloads, momentloads, triangleloads

    if current_project is None:
        return

    # Point to correct current values from loaded project
    beam_length = current_project.get('beam_length', 0)
    A = current_project.get('support_A_pos', 0)
    B = current_project.get('support_B_pos', 0)
    A_restraint = current_project.get('support_A_restraint', [])
    B_restraint = current_project.get('support_B_restraint', [])
    A_type = current_project.get('support_A_type', '')
    B_type = current_project.get('support_B_type', '')
    
    profile = current_project.get('profile', {})
    Ix = profile.get('Ix', 0)
    shape = profile.get('shape', '')
    c = profile.get('c', 0)
    b = profile.get('b', 0)
    y_array = np.array(profile.get('y_array', []))

    material_data = current_project.get('material', {}).get('material', {})
    if material_data:
        selected_material = material_data
        density = float(material_data.get("Density", 0))
        yield_strength = float(material_data.get("Yield Strength", 0)) * 1e6
        ultimate_strength = float(material_data.get("Ultimate Strength", 0)) * 1e6
        elastic_modulus = float(material_data.get("Elastic Modulus", 0)) * 1e9
        poisson_ratio = float(material_data.get("Poisson Ratio", 0))
        shear_yield_strength = 0.55 * yield_strength

    loads = current_project.get('loads', {})
    # If needed, rebuild internal load structures from `loads`
    pointloads = loads.get("pointloads", [])
    distributedloads = loads.get("distributedloads", [])
    momentloads = loads.get("momentloads", [])
    triangleloads = loads.get("triangleloads", [])

    X_Field = np.array(current_project.get('X_Field', []))
    Total_ShearForce = np.array(current_project.get('Total_ShearForce', []))
    Total_BendingMoment = np.array(current_project.get('Total_BendingMoment', []))
    Reactions = np.array(current_project.get('Reactions', []))


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


def save_project(beam_length, A, B, A_restraint, B_restraint,
                 X_Field, Total_ShearForce, Total_BendingMoment, Reactions,
                 A_type, B_type,
                 loads_dict=loads,
                 profile_data={'Ix': Ix, 'shape': shape, 'c': c, 'b': b, 'y_array': safe_serialize(y_array)},
                 material_data={'material': selected_material}):
    """
    Save or update a project in memory, and persist later to disk.
    """
    global beam_storage, current_project
    project_name = input(colored("Enter a name for this project ➔ ", 'cyan')).strip()

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
        'loads': loads_dict if loads_dict is not None else {},
        'profile': profile_data if profile_data is not None else {},
        'material': material_data if material_data is not None else {}
    }

    # Update existing project if name matches
    for idx, proj in enumerate(beam_storage):
        if proj['name'].lower() == project_name.lower():
            beam_storage[idx] = project_data
            print_success(f"Project '{project_name}' updated successfully!")
            break
    else:
        beam_storage.append(project_data)
        print_success(f"Project '{project_name}' saved successfully!")

    current_project = project_data
    print("")


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
    except Exception as e:
        print_error(f"Error saving projects to disk: {e}")
    print("")


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
    global Materials
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
def run_extended_menu():
    global current_project
    global project_loaded, profile_loaded, material_loaded, loads_loaded, supports_loaded
    global beam_length, A, B, A_restraint, B_restraint, A_type, B_type
    global Ix, shape, c, b, y_array
    global selected_material, density, yield_strength, ultimate_strength, elastic_modulus, poisson_ratio, shear_yield_strength
    global pointloads, distributedloads, momentloads, triangleloads, loads
    global support_types

    load_material_database()

    # Flags for load/project state
    project_loaded = False
    profile_loaded = False
    material_loaded = False
    loads_loaded = False
    supports_loaded = False

    while True:
        selection = main_menu_template()

        if selection == '1':  # Project Management
            while True:
                sub_choice = project_management_menu()
                if sub_choice == '4':
                    break
                elif sub_choice == '1':
                    New_Project()
                    project_loaded = profile_loaded = material_loaded = loads_loaded = supports_loaded = False
                    break
                elif sub_choice == '2':
                    load_project()
                    apply_loaded_project()
                    project_loaded = profile_loaded = material_loaded = loads_loaded = supports_loaded = True
                    break
                elif sub_choice == '3':
                    delete_project()
                else:
                    print_error("Invalid selection! Please try again.")
                    time.sleep(1)

        elif selection == '2':  # Profile Definition
            while True:
                sub_choice = profile_definition_menu()
                if sub_choice == '4':
                    break
                elif sub_choice == '1':
                    if project_loaded:
                        print(colored("Beam length was loaded from a saved project. Skipping input.", "yellow"))
                        time.sleep(1)
                    else:
                        beam_length = Beam_Length()
                        print(f"Beam Length is set to: {beam_length} m")
                        time.sleep(2)
                elif sub_choice == '2':
                    if profile_loaded:
                        print(colored("Profile was loaded from saved project. Skipping profile selection.", "yellow"))
                        time.sleep(1)
                    else:
                        profile_choice = choose_profile()
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
                        profile_loaded = True
                        time.sleep(2)
                elif sub_choice == '3':
                    try:
                        print(f"\nCurrent Profile: {shape}")
                        print(colored(f"Ix = {Ix:.6e} m⁴", "green"))
                        input("Press Enter to return to the menu...")
                    except Exception:
                        print_error("No profile defined yet!")
                        time.sleep(2)

        elif selection == '3':  # Material Selection
            while True:
                sub_choice = material_selection_menu()
                if sub_choice == '3':
                    break
                elif sub_choice == '1':
                    if material_loaded:
                        print(colored("Material was loaded from saved project. Skipping selection.", "yellow"))
                        time.sleep(1)
                    else:
                        selected_material = select_material()
                        if selected_material:
                            density = float(selected_material["Density"])
                            yield_strength = float(selected_material["Yield Strength"]) * 1e6
                            ultimate_strength = float(selected_material["Ultimate Strength"]) * 1e6
                            elastic_modulus = float(selected_material["Elastic Modulus"]) * 1e9
                            poisson_ratio = float(selected_material["Poisson Ratio"])
                            shear_yield_strength = 0.55 * yield_strength
                            material_loaded = True
                            time.sleep(1)
                elif sub_choice == '2':
                    try:
                        print(f"\nMaterial: {selected_material['Material']}")
                        print(f"Density: {density} kg/m³")
                        print(f"Yield Strength: {yield_strength} Pa")
                        print(f"Ultimate Strength: {ultimate_strength} Pa")
                        print(f"Elastic Modulus: {elastic_modulus} Pa")
                        print(f"Poisson Ratio: {poisson_ratio}")
                        print(f"Shear Yield Strength: {shear_yield_strength} Pa\n")
                        input("Press Enter to return to the Material Selection menu...")
                    except:
                        print_error("No material selected yet.")
                        time.sleep(2)

        elif selection == '4':  # Boundary Conditions
            while True:
                sub_choice = boundary_conditions_menu()
                if sub_choice == '3':
                    break
                elif sub_choice == '1':
                    if supports_loaded:
                        print(colored("Supports were loaded from saved project. Skipping input.", "yellow"))
                        time.sleep(1)
                    else:
                        A, B, A_restraint, B_restraint, A_type, B_type = Beam_Supports()
                        supports_loaded = True
                        support_types = ("pin", "roller")
                        print(f"Support A: {A} m, Type: {A_type}")
                        print(f"Support B: {B} m, Type: {B_type}")
                        input("Press Enter to return to the menu...")
                elif sub_choice == '2':
                    if not supports_loaded:
                        print_error("No supports defined yet!")
                        time.sleep(2)
                    else:
                        print(f"\nSupport A: {A} m, Type: {A_type}, Restraints: {A_restraint}")
                        print(f"Support B: {B} m, Type: {B_type}, Restraints: {B_restraint}\n")
                        input("Press Enter to return to the menu...")

        elif selection == '5':  # Loads Definition
            while True:
                sub_choice = loads_definition_menu()
                if sub_choice == '4':
                    break
                elif sub_choice == '1':
                    if loads_loaded:
                        print(colored("Loads were loaded from saved project. Skipping input.", "yellow"))
                        time.sleep(1)
                    else:
                        print("Define Loads:")
                        loads_dict = manage_loads()
                        pointloads = loads_dict["pointloads"]
                        distributedloads = loads_dict["distributedloads"]
                        momentloads = loads_dict["momentloads"]
                        triangleloads = loads_dict["triangleloads"]
                        loads = Plotting.format_loads_for_plotting(loads_dict)
                        loads_loaded = True
                        print("Loads defined successfully!")
                        time.sleep(2)
                elif sub_choice == '2':
                    if not loads_loaded:
                        print_error("No loads defined yet!")
                        time.sleep(2)
                    else:
                        print(f"\nPoint Loads: {pointloads}")
                        print(f"Distributed Loads: {distributedloads}")
                        print(f"Moment Loads: {momentloads}")
                        print(f"Triangular Loads: {triangleloads}\n")
                        input("Press Enter to return to the menu...")
                elif sub_choice == '3':
                    try:
                        beam_plot.plot_beam_schematic(beam_length, A, B, support_types, loads)
                    except Exception as e:
                        print_error(f"Error plotting schematic: {e}")
                        time.sleep(2)
                        continue
                    else:
                        print_error("Invalid selection! Please try again.")
                        time.sleep(2)
        elif selection == '6':  # Show Beam Schematic (Standalone)
            try:
                beam_plot.plot_beam_schematic(beam_length, A, B, support_types, loads)
            except Exception as e:
                print_error(f"Error plotting beam schematic: {e}")
                time.sleep(2)
                continue

        elif selection == '7':  # Analysis/Simulation
            while True:
                sub_choice = analysis_simulation_menu()
                if sub_choice == '5':
                    break
                else:
                    if sub_choice == '1':
                        try:
                            print("Solver Information:")
                            print("")
                            print(f"Beam Length: {beam_length} m")
                            print("Number of Divisions = 10000")
                            print(f"Support A Position: {A} m")
                            print(f"Support B Position: {B} m")
                            print(f"Support A Type: {A_type}")
                            print(f"Support B Type: {B_type}")
                            print(f"Point Loads: {pointloads} (position in m and magnitude in N)")
                            print(f"Distributed Loads: {distributedloads} (start, end in m and intensity in N/m)")
                            print(f"Moment Loads: {momentloads} (position in m and moment in N·m)")
                            print(f"Triangular Loads: {triangleloads} (position and magnitude)")
                            print("")
                            cprint("---------------------------------------------------------", 'red')
                            print("Calculating reactions, shear force, and bending moment...")
                        except: 
                            # Handle case where loads are not defined
                            print_error("No loads defined yet!")
                            time.sleep(2)
                            continue

                        try:
                            X_Field, Total_ShearForce, Total_BendingMoment, Reactions = Solver.solve_simple_beam(
                                beam_length, A, B,
                                pointloads_in=pointloads,
                                distributedloads_in=distributedloads,
                                momentloads_in=momentloads,
                                triangleloads_in=triangleloads)
                        except Exception as e:
                            print_error(f"Error solving beam: {e}")
                            time.sleep(2)
                            continue

                        Va = Reactions[0]
                        Ha = Reactions[1]
                        Vb = Reactions[2]
                        max_shear = round(np.max(Total_ShearForce), 3)
                        min_shear = round(np.min(Total_ShearForce), 3)
                        max_bending = round(np.max(Total_BendingMoment), 3)
                        min_bending = round(np.min(Total_BendingMoment), 3)
                        print("Beam analysis completed successfully!")
                        input("Press Enter to return to the Analysis/Simulation menu...")

                    elif sub_choice == '2':
                        try:
                            print("Analysis Results:")
                            cprint("---------------------------------------------------------", 'red')
                            print("")
                            print(f"Reactions: Rv-A: {Va} N")
                            print(f"Reactions: Rh-A: {Ha} N")
                            print(f"Reactions: Rv-B: {Vb} N")
                            print(f"Max Shear Force: {max_shear} N")
                            print(f"Min Shear Force: {min_shear} N")
                            print(f"Max Bending Moment: {max_bending} N·m")
                            print(f"Min Bending Moment: {min_bending} N·m")
                            print("")
                            cprint("---------------------------------------------------------", 'red')
                        except Exception as e:
                            print_error("No analysis results available yet!")
                            time.sleep(2)
                        input("Press Enter to return to the Analysis/Simulation menu...")

                    elif sub_choice == '4':
                        try:
                            Q_array = first_moment_of_area_rect(b, y_array)
                            Total_stress = calculate_shear_stress(Total_ShearForce, Q_array, Ix, b)
                            Max_stress = np.max(Total_stress)
                            sigma = calculate_bending_stress(Total_BendingMoment, c, Ix)
                            Max_sigma = np.max(np.abs(sigma))
                            # Calculate and display Factor of Safety
                            Factor_of_Safety(Total_BendingMoment, c, yield_strength, Ix)
                            print("---------------------------------------------------------")
                            print("")
                            print("Stress and Factor of Safety calculations completed successfully!")
                            time.sleep(2)
                            print("For the shear stress, the maximum value is:", Max_stress, "Pa")
                            print("For the bending stress, the maximum value is:", Max_sigma, "N/m²")
                            print("---------------------------------------------------------")
                        except Exception as e:
                            print_error(f"Error in stress/F.O.S calculations: {e}")
                            time.sleep(2)
                    elif sub_choice == '3':
                        try:
                            print("Calculating deflection...")
                            Deflection,Slope,curv = calculate_beam_deflection(X_Field, Total_BendingMoment, elastic_modulus, Ix)
                            print("Deflection calculations completed successfully!")
                            time.sleep(2)
                        except Exception as e:
                            print_error(f"Error calculating deflection: {e}")
                            time.sleep(2)
        elif selection == '8':  # Postprocessing/Visualization
            while True:
                sub_choice = postprocessing_menu()
                if sub_choice == '6':
                    break
                else:
                    if sub_choice == '1':
                        try:
                            print("Reactions Schematic Plots:")
                            beam_plot.plot_reaction_diagram(A, B, Reactions, support_types)
                        except Exception as e:
                            print_error(f"Error plotting reaction diagram: {e}")
                            time.sleep(2)
                            continue
                    elif sub_choice == '2':
                        try:
                            print("SFD/BMD Plots (Matplotlib):")
                            Plotting.Matplot_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment)
                        except Exception as e:
                            print_error(f"Error plotting using Matplotlib: {e}")
                            time.sleep(2)
                            continue
                    elif sub_choice == '3':
                        try:
                            print("SFD/BMD Plots (Plotly):")
                            Plotting.Plotly_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment, beam_length)
                        except Exception as e:
                            print_error(f"Error plotting using Plotly: {e}")
                            time.sleep(2)
                            continue

                    elif sub_choice == '4':
                        try:
                            print("Deflection/Discplacement Plots (Plotly/Matplotlip):")
                            style = input(colored("Choose a style (1 for Matplotlib, 2 for Plotly) ➔ ", 'cyan'))
                            if style == '1':
                                Plotting.Matplot_Deflection(X_Field, -Deflection)
                            elif style == '2':
                                Plotting.Plotly_Deflection(X_Field,-Deflection,beam_length)
                            else:
                                print_error("Invalid style selection!")
                                time.sleep(2)
                                continue

                        except Exception as e:
                            print_error(f"Error plotting Delection Plot {e}")
                            time.sleep(2)
                            continue
                    elif sub_choice == '4':
                        try:
                            print("Stress/F.O.S Contours:")
                            Plotting.Plotly_stress_contours(X_Field, Total_ShearForce, Total_BendingMoment)
                        except Exception as e:
                            print_error(f"Error plotting stress contours: {e}")
                            time.sleep(2)
                            continue
        elif selection == '9':  # Save Project
            while True:
                    try:
                        save_decision = input(colored("Do you want to save this solved beam? (Y/N) ➔ ", 'cyan'))
                        print("")
                        if save_decision.lower() == 'y':
                            # Save extended parameters including loads, profile, and material data.
                            save_project(beam_length, A, B, A_restraint, B_restraint,
                                         X_Field, Total_ShearForce, Total_BendingMoment, Reactions,
                                         A_type, B_type,
                                         loads_dict=loads_dict if 'loads_dict' in locals() else {},
                                         profile_data={'Ix': Ix, 'shape': shape, 'c': c, 'b': b} if 'Ix' in locals() else {},
                                         material_data={'material': selected_material} if 'selected_material' in locals() else {})
                            save_projects_to_disk()
                            break
                        else:
                            print(colored("Beam not saved. Continuing...", 'yellow'))
                            print("")
                            time.sleep(2)
                            break
                    except: print_error("No project to save!")
        else:
            print_error("Invalid selection! Please try again.")
            time.sleep(1)



        # Keep your Analysis and Postprocessing menus unchanged if not needed for flag-checks






# =============================
# Main Program Execution
# =============================
if __name__ == "__main__":
    # Start the extended menu-driven application.
    run_extended_menu()