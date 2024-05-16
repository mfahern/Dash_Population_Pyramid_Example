import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, ctx
import plotly.express as px
import plotly.graph_objects as go
import gunicorn
from whitenoise import WhiteNoise
import numpy as np
import json

app = Dash()
server = app.server

#server.wsgi_app = WhiteNoise(server.wsgi_app, root='data/')

UN_countries_pop_estimates_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/UN_countries_pop_estimates.csv')
pop_growth_multi_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/pop_growth_multi.csv', skiprows=[2])
population_1950_2050_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/population_1950_2050.csv')
growth_1950_2050_df = pd.read_csv('https://raw.githubusercontent.com/mfahern/Dash_Population_Pyramid_Example/main/data/growth_1950_2050.csv')
young_dependency_ratio_df = pd.read_csv('./data/young_dependency_ratio.csv')
old_dependency_ratio_df = pd.read_csv('./data/old_dependency_ratio.csv')
total_dependency_ratio_df = pd.read_csv('./data/total_dependency_ratio.csv')

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
        html.Div([
            html.Button('Play', id='play-button', n_clicks=0),
            html.Button('Stop', id='stop-button', n_clicks=0),
        ]),
        dcc.Loading(
            id='loading',
            type="circle",
            children=[
                # dcc.Graph(id='graph'),
                html.Div(id='message-output'),
                dcc.Graph(id='population_pyramid_go'),
                dcc.Graph(id='dependency_ratio_table'),
                ],
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


def generate_frames():
    countries = sorted(list(set(UN_countries_pop_estimates_df["Country"])))
    all_countries_years_frames = dict()
    country_selected_bar_ls = []

    for country in countries:     # countries
        country_selected = UN_countries_pop_estimates_df.loc[UN_countries_pop_estimates_df['Country'] == country]
        country_selected['Open_Age_Bracket'] = country_selected['Age']-4
        country_selected['Positive_Population'] = np.select([country_selected['Sex'] == 'Male', country_selected['Sex'] == 'Female'], [country_selected['Value']*-1, country_selected['Value']])/1000
        country_selected_male = country_selected.loc[country_selected['Sex'] == 'Male']
        country_selected_female = country_selected.loc[country_selected['Sex'] == 'Female']
        all_years_frames_dict = dict()
        frames_by_country_list = []
        sliders_country_dict = dict()

        for year, i in zip(range(1950,2101,1), range(151)): #list(set(country_selected_male['Time'])):
            year_dict = dict()
            year_str = str(year)
            sliders_dict = dict()

            young_dependency_ratio = young_dependency_ratio_df['Young to Working Age Dependency Ratio'].loc[young_dependency_ratio_df['Country'] == country]
            young_dependency_ratio_ls = list(young_dependency_ratio)
            old_dependency_ratio = old_dependency_ratio_df['Old to Working Age Dependency Ratio'].loc[old_dependency_ratio_df['Country'] == country]
            old_dependency_ratio_ls = list(old_dependency_ratio)
            total_dependency_ratio = total_dependency_ratio_df['Young and Old to Working Age Dependency Ratio'].loc[total_dependency_ratio_df['Country'] == country]
            total_dependency_ratio_ls = list(total_dependency_ratio)

            country_selected_male_year = country_selected_male.loc[country_selected_male['Time'] == year ]
            country_selected_female_year = country_selected_female.loc[country_selected_female['Time'] == year]

            # for a given year and country, one male and one female go.Bar is created 
            country_selected_male_year_fig = go.Bar(name='Male', x=list(country_selected_male_year['Value']), y=list(country_selected_male_year['Age']), orientation='h', width=4.9,  marker_color='#3260F2', customdata=country_selected_male_year[['Positive_Population','Open_Age_Bracket']],  hovertemplate='Population: %{customdata[0]:.3f}M<br>Male Age: %{customdata[1]}-%{y}<extra></extra>')
            country_selected_female_year_fig = go.Bar(name='Female', x=list(country_selected_female_year['Value']), y=list(country_selected_female_year['Age']), orientation='h', width=4.9, marker_color='#C00000', customdata=country_selected_female_year[['Positive_Population','Open_Age_Bracket']],  hovertemplate='Population: %{customdata[0]:.3f}M<br>Female Age: %{customdata[1]}-%{y}<extra></extra>')
            country_selected_table = go.Table(header=dict(values=['Dependency Ratio', 'Values']),cells=dict(values=[['Young to Working Age','Old to Working Age','Young plus Old to Working Age'],[young_dependency_ratio_ls[i],old_dependency_ratio_ls[i],total_dependency_ratio_ls[i]],]),)
            # create list of male and female go.bar
            country_sex_year_goBar_fig_ls = list()
            country_sex_year_goBar_fig_ls.append(country_selected_male_year_fig)
            country_sex_year_goBar_fig_ls.append(country_selected_female_year_fig)
            country_sex_year_goBar_fig_ls.append(country_selected_table)

            # create go.Frame
            frame = go.Frame(data=country_sex_year_goBar_fig_ls, name=year_str)
            frames_by_country_list.append(frame)

            # year_dict[year_str] = country_sex_year_goBar_fig_ls
            # all_years_frames_dict = all_years_frames_dict | year_dict

            slider_step = {"args": [
                    [year],
            {"frame": {"duration": 300, "redraw": False},
            "mode": "immediate",
            "transition": {"duration": 300}}
            ]       ,
            "label": year,
            "method": "animate"}
            sliders_dict["steps"] = slider_step
        
        sliders_country_dict[country] = sliders_dict
        frames_by_country_tuple = tuple(frames_by_country_list)
        all_countries_years_frames[country] = frames_by_country_tuple
    
    return all_countries_years_frames

all_countries_frames = generate_frames()

# with open('tuple_test.txt', 'w') as f:
#      print(all_countries_frames, file=f)

# with open('Afghanistan.txt', 'w') as f:
#     print(all_countries_frames['Afghanistan'], file=f)

# with open('China.txt', 'w') as f:
#     print(all_countries_frames['China'], file=f)

# with open('China_1955.txt', 'w') as f:
#     print(all_countries_frames['China']['1955'], file=f)

@app.callback(
    Output('dependency_ratio_table', 'figure'),
    Output('population_pyramid_go', 'figure'),
    Input('country_dropdown','value'),
)
def bar_fig(value, all_countries_frames=all_countries_frames):
    country_selected = UN_countries_pop_estimates_df.loc[UN_countries_pop_estimates_df['Country'] == f'{value}']
    country_selected_male = country_selected.loc[country_selected['Sex'] == 'Male']
    country_selected_female = country_selected.loc[country_selected['Sex'] == 'Female']

    country_selected_male_bar_ls = []
    country_selected_female_bar_ls = []
    country_selected_bar_ls = []
    years = []

    for year in list(set(country_selected_male['Time'])):
        year = str(year)
        years.append(year)

    country_selected_male_1950 = country_selected_male.loc[country_selected_male['Time'] == 1950 ]
    country_selected_male_1950['Open_Age_Bracket'] = country_selected_male_1950['Age']-4
    country_selected_male_1950['Positive_Population'] = (country_selected_male_1950['Value']*-1)/1000

    country_selected_female_1950 = country_selected_female.loc[country_selected_female['Time'] == 1950]
    country_selected_female_1950['Open_Age_Bracket'] = country_selected_female_1950['Age']-4
    country_selected_female_1950['Positive_Population'] = country_selected_female_1950['Value']/1000

    country_selected_male_1951 = country_selected_male.loc[country_selected_male['Time'] == 1951 ]
    country_selected_male_1951['Open_Age_Bracket'] = country_selected_male_1951['Age']-4
    country_selected_male_1951['Positive_Population'] = (country_selected_male_1951['Value']*-1)/1000

    country_selected_female_1951 = country_selected_female.loc[country_selected_female['Time'] == 1951]
    country_selected_female_1951['Open_Age_Bracket'] = country_selected_female_1951['Age']-4
    country_selected_female_1951['Positive_Population'] = country_selected_female_1951['Value']/1000

    country_selected_male_1952 = country_selected_male.loc[country_selected_male['Time'] == 1952 ]
    country_selected_male_1952['Open_Age_Bracket'] = country_selected_male_1952['Age']-4
    country_selected_male_1952['Positive_Population'] = (country_selected_male_1952['Value']*-1)/1000

    country_selected_female_1952 = country_selected_female.loc[country_selected_female['Time'] == 1952]
    country_selected_female_1952['Open_Age_Bracket'] = country_selected_female_1952['Age']-4
    country_selected_female_1952['Positive_Population'] = country_selected_female_1952['Value']/1000

    country_selected['Open_Age_Bracket'] = country_selected['Age']-4
    country_selected['Positive_Population'] = np.select([country_selected['Sex'] == 'Male', country_selected['Sex'] == 'Female'], [country_selected['Value']*-1, country_selected['Value']])/1000
    population_pyramid_fig = px.bar(country_selected, x="Value", y="Age", animation_frame="Time", orientation="h", color="Sex", color_discrete_map={'Male':'#3260F2', 'Female':'#C00000'}, height=500, custom_data=['Sex','Positive_Population','Time','Open_Age_Bracket'])
    population_pyramid_fig.update_traces(width=4.9, hovertemplate=('Sex=%{customdata[0]}<br>Population=%{customdata[1]:.3f}M<br>Age=%{customdata[3]}-%{y}<extra></extra>'))


    # with open('plotly_express_layout.txt', 'w') as f:
    #     print(population_pyramid_fig.layout, file=f)

    # with open('plotly_express_frames.txt', 'w') as f:
    #     print(population_pyramid_fig.frames, file=f)

    young_dependency_ratio = young_dependency_ratio_df['Young to Working Age Dependency Ratio'].loc[young_dependency_ratio_df['Country'] == value]
    young_dependency_ratio_ls = list(young_dependency_ratio)
    old_dependency_ratio = old_dependency_ratio_df['Old to Working Age Dependency Ratio'].loc[old_dependency_ratio_df['Country'] == value]
    old_dependency_ratio_ls = list(old_dependency_ratio)
    total_dependency_ratio = total_dependency_ratio_df['Young and Old to Working Age Dependency Ratio'].loc[total_dependency_ratio_df['Country'] == value]
    total_dependency_ratio_ls = list(total_dependency_ratio)


    dependency_ratio_frames = []
    for i in range(151):
        frame_to_add = go.Frame(data=[go.Table(header=dict(values=['Dependency Ratio', 'Values']),cells=dict(values=[['Young to Working Age','Old to Working Age','Young plus Old to Working Age'],[young_dependency_ratio_ls[i],old_dependency_ratio_ls[i],total_dependency_ratio_ls[i]],]),)],)
        dependency_ratio_frames.append(frame_to_add)

    dependency_ratio_frames_tp = tuple(dependency_ratio_frames)

    with open('dependency_ratio_table_loop_frames_tuple.txt', 'w') as f:
        print(dependency_ratio_frames_tp, file=f)


    population_pyramid_go = go.Figure(
        data=[
            go.Bar(name='Male', x=list(country_selected_male_1950['Value']), y=list(country_selected_male_1950['Age']), orientation='h', width=4.9,  marker_color='#3260F2', customdata=country_selected_male_1950[['Positive_Population','Open_Age_Bracket']],  hovertemplate='Population: %{customdata[0]:.3f}M<br>Male Age: %{customdata[1]}-%{y}<extra></extra>', xaxis='x1', yaxis='y1'),
            go.Bar(name='Female', x=list(country_selected_female_1950['Value']), y=list(country_selected_female_1950['Age']), orientation='h', width=4.9, marker_color='#C00000',customdata=country_selected_female_1950[['Positive_Population','Open_Age_Bracket']],  hovertemplate='Population: %{customdata[0]:.3f}M<br>Female Age: %{customdata[1]}-%{y}<extra></extra>', xaxis='x1', yaxis='y1'),
            go.Table(
                header=dict(values=['Dependency Ratio', 'Values']),
                cells=dict(values=[
                    ['Young to Working Age','Old to Working Age','Young plus Old to Working Age'], # column 1
                    [young_dependency_ratio_ls[0],old_dependency_ratio_ls[0],total_dependency_ratio_ls[0]], # column 2
                ], format=["", ".2f"]),
                domain=dict(x=[0, 1],
                            y=[.5, 1])
            )
        ],
        layout=go.Layout(
            updatemenus=[{'buttons': [{'args': [None, {'frame': {'duration': 500,
                                           'redraw': True}, 'mode': 'immediate',
                                           'fromcurrent': True, 'transition':
                                           {'duration': 500, 'easing': 'linear'}}],
                                  'label': '&#9654;',
                                  'method': 'animate'},
                                 {'args': [[None], {'frame': {'duration': 0,
                                           'redraw': True}, 'mode': 'immediate',
                                           'fromcurrent': True, 'transition':
                                           {'duration': 0, 'easing': 'linear'}}],
                                  'label': '&#9724;',
                                  'method': 'animate'}],
                     'direction': 'left',
                     'pad': {'r': 10, 't': 70},
                     'showactive': False,
                     'type': 'buttons',
                     'x': 0.1,
                     'xanchor': 'right',
                     'y': 0,
                     'yanchor': 'top'}],
            sliders=population_pyramid_fig.layout['sliders'],
            xaxis=dict(dict(domain=[0, 1], anchor='y1')),
            yaxis=dict( dict(domain=[0, 0.5], anchor='x1')),           
        ),
         frames=all_countries_frames[value]
   
    )

    population_pyramid_go.update_layout(barmode='relative')

    dependency_ratio_table = go.Figure(
        data=[go.Table(
            header=dict(values=['Dependency Ratio', 'Values']),
            cells=dict(values=[
                ['Young to Working Age','Old to Working Age','Young plus Old to Working Age'], # column 1
                [young_dependency_ratio_ls[0],old_dependency_ratio_ls[0],total_dependency_ratio_ls[0]], # column 2
            ],
            format=["", ".2f"]),   
        )],
        layout=go.Layout(
            updatemenus=[{'buttons': [{'args': [None, {'frame': {'duration': 500,
                                           'redraw': True}, 'mode': 'immediate',
                                           'fromcurrent': True, 'transition':
                                           {'duration': 500, 'easing': 'linear'}}],
                                  'label': '&#9654;',
                                  'method': 'animate',
                                  'visible': True
                                  },
                                 {'args': [[None], {'frame': {'duration': 0,
                                           'redraw': True}, 'mode': 'immediate',
                                           'fromcurrent': True, 'transition':
                                           {'duration': 0, 'easing': 'linear'}}],
                                  'label': '&#9724;',
                                  'method': 'animate',
                                  'visible': True
                                  }],
                     'direction': 'left',
                     'pad': {'r': 10, 't': 70},
                     'showactive': False,
                     'type': 'buttons',
                     'x': 0.1,
                     'xanchor': 'right',
                     'y': 0,
                     'yanchor': 'top'}],
        ),
        frames=dependency_ratio_frames_tp   #[
        #     go.Frame(
        #         data=[
        #             go.Table(
        #                 header=dict(values=['Dependency Ratio', 'Values']),
        #                 cells=dict(values=[
        #                     ['Young to Working Age','Old to Working Age','Young plus Old to Working Age'],
        #                     [young_dependency_ratio_ls[i],old_dependency_ratio_ls[i],total_dependency_ratio_ls[i]],
        #                 ]),
        #             )
        #         ],
        #     ) for i in range(151)
        # ]
    )

    # with open('dependency_ratio_table_frames.txt', 'w') as f:
    #     print(dependency_ratio_table.frames, file=f)

    return dependency_ratio_table, population_pyramid_go

@app.callback(
    Output('message-output', 'children'),
    # Output('dependency_ratio_table','figure'),
    # Output('population_pyramid_go','figure'),
    Input('play-button','n_clicks'),
    Input('stop-button','n_clicks'),
    Input('dependency_ratio_table','figure'),
    Input('population_pyramid_go','figure'),
)
def animate_charts(play_button,stop_button,dependency_ratio_table,population_pyramid_go):
    dependency_ratio_table = go.Figure(dependency_ratio_table)
    population_pyramid_go = go.Figure(population_pyramid_go)
    msg = ''
    if 'play-button' == ctx.triggered_id:
        msg = 'play'
        dependency_ratio_table.update_layout(title='Pressed Play')
        population_pyramid_go.update_layout(title='Pressed Play')
        # print(dependency_ratio_table.type)
        # print("test")
        # print(population_pyramid_go.type)
        # dependency_ratio_table.update_layout.buttons.method
        # population_pyramid_go.update_layout.buttons.method
    elif 'stop-button' == ctx.triggered_id:
        msg = 'stop'
        dependency_ratio_table.update_layout(title='Pressed Stop')
        population_pyramid_go.update_layout(title='Pressed Stop')
        # dependency_ratio_table.update_layout(updatemenus.active[1])
        # population_pyramid_go.update_layout(updatemenus.active[1])
    return html.Div(msg)#, dependency_ratio_table, population_pyramid_go

def main() -> None:
    app.run_server(debug=False, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    main()