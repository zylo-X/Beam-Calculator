import numpy as np
import plotly.graph_objs as go
import matplotlib.pyplot as plt 

def Plotly_shear_force(X_Field,Total_ShearForce,beam_length):
    # --- Shear Force Diagram Data ---
    x_shear = X_Field
    y_shear = Total_ShearForce

    # Find max/min values and their positions for annotations
    max_shear = round(np.max(y_shear), 3)
    min_shear = round(np.min(y_shear), 3)
    idx_max_shear = np.argmax(y_shear)
    idx_min_shear = np.argmin(y_shear)
# --- Shear Force Trace ---
    trace_shear = go.Scatter(
        x=x_shear,
        y=y_shear,
        mode="lines",
        line=dict(color='blue', width=3),   # (Optimized: More visible line)
        name="Shear Force",
        hovertemplate="Position: %{x:.2f} m<br>Shear Force: %{y:.2f} N",
        fill="tozeroy",
        fillcolor="rgba(0,0,255,0.2)"    # (Optimized: Lighter fill)
    )
    
     # --- Horizontal Axis Line (Reference) ---
    trace_line = go.Scatter(
        x=[0, beam_length],
        y=[0, 0],
        mode="lines",
        line=dict(color="black", width=2),
        showlegend=False
    )

# --- Annotations for SFD ---
    annotations_shear = [
        dict(
            x=x_shear[idx_max_shear],
            y=max_shear,
            text=f"Max: {max_shear} N",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(color="blue")
        ),
        dict(
            x=x_shear[idx_min_shear],
            y=min_shear,
            text=f"Min: {min_shear} N",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=30,
            font=dict(color="blue")
        )
    ]
        # ================================
        #         PLOT LAYOUTS
        # ================================

# --- Layout for Shear Force Diagram ---
    layout_shear = go.Layout(
        title="Shear Force Diagram",
        xaxis=dict(title="Position along Beam (m)"),
        yaxis=dict(title="Shear Force (N)"),
        annotations=annotations_shear,
        width=700,
        height=500
)
    # --- Build Figures ---
    fig_shear = go.Figure(data=[trace_shear, trace_line], layout=layout_shear)
    fig_shear.show()




def Plotly_Deflection(X_Field,Deflection,beam_length):
    # --- Deflection Diagram Data ---
    x_Deflection = X_Field
    y_Deflection = Deflection

    # Find max/min values and their positions for annotations
    max_Deflection = round(np.max(y_Deflection), 3)
    min_Deflection = round(np.min(y_Deflection), 3)
    idx_max_Deflection = np.argmax(y_Deflection)
    idx_min_Deflection = np.argmin(y_Deflection)
# --- Deflection Trace ---
    trace_shear = go.Scatter(
        x=x_Deflection,
        y=y_Deflection,
        mode="lines",
        line=dict(color='blue', width=3),   # (Optimized: More visible line)
        name="Deflection",
        hovertemplate="Position: %{x:.2f} m<br>Deflection: %{y:.2f} N",
        fill="tozeroy",
        fillcolor="rgba(0,0,255,0.2)"    # (Optimized: Lighter fill)
    )
    
     # --- Horizontal Axis Line (Reference) ---
    trace_line = go.Scatter(
        x=[0, beam_length],
        y=[0, 0],
        mode="lines",
        line=dict(color="black", width=2),
        showlegend=False
    )

# --- Annotations for Deflection ---
    annotations_Deflection = [
        dict(
            x=x_Deflection[idx_max_Deflection],
            y=max_Deflection,
            text=f"Max: {max_Deflection} N",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(color="blue")
        ),
        dict(
            x=x_Deflection[idx_min_Deflection],
            y=min_Deflection,
            text=f"Min: {min_Deflection} N",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=30,
            font=dict(color="blue")
        )
    ]
        # ================================
        #         PLOT LAYOUTS
        # ================================

# --- Layout for Deflection Diagram ---
    layout_Deflection = go.Layout(
        title="Deflection Diagram",
        xaxis=dict(title="Position along Beam (m)"),
        yaxis=dict(title="Deflection(m)"),
        annotations=annotations_Deflection,
        width=1000,
        height=800
)
    # --- Build Figures ---
    fig_shear = go.Figure(data=[trace_shear, trace_line], layout=layout_Deflection)
    fig_shear.show()





