import pandas as pd
import os

def strip_all_columns(df):
    cl = []
    for columns in df:
        cl.append(columns)
    return cl


def strip(df):
    """
    Function to strip whitespace from all columns of datatype = object
    """
    cl = strip_all_columns(df)
    for column_name in cl:
        if df[column_name].dtype == 'object':  # Check if the column contains object (string) values
            df.loc[:, column_name] = df[column_name].str.strip()
    return df


def removedup_id(df):
    """
    Remove duplicate records based on property_id
    """
    dup = df.duplicated(subset=["property_id"]).sum()
    print("Number of duplicates BEFORE:",dup)
    df.drop_duplicates(subset=["property_id"],keep="first", inplace=True)
    dup = df.duplicated(subset=["property_id"]).sum()
    print("Number of duplicates AFTER:",dup)


def remove_none_prices(df):
    """
    Remove records with empty price field
    """
    price_empty_before = df["price"].isnull().sum()
    print("Number of records with empty price BEFORE:", price_empty_before)
    df.dropna(subset=['price'], inplace=True)
    price_empty_after = df["price"].isnull().sum()
    print("Number of records with empty price AFTER:", price_empty_after)
    return df

def remove_none_living_area(df):
    """
    Remove records with empty living area
    """
    area_empty_before = df["living_area"].isnull().sum()
    print("Number of records with empty area BEFORE:", area_empty_before)
    df.dropna(subset=['living_area'], inplace=True)
    area_empty_after = df["living_area"].isnull().sum()
    print("Number of records with empty price AFTER:", area_empty_after)
    return df

def remove_outliers_living_area (df):
    """
    Remove too large or to small living area based on interquartile range
    """
    seventy_fifth = df["living_area"].quantile(0.75)
    print("75th percentile = ", seventy_fifth)
    twenty_fifth = df["living_area"].quantile(0.25)
    print("25th percentile = ", twenty_fifth)
    area_iqr = seventy_fifth-twenty_fifth
    print("area iqr = ", area_iqr)
    upper = seventy_fifth + (1.5*area_iqr)
    lower = twenty_fifth - (1.5*area_iqr)
    df = df.loc[(df["living_area"] <= upper)&(df["living_area"] >= lower)]
    print(df["living_area"].describe())
    return df


def remove_dup_no_id(df):
    """
    Function to remove all duplicate rows without looking at property_id
    """ 
    columns_to_compare = [col for col in df.columns if col != "property_id"]
    df.drop_duplicates(subset=columns_to_compare, keep="first", inplace=True)
    return df


def remove_street_nr(df):
    """
    Function to remove street_name and house_number columns
    """
    df.drop(["street_name", "house_number"], axis="columns", inplace= True)
    return df


def remove_empty(df):
    """
    Function to remove completely empty rows (where only property_id is filled in)
    """
    columns_to_compare = [col for col in df.columns if col != "property_id"]
    #checks completely empty rows
    df.dropna(how='all', inplace=True)
    #checks if property-id is completely empty
    df.dropna(how='all', subset=columns_to_compare, inplace=True)
    return df


def remove_house_in_app(df):
    """
    Function to remove records that don't have property type = house or house_group for the house data
    """
    df = df[~df["property_type"].isin(["HOUSE", "HOUSE_GROUP"])]
    return df


def remove_app_in_house(df):
    """
    Function to remove house and house_group records for the appartement data
    """
    df = df[df["property_type"].isin(["HOUSE", "HOUSE_GROUP"])]
    return df


def open_and_lowercase(df):
    """
    The function lowercases all locality names to avoid ambiguity
    """
    df["locality_name"] = df["locality_name"].str.lower()
    return df


def drop_non_belgian(df):
    """
    The function checks if postal codes are in Belgium to remove non-belgian properties
    """
    df['is_belgian'] = df['postal_code'].astype(str).isin(bpost_codes['Postcode'].astype(str))

    df.loc[df['is_belgian']==False]

    df = df.drop(df[df['is_belgian'] == False].index)
    return df


def get_dutch_locality_name(current_locality_name):
    """
    The function translates the locality name into Dutch in case it exists
    """
    name_loc = georef_with_nl.loc[(georef_with_nl["Sub-municipality name (French)"] == current_locality_name) | (georef_with_nl["Sub-municipality name (German)"] == current_locality_name)]
    if not name_loc.empty:
        return(name_loc["Sub-municipality name (Dutch)"].iloc[0])
    else:
        return current_locality_name


def change_locality_name(df):
    df["locality_name"] = df["locality_name"].apply(get_dutch_locality_name)
    return df

