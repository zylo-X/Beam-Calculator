
#!/usr/bin/env python
# coding: utf-8

# --------------------------------------------------------------------------------
# Determined Beam Shear Force and Bending Moment Calculator V1.2
# (Built for simply supported beams under various load conditions)
# --------------------------------------------------------------------------------
    
# ================================
#          Libraries
# ================================

import numpy as np
import plotly 
import plotly.graph_objs as go
import matplotlib.pyplot as plt  

# ================================
#         Beam Geometry
# ================================

Length = 6.4   # Total length of the beam (meters)
A = 1.2        # Position of pin support (meters from origin)
B = 5.2        # Position of roller support (meters from origin)

# ================================
#       Cross Section Profile
# ================================

Profile_Shape = "ibeam"   # Choose from: "ibeam", "circle", "rectangle", "square", "hollow_circle", "hollow_rectangle", "hollow_square"

# ---- I-Beam Dimensions (meters) ----
bf = 0.2      # Flange width
tf = 0.01     # Flange thickness
hw = 0.3      # Web height
tw = 0.005    # Web thickness

# ---- Other Shapes Dimensions (meters) ----
d = 0.2       # Circle diameter
b = 0.1       # Rectangle base
h = 0.3       # Rectangle height
a = 0.2       # Square side length

outer_d = 0.4    # Hollow circle outer diameter
inner_d = 0.3    # Hollow circle inner diameter

outer_b = 0.4    # Hollow rectangle outer base
outer_h = 0.6    # Hollow rectangle outer height
inner_b = 0.3    # Hollow rectangle inner base
inner_h = 0.5    # Hollow rectangle inner height

outer_a = 0.4    # Hollow square outer side
inner_a = 0.2    # Hollow square inner side

# ================================
#         Load Definitions
# ================================

# --- Point Loads: [Position (m), X-Force (kN), Y-Force (kN)] ---
pointloads = np.array([[1, 2, 3],
                       [4, 6, 7]])

# --- Uniform Distributed Loads: [Start (m), End (m), Intensity (kN/m)] ---
distributedloads = np.array([[1.2, 5.2, -2]])

# --- Triangular Distributed Loads: [Start (m), End (m), Start Intensity (kN/m), End Intensity (kN/m)] ---
Triangleloads = np.array([[]])

# --- Point Moments: [Position (m), Magnitude (kNm)] ---
momentloads = np.array([[3.2, -8]])

# ================================
#     Solver Initialization
# ================================

Divisions = 10000    # Number of segments for calculation (higher = more accurate)
Delta = Length / Divisions
X_Field = np.arange(0, Length + Delta, Delta)  # Discretized beam length

# ================================
#   Containers for Calculations
# ================================

# --- Reaction Forces and Recorders ---
Reactions = np.array([0.0, 0.0, 0.0])               # [Va, Ha, Vb]
Force_Reactions_Recorder = np.empty((0, 3))
Moment_Reactions_Recorder = np.empty((0, 2))
UDLs_Reactions_Recorder = np.empty((0, 2))
TRLs_Reactions_Recorder = np.empty((0, 2))

# --- Shear Force and Bending Moment Recorders ---
ShearForce_Recorder = np.empty((0, len(X_Field)))
BendingMoment_Recorder = np.empty((0, len(X_Field)))

# --- Check presence of different loads ---
Test_pointloads = len(pointloads[0])
Test_momentloads = len(momentloads[0])
Test_UDLs = len(distributedloads[0])
Test_TRLs = len(Triangleloads[0])

# --------------------------------------------------------------------------------
#            Moment of Inertia (MOI) Solver
# --------------------------------------------------------------------------------

# --- Functions for Different Cross-Sections ---

def inertia_moment_ibeam(bf, tf, hw, tw):
    """Calculate moment of inertia for an I-Beam."""
    Ix = (bf * tf**3 / 12) + (bf * tf * (hw/2 - tf/2)**2) + (tw * hw**3 / 12)
    return Ix

def inertia_moment_circle(diameter):
    """Calculate moment of inertia for a circle."""
    r = diameter / 2
    return (np.pi * r**4) / 4

