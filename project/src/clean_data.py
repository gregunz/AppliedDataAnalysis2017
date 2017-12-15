import re
import pandas as pd
import datetime
import unidecode

from fetch_gdelt_data import *
from fetch_location import get_mapping
from fetch_source_country import get_tld_to_country_dict, get_all_newspapers_to_country_dict
from tqdm import tqdm_notebook as tqdm
from pycountry_convert import country_name_to_country_alpha3

default_columns = ['EventCode', 'SOURCEURL', 'ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long',
                   'IsRootEvent', 'QuadClass', 'GoldsteinScale', 'AvgTone',
                   'NumMentions', 'NumSources', 'NumArticles', 'ActionGeo_Type', 'Day']


cleaned_columns = ['EventCode', 'ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long',
                    'IsRootEvent', 'QuadClass', 'GoldsteinScale', 'AvgTone',
                    'NumMentions', 'NumSources', 'NumArticles', 'ActionGeo_Type',
                    'Day','Country_Code', 'Country_Source', 'Country_Name']


def country_to_cca3(c, dict_):
    """ This function convert a country name to its ISO 3166-1 alpha-3 code

         Keyword arguments:
         c -- The country name to convert
         dict -- The dicitonnary create by the function get_dict_countries_to_cca3() also stored in dict_countries_to_cca3
    """
    countries_to_discard = [
        'Near and Middle East Regional',
        'Caribbean Regional',
        'Asia Regional',
        'International',
        'Europe Regional',
        'Central Africa Republic',
        'Africa Regional',
        'Americas Regional',
        'Central America Regional',
        'United Nations',
        'Latin America',
        'NOWEBSITE',
        'NOENTRY',
    ]

    c = c.strip()
    if c in countries_to_discard:
        return 'DISCARDED'
    try:
        c = dict_[c]
    except KeyError:
        try:
            c = country_name_to_country_alpha3(c)
        except KeyError as e:
            no_accent = unidecode.unidecode(c)
            if c == no_accent:
                raise e
            else:
                return country_to_cca3(no_accent, dict_)
    return c


def get_dict_countries_to_cca3():
    """ This function return a dict: a country name to its ISO 3166-1 alpha-3 code
    """

    r = requests.get('https://raw.githubusercontent.com/mledoze/countries/master/countries.json')

    dict_ = dict([(c['name']['common'], c['cca3']) for c in r.json()])

    mismatches = [
        ('Holy See', 'Vatican City'),
        ('Wallis and Futuna Islands', 'Wallis and Futuna'),
        ('Reunion', 'Réunion'),
        ('Congo Kinshasa', 'Congo'),
        ('Timor Leste', 'Timor-Leste'),
        ('Congo Brazzaville', 'Congo'),
        ('Dutch Caribbean', 'Netherlands'),
        ('Cote d\'Ivoire', 'Côte d\'Ivoire'),
        ('Curacao', 'Curaçao'),
        ('Svalbard and Jan Mayen Islands', 'Norway'),
        ('Faeroe Islands', 'Faroe Islands'),
        ('Guinea Bissau', 'Guinea-Bissau')
    ]

    for new_c, to_c in mismatches:
        dict_[new_c] = country_to_cca3(to_c, dict_)

    return dict_
    

dict_countries_to_cca3 = get_dict_countries_to_cca3()



def clean_df(df, selected_columns=default_columns):
    """Take a dataframe with GDELT2.0 data and only retain the useful columns for us and also add the country where the news was written

        Keyword arguments:
        df -- The dataframe complying to GDELT2.0 columns format
        selected_columns (optionnal) -- The set of columns we want to keep
    """
    df = df[selected_columns]
    df = df.dropna(axis=0, how='any')
    mapping = get_mapping(df).set_index('ActionGeo_CountryCode')
    df['Country_Code'] = df['ActionGeo_CountryCode'].apply(
        lambda x: mapping.loc[x]['Country_Code'] if x in mapping['Country_Code'].index.values else 'None')

    df['Country_Source'] = get_countries_for_dataframe(df, 'SOURCEURL', get_all_newspapers_to_country_dict(),
                                                       get_tld_to_country_dict())

    r = requests.get('https://raw.githubusercontent.com/mledoze/countries/master/countries.json')
    d = {}
    for c in r.json():
        d[c['cca3']] = c['name']['common']

    df['Country_Name'] = df['Country_Code'].apply(lambda x: d[x] if x in d else 'None')

    return df[cleaned_columns]


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

        if len(url_pair) == 0:  # If it is not a url
            return 'NOWEBSITE'
        else:
            url_pair = url_pair[0]

        # Try 1: website matching
        country = website_dict.get(url_pair[0], "NOENTRY")

        # Try 2: Top level domain matching
        if country == 'NOENTRY':
            country = tld_dict.get(url_pair[1], "NOENTRY")

        return country

    return df[column_name].apply(lambda x: get_country_from_url(x))