def get_province(df):
    df["postal_code"] = df["postal_code"].astype(int)
    bpost_code_df = bpost_codes[["Postcode","Hoofdgemeente","Provincie"]]
    bpost_code_df = bpost_code_df.drop_duplicates()
    merged_df = pd.merge(df, bpost_code_df, left_on='postal_code', right_on='Postcode', how='inner')
    merged_df = merged_df.drop(columns=["Postcode", "is_belgian"])
    new_column_names = {'Hoofdgemeente': 'main_city', 'Provincie': 'province'}
    merged_df.rename(columns=new_column_names, inplace=True)
    return merged_df


# Define the file paths using os.path.join to ensure compatibility
raw_huis_te_koop_path = os.path.join(".","dags", "immoweb", "data", "raw", "raw_huis_te_koop.csv")
raw_apartement_te_koop_path = os.path.join(".","dags", "immoweb", "data", "raw", "raw_apartement_te_koop.csv")
zipcodes_alpha_nl_new = os.path.join(".","dags", "immoweb", "data", "raw", "zipcodes_alpha_nl_new.csv")
georef_belgium_postal_codes = os.path.join(".","dags", "immoweb", "data", "raw", "georef-belgium-postal-codes.csv")

    #open a the file from bpost and lowercase all location names
bpost_codes = pd.read_csv(zipcodes_alpha_nl_new, delimiter=";")
bpost_codes[['Plaatsnaam', 'Hoofdgemeente', 'Provincie']] = bpost_codes[['Plaatsnaam', 'Hoofdgemeente', 'Provincie']].apply(lambda x: x.astype(str).str.lower())

    #open a the file from georef and lowercase all location names
georef = pd.read_csv(georef_belgium_postal_codes, delimiter=";")
georef[['Sub-municipality name (French)','Sub-municipality name (Dutch)', 'Sub-municipality name (German)']] = georef[['Sub-municipality name (French)','Sub-municipality name (Dutch)', 'Sub-municipality name (German)']].apply(lambda x: x.str.lower())
georef_with_nl = georef[~georef['Sub-municipality name (Dutch)'].isna()] #drop NaN from the Dutch values

house1 = pd.read_csv(raw_huis_te_koop_path, sep=",")
app1 = pd.read_csv(raw_apartement_te_koop_path, sep=",")
def clean_data():
    house= house1
    app= app1

    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    print("---Stripping blancs from all columns")
    house = strip(house)
    app = strip(app)    
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    print("---Removing Duplicates from Houses")
    removedup_id(house)
    print("---Removing Duplicates from Appartments")
    removedup_id(app)
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    print("---Removing records with empty price field from Houses")
    remove_none_prices(house)
    print("---Removing records with empty price field from Appartements")
    remove_none_prices(app)
    print("-------------------------------")

    print("---Removing records with empty area field from Houses")
    remove_none_living_area(house)
    print("---Removing records with empty field from Appartements")
    remove_none_living_area(app)
    print("-------------------------------")


    print("---Removing outliers in living area from Houses")
    house = remove_outliers_living_area(house)
    print("---Removing utliers in living area from Appartements")
    app = remove_outliers_living_area(app)
    print("-------------------------------")

    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")
    print("---Removing Duplicates from Houses that have the same property_id")
    remove_dup_no_id(house)
    print("---Removing Duplicates from Appartments that have the same property_id")
    remove_dup_no_id(app)
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    print("---Removing Streetnames and House Numbers")
    remove_street_nr(house)
    remove_street_nr(app)
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    print("---Removing Empty records that only have property_id")
    remove_empty(house)
    remove_empty(app)
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    house = remove_app_in_house(house)
    app = remove_house_in_app(app)
    print("-------------------------------")
    print("---Removing House in Appartments")
    print("---Removing Appartments in Houses")
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    house = open_and_lowercase(house)
    app = open_and_lowercase(app)
    print("-------------------------------")
    print("---Lowercasing Houses")
    print("---Lowercasing Appartments")
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    house = drop_non_belgian(house)
    app = drop_non_belgian(app)
    print("-------------------------------")
    print("---Removing Houses outside Belgium")
    print("---Removing Appartments outside Belgium")
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")


    house = change_locality_name(house)
    app = change_locality_name(app)
    print("-------------------------------")
    print("--- Translation into Dutch: Houses")
    print("---Translation into Dutch: Appartments")
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    house = get_province(house)
    app = get_province(app)
    print("-------------------------------")
    print("--- Getting Province: Houses")
    print("---Getting Province: Apartments")
    print("-------------------------------")
    print("TOTAL HOUSE RECORDS:",len(house))
    print("TOTAL APP RECORDS:",len(app))
    print("-------------------------------")

    house.to_csv("./dags/immoweb/data/clean/clean_house2.csv", sep=',', index=False, encoding='utf-8') 
    app.to_csv("./dags/immoweb/data/clean/clean_app2.csv", sep=',', index=False, encoding='utf-8')   

if __name__ == '__main__':
    clean_data()