def inertia_moment_rectangle(b, h):
    """Calculate moment of inertia for a rectangle."""
    return b * h**3 / 12

def inertia_moment_square(a):
    """Calculate moment of inertia for a square."""
    return a**4 / 12

def inertia_moment_hollow_circle(outer_diameter, inner_diameter):
    """Calculate moment of inertia for a hollow circle."""
    r_outer = outer_diameter / 2
    r_inner = inner_diameter / 2
    return (np.pi * (r_outer**4 - r_inner**4)) / 4

def inertia_moment_hollow_square(outer_width, inner_width):
    """Calculate moment of inertia for a hollow square."""
    return (outer_width**4 - inner_width**4) / 12

def inertia_moment_hollow_rectangle(outer_b, outer_h, inner_b, inner_h):
    """Calculate moment of inertia for a hollow rectangle."""
    return (outer_b * outer_h**3 / 12) - (inner_b * inner_h**3 / 12)

# --- Moment of Inertia Calculation based on Selected Profile ---
if Profile_Shape == "ibeam":
    Ix_ibeam = inertia_moment_ibeam(bf, tf, hw, tw)
elif Profile_Shape == "circle":
    Ix_circle = inertia_moment_circle(d)
elif Profile_Shape == "rectangle":
    Ix_rectangle = inertia_moment_rectangle(b, h)
elif Profile_Shape == "square":
    Ix_square = inertia_moment_square(a)
elif Profile_Shape == "hollow_circle":
    Ix_hollow_circle = inertia_moment_hollow_circle(outer_d, inner_d)
elif Profile_Shape == "hollow_rectangle":
    Ix_hollow_rectangle = inertia_moment_hollow_rectangle(outer_b, outer_h, inner_b, inner_h)
elif Profile_Shape == "hollow_square":
    Ix_hollow_square = inertia_moment_hollow_square(outer_a, inner_a)

# --------------------------------------------------------------------------------
#              REACTION SOLVER SECTION
# --------------------------------------------------------------------------------

# --- Functions for Calculating Reactions Based on Load Types ---

def Calculate_Force_Reactions(n):
    """Calculate reactions at supports due to a point force."""
    Xp = pointloads[n, 0]         # Point Load Position
    Fx = pointloads[n, 1]         # X-component (horizontal force)
    Fy = pointloads[n, 2]         # Y-component (vertical force)

    Vb = Fy * (A - Xp) / (B - A)  # Vertical Reaction at B using moment equilibrium
    Va = -Fy - Vb                 # Vertical Reaction at A from force equilibrium
    Ha = Fx                       # Horizontal Reaction at A (Roller allows movement, Pin resists Fx)

    return Va, Vb, Ha

def Calculate_Moment_Reactions(n):
    """Calculate reactions at supports due to an applied point moment."""
    Xm = momentloads[n, 0]    # Moment position
    m = momentloads[n, 1]     # Moment magnitude

    Vb = m / (B - A)          # Reaction at B
    Va = -Vb                  # Reaction at A (equilibrium)

    return Va, Vb

def Calculate_UDL_Reactions(n):
    """Calculate reactions at supports due to a Uniformly Distributed Load (UDL)."""
    Xstart = distributedloads[n, 0]
    Xend = distributedloads[n, 1]
    Fy = distributedloads[n, 2]

    Fy_res = Fy * (Xend - Xstart)          # Resultant Force of UDL
    X_res = Xstart + 0.5 * (Xend - Xstart) # Centroid Position

    Vb = Fy_res * (A - X_res) / (B - A)
    Va = -Fy_res - Vb

    return Va, Vb

def Calculate_TRL_Reactions(n):
    """Calculate reactions at supports due to a Triangular Distributed Load."""
    Xstart = Triangleloads[n, 0]
    Xend = Triangleloads[n, 1]
    Fy_start = Triangleloads[n, 2]
    Fy_end = Triangleloads[n, 3]

    if abs(Fy_start) > 0:
        # Triangle rising from left to right
        Fy_res = 0.5 * Fy_start * (Xend - Xstart)
        X_res = Xstart + (1/3)*(Xend - Xstart)
    else:
        # Triangle falling from left to right
        Fy_res = 0.5 * Fy_end * (Xend - Xstart)
        X_res = Xstart + (2/3)*(Xend - Xstart)

    Vb = Fy_res * (A - X_res) / (B - A)
    Va = -Fy_res - Vb

    return Va, Vb

