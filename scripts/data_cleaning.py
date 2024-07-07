import pandas as pd

df = pd.read_excel('data/census_2011.xlsx')

#total missing data
total_cells = df.size
total_missing_fields = df.isnull().sum().sum()
missing_per_befor_cleaning = (total_missing_fields / total_cells) * 100

print("missing_per_befor_cleaning", missing_per_befor_cleaning)

#renaming column name
df.rename(columns = {'State name':'State/UT', 'District name':'District', 'Male_Literate':'Literate_Male', 'Female_Literate':'Literate_Female', 
                     'Rural_Households':'Households_Rural', 'Urban_ Households':'Households_Urban', 'Age_Group_0_29':'Young_and_Adult',
                     'Age_Group_30_49':'Middle_Aged', 'Age_Group_50':'Senior_Citizen', 'Age not stated':'Age_Not_Stated'}, inplace = True)

#renaming the state name 
df['State/UT'] = df['State/UT'].apply(
    lambda x: ' '.join([word.title() if word.lower() != 'and' else word.lower() for word in x.split()])
)

#changing the state acording to district
def change_state(dist):
    telangana = ['Adilabad', 'Nizamabad', 'Karimnagar', 'Medak', 'Hyderabad', 'Rangareddy', 'Mahbubnagar', 'Nalgonda',
                            'Warangal', 'Khammam']
    ladakh = ['Leh', 'Kargil']
    if dist['District'] in telangana:
        return 'Telangana'
    if dist['District'] in ladakh:
        return 'Ladakh'
    return dist['State/UT']
    
df['State/UT'] = df.apply(change_state, axis=1)

#calculate population
def cal_pop(x):
    if pd.isnull(x['Population']):
        return x['Male'] + x['Female']
    return x['Population']
df['Population']=df.apply(cal_pop, axis=1)

#calculate male female
def cal_male_female(value):
    if pd.isnull(value['Male']):
        value['Male'] = value['Population'] - value['Female']
    if pd.isnull(value['Female']):
        value['Female'] = value['Population'] - value['Male']
    return value

df = df.apply(cal_male_female, axis=1)

#calculate literate
def cal_literate(value):
    if pd.isnull(value['Literate_Male']):
        value['Literate_Male'] = value['Literate'] - value['Literate_Female']
    if pd.isnull(value['Literate_Female']):
        value['Literate_Female'] = value['Literate'] - value['Literate_Male']
    if pd.isnull(value['Literate']):
        value['Literate'] = value['Literate_Male'] - value['Literate_Female']
    return value

df = df.apply(cal_literate, axis=1)

def cal_literate(value):
    if pd.isnull(value['Literate_Male']):
        value['Literate_Male'] = value['Literate'] - value['Literate_Female']
    if pd.isnull(value['Literate_Female']):
        value['Literate_Female'] = value['Literate'] - value['Literate_Male']
    if pd.isnull(value['Literate']):
        value['Literate'] = value['Literate_Male'] - value['Literate_Female']
    return value

df = df.apply(cal_literate, axis=1)

def cal_work(row):
    if pd.isnull(row['Workers']):
        row['Workers'] = row['Male_Workers'] + row['Female_Workers']
    if pd.isnull(row['Male_Workers']):
        row['Male_Workers'] = row['Workers'] - row['Female_Workers']
    if pd.isnull(row['Female_Workers']):
        row['Female_Workers'] = row['Workers'] - row['Male_Workers']
    return row

df = df.apply(cal_work, axis=1)

def cal_work_by_prof(row):
    if pd.isnull(row['Non_Workers']):
        row['Non_Workers'] = row['Population'] - row['Workers']
    if pd.isnull(row['Marginal_Workers']):
        row['Marginal_Workers'] = row['Workers'] - row['Main_Workers']
    if pd.isnull(row['Main_Workers']):
        row['Main_Workers'] = row['Workers'] - row['Marginal_Workers']
    return row

