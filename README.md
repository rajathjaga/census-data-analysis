# Census Data Processing and Analysis

## Overview

This project involves cleaning, processing, and analyzing census data from a given source. The tasks include renaming columns, handling missing data, standardizing state/UT names, managing new state/UT formations, data storage, database connection, and querying. The goal is to ensure uniformity, accuracy, and accessibility of the census data for further analysis and visualization.

## Tasks

### Task 1: Rename the Column Names
For uniformity in the datasets, rename the following columns:

- `State name` to `State/UT`
- `District name` to `District`
- `Male_Literate` to `Literate_Male`
- `Female_Literate` to `Literate_Female`
- `Rural_Households` to `Households_Rural`
- `Urban_Households` to `Households_Urban`
- `Age_Group_0_29` to `Young_and_Adult`
- `Age_Group_30_49` to `Middle_Aged`
- `Age_Group_50` to `Senior_Citizen`
- `Age not stated` to `Age_Not_Stated`

### Task 2: Rename State/UT Names
Standardize State/UT names so that only the first character of each word is in uppercase and the rest are in lowercase. The word "and" should be all lowercase.

**Examples:**
- Andaman and Nicobar Islands
- Arunachal Pradesh
- Bihar

### Task 3: New State/UT Formation
Handle the formation of new states/UTs:
- **Telangana (2014):** Rename `State/UT` from "Andhra Pradesh" to "Telangana" for districts listed in `Data/Telangana.txt`.
- **Ladakh (2019):** Rename `State/UT` from "Jammu and Kashmir" to "Ladakh" for districts Leh and Kargil.

### Task 4: Find and Process Missing Data
Identify and store the percentage of missing data for each column. Fill missing data using information from other cells where possible. Compare the amount of missing data before and after the data-filling process.

**Hints:**
- `Population = Male + Female`
- `Literate = Literate_Male + Literate_Female`
- `Population = Young_and_Adult + Middle_Aged + Senior_Citizen + Age_Not_Stated`
- `Households = Households_Rural + Households_Urban`

### Task 5: Save Data to MongoDB
Save the processed data to MongoDB in a collection named `census`.

### Task 6: Database Connection and Data Upload
Fetch data from MongoDB and upload it to a relational database. Table names should be the same as the file names without the extension. Include primary and foreign key constraints where required.

### Task 7: Run Query on the Database and Show Output on Streamlit
Execute the following queries and display the results on Streamlit:

1. Total population of each district.
2. Number of literate males and females in each district.
3. Percentage of workers (both male and female) in each district.
4. Number of households with access to LPG or PNG as cooking fuel in each district.
5. Religious composition (Hindus, Muslims, Christians, etc.) of each district.
6. Number of households with internet access in each district.
7. Educational attainment distribution (below primary, primary, middle, secondary, etc.) in each district.
8. Number of households with various modes of transportation (bicycle, car, radio, television, etc.) in each district.
9. Condition of occupied census houses (dilapidated, with separate kitchen, with bathing facility, with latrine facility, etc.) in each district.
10. Household size distribution (1 person, 2 persons, 3-5 persons, etc.) in each district.
11. Total number of households in each state.
12. Number of households with a latrine facility within the premises in each state.
13. Average household size in each state.
14. Number of owned versus rented households in each state.
15. Distribution of different types of latrine facilities (pit latrine, flush latrine, etc.) in each state.
16. Number of households with access to drinking water sources near the premises in each state.
17. Average household income distribution in each state based on power parity categories.
18. Percentage of married couples with different household sizes in each state.
19. Number of households below the poverty line in each state based on power parity categories.
20. Overall literacy rate (percentage of literate population) in each state.

## How to Run the Project

### Prerequisites
- Python 3.x
- MongoDB
- A relational database (e.g., MySQL)
- Streamlit

### Setup

1. Clone the repository:
   git clone https://github.com/rajathjaga/census-data-analysis.git
   cd census-data-analysis

2. Install the required packages:
   pip install -r requirements.txt

### Execution

1. Run the data processing script:
   python data_cleaning.py

2. Upload data to the mongodb:
   python data_to_mongodb.py

3. Upload data to the Mysql to mongodb:
   python mongodb_to_sql.py

4. Run the Streamlit application:
   streamlit run streamlit_app.py

