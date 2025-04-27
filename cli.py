# cli.py
# --------------------------------------------------------------------------------
#           FANCY CLI SYSTEM - Using Termcolor
# --------------------------------------------------------------------------------
from termcolor import colored
import Solver
import Plotter
import MOI_Solver



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

def moi_menu():
    print_title("Moment of Inertia Calculator 📐")

    print_option("1) Rectangle")
    print_option("2) Square")
    print_option("3) Circle")
    print_option("4) Hollow Rectangle")
    print_option("5) Hollow Square")
    print_option("6) Hollow Circle")
    print_option("7) I-Beam")
    print_option("8) T-Beam")
    print_option("0) Back to Main Menu")

    choice = input(colored("\nSelect cross-section type ➔ ", 'cyan'))
    return choice

# --------------------------------------------------------------------------------
# Example Main App Runner
# --------------------------------------------------------------------------------

if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == '1':
            print_success("Simple Beam Solver - Not implemented yet! 🚧")
            # You will call solver function here
        elif choice == '2':
            print_success("Plotting Diagrams - Not implemented yet! 🎨")
            # You will call plotting function here
        elif choice == '3':
            moi_choice = moi_menu()

            if moi_choice == '1':
                print_success("You selected Rectangle section! 📏")
                # Call inertia_moment_rectangle()
            elif moi_choice == '7':
                print_success("You selected I-Beam section! 🏗️")
                # Call inertia_moment_ibeam()
            elif moi_choice == '8':
                print_success("You selected T-Beam section! 🛠️")
                # Call inertia_moment_tbeam()
            elif moi_choice == '0':
                continue
            else:
                print_error("Invalid MOI Section. Please try again!")

        elif choice == '0':
            print_success("Thanks for using Zylo-X Beam Calculator! Goodbye 🚀")
            break
        else:
            print_error("Invalid choice! Please select a valid option.")
