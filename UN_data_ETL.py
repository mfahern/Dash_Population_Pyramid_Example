import pandas as pd
import numpy as np
import os
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

data_estimates_male = pd.read_excel("./data/WPP2022_POP_F02_2_POPULATION_5-YEAR_AGE_GROUPS_MALE.xlsx", header=16)
data_projections_male = pd.read_excel("./data/WPP2022_POP_F02_2_POPULATION_5-YEAR_AGE_GROUPS_MALE.xlsx", sheet_name="Medium variant", header=16)

data_estimates_female = pd.read_excel("./data/WPP2022_POP_F02_3_POPULATION_5-YEAR_AGE_GROUPS_FEMALE.xlsx", header=16)
data_projections_female = pd.read_excel("./data/WPP2022_POP_F02_3_POPULATION_5-YEAR_AGE_GROUPS_FEMALE.xlsx", sheet_name="Medium variant", header=16)

projections_estimates_male = pd.concat([data_estimates_male, data_projections_male])
projections_estimates_female = pd.concat([data_estimates_female, data_projections_female])

UN_countries_set = set(projections_estimates_male["Region, subregion, country or area *"])

drop_list = ["Notes", "Location code", "ISO3 Alpha-code", "ISO2 Alpha-code", "SDMX code**", "Type", "Parent code"]
projections_estimates_male = projections_estimates_male.drop(columns = drop_list)
projections_estimates_female = projections_estimates_female.drop(columns = drop_list)

def country_data_extraction(country):
    try:
        male_pop_estimates = projections_estimates_male.loc[projections_estimates_male["Region, subregion, country or area *"] == f'{country}']
        female_pop_estimates = projections_estimates_female.loc[projections_estimates_female["Region, subregion, country or area *"] == f'{country}']

        male_pop_estimates_T = male_pop_estimates.iloc[:,4:].T
        female_pop_estimates_T = female_pop_estimates.iloc[:,4:].T
        pop_estimates = pd.DataFrame(columns=["Time","Age","Sex","Value","Country"])
    
        male_values_list = []
        male_ages_list = []
        for i in male_pop_estimates_T.columns:
            male_temp_ages_list = [4,9,14,19,24,29,34,39,44,49,54,59,64,69,74,79,84,89,94,99,100]
            male_temp_values_list = male_pop_estimates_T[i].to_list()
            male_values_list = male_values_list + male_temp_values_list
            male_ages_list = male_ages_list + male_temp_ages_list

        male_values_np_array = np.array(male_values_list)
        male_values_list = list(-male_values_np_array)
    
        female_values_list = []
        female_ages_list = []
        for i in female_pop_estimates_T.columns:
            female_temp_ages_list = [4,9,14,19,24,29,34,39,44,49,54,59,64,69,74,79,84,89,94,99,100]
            female_temp_values_list = female_pop_estimates_T[i].to_list()
            female_values_list = female_values_list + female_temp_values_list
            female_ages_list = female_ages_list + female_temp_ages_list

        year_list = []
        country_list = []
        male_list = []
        female_list = []
        for i in range(1950,2101):
            for j in range(0,21):
                year_list.append(i)
                country_list.append(f'{country}')
                male_list.append('Male')
                female_list.append('Female')

        male_pop_estimates_columns = pd.DataFrame(columns=["Time","Age","Sex","Value","Country"])
        male_pop_estimates_columns["Time"] = year_list
        male_pop_estimates_columns["Country"] = country_list
        male_pop_estimates_columns["Value"] = male_values_list
        male_pop_estimates_columns["Age"] = male_ages_list
        male_pop_estimates_columns["Sex"] = male_list

        female_pop_estimates_columns = pd.DataFrame(columns=["Time","Age","Sex","Value","Country"])
        female_pop_estimates_columns["Time"] = year_list
        female_pop_estimates_columns["Country"] = country_list
        female_pop_estimates_columns["Value"] = female_values_list
        female_pop_estimates_columns["Age"] = female_ages_list
        female_pop_estimates_columns["Sex"] = female_list

        pop_estimates_columns_df = pd.concat([male_pop_estimates_columns, female_pop_estimates_columns])
  
        return pop_estimates_columns_df
    except:
        if country not in UN_countries_set:
           raise Exception(f'{country} is not the UN name of a specific jurisdiction.')

