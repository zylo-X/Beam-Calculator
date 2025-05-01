import os
import time
from termcolor import colored, cprint

# =============================
# Utility & Helper Functions
# =============================
def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_title(title):
    """Print a formatted title for menus and sections."""
    print(colored(f"\n=== {title} ===\n", 'cyan', attrs=['bold']))


def print_option(option):
    """Print a formatted option."""
    print(colored(option, 'yellow'))


def print_error(error_msg):
    """Print an error message (in red)."""
    print(colored(error_msg, 'red', attrs=['bold']))


def print_success(msg):
    """Print a success message (in green)."""
    print(colored(msg, 'green'))

# =============================
# Extended Main Menu and Runner
# =============================
def main_menu_template():
    """Display the main menu and return the user's selection."""
    clear_screen()
    print_title("Main Menu")
    print_option("1 - Project Management")
    print_option("2 - Profile Definition")
    print_option("3 - Material Selection")
    print_option("4 - Boundary Conditions")
    print_option("5 - Loads Definition")
    print_option("6 - Show Beam Schematic")
    print_option("7 - Analysis/Simulation")
    print_option("8 - Postprocessing/Visualization")
    print_option("9 - Save Project")
    print("")
    selection = input(colored("Enter your selection: ➔ ", 'cyan'))
    return selection

# =============================
# Project Management Functions
# =============================
def project_management_menu():
    """Display the project management submenu and return the user's choice."""
    clear_screen()
    print_title("Project Management")
    print_option("1 - New Project")
    print_option("2 - Load Project")
    print_option("3 - Delete Project")
    print_option("4 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice



# =============================
# Profile Definition Functions
# =============================
def profile_definition_menu():
    """Display the profile definition menu and return the user's choice."""
    clear_screen()
    print_title("Profile Definition")
    print_option("1 - Enter Beam Length (m)")
    print_option("2 - Define Profile")
    print_option("3 - View Current Profile")
    print_option("4 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice

def choose_profile():
    """
    Display available profile options and prompt for a choice.
    
    Returns:
        str: The chosen profile number (as a string).
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
    print("")
    profile_choice = input(colored("Enter your preferred profile number ➔ ", 'cyan'))
    return profile_choice


# =============================
# Material Selection Functions
# =============================
def material_selection_menu():
    """
    Display the material selection menu.
    Loads the material database and returns the user's choice.
    """
    
    clear_screen()
    print_title("Material Selection")
    print_option("1 - Select Material")
    print_option("2 - View Current Material Details")
    print_option("3 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice


# =============================
# Boundary Conditions Functions
# =============================
def boundary_conditions_menu():
    """Display the boundary conditions menu and return the user's choice."""
    clear_screen()
    print_title("Boundary Conditions")
    print_option("1 - Define Supports")
    print_option("2 - View Supports")
    print_option("3 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice

# =============================
# Loads Definition Functions
# =============================
def loads_definition_menu():
    """Display the loads definition menu and return the user's choice."""
    clear_screen()
    print_title("Loads Definition")
    print_option("1 - Define Loads")
    print_option("2 - View Loads")
    print_option("3 - Show Beam Schematic")
    print_option("4 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice

# =============================
# Analysis/Simulation & Postprocessing Functions
# =============================
def analysis_simulation_menu():
    """Display the analysis/simulation menu and return the user's choice."""
    clear_screen()
    print_title("Analysis/Simulation")
    print_option("1 - Solve Beam")
    print_option("2 - View Analysis Results")
    print_option("3 - Calculate Deflection")
    print_option("4 - Calculate Stress and F.O.S")
    print_option("5 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice

# =============================
# Postprocessing Functions
# =============================

def postprocessing_menu():
    """Display the postprocessing/visualization menu and return the user's choice."""
    clear_screen()
    print_title("Postprocessing/Visualization")
    print_option("1 - Reactions Schematic Plots")
    print_option("2 - SFD/BMD Plots (Matplotlib)")
    print_option("3 - SFD/BMD Plots (Plotly)")
    print_option("4 - Deflection Plots (Plotly)")
    print_option("5 - Stress/F.O.S Contours")
    print_option("6 - Return to Main Menu")
    print("")
    choice = input(colored("Enter your choice: ➔ ", 'cyan'))
    return choice

