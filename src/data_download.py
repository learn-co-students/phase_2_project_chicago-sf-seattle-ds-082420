from io import BytesIO, TextIOWrapper, StringIO
from zipfile import ZipFile
import pandas as pd
import requests
import pandas as pd

def get_tables(dictionary):
    
    """
    Takes a dictionary of tables, dictionary
    returns 2 tables, ordinaltable and category table
    ordinaltable is a table of just the ordinal columns from all sales, parcels and residential buildings
    categorytable is the table of categorical variables from the same.
    ordinal table will be return[0], categorical will be return[1]
    
    """
    
    sales = dictionary['rp_sale']
    parcels = dictionary['res_bldg']
    residences = dictionary['parcel']

    sales = sales[sales['DocumentDate'].astype(str).str.endswith('2019')]
    sales = sales[(sales['SalePrice'] > 120000) & (sales['SalePrice'] < 3000000)]
    combo = sales.merge(residences, on = ['Major','Minor'])
    combo = combo.merge(parcels, on = ['Major','Minor'])
    combo = combo[combo['BldgGrade'] > 1]
    combo = combo[(combo['PresentUse'] == 2)
                 | (combo['PresentUse'] == 29)
                 | (combo['PresentUse'] == 300)
                 | (combo['PresentUse'] == 6)]
    combo = combo[combo['NbrLivingUnits'] != 10]

    ordinalcols = ['SalePrice','BrickStone','NbrLivingUnits',
                   'Stories','BldgGrade','SqFt1stFloor','SqFtUpperFloor','SqFtUnfinFull',
                  'SqFtUnfinHalf','SqFtTotLiving','SqFtTotBasement','SqFtFinBasement','SqFtGarageBasement',
                  'FinBasementGrade','SqFtGarageAttached','SqFtOpenPorch','SqFtEnclosedPorch',
                  'SqFtDeck','Bedrooms','BathHalfCount','Bath3qtrCount','BathFullCount','FpSingleStory',
                  'FpMultiStory','FpFreestanding','FpAdditional','YrBuilt','YrRenovated','Condition',
                  'AddnlCost','SqFtLot','MtRainier','Olympics','Cascades','Territorial','SeattleSkyline',
                   'PugetSound','LakeWashington','LakeSammamish','SmallLakeRiverCreek','OtherView',
                  'WfntFootage','LotDepthFactor','TrafficNoise']

    categorycols = ['SaleReason', 'PropertyClass','HeatSystem','HeatSource','PresentUse','HBUAsIfVacant',
                   'HBUAsImproved','WaterSystem','SewerSystem','Access','InadequateParking','StreetSurface',
                   'Topography','WfntLocation','WfntBank','WfntPoorQuality','WfntRestrictedAccess',
                    'WfntAccessRights','WfntProximityInfluence','TidelandShoreland','PowerLines',
                    'OtherNuisances','AdjacentGolfFairway','AdjacentGreenbelt'] 

    ordinaltable = combo[ordinalcols]
    categorytable = combo[categorycols]

    return (ordinaltable, categorytable)

def download_zipfile(URL):
    """
    Given a URL for a .zip, download and unzip the .zip file
    this function is borrowed from code provided in the phase 1 project
    """
    response = requests.get(URL)
    print(f"""Successfully downloaded ZIP file
    {URL}
    """)

    content_as_file = BytesIO(response.content)
    zip_file = ZipFile(content_as_file)
    return zip_file

def open_csv_from_zip(zip_file, csv_name):
    """
    Given an unzipped .zip file and the name of a CSV inside of it, 
    extract the CSV and return the relevant file
    this function is borrowed from code provided in the phase 1 project
    """
    csv_file_bytes = zip_file.open(csv_name)
    # it seems we have to open the .zip as bytes, but CSV reader requires text
    csv_file_text = TextIOWrapper(csv_file_bytes, encoding="ISO-8859-1")
    return csv_file_text

def get_parcel_table():
    parcel_url = 'https://aqua.kingcounty.gov/extranet/assessor/Parcel.zip'
    csv_name = 'EXTR_Parcel.csv'
    zip_file = download_zipfile(parcel_url)
    csv_as_text = open_csv_from_zip(zip_file, csv_name)
    rp_sale_table = pd.read_csv(csv_as_text)
    return rp_sale_table
    
def get_lookup_table():
    lookup_url = 'https://aqua.kingcounty.gov/extranet/assessor/Lookup.zip'
    csv_name = 'EXTR_LookUp.csv'
    zip_file = download_zipfile(lookup_url)
    csv_as_text = open_csv_from_zip(zip_file, csv_name)
    rp_sale_table = pd.read_csv(csv_as_text)
    return rp_sale_table
    
def get_res_bldg_table():
    res_bldg_url = 'https://aqua.kingcounty.gov/extranet/assessor/Residential%20Building.zip'
    csv_name = 'EXTR_ResBldg.csv'
    zip_file = download_zipfile(res_bldg_url)
    csv_as_text = open_csv_from_zip(zip_file, csv_name)
    rp_sale_table = pd.read_csv(csv_as_text, encoding = 'ISO-9959-1')
    return rp_sale_table

def get_rp_sale_table():
    rp_sale_url = 'https://aqua.kingcounty.gov/extranet/assessor/Real%20Property%20Sales.zip'
    csv_name = 'EXTR_RPSale.csv'
    zip_file = download_zipfile(rp_sale_url)
    csv_as_text = open_csv_from_zip(zip_file, csv_name)
    rp_sale_table = pd.read_csv(csv_as_text)
    return rp_sale_table

def get_dataframes():
    """
    Create a dictionary with the each csv file as a pandas dataframe.
    """
    dataframes_dict = {
        "parcel": get_parcel_table(),
        "res_bldg": get_res_bldg_table(),
        "rp_sale": get_rp_sale_table(),
        "lookup": get_lookup_table(),
    }
    return dataframes_dict