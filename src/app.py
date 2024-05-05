import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import gunicorn
from whitenoise import WhiteNoise

app = Dash()
server = app.server

#server.wsgi_app = WhiteNoise(server.wsgi_app, root='data/')

UN_countries_pop_estimates_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/UN_countries_pop_estimates.csv')
pop_growth_multi_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/pop_growth_multi.csv', skiprows=[2])
population_1950_2050_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/population_1950_2050.csv')
growth_1950_2050_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/growth_1950_2050.csv')

pop_growth_multi_df.rename(columns={'Unnamed: 0':'Year','Afghanistan':'Afghanistan', 'Afghanistan.1':'Afghanistan','Bangladesh':'Bangladesh', 'Bangladesh.1':'Bangladesh', 'Brazil':'Brazil', 'Brazil.1':'Brazil',
       'China':'China', 'China.1':'China', 'India':'India', 'India.1':'India', 'Indonesia':'Indonesia', 'Indonesia.1':'Indonesia','Japan':'Japan','Japan.1':'Japan',
       'Mexico':'Mexico', 'Mexico.1':'Mexico', 'Nigeria':'Nigeria', 'Nigeria.1':'Nigeria', 'Pakistan':'Pakistan', 'Pakistan.1':'Pakistan','Republic of Korea':'Republic of Korea','Republic of Korea.1':'Republic of Korea',
       'Russian Federation':'Russian Federation', 'Russian Federation.1':'Russian Federation', 'United States of America':'United States of America', 'United States of America.1':'United States of America'}, inplace=True)

app.layout = html.Div(
    style={
        'margin-top':'10px',
        'margin-botton':'10px',
        'margin-right':'10px',
        'margin-left':'10px',
    },
    children=[
        dcc.Dropdown(['Afghanistan','Bangladesh','Brazil','China','India','Indonesia','Japan','Mexico','Nigeria','Pakistan','Republic of Korea','Russian Federation','United States of America'], 'Afghanistan', id='country_dropdown'),
        html.H3("Population Pyramid"),
        html.P("UN Population Projections 2023 Midyear Medium Varient Estimates (1950-2100)"), 
        dcc.Loading(
            id='loading',
            type="cube",
            children=dcc.Graph(id='graph')
        ),
        html.H3("Working Age Population Level and Growth"),
        dash_table.DataTable(
            columns=[
            {"name": ["", ""], "id":"year"},
            {"name": ["Afghanistan", "Population"], "id":"Afghanistan_Pop"},
            {"name": ["Afghanistan", "Growth"], "id":"Afghanistan_Growth"},
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
            {"name": ["Japan", "Population"], "id":"Japan_Pop"},
            {"name": ["Japan", "Growth"], "id":"Japan_Growth"},
            {"name": ["Mexico", "Population"], "id":"Mexico_Pop"},
            {"name": ["Mexico", "Growth"], "id":"Mexico_Growth"},
            {"name": ["Nigeria", "Population"], "id":"Nigeria_Pop"},
            {"name": ["Nigeria", "Growth"], "id":"Nigeria_Growth"},
            {"name": ["Pakistan", "Population"], "id":"Pakistan_Pop"},
            {"name": ["Pakistan", "Growth"], "id":"Pakistan_Growth"},
            {"name": ["South Korea", "Population"], "id":"South_Korea_Pop"},
            {"name": ["South Korea", "Growth"], "id":"South_Korea_Growth"},
            {"name": ["Russia", "Population"], "id":"Russia_Pop"},
            {"name": ["Russia", "Growth"], "id":"Russia_Growth"},
            {"name": ["United States", "Population"], "id":"United_States_Pop"},
            {"name": ["United States", "Growth"], "id":"United_States_Growth"},
           ],
            data=[
            {
                "year":  growth_1950_2050_df["Time"].iloc[i],
                "Afghanistan_Pop": population_1950_2050_df["Afghanistan"].iloc[i],   
                "Afghanistan_Growth": growth_1950_2050_df["Afghanistan"].iloc[i],
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
                "Japan_Pop": population_1950_2050_df["Japan"].iloc[i],   
                "Japan_Growth": growth_1950_2050_df["Japan"].iloc[i],
                "Mexico_Pop": population_1950_2050_df["Mexico"].iloc[i],   
                "Mexico_Growth": growth_1950_2050_df["Mexico"].iloc[i],
                "Nigeria_Pop": population_1950_2050_df["Nigeria"].iloc[i],   
                "Nigeria_Growth": growth_1950_2050_df["Nigeria"].iloc[i],
                "Pakistan_Pop": population_1950_2050_df["Pakistan"].iloc[i],   
                "Pakistan_Growth": growth_1950_2050_df["Pakistan"].iloc[i],
                "South_Korea_Pop": population_1950_2050_df["Republic of Korea"].iloc[i],   
                "South_Korea_Growth": growth_1950_2050_df["Republic of Korea"].iloc[i],
                "Russia_Pop": population_1950_2050_df["Russian Federation"].iloc[i],   
                "Russia_Growth": growth_1950_2050_df["Russian Federation"].iloc[i],
                "United_States_Pop": population_1950_2050_df["United States of America"].iloc[i],   
                "United_States_Growth": growth_1950_2050_df["United States of America"].iloc[i],
            }
            for i in range(11)
            ],
#            style_data={'border':'1px solid black'},
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            },
            {
                'if':{'column_id':['year','Afghanistan_Pop','Bangladesh_Pop','China_Pop','Indonesia_Pop', 'Mexico_Pop', 'Pakistan_Pop', 'Russia_Pop']},
                'border-left':'1px solid black',
            },
            {
                'if':{'column_id':['Bangladesh_Growth','China_Growth','Indonesia_Growth', 'Mexico_Growth', 'Pakistan_Growth','Russia_Growth', 'United_States_Growth']},
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
def bar_fig(value):
    country_selected = UN_countries_pop_estimates_df.loc[UN_countries_pop_estimates_df['Country'] == f'{value}']
    population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", color_discrete_map={'Male':'#3260F2', 'Female':'#C00000'}, height=1000,)
    population_pyramid_fig.update_traces(width=4.9)
#TODO fix hovertemplate to show ages are 5 year brackets
#    population_pyramid_fig.update_traces(hovertemplate=f"Sex: {UN_countries_pop_estimates_df['Sex'][0]}"+f"Time: {UN_countries_pop_estimates_df['Time']}"+f"Count: {UN_countries_pop_estimates_df['Value']}"+f"Age: {UN_countries_pop_estimates_df['Age']-5}-{UN_countries_pop_estimates_df['Age']}")
    return population_pyramid_fig

def main() -> None:
    app.run_server(debug=False, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    main()
