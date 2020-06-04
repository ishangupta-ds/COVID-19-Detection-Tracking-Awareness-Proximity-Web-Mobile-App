
import numpy as np
import pandas as pd
import requests
from math import sin, cos, sqrt, atan2, radians

import warnings
warnings.filterwarnings("ignore")


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def makedatabase():
    file_id = '1-seQP2_RreSZHBxt1nI2Dqoe9vCmbwHY'
    destination = 'IndiaPostalCodes.csv'
    download_file_from_google_drive(file_id, destination)


def get_distance_between_lats_lons(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
        R = 6373

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return(distance)


def fewmoreextrathings():

    makedatabase()
    file = 'IndiaPostalCodes.csv'
    city_wise_coordinates = pd.read_csv(file)
    city_wise_coordinates['City'] = city_wise_coordinates['City'].str.upper()
    city_wise_coordinates['District'] = city_wise_coordinates['District'].str.upper()
    city_wise_coordinates['State'] = city_wise_coordinates['State'].str.upper()

    district_wise_pin_states = city_wise_coordinates.groupby('District')['PIN', 'State'].agg(lambda x: x.value_counts().index[0])
    district_wise_lat_lng = city_wise_coordinates.groupby('District')['Lat', 'Lng'].agg(pd.Series.mean)

    district_wise_data_geonames = district_wise_pin_states.merge(district_wise_lat_lng, left_on='District', right_on='District', how='inner').reset_index()

    # data from covid19india.org
    df = pd.read_json("https://api.covid19india.org/raw_data.json")
    df3 = []
    for row in range(0, df.shape[0]):
        df1 = df['raw_data'][row]
        df2 = pd.DataFrame(df1.items()).set_index(0)
        df3.append(df2.T)

    appended_data = pd.concat(df3, sort=False)
    appended_data.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    appended_data.rename(columns={'detectedcity': 'City'}, inplace=True)
    appended_data.rename(columns={'detecteddistrict': 'District'}, inplace=True)
    appended_data.rename(columns={'detectedstate': 'State'}, inplace=True)

    appended_data['City'] = appended_data['City'].str.upper()
    appended_data['District'] = appended_data['District'].str.upper()
    appended_data['State'] = appended_data['State'].str.upper()
    appended_data = appended_data.dropna(thresh=3)

    district_wise_counts = appended_data.groupby('District').agg({'patientnumber': 'count'})
    district_wise_counts.rename(columns={'patientnumber': 'd_patient_counts'}, inplace=True)
    district_wise_counts = district_wise_counts.reset_index()
    district_wise_counts['District'] = district_wise_counts['District'].str.upper()

    corona_db_with_latlng = district_wise_counts.merge(district_wise_data_geonames, left_on='District', right_on='District', how='inner')
    corona_db_with_latlng.rename(columns={'d_patient_counts': 'Num_Positive_cases'}, inplace=True)

    return (corona_db_with_latlng, city_wise_coordinates)


def extrathings():

    makedatabase()
    file = 'IndiaPostalCodes.csv'
    city_wise_coordinates = pd.read_csv(file)
    city_wise_coordinates['City'] = city_wise_coordinates['City'].str.upper()
    city_wise_coordinates['District'] = city_wise_coordinates['District'].str.upper()
    city_wise_coordinates['State'] = city_wise_coordinates['State'].str.upper()

    district_wise_pin_states = city_wise_coordinates.groupby('District')['PIN', 'State'].agg(lambda x: x.value_counts().index[0])
    district_wise_lat_lng = city_wise_coordinates.groupby('District')['Lat', 'Lng'].agg(pd.Series.mean)

    district_wise_data_geonames = district_wise_pin_states.merge(district_wise_lat_lng, left_on='District', right_on='District', how='inner').reset_index()

    # data from covid19india.org
    df = pd.read_json("https://api.covid19india.org/raw_data.json")
    df3 = []
    for row in range(0, df.shape[0]):
        df1 = df['raw_data'][row]
        df2 = pd.DataFrame(df1.items()).set_index(0)
        df3.append(df2.T)

    appended_data = pd.concat(df3, sort=False)
    appended_data.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    appended_data.rename(columns={'detectedcity': 'City'}, inplace=True)
    appended_data.rename(columns={'detecteddistrict': 'District'}, inplace=True)
    appended_data.rename(columns={'detectedstate': 'State'}, inplace=True)

    appended_data['City'] = appended_data['City'].str.upper()
    appended_data['District'] = appended_data['District'].str.upper()
    appended_data['State'] = appended_data['State'].str.upper()
    appended_data = appended_data.dropna(thresh=3)

    district_wise_counts = appended_data.groupby('District').agg({'patientnumber': 'count'})
    district_wise_counts.rename(columns={'patientnumber': 'd_patient_counts'}, inplace=True)
    district_wise_counts = district_wise_counts.reset_index()
    district_wise_counts['District'] = district_wise_counts['District'].str.upper()

    corona_db_with_latlng = district_wise_counts.merge(district_wise_data_geonames, left_on='District', right_on='District', how='inner')
    corona_db_with_latlng.rename(columns={'d_patient_counts': 'Num_Positive_cases'}, inplace=True)
    
    return corona_db_with_latlng


def get_idx_distance_from_query_locations(q_lat, q_lng, corona_db_with_latlng):
    
    dist_array = []
    for index, row in corona_db_with_latlng.iterrows():
        dist = int(get_distance_between_lats_lons(q_lat, q_lng, row['Lat'], row['Lng']))
        dist_array.append(dist)

    minpos = dist_array.index(min(dist_array))
    mindist = dist_array[minpos]
    cases = corona_db_with_latlng.loc[minpos, 'Num_Positive_cases']
    location = corona_db_with_latlng.loc[minpos, 'District']
    state = corona_db_with_latlng.loc[minpos, 'State']
    Lats = corona_db_with_latlng.loc[minpos, 'Lat']
    Lngs = corona_db_with_latlng.loc[minpos, 'Lng']

    return(mindist, cases, location, state, Lats, Lngs)