selected_countries = ['Afghanistan','Bangladesh','Brazil','China','India','Indonesia','Japan','Mexico','Nigeria','Pakistan','Republic of Korea','Russian Federation','United States of America' ]

selected_countries_ls = list()
selected_countries_df_ls = list()

for country in selected_countries:
    selected_countries_ls.append(f'{country}_pop_estimates_df')

for country, country_df in zip(selected_countries, selected_countries_ls):
    country_df = country_data_extraction(country)
    selected_countries_df_ls.append(country_df)

UN_countries_pop_estimates = pd.concat(selected_countries_df_ls)

dependent_pop_df = pysqldf("SELECT * FROM UN_countries_pop_estimates WHERE Age in (4,9,14);")
dependent_pop_df['positive_value'] = np.select([dependent_pop_df['Sex'] == 'Male', dependent_pop_df['Sex'] == 'Female'], [dependent_pop_df['Value']*-1, dependent_pop_df['Value']])

old_age_pop_df = pysqldf("SELECT * FROM UN_countries_pop_estimates WHERE Age in (69,74,79,84,89,94,99,100);")
old_age_pop_df['positive_value'] = np.select([old_age_pop_df['Sex'] == 'Male', old_age_pop_df['Sex'] == 'Female'], [old_age_pop_df['Value']*-1, old_age_pop_df['Value']])

dependent_pop_filtered_df = pysqldf("SELECT Time, SUM(positive_value) AS 'Dependent Population', Country FROM dependent_pop_df GROUP BY Country, Time;")
old_age_pop_filtered_df = pysqldf("SELECT Time, SUM(positive_value) AS 'Old Age Population', Country FROM old_age_pop_df GROUP BY Country, Time;")

working_age_growth_df = pd.DataFrame()
working_age_growth_df = UN_countries_pop_estimates.loc[UN_countries_pop_estimates['Sex'] == 'Male']

working_age_growth_df['Value'] = working_age_growth_df['Value'] * -1

working_age_growth_df = pd.concat([working_age_growth_df, UN_countries_pop_estimates.loc[UN_countries_pop_estimates['Sex'] == 'Female']])

working_age_df = pysqldf("SELECT * FROM working_age_growth_df WHERE Age in (19,24,29,34,39,44,49,54,59,64);")

working_age_total_df = pysqldf("Select Time, Country, SUM(Value) AS 'Working Age Population' FROM working_age_df GROUP BY Country, Time")


# Calculate dependency ratios
young_dependency_ratio = pd.DataFrame()
young_dependency_ratio['Time'] = dependent_pop_filtered_df['Time']
young_dependency_ratio['Country'] = dependent_pop_filtered_df['Country']
young_dependency_ratio['Young to Working Age Dependency Ratio'] = (dependent_pop_filtered_df['Dependent Population']/working_age_total_df['Working Age Population']) * 100

old_dependency_ratio = pd.DataFrame()
old_dependency_ratio['Time'] = dependent_pop_filtered_df['Time']
old_dependency_ratio['Country'] = dependent_pop_filtered_df['Country']
old_dependency_ratio['Old to Working Age Dependency Ratio'] = (old_age_pop_filtered_df['Old Age Population']/working_age_total_df['Working Age Population']) * 100

total_dependency_ratio = pd.DataFrame()
total_dependency_ratio['Time'] = dependent_pop_filtered_df['Time']
total_dependency_ratio['Country'] = dependent_pop_filtered_df['Country']
total_dependency_ratio['Young and Old to Working Age Dependency Ratio'] = ((old_age_pop_filtered_df['Old Age Population']+dependent_pop_filtered_df['Dependent Population'])/working_age_total_df['Working Age Population']) * 100

aggregated_working_age_growth_df = pysqldf("SELECT Time, Sex, SUM(Value) AS 'Working Age Population', Country FROM working_age_df GROUP BY Country, Time, Sex;")

