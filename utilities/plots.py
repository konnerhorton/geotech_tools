import plotly.express as px
import plotly.graph_objects as go
import math


def plot_empty_mohr_circle():
    # test_results = df[df["Sample ID"] == sample_id][
    #     ["Test Number", "sigma_3", "sigma_1"]
    # ].to_dict("records")

    fig = go.Figure()

    x_max = 2000
    y_max = x_max / 2.5

    fig.update_xaxes(range=[0, x_max], constrain="domain")
    fig.update_yaxes(
        range=[0, y_max], scaleanchor="x", scaleratio=1, constrain="domain"
    )

    return fig


def plot_mohr_circles(df, sample):
    test_results = df[df["Sample ID"] == sample].to_dict("records")

    fig = plot_empty_mohr_circle()
    fig.add_trace(go.Scatter())

    for i in test_results:
        x0 = i["Minor Principal Stress"]
        x1 = i["Major Principal Stress"]
        y0 = (x0 - x1) / 2
        y1 = -y0
        fig.add_shape(type="circle", xref="x", yref="y", x0=x0, y0=y0, x1=x1, y1=y1)

    x_max = max(i["Major Principal Stress"] for i in test_results) * 1.1
    y_max = x_max / 2.5

    fig.update_xaxes(range=[0, x_max], constrain="domain")
    fig.update_yaxes(
        range=[0, y_max], scaleanchor="x", scaleratio=1, constrain="domain"
    )
    return fig


def add_cohesion_and_friction_angle_to_mohr_circle(fig, cohesion, friction_angle):
    x_max = fig.layout.xaxis.range[1]
    line_coords = (
        (0, x_max),
        (cohesion, x_max * math.tan(math.radians(friction_angle)) - cohesion),
    )

    fig.add_trace(go.Scatter(x=line_coords[0], y=line_coords[1], mode="lines"))

    return fig