# --------------------------------------------------------------------------------
#            Main Reaction Calculation Routine
# --------------------------------------------------------------------------------

# --- Solve Reactions Due to Point Loads ---
if Test_pointloads > 0:
    for n, _ in enumerate(pointloads):
        Va, Vb, Ha = Calculate_Force_Reactions(n)

        new_reaction = np.array([[Va, Ha, Vb]])
        Force_Reactions_Recorder = np.vstack([Force_Reactions_Recorder, new_reaction])  # (Optimized)

        Reactions[0] += Va
        Reactions[1] += Ha
        Reactions[2] += Vb

# --- Solve Reactions Due to Point Moments ---
if Test_momentloads > 0:
    for n, _ in enumerate(momentloads):
        Va, Vb = Calculate_Moment_Reactions(n)

        new_reaction = np.array([[Va, Vb]])
        Moment_Reactions_Recorder = np.vstack([Moment_Reactions_Recorder, new_reaction])  # (Optimized)

        Reactions[0] += Va
        Reactions[2] += Vb

# --- Solve Reactions Due to Uniform Distributed Loads (UDLs) ---
if Test_UDLs > 0:
    for n, _ in enumerate(distributedloads):
        Va, Vb = Calculate_UDL_Reactions(n)

        new_reaction = np.array([[Va, Vb]])
        UDLs_Reactions_Recorder = np.vstack([UDLs_Reactions_Recorder, new_reaction])  # (Optimized)

        Reactions[0] += Va
        Reactions[2] += Vb

# --- Solve Reactions Due to Triangular Distributed Loads ---
if Test_TRLs > 0:
    for n, _ in enumerate(Triangleloads):
        Va, Vb = Calculate_TRL_Reactions(n)

        new_reaction = np.array([[Va, Vb]])
        TRLs_Reactions_Recorder = np.vstack([TRLs_Reactions_Recorder, new_reaction])  # (Optimized)

        Reactions[0] += Va
        Reactions[2] += Vb

# --------------------------------------------------------------------------------
#         SHEAR FORCE AND BENDING MOMENT SOLVER SECTION
# --------------------------------------------------------------------------------

# --- Functions for Calculating SF and BM from Each Load Type ---

def Calculate_SF_BM_Force(n):
    """Calculate Shear Force and Bending Moment across the beam due to a point load."""
    Xp = pointloads[n, 0]
    Fy = pointloads[n, 2]
    Va = Force_Reactions_Recorder[n, 0]
    Vb = Force_Reactions_Recorder[n, 2]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0

        # Apply support reactions
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)

        # Apply point load
        if x > Xp:
            shear += Fy
            moment -= Fy * (x - Xp)

        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

def Calculate_SF_BM_Moment(n):
    """Calculate Shear Force and Bending Moment across the beam due to a point moment."""
    Xm = momentloads[n, 0]
    m = momentloads[n, 1]
    Va = Moment_Reactions_Recorder[n, 0]
    Vb = Moment_Reactions_Recorder[n, 1]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0

        # Apply support reactions
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)

        # Apply point moment
        if x > Xm:
            moment -= m

        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

def Calculate_SF_BM_UDL(n):
    """Calculate Shear Force and Bending Moment across the beam due to a Uniform Distributed Load."""
    Xstart = distributedloads[n, 0]
    Xend = distributedloads[n, 1]
    Fy = distributedloads[n, 2]
    Va = UDLs_Reactions_Recorder[n, 0]
    Vb = UDLs_Reactions_Recorder[n, 1]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0

        # Apply support reactions
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)

        # Apply UDL effect
        if Xstart < x <= Xend:
            shear += Fy * (x - Xstart)
            moment -= Fy * (x - Xstart) * 0.5 * (x - Xstart)

        elif x > Xend:
            shear += Fy * (Xend - Xstart)
            moment -= Fy * (Xend - Xstart) * (x - Xstart - 0.5 * (Xend - Xstart))

        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

