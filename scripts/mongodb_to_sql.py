import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean

#making connectin with mongodb server
client = MongoClient(f'mongodb://localhost:27017/') 
db=client['project'] 
collection=db['census']

# Fetch data
data = list(collection.find())
cleaned_df = pd.DataFrame(data)

#dropping the column _id
if '_id' in cleaned_df.columns:
    cleaned_df.drop('_id', axis=1, inplace=True)

#to create column it's name size should be less than 64 so truncating the names
cleaned_df.rename(columns = {'Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car':'HH_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car', 
                             'Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households':'Latrine_with_Night_soil_disposed_into_open_drain_Households', 
                             'Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households':'Latrine_with_Flush_pour_flush_latrine_connected_to_other_system', 
                             'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households':'Not_having_latrine_facility_within_the_premises',
                             'Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households':'Drinking_water_From_Handpump_Tubewell_Borewell_Households',
                             'Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households':'Drinking_water_Spring_River_Canal_Tank_Pond_Lake_Other_sources',
                            }, inplace = True)

# Create SQLAlchemy engine
sql_server = 'mysql+mysqlconnector://root:1234567890@localhost:3306/project' #connecting mysql server
engine = create_engine(sql_server)

def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return Integer
    elif pd.api.types.is_float_dtype(dtype):
        return Float
    elif pd.api.types.is_bool_dtype(dtype):
        return Boolean
    else:
        return String(50)  # Default to String if no other types match

# Dynamically create the table schema using Table and MetaData 
metadata = MetaData()
columns = []

for column_name, dtype in cleaned_df.dtypes.items():
    if column_name == 'District code':
        columns.append(Column(column_name, map_dtype(dtype), primary_key=True))
        continue
    else:
        columns.append(Column(column_name, map_dtype(dtype)))
    
dynamic_table = Table('census_2011', metadata, *columns) # Create the table in the database 
metadata.create_all(engine)
cleaned_df.to_sql(name='census_2011', con=engine, if_exists='append', index=False)