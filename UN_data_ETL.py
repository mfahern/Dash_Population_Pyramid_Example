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
           raise Exception('Country is not the UN name of a specific jurisdiction.')

India_pop_estimates_df = country_data_extraction('India')
China_pop_estimates_df = country_data_extraction('China')
United_States_pop_estimates_df = country_data_extraction('United States of America')
Indonesia_pop_estimates_df = country_data_extraction('Indonesia')
Pakistan_pop_estimates_df = country_data_extraction('Pakistan')
Nigeria_pop_estimates_df = country_data_extraction('Nigeria')
Brazil_pop_estimates_df = country_data_extraction('Brazil')
Bangladesh_pop_estimates_df = country_data_extraction('Bangladesh')
Russia_pop_estimates_df = country_data_extraction('Russian Federation')
Mexico_pop_estimates_df = country_data_extraction('Mexico')

UN_10_largest_countries_pop_estimates = pd.concat([
    India_pop_estimates_df, China_pop_estimates_df,
    United_States_pop_estimates_df, Indonesia_pop_estimates_df, 
    Pakistan_pop_estimates_df, Nigeria_pop_estimates_df, 
    Brazil_pop_estimates_df, Bangladesh_pop_estimates_df,
    Russia_pop_estimates_df, Mexico_pop_estimates_df
])

UN_10_largest_countries_pop_estimates.to_csv('./data/UN_10_largest_countries_pop_estimates.csv')

working_age_growth_df = pd.DataFrame()
working_age_growth_df = UN_10_largest_countries_pop_estimates.loc[UN_10_largest_countries_pop_estimates['Sex'] == 'Male']

working_age_growth_df['Value'] = working_age_growth_df['Value'] * -1

working_age_growth_df = pd.concat([working_age_growth_df, UN_10_largest_countries_pop_estimates.loc[UN_10_largest_countries_pop_estimates['Sex'] == 'Female']])

working_age_df = pysqldf("SELECT * FROM working_age_growth_df WHERE Age in (19,24,29,34,39,44,49,54,59,64);")

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

arrays = [
    np.array(["Bangladesh","Bangladesh", "Brazil", "Brazil","China", "China","India", "India","Indonesia", "Indonesia","Mexico","Mexico", "Nigeria","Nigeria", "Pakistan","Pakistan", "Russia","Russia", "United States","United States"]),
    np.array(["Population","Growth","Population","Growth","Population","Growth","Population","Growth","Population","Growth","Population","Growth","Population","Growth","Population","Growth","Population","Growth","Population","Growth"]),
]

pop_growth_multi_df = pd.DataFrame(columns=arrays)
pop_growth_multi_df['Bangladesh','Population'] = all_joined_df['Bangladesh Working Age Population']/1000
pop_growth_multi_df['Bangladesh','Growth'] = all_joined_df['Bangladesh Working Age Growth']
pop_growth_multi_df['Brazil','Population'] = all_joined_df['Brazil Working Age Population']/1000
pop_growth_multi_df['Brazil','Growth'] = all_joined_df['Brazil Working Age Growth']
pop_growth_multi_df['China','Population'] = all_joined_df['China Working Age Population']/1000
pop_growth_multi_df['China','Growth'] = all_joined_df['China Working Age Growth']
pop_growth_multi_df['India','Population'] = all_joined_df['India Working Age Population']/1000
pop_growth_multi_df['India','Growth'] = all_joined_df['India Working Age Growth']
pop_growth_multi_df['Indonesia','Population'] = all_joined_df['Indonesia Working Age Population']/1000
pop_growth_multi_df['Indonesia','Growth'] = all_joined_df['Indonesia Working Age Growth']
pop_growth_multi_df['Mexico','Population'] = all_joined_df['Mexico Working Age Population']/1000
pop_growth_multi_df['Mexico','Growth'] = all_joined_df['Mexico Working Age Growth']
pop_growth_multi_df['Nigeria','Population'] = all_joined_df['Nigeria Working Age Population']/1000
pop_growth_multi_df['Nigeria','Growth'] = all_joined_df['Nigeria Working Age Growth']
pop_growth_multi_df['Pakistan','Population'] = all_joined_df['Pakistan Working Age Population']/1000
pop_growth_multi_df['Pakistan','Growth'] = all_joined_df['Pakistan Working Age Growth']
pop_growth_multi_df['Russia','Population'] = all_joined_df['Russian Federation Working Age Population']/1000
pop_growth_multi_df['Russia','Growth'] = all_joined_df['Russian Federation Working Age Growth']
pop_growth_multi_df['United States','Population'] = all_joined_df['United States of America Working Age Population']/1000
pop_growth_multi_df['United States','Growth'] = all_joined_df['United States of America Working Age Growth']

pop_growth_multi_df = pop_growth_multi_df.fillna(0)

pop_growth_multi_df['Bangladesh','Population'] = pop_growth_multi_df['Bangladesh','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['Bangladesh','Growth'] = pop_growth_multi_df['Bangladesh','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['Brazil','Population'] = pop_growth_multi_df['Brazil','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['Brazil','Growth'] = pop_growth_multi_df['Brazil','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['China','Population'] = pop_growth_multi_df['China','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['China','Growth'] = pop_growth_multi_df['China','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['India','Population'] = pop_growth_multi_df['India','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['India','Growth'] = pop_growth_multi_df['India','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['Indonesia','Population'] = pop_growth_multi_df['Indonesia','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['Indonesia','Growth'] = pop_growth_multi_df['Indonesia','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['Mexico','Population'] = pop_growth_multi_df['Mexico','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['Mexico','Growth'] = pop_growth_multi_df['Mexico','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['Nigeria','Population'] = pop_growth_multi_df['Nigeria','Population'].map("{:,.2f}".format)
pop_growth_multi_df['Nigeria','Growth'] = pop_growth_multi_df['Nigeria','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['Pakistan','Population'] = pop_growth_multi_df['Pakistan','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['Pakistan','Growth'] = pop_growth_multi_df['Pakistan','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['Russia','Population'] = pop_growth_multi_df['Russia','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['Russia','Growth'] = pop_growth_multi_df['Russia','Growth'].map("{:,.1%}".format)
pop_growth_multi_df['United States','Population'] = pop_growth_multi_df['United States','Population'].map("{:,.2f}M".format)
pop_growth_multi_df['United States','Growth'] = pop_growth_multi_df['United States','Growth'].map("{:,.1%}".format)

population_1950_2050_df = pop_growth_multi_df.xs('Population', level=1, axis = 1)
growth_1950_2050_df = pop_growth_multi_df.xs('Growth', level=1, axis = 1)

population_1950_2050_df.to_csv('./data/population_1950_2050.csv')
growth_1950_2050_df.to_csv('./data/growth_1950_2050.csv')





