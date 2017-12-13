# -*- coding: utf-8 -*-
import json

import pandas as pd
from shapely.geometry import shape, Point


def get_country_from_point(lat, long, js):
    """Take a latitude, a longitude and a geojson and return the country associated to this coordinated according to the geojson
    
        Keyword arguments:
        lat -- The latitude
        long -- The longitude
        js -- The geojson with countries of the world
    """
    # construct point based on lon/lat returned by geocoder
    point = Point(long, lat)

    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['id']
    return 'None'


def create_mapping(dataframe):
    """Take a dataframe and outputs a mapping between the country code used and the country code convention CCA3 and stores it

        Keyword arguments:
        dataframe -- The dataframe
    """
    world_geo_path = '../data/locations/countries.geo.json'
    world_json_data = json.load(open(world_geo_path, encoding="UTF-8"))

    positions = dataframe[['ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long']].groupby(
        ['ActionGeo_Lat', 'ActionGeo_Long']).agg(lambda x: x.mode()).reset_index()
    positions["Lat_Long"] = positions['ActionGeo_Lat'].map(float).map('{:,.2f}'.format).map(str) + ' , ' + positions[
        'ActionGeo_Long'].map(float).map('{:,.2f}'.format).map(str)
    positions = positions.drop_duplicates(subset=['Lat_Long'], keep=False)
    positions['ActionGeo_CountryCode'] = positions['ActionGeo_CountryCode'].apply(
        lambda x: x[0] if not type(x) is str else x)
    positions['Country_Code'] = positions['Lat_Long'].apply(
        lambda x: get_country_from_point(float(x.split(',')[0]), float(x.split(',')[1]), world_json_data))
    positions = positions[positions['Country_Code'] != 'None']

    mapping = positions[['ActionGeo_CountryCode', 'Country_Code']].groupby('ActionGeo_CountryCode').agg(
        lambda x: x.mode()[0])

    mapping.to_csv('../data/country_code_name.csv')

    return mapping


def get_mapping(dataframe):
    """Fetches a dataframe and outputs a mapping between the country code used and the country code convention CCA3, creates it if necessary.

        Keyword arguments:
        dataframe -- The dataframe
    """
    try:
        return pd.read_csv('../data/country_code_name.csv')
    except:
        print("Generating the mapping...")
        return create_mapping(dataframe)
