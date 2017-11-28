import pandas as pd
import datetime
from fetch_gdelt_data import *
from fetch_source_country import get_tld_to_country_dict, get_all_newspapers_to_country_dict
from fetch_location import get_mapping
import re
import requests

def clean_df(dataframe):
    dataframe = dataframe[['EventCode', 'SOURCEURL', 'ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long',
                           'IsRootEvent', 'QuadClass', 'GoldsteinScale', 'AvgTone',
                           'NumMentions', 'NumSources', 'NumArticles', 'ActionGeo_Type', 'Day']]
    dataframe = dataframe.dropna(axis=0, how='any')
    mapping = get_mapping(dataframe).set_index('ActionGeo_CountryCode')
    dataframe['Country_Code'] = dataframe['ActionGeo_CountryCode'].apply(lambda x: mapping.loc[x]['Country_Code']  if x in mapping['Country_Code'].index.values else 'None')
    
    dataframe['SOURCEURL'] = dataframe['SOURCEURL'].apply(lambda x: clean_url(x))
    dataframe['Country_Source'] = get_countries_for_dataframe(dataframe, 'SOURCEURL', get_all_newspapers_to_country_dict(), get_all_newspapers_to_country_dict())
    
    r = requests.get('https://raw.githubusercontent.com/mledoze/countries/master/countries.json')
    d = {}
    for c in r.json():
        d[c['cca3']] = c['name']['common']
        
    dataframe['Country_Name'] = dataframe['Country_Code'].apply(lambda x: d[x] if x in d else 'None')
    
    return dataframe


def clean_url(url):
            """ This function clean a url.
                For example https://example.com will be returned as example.com

                Keyword arguments:
                url -- The url
            """
            url_pair = re.findall(r'\b(?!www\.)([a-zA-Z0-9-]+(\.[a-z]+)+)', url.lower())

            if(url_pair == []): #If it is not a url
                return url
            else:
                return url_pair[0][0]

def get_countries_for_dataframe(df, column_name, website_dict, tld_dict):
    """Take a dataframe and return the country associated to the url in the column_name column

        Keyword arguments:
        df -- The dataframe
        column_name -- The name of the column containing the urls
        website_dict -- A dictionary url -> Country
        tld_dict -- A dictionary top level domain -> Country
    """

    def get_country_from_url(url):
        """ Return the country corresponding to an url

            Keyword arguments:
            url -- The url
        """

        url_pair = re.findall(r'\b(?!www\.)([a-zA-Z0-9-]+(\.[a-z]+)+)', url)

        if(url_pair == []): #If it is not a url
            return 'NOWEBSITE'
        else:
            url_pair = url_pair[0]

        #Try 1: website matching
        country = website_dict.get(url_pair[0], "NOENTRY")

        #Try 2: Top level domain matching
        if country == 'NOENTRY':
            country = tld_dict.get(url_pair[1], "NOENTRY")

        return country

    return df[column_name].apply(lambda x: get_country_from_url(x))
