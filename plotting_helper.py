import plotly.graph_objs as go
import numpy as np

def draw_beam(length):
    return go.Scatter(
        x=[0, length],
        y=[0, 0],
        mode="lines",
        line=dict(color="purple", width=5),
        showlegend=False
    )

def draw_support(x, support_type):
    if support_type == "pin":
        return go.Scatter(
            x=[x],
            y=[0],
            mode="markers",
            marker=dict(symbol="circle", color="blue", size=15),
            name="Pin Support",  # Legend entry for pin support
            showlegend=True
        )
    elif support_type == "roller":
        return go.Scatter(
            x=[x],
            y=[0],
            mode="markers",
            marker=dict(symbol="circle", color="red", size=15),
            name="Roller Support",  # Legend entry for roller support
            showlegend=True
        )

def draw_big_support(x, support_type):
    if support_type == "pin":
        return go.Scatter(
            x=[x],
            y=[0],
            mode="markers",
            marker=dict(symbol="circle", color="blue", size=25),
            name="Pin Support",  # Legend entry for pin support
            showlegend=True
        )
    elif support_type == "roller":
        return go.Scatter(
            x=[x],
            y=[0],
            mode="markers",
            marker=dict(symbol="circle", color="red", size=25),
            name="Roller Support",  # Legend entry for roller support
            showlegend=True
        )



def draw_point_load(x, magnitude):
    return go.Scatter(
        x=[x, x],
        y=[0, 0.8 * (1 if magnitude > 0 else -1)],
        mode="lines+text+markers",
        marker= dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
        line=dict(color="red", width=4),
        text=[None, f"<b>{abs(magnitude):.3f} N</b>"],
        textposition="top center" if magnitude > 0 else "bottom center",
        showlegend=False,  
        # Legend entry for point load
        name="Point Load"
    )

def draw_udl(x_start, x_end, magnitude):
    traces = []

    y_val = 0.5 * (1 if magnitude > 0 else -1)
    fill_y = 0.5 * (1 if magnitude > 0 else -1)

    traces.append(go.Scatter(
        x=[x_start, x_start],
        y=[0, y_val],
        mode="lines",
        line=dict(color="purple", width=4),
        showlegend=False
    ))
    traces.append(go.Scatter(
        x=[x_end, x_end],
        y=[0, y_val],
        mode="lines",
        line=dict(color="purple", width=4),
        showlegend=False
    ))

    traces.append(go.Scatter(
        x=[x_start, x_end, x_end, x_start, x_start],
        y=[0, 0, fill_y, fill_y, 0],
        fill="toself",
        fillcolor="rgba(128,0,128,0.3)",  # Purple with transparency
        line=dict(color="rgba(0,0,0,0)"),
        showlegend=False
    ))

    mid_x = (x_start + x_end) / 2
    traces.append(go.Scatter(
        x=[mid_x],
        y=[0.8 * (1 if magnitude > 0 else -1)],
        mode="text",
        text=[f"<b>{abs(magnitude):.3f} N/m</b>"],
        textposition="top center",
        showlegend=False
    ))

    return traces

import numpy as np
import plotly.graph_objs as go

def draw_moment(x, magnitude):
    arc_radius = 0.3
    
    # Choose the arc (and tip) depending on the moment's sign.
    if magnitude > 0:
        theta = np.linspace(-np.pi/2, np.pi/2, 30)
        arrow_tip_angle = np.pi/2  # tip at the top of the arc
    else:
        theta = np.linspace(np.pi/2, 3*np.pi/2, 30)
        arrow_tip_angle = 3*np.pi/2  # tip at the bottom of the arc

    # Compute arc coordinates.
    arc_x = x + arc_radius * np.cos(theta)
    arc_y = 0 + arc_radius * np.sin(theta)
    
    # Determine the tip coordinates.
    tip_x = x + arc_radius * np.cos(arrow_tip_angle)
    tip_y = 0 + arc_radius * np.sin(arrow_tip_angle)
    
    # Compute the unit tangent at the tip.
    # For the circle, the derivative gives: (-sin(theta), cos(theta)).
    T = np.array([-np.sin(arrow_tip_angle), np.cos(arrow_tip_angle)])
    # For the arrow head, we use the backward (opposite) direction.
    backward = -T  # unit vector pointing backward from the tip.
    
    # Build a local coordinate system at the tip:
    # Let the local x-axis be backward, and the local y-axis be a 90° CCW rotation of it.
    local_x = -backward
    local_y = np.array([-backward[1], backward[0]])
    
    # Now, define the arrow head in local coordinates.
    # Unlike the V-shape (where points would be symmetric about (0,0)),
    # we want a "<" shape where both points lie to the left of the tip.
    # In local coordinates, set the tip at (0,0),
    # and choose points at (-d, +h) and (-d, -h), with d>0.
    d = 0.08 # how far backward from the tip (controls arrow head length)
    h = 0.05  # half the arrow head's width 
    upper_local = np.array([-d, h])
    lower_local = np.array([-d, -h])
    
    # Transform these local points back to global coordinates:
    tip_global = np.array([tip_x, tip_y])
    upper_global = tip_global + upper_local[0]*local_x + upper_local[1]*local_y
    lower_global = tip_global + lower_local[0]*local_x + lower_local[1]*local_y

    # Build an arrow head trace that draws a continuous line from upper point → tip → lower point.
    arrow_head_trace = go.Scatter(
        x=[upper_global[0], tip_x, lower_global[0]],
        y=[upper_global[1], tip_y, lower_global[1]],
        mode="lines",
        line=dict(color="magenta", width=4),
        showlegend=False
    )
    
    # Text annotation trace (placing the moment value slightly above the arc).
    text_trace = go.Scatter(
        x=[x],
        y=[arc_radius + 0.2],
        mode="text",
        text=[f"<b>{abs(magnitude):.3f} Nm</b>"],
        textposition="top center",
        showlegend=False
    )
    
    # Arc trace remains unchanged.
    arc_trace = go.Scatter(
        x=arc_x,
        y=arc_y,
        mode="lines",
        line=dict(color="magenta", width=4),
        showlegend=False
    )
    
    return [arc_trace, arrow_head_trace, text_trace]




def draw_reaction(x, magnitude):
    arrow_tip = 1.2 * (1 if magnitude > 0 else -1)
    return go.Scatter(
        x=[x, x],
        y=[0, arrow_tip],
        mode="lines+text+markers",
        line=dict(color="red", width=4),
        marker=dict(symbol="triangle-up" if magnitude > 0 else "triangle-down", color="red", size=10),
        text=[None, f"<b>{abs(magnitude):.2f} N</b>"],
        textposition="top center" if magnitude > 0 else "bottom center",
        showlegend=False,
        name="Vertical_R", # Legend entry for vertical reaction
    )

def draw_horizontal_reaction(x, magnitude):
    arrow_tip = x + 1.2 * (1 if magnitude > 0 else -1)
    return go.Scatter(
        x=[x, arrow_tip],
        y=[0, 0],
        mode="lines+text+markers",
        line=dict(color="orange", width=4),
        marker=dict(symbol="triangle-right" if magnitude > 0 else "triangle-left", color="orange", size=10),
        text=[None, f"<b>{abs(magnitude):.2f} N</b>"],
        textposition="top right" if magnitude > 0 else "top left",  # Adjusted to avoid overlap
        showlegend=False,
        name="Horizontal_R", # Legend entry for horizontal reaction
    )


