from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotting_helper as ph

def plot_beam_schematic(beam_length, A, B, support_types, loads):
    fig = make_subplots(rows=1, cols=1)

    # Beam line
    fig.add_trace(ph.draw_beam(beam_length))

    # Loads
    for load in loads:
        if load[0] == "point_load":
            fig.add_trace(ph.draw_point_load(*load[1:]))
        elif load[0] == "udl":
            for trace in ph.draw_udl(*load[1:]):
                fig.add_trace(trace)
        elif load[0] == "moment":
            for trace in ph.draw_moment(*load[1:]):
                fig.add_trace(trace)
    # Supports
    fig.add_trace(ph.draw_big_support(A, support_types[0]))
    fig.add_trace(ph.draw_big_support(B, support_types[1]))

    fig.update_layout(
        width=1000,
        height=600,
        title=dict(text="Beam Schematic", x=0.4),
        xaxis=dict(title="Beam Length (m)", range=[-0.5, beam_length + 0.5]),
        yaxis=dict(title="", range=[-2, 2], showgrid=False, zeroline=False),
        hovermode="closest",
        plot_bgcolor="rgba(173,216,230,0.3)"  # Light blue background
    )
    fig.show()


def plot_reaction_diagram(A, B, reactions,support_types):
    Va, Ha, Vb = reactions
    fig = make_subplots(rows=1, cols=1)


    fig.add_trace(ph.draw_beam(B + 0.5))  # baseline
    fig.add_trace(ph.draw_reaction(A, Va))
    fig.add_trace(ph.draw_reaction(B, Vb))
    


    if abs(Ha) > 0:
        fig.add_trace(ph.draw_horizontal_reaction(A, Ha))

    # Supports
    fig.add_trace(ph.draw_support(A, support_types[0]))
    fig.add_trace(ph.draw_support(B, support_types[1]))

    fig.update_layout(
        width=1000,
        height=600,
        title=dict(text="Support Reaction Diagram", x=0.4),
        xaxis=dict(title="Beam Length (m)", range=[-0.5, B + 0.5]),
        yaxis=dict(title="", range=[-2, 2], showgrid=False, zeroline=False, showticklabels=False),  # Removed Y-axis numbers
        hovermode="closest",
        plot_bgcolor="rgba(173,216,230,0.3)"  # Light blue background
    )
    fig.show()

