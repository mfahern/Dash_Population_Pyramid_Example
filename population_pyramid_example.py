import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go

UN_10_largest_countries_pop_estimates_df = pd.read_csv('./data/UN_10_largest_countries_pop_estimates.csv')
population_1950_2050_df = pd.read_csv('./data/population_1950_2050.csv')
growth_1950_2050_df = pd.read_csv('./data/growth_1950_2050.csv')

app = Dash()

app.layout = html.Div(
    children=[
        dcc.Dropdown(['India','China','United States of America','Indonesia','Pakistan','Nigeria','Brazil','Bangladesh','Russia','Mexico'], 'India', id='country_dropdown'),
        html.H4("Population Pyramid"),
        dcc.Loading(
            id='loading',
            type="cube",
            children=dcc.Graph(id='graph')
        ),
        html.H4("Population Level"),
        dash_table.DataTable(
            data=population_1950_2050_df.to_dict('records')
        ),
        html.H4("Population Growth"),
        dash_table.DataTable(
            data=growth_1950_2050_df.to_dict('records')
        )
    ]
)

@app.callback(
    Output('graph', 'figure'),
    Input('country_dropdown', 'value'),
)

def create_country_bar(value):
    match value:
        case 'China':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'China']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'India':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'India']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'United States of America':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'United States of America']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'Indonesia':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Indonesia']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'Pakistan':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Pakistan']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'Nigeria':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Nigeria']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'Brazil':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Brazil']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'Bangladesh':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Bangladesh']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'Russia':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Russian Federation']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
        case 'Mexico':
            country_selected = UN_10_largest_countries_pop_estimates_df.loc[UN_10_largest_countries_pop_estimates_df['Country'] == 'Mexico']
            population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", height=1000,)
    return population_pyramid_fig

def main() -> None:
    app.run()

if __name__ == "__main__":
    main()