def Plotly_bending_moment(X_Field,Total_BendingMoment,beam_length):
    # --- Bending Moment Diagram Data ---
    x_bend = X_Field
    y_bend = Total_BendingMoment

    # Find max/min values and their positions for annotations
    max_bend = round(np.max(y_bend), 3)
    min_bend = round(np.min(y_bend), 3)
    idx_max_bend = np.argmax(y_bend)
    idx_min_bend = np.argmin(y_bend)

    # ================================
    #        CREATE PLOTLY TRACES
    # ================================
    # --- Bending Moment Trace ---
    trace_bend = go.Scatter(
        x=x_bend,
        y=y_bend,
        mode="lines",
        line=dict(color='red', width=3),    # (Optimized: More visible line)
        name="Bending Moment",
        hovertemplate="Position: %{x:.2f} m<br>Bending Moment: %{y:.2f} N.m",
        fill="tozeroy",
        fillcolor="rgba(255,0,0,0.2)"        # (Optimized: Lighter fill)
        )
    # --- Horizontal Axis Line (Reference) ---
    trace_line = go.Scatter(
        x=[0, beam_length],
        y=[0, 0],
        mode="lines",
        line=dict(color="black", width=2),
        showlegend=False
    )

    # ================================
    #         ANNOTATIONS
    # ================================
    # --- Annotations for BMD ---
    annotations_bend = [
        dict(
            x=x_bend[idx_max_bend],
            y=max_bend,
            text=f"Max: {max_bend} N.m",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(color="red")
        ),
        dict(
            x=x_bend[idx_min_bend],
            y=min_bend,
            text=f"Min: {min_bend} N.m",
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

    # --- Layout for Bending Moment Diagram ---
    layout_bend = go.Layout(
        title="Bending Moment Diagram",
        xaxis=dict(title="Position along Beam (m)"),
        yaxis=dict(title="Bending Moment (N.m)"),
        annotations=annotations_bend,
        width=700,
        height=500
)

    # ================================
    #         FINAL PLOTS
    # ================================
    # --- Build Figures ---
    fig_bend = go.Figure(data=[trace_bend, trace_line], layout=layout_bend)
    # --- Show Plotly Figures ---
    fig_bend.show()


def Matplot_shear_force(X_Field,Total_ShearForce):
    # --- Shear Force Diagram Data ---
    x_shear = X_Field
    y_shear = Total_ShearForce

    # Find max/min values and their positions for annotations
    max_shear = round(np.max(y_shear), 3)
    min_shear = round(np.min(y_shear), 3)
    idx_max_shear = np.argmax(y_shear)
    idx_min_shear = np.argmin(y_shear)

    fig_shear, ax_shear = plt.subplots(figsize=(10, 6))

    ax_shear.plot(x_shear, y_shear, color='black', linewidth=2, label='Shear Force')
    ax_shear.fill_between(x_shear, y_shear, 0, where=(y_shear >= 0), interpolate=True, alpha=0.3, color='blue')
    ax_shear.fill_between(x_shear, y_shear, 0, where=(y_shear < 0), interpolate=True, alpha=0.3, color='red')

    ax_shear.axhline(y=0, color='black', linewidth=2)
    ax_shear.set_title('Shear Force Diagram', fontsize=16)
    ax_shear.set_xlabel('Position along Beam (m)', fontsize=14)
    ax_shear.set_ylabel('Shear Force (N)', fontsize=14)

    # Annotate Max and Min points
    ax_shear.annotate(f"Max: {max_shear:.2f} N", 
                      xy=(x_shear[idx_max_shear], max_shear), 
                      xytext=(10, 30), textcoords='offset points',
                      arrowprops=dict(arrowstyle="->", color='blue'),
                      fontsize=12, color='blue')

    ax_shear.annotate(f"Min: {min_shear:.2f} N", 
                      xy=(x_shear[idx_min_shear], min_shear), 
                      xytext=(10, -40), textcoords='offset points',
                      arrowprops=dict(arrowstyle="->", color='red'),
                      fontsize=12, color='red')

    ax_shear.legend()
    ax_shear.grid(True)

    # --- Show Shear Force Plot Separately ---
    fig_shear.tight_layout()
    fig_shear.show()
    #plt.close(fig_shear)

def Matplot_bending_moment(X_Field,Total_BendingMoment):
    # --- Bending Moment Diagram Data ---
    x_bend = X_Field
    y_bend = Total_BendingMoment

    # Find max/min values and their positions for annotations
    max_bend = round(np.max(y_bend), 3)
    min_bend = round(np.min(y_bend), 3)
    idx_max_bend = np.argmax(y_bend)
    idx_min_bend = np.argmin(y_bend)

    # --- Create the Bending Moment Diagram ---
    fig_bend, ax_bend = plt.subplots(figsize=(10, 6))

    ax_bend.plot(x_bend, y_bend, color='black', linewidth=2, label='Bending Moment')
    ax_bend.fill_between(x_bend, y_bend, 0, where=(y_bend >= 0), interpolate=True, alpha=0.3, color='red')
    ax_bend.fill_between(x_bend, y_bend, 0, where=(y_bend < 0), interpolate=True, alpha=0.3, color='blue')

    ax_bend.axhline(y=0, color='black', linewidth=2)
    ax_bend.set_title('Bending Moment Diagram', fontsize=16)
    ax_bend.set_xlabel('Position along Beam (m)', fontsize=14)
    ax_bend.set_ylabel('Bending Moment (N.m)', fontsize=14)

    # Annotate Max and Min points
    ax_bend.annotate(f"Max: {max_bend:.2f} N.m", 
                     xy=(x_bend[idx_max_bend], max_bend), 
                     xytext=(10, 30), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->", color='red'),
                     fontsize=12, color='red')

    ax_bend.annotate(f"Min: {min_bend:.2f} N.m", 
                     xy=(x_bend[idx_min_bend], min_bend), 
                     xytext=(10, -40), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->", color='blue'),
                     fontsize=12, color='blue')

    ax_bend.legend()
    ax_bend.grid(True)

    # --- Show Bending Moment Plot Separately ---
    fig_bend.tight_layout()
    plt.close(fig_bend)
    fig_bend.show()
    plt.close(fig_bend)

def Matplot_Deflection(X_Field,Deflection):
    # --- Deflection Diagram Data ---
    x_shear = X_Field
    y_shear = Deflection

    # Find max/min values and their positions for annotations
    max_shear = round(np.max(y_shear), 3)
    min_shear = round(np.min(y_shear), 3)
    idx_max_shear = np.argmax(y_shear)
    idx_min_shear = np.argmin(y_shear)

    fig_shear, ax_shear = plt.subplots(figsize=(10, 6))

    ax_shear.plot(x_shear, y_shear, color='black', linewidth=2, label='Deflection Plot')
    ax_shear.fill_between(x_shear, y_shear, 0, where=(y_shear >= 0), interpolate=True, alpha=0.3, color='blue')
    ax_shear.fill_between(x_shear, y_shear, 0, where=(y_shear < 0), interpolate=True, alpha=0.3, color='red')

    ax_shear.axhline(y=0, color='black', linewidth=2)
    ax_shear.set_title('Deflection Diagram', fontsize=16)
    ax_shear.set_xlabel('Position along Beam (m)', fontsize=14)
    ax_shear.set_ylabel('Deflection (m)', fontsize=14)

    # Annotate Max and Min points
    ax_shear.annotate(f"Max: {max_shear:.2f} N", 
                      xy=(x_shear[idx_max_shear], max_shear), 
                      xytext=(10, 30), textcoords='offset points',
                      arrowprops=dict(arrowstyle="->", color='blue'),
                      fontsize=12, color='blue')

    ax_shear.annotate(f"Min: {min_shear:.2f} N", 
                      xy=(x_shear[idx_min_shear], min_shear), 
                      xytext=(10, -40), textcoords='offset points',
                      arrowprops=dict(arrowstyle="->", color='red'),
                      fontsize=12, color='red')

    ax_shear.legend()
    ax_shear.grid(True)

    # --- Show Deflection Plot Separately ---
    fig_shear.tight_layout()
    fig_shear.show()
    #plt.close(fig_shear)






def Matplot_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment):
    # --- Call Matplotlib Functions ---
    Matplot_shear_force(X_Field, Total_ShearForce)
    Matplot_bending_moment(X_Field, Total_BendingMoment)

def Plotly_sfd_bmd(X_Field, Total_ShearForce, Total_BendingMoment, beam_length):
    # --- Call Plotly Functions ---
    Plotly_shear_force(X_Field, Total_ShearForce, beam_length)
    Plotly_bending_moment(X_Field, Total_BendingMoment, beam_length)




def format_loads_for_plotting(loads_dict):
    """
    Transform the dynamic load inputs into a list of tuples 
    in the format required by your plotting routines.
    
    Parameters:
      loads_dict: Dictionary containing keys "pointloads", "distributedloads",
                  "momentloads", and "triangleloads".
                  
    Returns:
      A list of loads formatted as:
         ("point_load", pos, magnitude)
         ("udl", start, end, intensity)
         ("moment", pos, moment)
         ("trl", ...)  # if applicable
    """
    formatted_loads = []
    
    # Process point loads:
    for load in loads_dict.get("pointloads", []):
        pos, Fx, Fy = load
        # Choose which component to plot.
        # Here, we choose vertical if its magnitude is greater (or equal) than horizontal.
        if abs(Fy) >= abs(Fx):
            mag = Fy
        else:
            # Option: For a horizontal load, you might want to plot it differently.
            # For now, we simply take the horizontal force.
            mag = Fx
        formatted_loads.append(("point_load", pos, mag))
        
    # Process distributed loads (UDL):
    for udl in loads_dict.get("distributedloads", []):
        start, end, intensity = udl
        formatted_loads.append(("udl", start, end, intensity))
        
    # Process moment loads:
    for mom in loads_dict.get("momentloads", []):
        pos, moment = mom
        formatted_loads.append(("moment", pos, moment))
    
    # Optionally, process triangular loads if provided.
    # For now, if no triangular loads are used, we can leave this empty.
    for trl in loads_dict.get("triangleloads", []):
        # Assuming each triangular load is defined as [start, end, start_intensity, end_intensity]
        start, end, intensity_start, intensity_end = trl
        formatted_loads.append(("trl", start, end, intensity_start, intensity_end))
    
    return formatted_loads