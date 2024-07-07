from pymongo import MongoClient
import pandas as pd

# Load cleaned data
df = pd.read_csv('data/cleaned_census_data.csv')

#making connectin with mongodb server
client = MongoClient(f'mongodb://localhost:27017/') 
db=client['project'] 
collection=db['census']

#converting dataframe to dict
data_to_mongodb = df.to_dict(orient='records') 

#inserting data to mongodb
collection.insert_many(data_to_mongodb)