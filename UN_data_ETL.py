import pandas as pd
import numpy as np
import os

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