def Calculate_SF_BM_TRL(n):
    """Calculate Shear Force and Bending Moment across the beam due to a Triangular Distributed Load."""
    Xstart = Triangleloads[n, 0]
    Xend = Triangleloads[n, 1]
    Fy_start = Triangleloads[n, 2]
    Fy_end = Triangleloads[n, 3]
    Va = TRLs_Reactions_Recorder[n, 0]
    Vb = TRLs_Reactions_Recorder[n, 1]

    ShearForce = np.zeros(len(X_Field))
    BendingMoment = np.zeros(len(X_Field))

    for i, x in enumerate(X_Field):
        shear = 0
        moment = 0

        # Apply support reactions
        if x > A:
            shear += Va
            moment -= Va * (x - A)
        if x > B:
            shear += Vb
            moment -= Vb * (x - B)

        # Apply triangular load effect
        if Xstart < x <= Xend:

            if abs(Fy_start) > 0:
                # Triangle rises from start
                Xbase = x - Xstart
                F_cut = Fy_start - Xbase * (Fy_start / (Xend - Xstart))
                R1 = 0.5 * Xbase * (Fy_start - F_cut)
                R2 = Xbase * F_cut
                shear += R1 + R2
                moment -= R1 * (2/3) * Xbase + R2 * 0.5 * Xbase
            else:
                # Triangle falls from start
                Xbase = x - Xstart
                F_cut = Fy_end * (Xbase / (Xend - Xstart))
                R = 0.5 * Xbase * F_cut
                shear += R
                moment -= R * (1/3) * Xbase

        elif x > Xend:
            if abs(Fy_start) > 0:
                R = 0.5 * Fy_start * (Xend - Xstart)
                Xr = Xstart + (1/3) * (Xend - Xstart)
                shear += R
                moment -= R * (x - Xr)
            else:
                R = 0.5 * Fy_end * (Xend - Xstart)
                Xr = Xstart + (2/3) * (Xend - Xstart)
                shear += R
                moment -= R * (x - Xr)

        ShearForce[i] = shear
        BendingMoment[i] = moment

    return ShearForce, BendingMoment

# --------------------------------------------------------------------------------
#           Main Solver Routine for SF and BM
# --------------------------------------------------------------------------------

# --- Sum all Shear Forces and Bending Moments across all load types ---

if Test_pointloads > 0:
    for n, _ in enumerate(pointloads):
        Shear, Moment = Calculate_SF_BM_Force(n)
        ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])    # (Optimized)
        BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])  # (Optimized)

if Test_momentloads > 0:
    for n, _ in enumerate(momentloads):
        Shear, Moment = Calculate_SF_BM_Moment(n)
        ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])    # (Optimized)
        BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])  # (Optimized)

if Test_UDLs > 0:
    for n, _ in enumerate(distributedloads):
        Shear, Moment = Calculate_SF_BM_UDL(n)
        ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])    # (Optimized)
        BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])  # (Optimized)

if Test_TRLs > 0:
    for n, _ in enumerate(Triangleloads):
        Shear, Moment = Calculate_SF_BM_TRL(n)
        ShearForce_Recorder = np.vstack([ShearForce_Recorder, Shear])    # (Optimized)
        BendingMoment_Recorder = np.vstack([BendingMoment_Recorder, Moment])  # (Optimized)

# --- Final Total Shear Force and Bending Moment Fields ---
Total_ShearForce = np.sum(ShearForce_Recorder, axis=0)
Total_BendingMoment = -np.sum(BendingMoment_Recorder, axis=0)

# --------------------------------------------------------------------------------
#               RESULTS AND DIAGRAMS OUTPUT SECTION
# --------------------------------------------------------------------------------

# ================================
#        PRINTING RESULTS
# ================================

