# -*- coding: utf-8 -*-
from socket import getaddrinfo
import requests
import json
import re
from shapely.geometry import shape, Point
import pandas as pd

def get_country_from_point(lat, long, js):
    # construct point based on lon/lat returned by geocoder
    point = Point(long, lat)

    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['id']
    return 'None'


def create_mapping(dataframe):

    world_geo_path = '../data/locations/countries.geo.json'
    world_json_data = json.load(open(world_geo_path, encoding="UTF-8"))

    positions = dataframe[['ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long']].groupby(['ActionGeo_Lat', 'ActionGeo_Long']).agg(lambda x: x.mode()).reset_index()
    positions["Lat_Long"] = positions['ActionGeo_Lat'].map(float).map('{:,.2f}'.format).map(str) + ' , '+ positions['ActionGeo_Long'].map(float).map('{:,.2f}'.format).map(str)
    positions = positions.drop_duplicates(subset=['Lat_Long'], keep=False)
    positions['ActionGeo_CountryCode'] = positions['ActionGeo_CountryCode'].apply(lambda x: x[0] if not type(x) is str else x)
    positions['Country_Code'] = positions['Lat_Long'].apply(lambda x: get_country_from_point(float(x.split(',')[0]), float(x.split(',')[1]), world_json_data))
    positions = positions[positions['Country_Code'] != 'None']

    mapping = positions[['ActionGeo_CountryCode', 'Country_Code']].groupby('ActionGeo_CountryCode').agg(lambda x: x.mode()[0])

    mapping.to_csv('../data/country_code_name.csv')

    return mapping

def get_mapping(dataframe):
    try:
        return pd.read_csv('../data/country_code_name.csv')
    except:
        print("Generating the mapping...")
        return create_mapping(dataframe)

def get_location(url):
    url = re.findall('www(?:[a-zA-Z]|[0-9]|[.])+', url)[0]
    ipaddr = getaddrinfo(url, 80)
    geody = "ipinfo.io/" + ipaddr[0][-1][0] + "/geo"
    r = requests.get('http://www.'+geody)
    return r.json()


def add_entry(path, key, value):
    with open(path, 'r') as json_data:
        if json_data.read() != '':
            json_data.seek(0)
            data = json.load(json_data)
            json_data.close()
            if key in data:
                return
        else:
            data = {}
        data[key] = value
        json_data = open(path, 'w')
        json.dump(data, json_data)
        json_data.close()

def entry_exists(path, key):
    with open(path, 'r') as json_data:
        if json_data.read() != '':
            json_data.seek(0)
            data = json.load(json_data)
            json_data.close()
            if key in data:
                return True
            return False
        else:
            json_data.close()
            return False

#Get all the newspaper and their url for each country in the world in csv in the format: ['Country Name', "Newspaper Name', 'URL']
def get_all_newspapers_per_country():

    #Get country specific page and get all the newspapers
    def get_country_newspaper(country_name, url):
        df = pd.DataFrame(columns=columns)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        newspapers = soup.find_all('td', align='left')[1:]

        for n in newspapers:
            newspaper_name = n.find('strong').text
            #Get the newspaper specific page
            r = requests.get(base_url + n.find('a').get('href'))
            soup = BeautifulSoup(r.text, 'html.parser')
            n_url = soup.find_all('h1')
            newspaper_url = n_url[0].find('a').get('href') #Newspaper url

            news_df = pd.DataFrame([[country_name, newspaper_name, newspaper_url]], columns=columns)
            df = df.append(news_df)

        return df

    r = requests.get('https://www.thepaperboy.com/newspapers-by-country.cfm')
    soup = BeautifulSoup(r.text, 'html.parser')
    base_url = 'https://www.thepaperboy.com'
    country_links = soup.find_all('a', class_='mediumlink')

    columns = ['Country name', 'Newspaper Name', 'Newspaper Url']

    df = pd.DataFrame(columns=columns)

    for a in country_links:
        country_name = a.text.split(sep='(')[0]
        if country_name[0] == ' ' :
            country_name = country_name[1:]
        if country_name[-1] == ' ':
            country_name = country_name[:-1]

        print(country_name)
        #United states has a different structure
        if country_name != 'United States':
            df = df.append(get_country_newspaper(country_name, base_url + a.get('href')))
        else:
            r = requests.get('https://www.thepaperboy.com/united-states/newspapers/country.cfm')
            soup = BeautifulSoup(r.text, 'html.parser')

            us_states = soup.find_all('a', class_='mediumlink')
            for state in us_states:
                df = df.append(get_country_newspaper(country_name, base_url + state.get('href')))

    df.to_csv('countries_news.csv')
