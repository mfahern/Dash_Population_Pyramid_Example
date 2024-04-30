import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

UN_10_largest_countries_pop_estimates_df = pd.read_csv('./data/UN_10_largest_countries_pop_estimates.csv')

app = Dash()

app.layout = html.Div(
    children=[
        html.H4("Population Pyramid"),
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
    India_men_women = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'India']
    China_men_women = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'China']
    Brazil_men_women = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Brazil']
    return px.bar(
        India_men_women,
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