male_aggregated_working_age_growth_df = aggregated_working_age_growth_df.loc[aggregated_working_age_growth_df['Sex'] == 'Male']
female_aggregated_working_age_growth_df = aggregated_working_age_growth_df.loc[aggregated_working_age_growth_df['Sex'] == 'Female']

filtered_male_aggregated_working_age_growth_df = male_aggregated_working_age_growth_df.loc[(male_aggregated_working_age_growth_df['Time'] <= 2050) & (male_aggregated_working_age_growth_df['Time'] % 10 == 0)]
filtered_female_aggregated_working_age_growth_df = female_aggregated_working_age_growth_df.loc[(female_aggregated_working_age_growth_df['Time'] <= 2050) & (female_aggregated_working_age_growth_df['Time'] % 10 == 0)]

filtered_all_aggregated_working_age_growth_df = pd.DataFrame()
filtered_all_aggregated_working_age_growth_df['Time'] = filtered_male_aggregated_working_age_growth_df['Time']
filtered_all_aggregated_working_age_growth_df['Country'] = filtered_male_aggregated_working_age_growth_df['Country']
filtered_all_aggregated_working_age_growth_df['Working Age Population'] = list(filtered_female_aggregated_working_age_growth_df.set_index('Time')['Working Age Population'] + filtered_male_aggregated_working_age_growth_df.set_index('Time')['Working Age Population'])

pivot_filtered_male_aggregated_working_age_growth_df = filtered_male_aggregated_working_age_growth_df.pivot(index='Time', columns=['Country'], values='Working Age Population')
pivot_filtered_female_aggregated_working_age_growth_df = filtered_female_aggregated_working_age_growth_df.pivot(index='Time', columns=['Country'], values='Working Age Population')
pivot_filtered_all_aggregated_working_age_growth_df = filtered_all_aggregated_working_age_growth_df.pivot(index='Time', columns=['Country'], values='Working Age Population')

all_pct_change_df = pivot_filtered_all_aggregated_working_age_growth_df.pct_change()

all_joined_df = pivot_filtered_all_aggregated_working_age_growth_df.join(all_pct_change_df, on=['Time'],  lsuffix=' Working Age Population', rsuffix=' Working Age Growth')

double_selected_countries = sorted(selected_countries*2)

population_growth_ls = ["Population", "Growth"]
match_size_population_growth_ls = population_growth_ls * len(selected_countries)

arrays = [
    np.array(double_selected_countries),
    np.array(match_size_population_growth_ls),
]

pop_growth_multi_df = pd.DataFrame(columns=arrays)

all_joined_df_columns_sorted = sorted(all_joined_df.columns)

for i in range(1, len(double_selected_countries), 2):
    col_name = all_joined_df_columns_sorted[i]
    country_name = double_selected_countries[i]
    pop_growth_multi_df[country_name, 'Population'] = all_joined_df[col_name]/1000
    pop_growth_multi_df[country_name, 'Population'] = pop_growth_multi_df[country_name, 'Population'].map("{:,.2f}M".format)

for i in range(0, len(match_size_population_growth_ls), 2):
    col_name = all_joined_df_columns_sorted[i]  
    country_name = double_selected_countries[i]
    pop_growth_multi_df[country_name, 'Growth'] = all_joined_df[col_name]
    pop_growth_multi_df = pop_growth_multi_df.fillna(0)
    pop_growth_multi_df[country_name, 'Growth'] = pop_growth_multi_df[country_name, 'Growth'].map("{:,.1%}".format)

population_1950_2050_df = pop_growth_multi_df.xs('Population', level=1, axis = 1)
growth_1950_2050_df = pop_growth_multi_df.xs('Growth', level=1, axis = 1)

young_dependency_ratio.to_csv('./data/young_dependency_ratio.csv')
old_dependency_ratio.to_csv('./data/old_dependency_ratio.csv')
total_dependency_ratio.to_csv('./data/total_dependency_ratio.csv')

UN_countries_pop_estimates.to_csv('./data/UN_countries_pop_estimates.csv')
pop_growth_multi_df.to_csv('./data/pop_growth_multi.csv')
population_1950_2050_df.to_csv('./data/population_1950_2050.csv')
growth_1950_2050_df.to_csv('./data/growth_1950_2050.csv')