# --- Print Inertia Moment if Profile is selected ---
print("----------------------------------------------------------------------")
if Profile_Shape == "ibeam":
    print(f"Inertia moment for I-beam = {Ix_ibeam:.4f} m⁴")
elif Profile_Shape == "circle":
    print(f"Inertia moment for circle = {Ix_circle:.4f} m⁴")
elif Profile_Shape == "rectangle":
    print(f"Inertia moment for rectangle = {Ix_rectangle:.4f} m⁴")
elif Profile_Shape == "square":
    print(f"Inertia moment for square = {Ix_square:.4f} m⁴")
elif Profile_Shape == "hollow_circle":
    print(f"Inertia moment for hollow circle = {Ix_hollow_circle:.4f} m⁴")
elif Profile_Shape == "hollow_rectangle":
    print(f"Inertia moment for hollow rectangle = {Ix_hollow_rectangle:.4f} m⁴")
elif Profile_Shape == "hollow_square":
    print(f"Inertia moment for hollow square = {Ix_hollow_square:.4f} m⁴")
else:
    print("Profile shape not correctly defined.")

print("----------------------------------------------------------------------")
print(f"Reaction at Left Support (A): {round(Reactions[0], 2)} kN")
print(f"Reaction at Right Support (B): {round(Reactions[2], 2)} kN")
print("----------------------------------------------------------------------")
print(f"Maximum Shear Force: {round(np.max(np.abs(Total_ShearForce)), 2)} kN")
print(f"Maximum Bending Moment: {round(np.max(np.abs(Total_BendingMoment)), 2)} kNm")
print("----------------------------------------------------------------------")

# ================================
#        PREPARE PLOTTING DATA
# ================================

# --- Shear Force Diagram Data ---
x_shear = X_Field
y_shear = Total_ShearForce

# --- Bending Moment Diagram Data ---
x_bend = X_Field
y_bend = Total_BendingMoment

# Find max/min values and their positions for annotations
max_shear = round(np.max(y_shear), 3)
min_shear = round(np.min(y_shear), 3)
max_bend = round(np.max(y_bend), 3)
min_bend = round(np.min(y_bend), 3)

idx_max_shear = np.argmax(y_shear)
idx_min_shear = np.argmin(y_shear)
idx_max_bend = np.argmax(y_bend)
idx_min_bend = np.argmin(y_bend)

# ================================
#        CREATE PLOTLY TRACES
# ================================

# --- Shear Force Trace ---
trace_shear = go.Scatter(
    x=x_shear,
    y=y_shear,
    mode="lines",
    line=dict(color='blue', width=3),   # (Optimized: More visible line)
    name="Shear Force",
    hovertemplate="Position: %{x:.2f} m<br>Shear Force: %{y:.2f} kN",
    fill="tozeroy",
    fillcolor="rgba(0,0,255,0.2)"        # (Optimized: Lighter fill)
)

# --- Bending Moment Trace ---
trace_bend = go.Scatter(
    x=x_bend,
    y=y_bend,
    mode="lines",
    line=dict(color='red', width=3),    # (Optimized: More visible line)
    name="Bending Moment",
    hovertemplate="Position: %{x:.2f} m<br>Bending Moment: %{y:.2f} kNm",
    fill="tozeroy",
    fillcolor="rgba(255,0,0,0.2)"        # (Optimized: Lighter fill)
)

# --- Horizontal Axis Line (Reference) ---
trace_line = go.Scatter(
    x=[0, Length],
    y=[0, 0],
    mode="lines",
    line=dict(color="black", width=2),
    showlegend=False
)

# ================================
#         ANNOTATIONS
# ================================

# --- Annotations for SFD ---
annotations_shear = [
    dict(
        x=x_shear[idx_max_shear],
        y=max_shear,
        text=f"Max: {max_shear} kN",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-30,
        font=dict(color="blue")
    ),
    dict(
        x=x_shear[idx_min_shear],
        y=min_shear,
        text=f"Min: {min_shear} kN",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=30,
        font=dict(color="blue")
    )
]

