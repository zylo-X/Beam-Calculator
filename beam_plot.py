# beam_plot.py

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import plotting_helper as ph

def plot_beam_schematic(X_Field, beam_length, A, B, support_types, loads, reactions):
    """
    Plots the full beam schematic after solving.

    Parameters:
    - X_Field: Beam positions
    - beam_length: Beam Length
    - A, B: Support positions
    - support_types: tuple ("pin", "roller")
    - loads: list [ ("point_load", pos, mag), ("udl", start, end, mag), ("moment", pos, mag) ]
    - reactions: [Va, Ha, Vb]
    """

    fig = make_subplots(
        rows=1,
        cols=1,
        vertical_spacing=0.1,
        subplot_titles=("Beam Schematic",),
    )

    # --- Beam Line ---
    fig = ph.draw_beam_line(fig, 0, beam_length)

    # --- Supports ---
    if support_types[0] == "pin":
        fig = ph.draw_support_pin(fig, A)
    elif support_types[0] == "roller":
        fig = ph.draw_support_roller(fig, A)

    if support_types[1] == "pin":
        fig = ph.draw_support_pin(fig, B)
    elif support_types[1] == "roller":
        fig = ph.draw_support_roller(fig, B)

    # --- Loads ---
    for load in loads:
        if load[0] == "point_load":
            fig = ph.draw_point_load(fig, load[2], load[1])
        elif load[0] == "udl":
            fig = ph.draw_distributed_load(fig, load[1], load[2], load[3])
        elif load[0] == "moment":
            fig = ph.draw_point_moment(fig, load[2], load[1])

    # --- Reactions ---
    Va, Ha, Vb = reactions
    ph.draw_reaction_arrow(fig, Va, A)
    ph.draw_reaction_arrow(fig, Vb, B)

    # --- Layout ---
    fig.update_layout(
        height=500,
        width=1000,
        title={"text": "Beam External Schematic", "x": 0.5},
        title_font_size=22,
        showlegend=False,
        hovermode="closest",
    )

    fig.update_xaxes(title_text="Beam Length (m)")
    fig.update_yaxes(title_text="")

    fig.show()
