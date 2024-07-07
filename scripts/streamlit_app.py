import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, MetaData, Table, select, func

# Create SQLAlchemy engine
sql_server = 'mysql+mysqlconnector://root:1234567890@localhost:3306/project' #connecting mysql server
engine = create_engine(sql_server)
metadata = MetaData()
metadata.reflect(engine)
census = Table('census_2011', metadata, autoload=True, autoload_with=engine)

# Function to execute queries and return results
def execute_query(query):
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
    return result

# Streamlit app
st.title("Census Data Analysis")

#1)Total population of each district
# st.header("Total Population by District")
query_total_population = select(census.columns.District, func.sum(census.columns.Population).label('Population')).group_by(census.columns.District)
result_total_population = execute_query(query_total_population)
df_total_population = pd.DataFrame(result_total_population)


#2)How many literate males and females are there in each district?
literacy = select(census.columns.District, census.columns.Literate_Male, census.columns.Literate_Female)
total_literacy = execute_query(literacy)
df_literacy = pd.DataFrame(total_literacy)

#3)What is the percentage of workers (both male and female) in each district?
percentage_work = select(census.columns.Male_Workers, census.columns.Workers,
    (census.columns.Male_Workers / census.columns.Workers * 100).label('Percentage_Male_Workers'),
    (census.columns.Female_Workers / census.columns.Workers * 100).label('Percentage_Female_Workers'),
)
total_worker_per = execute_query(percentage_work)
df_percentage_work = pd.DataFrame(total_worker_per)

#4)How many households have access to LPG or PNG as a cooking fuel in each district?
households_with_LPG_or_PNG = select(census.columns.District, census.columns.LPG_or_PNG_Households)
result_households_with_LPG_or_PNG = execute_query(households_with_LPG_or_PNG)
df_households_with_LPG_or_PNG = pd.DataFrame(result_households_with_LPG_or_PNG)

#5)What is the religious composition (Hindus, Muslims, Christians, etc.) of each district?
religious_comp = select(census.columns.District, census.columns.Hindus, census.columns.Muslims, census.columns.Christians,
                       census.columns.Sikhs, census.columns.Buddhists, census.columns.Jains,
                       census.columns.Others_Religions
                       )
result_religious_comp = execute_query(religious_comp)
df_religious_comp = pd.DataFrame(result_religious_comp)

#6)How many households have internet access in each district?
households_with_internet = select(census.columns.District, census.columns.Households_with_Internet)
result_households_with_internet = execute_query(households_with_internet)
df_households_with_internet = pd.DataFrame(result_households_with_internet)

#7)What is the educational attainment distribution (below primary, primary, middle, secondary, etc.) in each district?
education = select(census.columns.District, census.columns.Primary_Education, census.columns.Middle_Education,
                       census.columns.Secondary_Education, census.columns.Higher_Education, census.columns.Graduate_Education,
                       census.columns.Other_Education, census.columns.Literate_Education, census.columns.Illiterate_Education, census.columns.Total_Education
                       )
result_education = execute_query(education)
df_education = pd.DataFrame(result_education)

#8)How many households have access to various modes of transportation (bicycle, car, radio, television, etc.) in each district?
transport = select(census.columns.District, census.columns.Households_with_Bicycle, census.columns.Households_with_Car_Jeep_Van,
                       census.columns.Households_with_Scooter_Motorcycle_Moped)
result_transport = execute_query(transport)
df_transport = pd.DataFrame(result_transport)

#9)What is the condition of occupied census houses (dilapidated, with separate kitchen, with bathing facility, with latrine facility, etc.) in each district?
condition_households = select(census.columns.District, census.columns.Condition_of_occupied_census_houses_Dilapidated_Households, census.columns.Households_with_separate_kitchen_Cooking_inside_house,
                census.columns.Having_bathing_facility_Total_Households, census.columns.Having_latrine_facility_within_the_premises_Total_Households)
result_condition_households = execute_query(condition_households)
df_condition_households = pd.DataFrame(result_condition_households)

#10)How is the household size distributed (1 person, 2 persons, 3-5 persons, etc.) in each district?
persons_metrics = select(census.columns.District, census.columns.Household_size_1_to_2_persons, census.columns.Household_size_2_persons_Households,
                census.columns.Household_size_3_persons_Households, census.columns.Household_size_3_to_5_persons_Households, census.columns.Household_size_4_persons_Households,
                census.columns.Household_size_5_persons_Households, census.columns.Household_size_6_8_persons_Households, census.columns.Household_size_9_persons_and_above_Households)
result_persons_metrics = execute_query(persons_metrics)
df_persons_metrics = pd.DataFrame(result_persons_metrics)

#11)What is the total number of households in each state?
households = select(census.columns['State/UT'], func.sum(census.columns.Households).label('Total Households')).group_by(census.columns['State/UT'])
result_households = execute_query(households)
df_households = pd.DataFrame(result_households)

#12)How many households have a latrine facility within the premises in each state?
latrine_within_household = select(census.columns['State/UT'], func.sum(census.columns.Having_latrine_facility_within_the_premises_Total_Households).label('Having_latrine_facility_within_the_premises_Total_Households')).group_by(census.columns['State/UT'])
result_latrine_within_household = execute_query(latrine_within_household)
df_latrine_within_household = pd.DataFrame(result_latrine_within_household)