df = df.apply(cal_work_by_prof, axis=1)

def cal_work_by_type(row):
    if pd.isnull(row['Cultivator_Workers']):
        row['Cultivator_Workers'] = row['Workers'] - row['Agricultural_Workers'] - row['Household_Workers'] - row['Other_Workers']
    if pd.isnull(row['Agricultural_Workers']):
        row['Agricultural_Workers'] = row['Workers'] - row['Cultivator_Workers'] - row['Household_Workers'] - row['Other_Workers']
    if pd.isnull(row['Household_Workers']):
        row['Household_Workers'] = row['Workers'] - row['Agricultural_Workers'] - row['Cultivator_Workers'] - row['Other_Workers']
    if pd.isnull(row['Other_Workers']):
        row['Other_Workers'] = row['Workers'] - row['Agricultural_Workers'] - row['Cultivator_Workers'] - row['Household_Workers']
    return row

df = df.apply(cal_work_by_type, axis=1)

#calculate missing religion
df['Hindus'].fillna(df['Population'] - df[['Muslims', 'Christians', 'Sikhs', 'Buddhists', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].sum(axis=1), inplace=True)
df['Muslims'].fillna(df['Population'] - df[['Hindus', 'Christians', 'Sikhs', 'Buddhists', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].sum(axis=1), inplace=True)
df['Christians'].fillna(df['Population'] - df[['Hindus', 'Muslims', 'Sikhs', 'Buddhists', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].sum(axis=1), inplace=True)
df['Sikhs'].fillna(df['Population'] - df[['Hindus', 'Muslims', 'Christians', 'Buddhists', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].sum(axis=1), inplace=True)
df['Buddhists'].fillna(df['Population'] - df[['Hindus', 'Muslims', 'Christians', 'Sikhs', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].sum(axis=1), inplace=True)
df['Jains'].fillna(df['Population'] - df[['Hindus', 'Muslims', 'Christians', 'Sikhs', 'Buddhists', 'Others_Religions', 'Religion_Not_Stated']].sum(axis=1), inplace=True)
df['Others_Religions'].fillna(df['Population'] - df[['Hindus', 'Muslims', 'Christians', 'Sikhs', 'Buddhists', 'Jains', 'Religion_Not_Stated']].sum(axis=1), inplace=True)
df['Religion_Not_Stated'].fillna(df['Population'] - df[['Hindus', 'Muslims', 'Christians', 'Sikhs', 'Buddhists', 'Jains', 'Others_Religions']].sum(axis=1), inplace=True)

#calculate education
df['Total_Education'].fillna(df[['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Below_Primary_Education'].fillna(df['Total_Education'] - df[['Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Primary_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Middle_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Primary_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Secondary_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Higher_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Graduate_Education', 'Other_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Graduate_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Other_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Other_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Literate_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Literate_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education', 'Illiterate_Education']].sum(axis=1), inplace=True)
df['Illiterate_Education'].fillna(df['Total_Education'] - df[['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education', 'Literate_Education']].sum(axis=1), inplace=True)

def cal_households(row):
    if pd.isnull(row['Households']):
        row['Households'] = row['Households_Rural'] + row['Urban_Households']
    if pd.isnull(row['Households_Rural']):
        row['Households_Rural'] = row['Households'] - row['Urban_Households']
    if pd.isnull(row['Urban_Households']):
        row['Urban_Households'] = row['Households'] - row['Households_Rural']
    return row

df = df.apply(cal_households, axis=1)

total_cells = df.size
total_missing_fields = df.isnull().sum().sum()
missing_per_after_cleaning = (total_missing_fields / total_cells) * 100

print('missing_per_after_cleaning', missing_per_after_cleaning)

missing_percentage = pd.DataFrame({"missing_per_befor_cleaning": [missing_per_befor_cleaning], "missing_per_after_cleaning": [missing_per_after_cleaning]})

# Save cleaned data
df.to_csv('data/cleaned_census_data.csv', index=False)