# --- Annotations for BMD ---
annotations_bend = [
    dict(
        x=x_bend[idx_max_bend],
        y=max_bend,
        text=f"Max: {max_bend} kNm",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-30,
        font=dict(color="red")
    ),
    dict(
        x=x_bend[idx_min_bend],
        y=min_bend,
        text=f"Min: {min_bend} kNm",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=30,
        font=dict(color="red")
    )
]

# ================================
#         PLOT LAYOUTS
# ================================

# --- Layout for Shear Force Diagram ---
layout_shear = go.Layout(
    title="Shear Force Diagram",
    xaxis=dict(title="Position along Beam (m)"),
    yaxis=dict(title="Shear Force (kN)"),
    annotations=annotations_shear,
    width=700,
    height=500
)

# --- Layout for Bending Moment Diagram ---
layout_bend = go.Layout(
    title="Bending Moment Diagram",
    xaxis=dict(title="Position along Beam (m)"),
    yaxis=dict(title="Bending Moment (kNm)"),
    annotations=annotations_bend,
    width=700,
    height=500
)

# ================================
#         FINAL PLOTS
# ================================

# --- Build Figures ---
fig_shear = go.Figure(data=[trace_shear, trace_line], layout=layout_shear)
fig_bend = go.Figure(data=[trace_bend, trace_line], layout=layout_bend)
# --- Show Plotly Figures ---
fig_shear.show()
fig_bend.show()

# --------------------------------------------------------------------------------

# ================================
#         Matplotlib Diagrams
# ================================


# Create the shear force diagram
fig_shear, ax_shear = plt.subplots(figsize=(10, 8))
ax_shear.plot(x_shear, y_shear, color='black', label='Shear Force')
ax_shear.fill_between(x_shear, y_shear, 0, where=(y_shear>=0), interpolate=True, alpha=0.5, color='blue')
ax_shear.fill_between(x_shear, y_shear, 0, where=(y_shear<0), interpolate=True, alpha=0.5, color='red')
ax_shear.axhline(y=0, color='black', linewidth=3)
ax_shear.set_title('Shear Force Diagram')
ax_shear.set_xlabel('Position (m)')
ax_shear.set_ylabel('Shear Force (kN)')

# Adjust the position of the min and max labels
ax_shear.annotate(f"Max: {max_shear} kN", xy=(x_shear[idx_max_shear], max_shear), xytext=(0.05, 0.95),
                  textcoords="axes fraction", ha="left", va="top", arrowprops=dict(arrowstyle="->"))
ax_shear.annotate(f"Min: {min_shear} kN", xy=(x_shear[idx_min_shear], min_shear), xytext=(0.05, 0.05),
                  textcoords="axes fraction", ha="left", va="center", arrowprops=dict(arrowstyle="->"))
ax_shear.legend()

# Create the bending moment diagram
fig_bend, ax_bend = plt.subplots(figsize=(10, 8))
ax_bend.plot(x_bend, y_bend, color='black', label='Bending Moment')
ax_bend.fill_between(x_bend, y_bend, 0, where=(y_bend>=0), interpolate=True, alpha=0.5, color='red')
ax_bend.fill_between(x_bend, y_bend, 0, where=(y_bend<0), interpolate=True, alpha=0.5, color='blue')
ax_bend.axhline(y=0, color='black', linewidth=3)
ax_bend.set_title('Bending Moment Diagram')
ax_bend.set_xlabel('Position (m)')
ax_bend.set_ylabel('Bending Moment (kNm)')

# Adjust the position of the min and max labels
ax_bend.annotate(f"Max: {max_bend} kNm", xy=(x_bend[idx_max_bend], max_bend), xytext=(0.05, 0.95),
                  textcoords="axes fraction", ha="left", va="top", arrowprops=dict(arrowstyle="->"))
ax_bend.annotate(f"Min: {min_bend} kNm", xy=(x_bend[idx_min_bend], min_bend), xytext=(0.05, 0.05),
                  textcoords="axes fraction", ha="left", va="center", arrowprops=dict(arrowstyle="->"))
ax_bend.legend()




# --- Show Matplotlib Figures ---
plt.show()