#13)What is the average household size in each state?
avg_household_size = select(census.columns['State/UT'],
    (
        (func.sum(census.columns.Household_size_1_person_Households * 1) +
         func.sum(census.columns.Household_size_2_persons_Households * 2) +
         func.sum(census.columns.Household_size_3_persons_Households * 3) +
         func.sum(census.columns.Household_size_3_to_5_persons_Households * 4) +
         func.sum(census.columns.Household_size_4_persons_Households * 4) +
         func.sum(census.columns.Household_size_5_persons_Households * 5) +
         func.sum(census.columns.Household_size_6_8_persons_Households * 7) +
         func.sum(census.columns.Household_size_9_persons_and_above_Households * 9)
        ) / (
         func.sum(census.columns.Household_size_1_person_Households) +
         func.sum(census.columns.Household_size_2_persons_Households) +
         func.sum(census.columns.Household_size_3_persons_Households) +
         func.sum(census.columns.Household_size_3_to_5_persons_Households) +
         func.sum(census.columns.Household_size_4_persons_Households) +
         func.sum(census.columns.Household_size_5_persons_Households) +
         func.sum(census.columns.Household_size_6_8_persons_Households) +
         func.sum(census.columns.Household_size_9_persons_and_above_Households)
        )
        ).label('Average_Household_Size')
        ).group_by(census.columns['State/UT'])

result_avg_household_size = execute_query(avg_household_size)
df_avg_household_size = pd.DataFrame(result_avg_household_size)

#14)How many households are owned versus rented in each state?
ownership = select(census.columns['State/UT'], func.sum(census.columns.Ownership_Owned_Households).label('Ownership_Owned_Households'), func.sum(census.columns.Ownership_Rented_Households).label('Ownership_Rented_Households')).group_by(census.columns['State/UT'])
result_ownership = execute_query(ownership)
df_ownership = pd.DataFrame(result_ownership)

#15)What is the distribution of different types of latrine facilities (pit latrine, flush latrine, etc.) in each state?
latrine_fac = select(census.columns['State/UT'], func.sum(census.columns.Latrine_with_Night_soil_disposed_into_open_drain_Households).label('Latrine_with_Night_soil_disposed_into_open_drain_Households'), func.sum(census.columns.Latrine_with_Flush_pour_flush_latrine_connected_to_other_system).label('Latrine_with_Flush_pour_flush_latrine_connected_to_other_system'),
                     func.sum(census.columns.Having_latrine_facility_within_the_premises_Total_Households).label('Having_latrine_facility_within_the_premises_Total_Households'), func.sum(census.columns.Type_of_latrine_facility_Pit_latrine_Households).label('Type_of_latrine_facility_Pit_latrine_Households'), func.sum(census.columns.Type_of_latrine_facility_Other_latrine_Households).label('Type_of_latrine_facility_Other_latrine_Households'),
                     func.sum(census.columns.Latrine_with_Flush_pour_flush_latrine_connected_to_other_system).label('Latrine_with_Flush_pour_flush_latrine_connected_to_other_system'), func.sum(census.columns.Not_having_latrine_facility_within_the_premises).label('Not_having_latrine_facility_within_the_premises')).group_by(census.columns['State/UT'])
result_latrine_fac = execute_query(latrine_fac)
df_latrine_fac = pd.DataFrame(result_latrine_fac)

#16)How many households have access to drinking water sources near the premises in each state?
drinking_wat = select(census.columns['State/UT'], func.sum(census.columns.Location_of_drinking_water_source_Near_the_premises_Households)).group_by(census.columns['State/UT'])
result_drinking_wat = execute_query(drinking_wat)
df_drinking_wat = pd.DataFrame(result_drinking_wat)

#17)What is the average household income distribution in each state based on the power parity categories?
household_income = select(census.columns['State/UT'],(func.sum(census.columns.Total_Power_Parity)
        / (func.sum(census.columns.Households))).label('Average_household_income')
        ).group_by(census.columns['State/UT'])

result_average_household_income = execute_query(household_income)
df_household_income = pd.DataFrame(result_average_household_income)

#18)What is the percentage of married couples with different household sizes in each state?
#a)
total_sum_subquery = select(
    func.sum(census.columns.Married_couples_1_Households).label('total_sum')
).scalar_subquery()

couple_with_1_house = select(
    census.columns['State/UT'],
    func.sum(census.columns.Married_couples_1_Households).label('Married_couples_1_Households'),
    (func.sum(census.columns.Married_couples_1_Households) / total_sum_subquery * 100).label('Percentage')
).group_by(census.columns['State/UT'])

result_couple_with_1_house = execute_query(couple_with_1_house)
df_couple_with_1_house = pd.DataFrame(result_couple_with_1_house)

#19)How many households fall below the poverty line in each state based on the power parity categories?
poverty_line = select(
    census.columns['State/UT'],
    func.sum(census.columns.Power_Parity_Less_than_Rs_45000).label('Households_Below_Poverty_Line')
).group_by(census.columns['State/UT'])
result_poverty_line = execute_query(poverty_line)
df_poverty_line = pd.DataFrame(result_poverty_line)

#20)What is the overall literacy rate (percentage of literate population) in each state?
literate_perc = select(
    census.columns['State/UT'],
    (func.sum(census.columns.Literate).label('Literate')/ func.sum(census.columns.Population).label('Population') * 100).label('Percentage')
).group_by(census.columns['State/UT'])

result_literate_perc = execute_query(literate_perc)
df_literate_perc = pd.DataFrame(result_literate_perc)

st.dataframe(df_couple_with_1_house)