import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import gunicorn
from whitenoise import WhiteNoise

UN_10_largest_countries_pop_estimates_df = pd.read_csv('UN_10_largest_countries_pop_estimates.csv')
pop_growth_multi_df = pd.read_csv('pop_growth_multi.csv', skiprows=[2])
population_1950_2050_df = pd.read_csv('population_1950_2050.csv')
growth_1950_2050_df = pd.read_csv('growth_1950_2050.csv')

pop_growth_multi_df.rename(columns={'Unnamed: 0':'Year', 'Bangladesh':'Bangladesh', 'Bangladesh.1':'Bangladesh', 'Brazil':'Brazil', 'Brazil.1':'Brazil',
       'China':'China', 'China.1':'China', 'India':'India', 'India.1':'India', 'Indonesia':'Indonesia', 'Indonesia.1':'Indonesia',
       'Mexico':'Mexico', 'Mexico.1':'Mexico', 'Nigeria':'Nigeria', 'Nigeria.1':'Nigeria', 'Pakistan':'Pakistan', 'Pakistan.1':'Pakistan',
       'Russia':'Russia', 'Russia.1':'Russia', 'United States':'United States', 'United States.1':'United States'}, inplace=True)


app = Dash()
server = app.server

server.wsgi_app = WhiteNoise(server.wsgi_app, root='data/')

app.layout = html.Div(
    style={
        'margin-top':'10px',
        'margin-botton':'10px',
        'margin-right':'10px',
        'margin-left':'10px',
    },
    children=[
        dcc.Dropdown(['India','China','United States of America','Indonesia','Pakistan','Nigeria','Brazil','Bangladesh','Russia','Mexico'], 'India', id='country_dropdown'),
        html.H4("Population Pyramid"),
        dcc.Loading(
            id='loading',
            type="cube",
            children=dcc.Graph(id='graph')
        ),
        html.H4("Working Age Population Level and Growth", style={'textAlign':'center'}),
        dash_table.DataTable(
            columns=[
            {"name": ["", ""], "id":"year"},
            {"name": ["Bangladesh", "Population"], "id":"Bangladesh_Pop"},
            {"name": ["Bangladesh", "Growth"], "id":"Bangladesh_Growth"},
            {"name": ["Brazil", "Population"], "id":"Brazil_Pop"},
            {"name": ["Brazil", "Growth"], "id":"Brazil_Growth"},
            {"name": ["China", "Population"], "id":"China_Pop"},
            {"name": ["China", "Growth"], "id":"China_Growth"},
            {"name": ["India", "Population"], "id":"India_Pop"},
            {"name": ["India", "Growth"], "id":"India_Growth"},
            {"name": ["Indonesia", "Population"], "id":"Indonesia_Pop"},
            {"name": ["Indonesia", "Growth"], "id":"Indonesia_Growth"},
            {"name": ["Mexico", "Population"], "id":"Mexico_Pop"},
            {"name": ["Mexico", "Growth"], "id":"Mexico_Growth"},
            {"name": ["Nigeria", "Population"], "id":"Nigeria_Pop"},
            {"name": ["Nigeria", "Growth"], "id":"Nigeria_Growth"},
            {"name": ["Pakistan", "Population"], "id":"Pakistan_Pop"},
            {"name": ["Pakistan", "Growth"], "id":"Pakistan_Growth"},
            {"name": ["Russia", "Population"], "id":"Russia_Pop"},
            {"name": ["Russia", "Growth"], "id":"Russia_Growth"},
            {"name": ["United States", "Population"], "id":"United_States_Pop"},
            {"name": ["United States", "Growth"], "id":"United_States_Growth"},
           ],
            data=[
            {
                "year":  growth_1950_2050_df["Time"].iloc[i],
                "Bangladesh_Pop": population_1950_2050_df["Bangladesh"].iloc[i],   
                "Bangladesh_Growth": growth_1950_2050_df["Bangladesh"].iloc[i],
                "Brazil_Pop": population_1950_2050_df["Brazil"].iloc[i],   
                "Brazil_Growth": growth_1950_2050_df["Brazil"].iloc[i],
                "China_Pop": population_1950_2050_df["China"].iloc[i],   
                "China_Growth": growth_1950_2050_df["China"].iloc[i],
                "India_Pop": population_1950_2050_df["India"].iloc[i],   
                "India_Growth": growth_1950_2050_df["India"].iloc[i],
                "Indonesia_Pop": population_1950_2050_df["Indonesia"].iloc[i],   
                "Indonesia_Growth": growth_1950_2050_df["Indonesia"].iloc[i],
                "Mexico_Pop": population_1950_2050_df["Mexico"].iloc[i],   
                "Mexico_Growth": growth_1950_2050_df["Mexico"].iloc[i],
                "Nigeria_Pop": population_1950_2050_df["Nigeria"].iloc[i],   
                "Nigeria_Growth": growth_1950_2050_df["Nigeria"].iloc[i],
                "Pakistan_Pop": population_1950_2050_df["Pakistan"].iloc[i],   
                "Pakistan_Growth": growth_1950_2050_df["Pakistan"].iloc[i],
                "Russia_Pop": population_1950_2050_df["Russia"].iloc[i],   
                "Russia_Growth": growth_1950_2050_df["Russia"].iloc[i],
                "United_States_Pop": population_1950_2050_df["United States"].iloc[i],   
                "United_States_Growth": growth_1950_2050_df["United States"].iloc[i],
            }
            for i in range(11)
            ],
#            style_data={'border':'1px solid black'},
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            },
            {
                'if':{'column_id':['year','Bangladesh_Pop','China_Pop','Indonesia_Pop', 'Nigeria_Pop', 'Russia_Pop']},
                'border-left':'1px solid black',
            },
            {
                'if':{'column_id':['Bangladesh_Growth','China_Growth','Indonesia_Growth', 'Nigeria_Growth', 'Russia_Growth', 'United_States_Growth']},
                'border-right':'1px solid black',
            },
            ],
            style_header={
                'textAlign':'center',
                'color': 'black',
                'fontWeight': 'bold',
                'border':'1px solid black',
            },

           merge_duplicate_headers=True,
       ),
       
#        dash_table.DataTable(
#            data=population_1950_2050_df.to_dict('records')
#        ),
#        html.H4("Working Age Population Growth"),
#        dash_table.DataTable(  
#          data=growth_1950_2050_df.to_dict('records')
#        )
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
    app.run_server(debug=False, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    main()
