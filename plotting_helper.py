# plotting_helper.py

import plotly.graph_objs as go
import numpy as np

def draw_beam_line(fig, x_start, x_end, y=0):
    fig.add_trace(go.Scatter(
        x=[x_start, x_end],
        y=[y, y],
        mode="lines",
        line=dict(color="black", width=6),
        hoverinfo="skip",
        showlegend=False
    ))
    return fig

def draw_support_pin(fig, x_pos, y_pos=0):
    # Triangle pointing UP 🔺 below the beam
    triangle_x = [x_pos-0.15, x_pos+0.15, x_pos]
    triangle_y = [y_pos, y_pos, y_pos-0.4]
    fig.add_trace(go.Scatter(
        x=triangle_x,
        y=triangle_y,
        fill="toself",
        mode="lines",
        line=dict(color="black"),
        hoverinfo="skip",
        showlegend=False
    ))
    return fig

def draw_support_roller(fig, x_pos, y_pos=0):
    # Three small circles ⚫⚫⚫ below the beam for roller
    fig.add_trace(go.Scatter(
        x=[x_pos-0.1, x_pos, x_pos+0.1],
        y=[y_pos-0.4, y_pos-0.4, y_pos-0.4],
        mode="markers",
        marker=dict(color="black", size=8, symbol="circle"),
        hoverinfo="skip",
        showlegend=False
    ))
    fig = draw_support_pin(fig, x_pos, y_pos)  # Add pin support shape too
    return fig

def draw_point_load(fig, magnitude, x_pos, y_pos=0):
    # Shorten arrows for Point Load
    arrow_length = 0.6 * (1 if magnitude > 0 else -1)
    fig.add_trace(go.Scatter(
        x=[x_pos, x_pos],
        y=[y_pos, y_pos + arrow_length],
        mode="lines+markers+text",
        line=dict(color="blue", width=3),
        marker=dict(symbol="arrow-bar-up" if magnitude > 0 else "arrow-bar-down", color="blue", size=10),
        text=[None, f"{abs(magnitude):.1f} kN"],
        textposition="top center" if magnitude > 0 else "bottom center",
        textfont=dict(color="blue"),
        hoverinfo="skip",
        showlegend=False
    ))
    return fig

def draw_reaction_arrow(fig, magnitude, x_pos, y_pos=0):
    # Shorten arrows for Reactions
    arrow_length = 0.6 * (1 if magnitude > 0 else -1)
    fig.add_trace(go.Scatter(
        x=[x_pos, x_pos],
        y=[y_pos, y_pos + arrow_length],
        mode="lines+markers+text",
        line=dict(color="red", width=3),
        marker=dict(symbol="arrow-bar-up" if magnitude > 0 else "arrow-bar-down", color="red", size=10),
        text=[None, f"{abs(magnitude):.1f} kN"],
        textposition="top center" if magnitude > 0 else "bottom center",
        textfont=dict(color="red"),
        hoverinfo="skip",
        showlegend=False
    ))
    return fig

def draw_point_moment(fig, magnitude, x_pos, y_pos=0):
    # Center Moment symbol 🔄️ at correct position
    arc_radius = 0.7
    if magnitude > 0:
        theta = np.linspace(-np.pi/2, np.pi/2, 30)
    else:
        theta = np.linspace(np.pi/2, 3*np.pi/2, 30)

    arc_x = x_pos + arc_radius * np.cos(theta)
    arc_y = y_pos + arc_radius * np.sin(theta)

    fig.add_trace(go.Scatter(
        x=arc_x,
        y=arc_y,
        mode="lines+text",
        line=dict(color="purple", width=3),
        text=[None] * 15 + [f"{abs(magnitude):.1f} kNm"] + [None] * 14,
        textposition="top center",
        textfont=dict(color="purple"),
        hoverinfo="skip",
        showlegend=False
    ))
    return fig

def draw_distributed_load(fig, x_start, x_end, magnitude, y_pos=0):
    # Arrows at start and end
    fig.add_trace(go.Scatter(
        x=[x_start, x_start],
        y=[y_pos, y_pos + 0.8 * (1 if magnitude > 0 else -1)],
        mode="lines+markers",
        line=dict(color="green", width=2),
        marker=dict(symbol="arrow-bar-up" if magnitude > 0 else "arrow-bar-down", color="green", size=8),
        hoverinfo="skip",
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[x_end, x_end],
        y=[y_pos, y_pos + 0.8 * (1 if magnitude > 0 else -1)],
        mode="lines+markers",
        line=dict(color="green", width=2),
        marker=dict(symbol="arrow-bar-up" if magnitude > 0 else "arrow-bar-down", color="green", size=8),
        hoverinfo="skip",
        showlegend=False
    ))
    # Transparent fill between
    fill_x = [x_start, x_end, x_end, x_start, x_start]
    fill_y = [y_pos, y_pos, y_pos + 0.4*(1 if magnitude > 0 else -1), y_pos + 0.4*(1 if magnitude > 0 else -1), y_pos]
    fig.add_trace(go.Scatter(
        x=fill_x,
        y=fill_y,
        fill="toself",
        fillcolor="rgba(0,255,0,0.2)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=False
    ))
    # UDL Magnitude Annotation
    mid_x = (x_start + x_end) / 2
    mid_y = y_pos + 0.6 * (1 if magnitude > 0 else -1)
    fig.add_trace(go.Scatter(
        x=[mid_x],
        y=[mid_y],
        mode="text",
        text=[f"{abs(magnitude):.1f} kN/m"],
        textfont=dict(color="green"),
        hoverinfo="skip",
        showlegend=False
    ))
    return fig
