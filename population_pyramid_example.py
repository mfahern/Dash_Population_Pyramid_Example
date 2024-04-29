import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = Dash()

app.layout = html.Div(
    children=[
        html.H4("Population Pyramid China"),
        dcc.Loading(
            id="loading",
            type="cube",
            children=dcc.Graph(id="graph")
        )
    ]
)

@app.callback(
    Output("graph", "figure"),
    Input("loading", "loading_states")
)

def display_animated_graph(loading_states):
    China_men_women = pd.read_csv("E:/Python/Dash_Apps/population_pyramid_example/data/China_pop_estimates_columns.csv")
    return px.bar(
        China_men_women,
        x="Value",
        y="Age",
        animation_frame="Time",
        orientation="h",
        color="Sex",
        height=1000,
    )

def main() -> None:
    app.run()

if __name__ == "__main__":
    main()
