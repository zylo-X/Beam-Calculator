﻿
from termcolor import colored
import time
import numpy as np
from Menus import print_error, print_success, print_title, print_option, clear_screen

#  Beam Classification Setup

def Beam_Classification():
    """
    Prompt the user to select a beam classification with enhanced
    explanations and visual representations.
    
    Returns:
        str: Selected beam type ("Simple" or "Cantilever")
    """
    clear_screen()
    print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
    print(colored("║                  BEAM CLASSIFICATION                         ║", 'cyan', attrs=['bold']))
    print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
    print("\n")
    
    print(colored("┌─ SELECT BEAM TYPE "+"─"*42, 'yellow', attrs=['bold']))
    print(colored("│", 'yellow'))
    
    # Option 1: Simple Supported Beam
    print(colored("│ 1 - Simple Supported Beam", 'yellow', attrs=['bold']))
    print(colored("│", 'yellow'))
    print(colored("│    Description:", 'green') + colored(" A beam supported at both ends with", 'white'))
    print(colored("│                 ", 'green') + colored(" no portion extending beyond supports.", 'white'))
    print(colored("│", 'yellow'))
    print(colored("│    Visual:", 'green'))
    print(colored("│           ↑                      ↑      ", 'white'))
    print(colored("│           |                      |      ", 'white'))
    print(colored("│    ─────────────────────────────────────", 'white'))
    print(colored("│    ◯                                   △      ", 'white'))
    print(colored("│    Roller                      Pin      ", 'white'))
    print(colored("│", 'yellow'))
    print(colored("│    Applications:", 'green') + colored(" Bridge spans, floor joists, roof beams", 'white'))
    print(colored("│", 'yellow'))
    
    # Option 2: Overhanging Beam
    print(colored("│ 2 - Overhanging Beam", 'yellow', attrs=['bold']))
    print(colored("│", 'yellow'))
    print(colored("│    Description:", 'green') + colored(" A simply supported beam with one or both", 'white'))
    print(colored("│                 ", 'green') + colored(" ends extending beyond the supports.", 'white'))
    print(colored("│", 'yellow'))
    print(colored("│    Visual:", 'green'))
    print(colored("│                 ↑           ↑                ", 'white'))
    print(colored("│                 |           |                ", 'white'))
    print(colored("│    ─────────────────────────────────────────", 'white'))
    print(colored("│                 ◯           △                ", 'white'))
    print(colored("│              Roller        Pin     Overhang ", 'white'))
    print(colored("│", 'yellow'))
    print(colored("│    Applications:", 'green') + colored(" Building eaves, balconies, footbridges,", 'white'))
    print(colored("│                 ", 'green') + colored(" cantilevered structural systems", 'white'))
    print(colored("│", 'yellow'))
    
    # Option 3: Cantilever Beam
    print(colored("│ 3 - Cantilever Beam", 'yellow', attrs=['bold']))
    print(colored("│", 'yellow'))
    print(colored("│    Description:", 'green') + colored(" A beam fixed at one end and free at", 'white'))
    print(colored("│                 ", 'green') + colored(" the other end.", 'white'))
    print(colored("│", 'yellow'))
    print(colored("│    Visual:", 'green'))
    print(colored("│    |", 'white'))
    print(colored("│    |", 'white'))
    print(colored("│    |━━━━━━━━━━━━━━━━━━━━━━━━━", 'white'))
    print(colored("│    |", 'white'))
    print(colored("│  Fixed                  Free", 'white'))
    print(colored("│", 'yellow'))
    print(colored("│    Applications:", 'green') + colored(" Balconies, canopies, crane arms,", 'white'))
    print(colored("│                 ", 'green') + colored(" diving boards, flag poles", 'white'))
    print(colored("│", 'yellow'))
    print(colored("└" + "─"*62, 'yellow', attrs=['bold']))
    
    print("\n")
    classification = input(colored("Enter your choice [1-3] ➔ ", 'cyan', attrs=['bold']))
    
    if classification == '1':
        clear_screen()
        print_success("Simple Supported Beam selected.")
        print("\n")
        print(colored("╔══════════════════════════════════════════════════════════════╗", 'green', attrs=['bold']))
        print(colored("║                SIMPLE SUPPORTED BEAM SELECTED                ║", 'green', attrs=['bold']))
        print(colored("╚══════════════════════════════════════════════════════════════╝", 'green', attrs=['bold']))
        print("\n")
        print(colored("Simple Supported Beam Configuration:", 'white', attrs=['bold']))
        print(colored("• Supports at both ends", 'white'))
        print(colored("• Typically with a pin support at one end and roller at the other", 'white'))
        print(colored("• Free to rotate at supports", 'white'))
        print(colored("• Can handle both symmetric and asymmetric loading", 'white'))
        print("\n")
        print(colored("Next Steps:", 'cyan'))
        print(colored("1. Define beam length", 'white'))
        print(colored("2. Select profile (cross-section)", 'white'))
        print(colored("3. Configure supports", 'white'))
        print("\n")
        input(colored("Press Enter to continue...", 'cyan', attrs=['bold']))
        return "Simple"
        
    elif classification == '2':
        clear_screen()
        print_success("Overhanging Beam selected.")
        print("\n")
        print(colored("╔══════════════════════════════════════════════════════════════╗", 'green', attrs=['bold']))
        print(colored("║                   OVERHANGING BEAM SELECTED                  ║", 'green', attrs=['bold']))
        print(colored("╚══════════════════════════════════════════════════════════════╝", 'green', attrs=['bold']))
        print("\n")
        print(colored("Overhanging Beam Configuration:", 'white', attrs=['bold']))
        print(colored("• Supports at two points with beam extending beyond one or both supports", 'white'))
        print(colored("• Typically uses pin and roller support combination", 'white'))
        print(colored("• Creates both positive and negative bending moments", 'white'))
        print(colored("• Can achieve better moment distribution and material efficiency", 'white'))
        print(colored("• Mathematically treated as a simply supported beam", 'white'))
        print("\n")
        print(colored("Next Steps:", 'cyan'))
        print(colored("1. Define beam length (including overhang portions)", 'white'))
        print(colored("2. Select profile (cross-section)", 'white'))
        print(colored("3. Configure supports and their positions", 'white'))
        print("\n")
        input(colored("Press Enter to continue...", 'cyan', attrs=['bold']))
        return "Simple"  # Returns "Simple" as overhanging beams are a type of simply supported beam
        
    elif classification == '3':
        clear_screen()
        print_success("Cantilever Beam selected.")
        print("\n")
        print(colored("╔══════════════════════════════════════════════════════════════╗", 'green', attrs=['bold']))
        print(colored("║                   CANTILEVER BEAM SELECTED                   ║", 'green', attrs=['bold']))
        print(colored("╚══════════════════════════════════════════════════════════════╝", 'green', attrs=['bold']))
        print("\n")
        print(colored("Cantilever Beam Configuration:", 'white', attrs=['bold']))
        print(colored("• Fixed support at one end (built-in/encastre)", 'white'))
        print(colored("• Free end with no support", 'white'))
        print(colored("• No rotation or translation at fixed support", 'white'))
        print(colored("• Maximum bending moment occurs at the fixed support", 'white'))
        print("\n")
        print(colored("Next Steps:", 'cyan'))
        print(colored("1. Define beam length", 'white'))
        print(colored("2. Select profile (cross-section)", 'white'))
        print(colored("3. Define loads", 'white'))
        print("\n")
        input(colored("Press Enter to continue...", 'cyan', attrs=['bold']))
        return "Cantilever"
        
    else:
        print_error("Invalid selection! Please choose a number between 1 and 3.")
        time.sleep(1.5)
        return Beam_Classification()  # Recursively call the function for another attempt

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
    Display an enhanced interactive menu to manage load inputs with visual aids and 
    engineering guidance for FEA applications.
    
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
        print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
        print(colored("║                  LOADS DEFINITION                            ║", 'cyan', attrs=['bold']))
        print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
        print("\n")
        
        # Display load definitions menu
        print(colored("┌─ LOAD TYPES "+"─"*48, 'yellow', attrs=['bold']))
        
        menu_items = [
            ("➕ Add Point Load", "Concentrated force at a single point"),
            ("📏 Add Distributed Load", "Uniform load over a length"),
            ("🔄 Add Moment Load", "Applied torque at a specific point"),
            ("📐 Add Triangular Load", "Linearly varying load over a length"),
            ("📋 Show Current Loads", "View all defined loads"),
            ("🗑️  Remove All Loads", "Clear all load definitions"),
            ("⬅️  Return to Main Menu", "Go back to the main menu")
        ]
        
        for idx, (title, description) in enumerate(menu_items, 1):
            print(colored(f"│ {idx:2d} │ {title}", 'yellow') + 
                  colored(f" - {description}", 'white'))
        
        print(colored("└───" + "─"*57, 'yellow', attrs=['bold']))
        
        # Display sign convention info
        print("\n")
        print(colored("┌─ SIGN CONVENTION "+"─"*44, 'magenta', attrs=['bold']))
        print(colored("│ Coordinate System:", 'magenta', attrs=['bold']))
        print(colored("│  • X-axis: Horizontal along beam (positive right)", 'magenta'))
        print(colored("│  • Y-axis: Vertical (positive up)", 'magenta'))
        print(colored("│", 'magenta'))
        print(colored("│ Forces:", 'magenta', attrs=['bold']))
        print(colored("│  • Positive Y-force: Upward ↑", 'magenta'))
        print(colored("│  • Positive X-force: Rightward →", 'magenta'))
        print(colored("│", 'magenta'))
        print(colored("│ Moments:", 'magenta', attrs=['bold']))
        print(colored("│  • Positive moment: Counter-clockwise ↺", 'magenta'))
        print(colored("└───" + "─"*57, 'magenta', attrs=['bold']))
        
        print("\n")
        choice = input(colored("Enter your choice [1-7] ➔ ", 'cyan', attrs=['bold']))
    
        if choice == '1':  # Add Point Load
            try:
                clear_screen()
                print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
                print(colored("║                  POINT LOAD DEFINITION                       ║", 'cyan', attrs=['bold']))
                print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
                print("\n")
                
                # Visual representation of point load
                print(colored("┌─ POINT LOAD DIAGRAM "+"─"*40, 'yellow', attrs=['bold']))
                print(colored("│", 'yellow'))
                print(colored("│                  ↓ P (Force)", 'white'))
                print(colored("│                  │", 'white'))
                print(colored("│                  │", 'white'))
                print(colored("│  ─────────────────────────────────────────", 'white'))
                print(colored("│                  ↑", 'white'))
                print(colored("│                  x (Position)", 'white'))
                print(colored("│", 'yellow'))
                print(colored("└───" + "─"*57, 'yellow', attrs=['bold']))
                
                print("\n")
                pos = float(input(colored("Enter position x (m): ➔ ", 'cyan')))
                
                print("\n")
                print(colored("┌─ LOAD TYPE "+"─"*48, 'green', attrs=['bold']))
                print(colored("│ 1 - Vertical Load (Y-direction)", 'green'))
                print(colored("│ 2 - Horizontal Load (X-direction)", 'green'))
                print(colored("│ 3 - Angled Load (Force & Angle)", 'green'))
                print(colored("└───" + "─"*57, 'green', attrs=['bold']))
                print("\n")
                
                load_type = input(colored("Enter your choice [1, 2, or 3] ➔ ", 'cyan'))
                
                if load_type == '1':
                    y_force = float(input(colored("\nEnter Y-force (N) [positive up ↑, negative down ↓]: ➔ ", 'cyan')))
                    loads["pointloads"].append([pos, 0, y_force])
                    print_success(f"Added vertical point load: {y_force} N at x = {pos} m")
                
                elif load_type == '2':
                    x_force = float(input(colored("\nEnter X-force (N) [positive right →, negative left ←]: ➔ ", 'cyan')))
                    loads["pointloads"].append([pos, x_force, 0])
                    print_success(f"Added horizontal point load: {x_force} N at x = {pos} m")
                
                elif load_type == '3':
                    print("\n")
                    print(colored("┌─ ANGLED LOAD "+"─"*46, 'blue', attrs=['bold']))
                    print(colored("│  Angle measured from positive X-axis", 'blue'))
                    print(colored("│         ↑ 90°", 'blue'))
                    print(colored("│         │", 'blue'))
                    print(colored("│  180° ←─┼─→ 0°", 'blue'))
                    print(colored("│         │", 'blue'))
                    print(colored("│        270°", 'blue'))
                    print(colored("└───" + "─"*57, 'blue', attrs=['bold']))
                    print("\n")
                    
                    force_mag = float(input(colored("Enter Force magnitude (N): ➔ ", 'cyan')))
                    angle = float(input(colored("Enter angle (degrees): ➔ ", 'cyan')))
                    x_force = force_mag * np.cos(np.radians(angle))
                    y_force = force_mag * np.sin(np.radians(angle))
                    loads["pointloads"].append([pos, x_force, y_force])
                    print_success(f"Added angled point load: {force_mag} N at {angle}° at x = {pos} m")
                
                else:
                    print_error("Invalid point load type selection!")
                    time.sleep(2)
                
                time.sleep(1.5)
            
            except Exception as e:
                print_error(f"Error adding point load: {e}")
                time.sleep(2)
    
        elif choice == '2':  # Add Distributed Load (UDL)
            try:
                clear_screen()
                print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
                print(colored("║              DISTRIBUTED LOAD DEFINITION                     ║", 'cyan', attrs=['bold']))
                print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
                print("\n")
                
                # Visual representation of UDL
                print(colored("┌─ UNIFORM DISTRIBUTED LOAD DIAGRAM "+"─"*26, 'yellow', attrs=['bold']))
                print(colored("│", 'yellow'))
                print(colored("│              ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓", 'white'))
                print(colored("│              ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼", 'white'))
                print(colored("│              ┏━━━━━━━━━━━━━━━━┓", 'white'))
                print(colored("│  ────────────┻━━━━━━━━━━━━━━━━┻──────────────", 'white'))
                print(colored("│              ↑              ↑", 'white'))
                print(colored("│          start_pos       end_pos", 'white'))
                print(colored("│", 'yellow'))
                print(colored("└───" + "─"*57, 'yellow', attrs=['bold']))
                
                print("\n")
                print(colored("┌─ ENGINEERING NOTE "+"─"*43, 'blue', attrs=['bold']))
                print(colored("│ Distributed loads are important in FEA as they", 'blue'))
                print(colored("│ more accurately represent real-world loading", 'blue'))
                print(colored("│ conditions like self-weight, snow loads, or", 'blue'))
                print(colored("│ pressure loads compared to point loads.", 'blue'))
                print(colored("└───" + "─"*57, 'blue', attrs=['bold']))
                print("\n")
                
                start = float(input(colored("Enter start position (m) for UDL: ➔ ", 'cyan')))
                end = float(input(colored("Enter end position (m) for UDL: ➔ ", 'cyan')))
                intensity = float(input(colored("Enter load intensity (N/m) [positive up ↑, negative down ↓]: ➔ ", 'cyan')))
                
                # Validation
                if start >= end:
                    print_error("End position must be greater than start position!")
                    time.sleep(2)
                    continue
                
                loads["distributedloads"].append([start, end, intensity])
                print_success(f"Added UDL: {intensity} N/m from x = {start} m to x = {end} m")
                time.sleep(1.5)
            
            except Exception as e:
                print_error(f"Error adding distributed load: {e}")
                time.sleep(2)
    
        elif choice == '3':  # Add Moment Load
            try:
                clear_screen()
                print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
                print(colored("║                  MOMENT LOAD DEFINITION                      ║", 'cyan', attrs=['bold']))
                print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
                print("\n")
                
                # Visual representation of moment load
                print(colored("┌─ MOMENT LOAD DIAGRAM "+"─"*39, 'yellow', attrs=['bold']))
                print(colored("│", 'yellow'))
                print(colored("│                   ↺ M (Moment)", 'white'))
                print(colored("│                  ╭─╮", 'white'))
                print(colored("│                  │ │", 'white'))
                print(colored("│  ─────────────────────────────────────────", 'white'))
                print(colored("│                  ↑", 'white'))
                print(colored("│                  x (Position)", 'white'))
                print(colored("│", 'yellow'))
                print(colored("└───" + "─"*57, 'yellow', attrs=['bold']))
                
                print("\n")
                print(colored("┌─ ENGINEERING NOTE "+"─"*43, 'blue', attrs=['bold']))
                print(colored("│ In FEA, moments are crucial for modeling", 'blue'))
                print(colored("│ connections, applied torques, and rotational", 'blue'))
                print(colored("│ constraints. Remember that positive moments", 'blue'))
                print(colored("│ are counter-clockwise (↺).", 'blue'))
                print(colored("└───" + "─"*57, 'blue', attrs=['bold']))
                print("\n")
                
                pos = float(input(colored("Enter position (m) for Moment Load: ➔ ", 'cyan')))
                moment = float(input(colored("Enter moment magnitude (N·m) [positive CCW ↺, negative CW ↻]: ➔ ", 'cyan')))
                
                loads["momentloads"].append([pos, moment])
                print_success(f"Added moment load: {moment} N·m at x = {pos} m")
                time.sleep(1.5)
            
            except Exception as e:
                print_error(f"Error adding moment load: {e}")
                time.sleep(2)
    
        elif choice == '4':  # Add Triangular Load
            try:
                clear_screen()
                print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
                print(colored("║              TRIANGULAR LOAD DEFINITION                      ║", 'cyan', attrs=['bold']))
                print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
                print("\n")
                
                # Visual representation of triangular load
                print(colored("┌─ TRIANGULAR LOAD DIAGRAM "+"─"*36, 'yellow', attrs=['bold']))
                print(colored("│", 'yellow'))
                print(colored("│              ↓  ↓  ↓  ↓  ↓", 'white'))
                print(colored("│              │  │  │  │  │", 'white'))
                print(colored("│              ▼  ▼  ▼  ▼  ▼", 'white'))
                print(colored("│              ┏━━━━━━┓", 'white'))
                print(colored("│  ────────────┻━━━━━━┻──────────────────", 'white'))
                print(colored("│              ↑      ↑", 'white'))
                print(colored("│          start_pos end_pos", 'white'))
                print(colored("│", 'yellow'))
                print(colored("└───" + "─"*57, 'yellow', attrs=['bold']))
                
                print("\n")
                print(colored("┌─ ENGINEERING NOTE "+"─"*43, 'blue', attrs=['bold']))
                print(colored("│ Triangular loads are ideal for modeling", 'blue'))
                print(colored("│ linearly varying loads such as hydrostatic", 'blue'))
                print(colored("│ pressure, wind loads on certain structures,", 'blue'))
                print(colored("│ or soil pressure distributions.", 'blue'))
                print(colored("└───" + "─"*57, 'blue', attrs=['bold']))
                print("\n")
                
                start = float(input(colored("Enter start position (m) for Triangular Load: ➔ ", 'cyan')))
                end = float(input(colored("Enter end position (m) for Triangular Load: ➔ ", 'cyan')))
                
                # Validation
                if start >= end:
                    print_error("End position must be greater than start position!")
                    time.sleep(2)
                    continue
                
                intensity = float(input(colored("Enter peak load intensity (N/m): ➔ ", 'cyan')))
                intensityL = float(input(colored("Enter lowest load intensity (N/m): ➔ ", 'cyan')))
                
                loads["triangleloads"].append([start, end, intensity, intensityL])
                print_success(f"Added triangular load from x = {start} m to x = {end} m")
                print_success(f"Peak intensity: {intensity} N/m, Lowest intensity: {intensityL} N/m")
                time.sleep(1.5)
            
            except Exception as e:
                print_error(f"Error adding triangular load: {e}")
                time.sleep(2)
    
        elif choice == '5':  # Show Current Loads
            clear_screen()
            
            print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
            print(colored("║                    CURRENT LOADS                             ║", 'cyan', attrs=['bold']))
            print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
            print("\n")
            
            # Point Loads Table
            if loads['pointloads']:
                print(colored("┌─ POINT LOADS "+"─"*47, 'yellow', attrs=['bold']))
                print(colored("│ Position (m) | X-Force (N) | Y-Force (N)", 'yellow'))
                print(colored("├" + "─"*61, 'yellow'))
                for i, load in enumerate(loads['pointloads'], 1):
                    pos, x_force, y_force = load
                    print(colored(f"│ {i:2d}) {pos:9.2f} | {x_force:10.2f} | {y_force:10.2f}", 'white'))
                print(colored("└" + "─"*62, 'yellow', attrs=['bold']))
                print("")
            else:
                print(colored("┌─ POINT LOADS "+"─"*47, 'yellow', attrs=['bold']))
                print(colored("│ No point loads defined", 'yellow'))
                print(colored("└" + "─"*62, 'yellow', attrs=['bold']))
                print("")
            
            # Distributed Loads Table
            if loads['distributedloads']:
                print(colored("┌─ DISTRIBUTED LOADS "+"─"*42, 'green', attrs=['bold']))
                print(colored("│ Start (m) | End (m) | Intensity (N/m)", 'green'))
                print(colored("├" + "─"*61, 'green'))
                for i, load in enumerate(loads['distributedloads'], 1):
                    start, end, intensity = load
                    print(colored(f"│ {i:2d}) {start:7.2f} | {end:6.2f} | {intensity:13.2f}", 'white'))
                print(colored("└" + "─"*62, 'green', attrs=['bold']))
                print("")
            else:
                print(colored("┌─ DISTRIBUTED LOADS "+"─"*42, 'green', attrs=['bold']))
                print(colored("│ No distributed loads defined", 'green'))
                print(colored("└" + "─"*62, 'green', attrs=['bold']))
                print("")
            
            # Moment Loads Table
            if loads['momentloads']:
                print(colored("┌─ MOMENT LOADS "+"─"*46, 'magenta', attrs=['bold']))
                print(colored("│ Position (m) | Magnitude (N·m)", 'magenta'))
                print(colored("├" + "─"*61, 'magenta'))
                for i, load in enumerate(loads['momentloads'], 1):
                    pos, moment = load
                    print(colored(f"│ {i:2d}) {pos:9.2f} | {moment:15.2f} {'(CCW ↺)' if moment > 0 else '(CW ↻)'}", 'white'))
                print(colored("└" + "─"*62, 'magenta', attrs=['bold']))
                print("")
            else:
                print(colored("┌─ MOMENT LOADS "+"─"*46, 'magenta', attrs=['bold']))
                print(colored("│ No moment loads defined", 'magenta'))
                print(colored("└" + "─"*62, 'magenta', attrs=['bold']))
                print("")
            
            # Triangular Loads Table
            if loads['triangleloads']:
                print(colored("┌─ TRIANGULAR LOADS "+"─"*43, 'blue', attrs=['bold']))
                print(colored("│ Start (m) | End (m) | Peak (N/m) | Low (N/m)", 'blue'))
                print(colored("├" + "─"*61, 'blue'))
                for i, load in enumerate(loads['triangleloads'], 1):
                    start, end, peak, low = load
                    print(colored(f"│ {i:2d}) {start:7.2f} | {end:6.2f} | {peak:10.2f} | {low:9.2f}", 'white'))
                print(colored("└" + "─"*62, 'blue', attrs=['bold']))
            else:
                print(colored("┌─ TRIANGULAR LOADS "+"─"*43, 'blue', attrs=['bold']))
                print(colored("│ No triangular loads defined", 'blue'))
                print(colored("└" + "─"*62, 'blue', attrs=['bold']))
            
            print("\n")
            input(colored("Press Enter to continue...", 'cyan', attrs=['bold']))
    
        elif choice == '6':  # Remove All Loads
            clear_screen()
            print(colored("╔══════════════════════════════════════════════════════════════╗", 'red', attrs=['bold']))
            print(colored("║                    WARNING                                   ║", 'red', attrs=['bold']))
            print(colored("╚══════════════════════════════════════════════════════════════╝", 'red', attrs=['bold']))
            print("\n")
            
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
                print(colored("No loads were removed.", 'yellow'))
                time.sleep(2)
    
        elif choice == '7':  # Return to Main Menu
            break
        
        else:
            print_error("Invalid selection! Please try again.")
            time.sleep(2)
    
    return loads
