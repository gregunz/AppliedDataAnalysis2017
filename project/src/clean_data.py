import re

from fetch_gdelt_data import *
from fetch_location import get_mapping
from fetch_source_country import get_tld_to_country_dict, get_all_newspapers_to_country_dict

default_columns = ['EventCode', 'SOURCEURL', 'ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long',
                   'IsRootEvent', 'QuadClass', 'GoldsteinScale', 'AvgTone',
                   'NumMentions', 'NumSources', 'NumArticles', 'ActionGeo_Type',
cleaned_columns = default_columns + ['Country_Code', 'Country_Source', 'Country_Name'] 'Day']


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

    return df


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

        if (url_pair == []):  # If it is not a url
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
