# -*- coding: utf-8 -*-
from socket import getaddrinfo
import requests
import json
import re
import os
import csv
import pandas as pd
from bs4 import BeautifulSoup
        
def get_all_newspapers_to_country_dict(v2=True):
    """Get the country associated to each newspapers url in a dict following the format: {'Clean URL' : 'Country name'}
        This function is not sufficient on its own to get the country of every newspaper, please see get_countries_for_dataframe in data_cleaning.py
    """
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
    
    
    if v2:
        columns = ['Country name', 'Newspaper Name', 'Newspaper Url']
        df = pd.DataFrame(columns=columns) 
        if not os.path.isfile('../data/locations/clean_url_to_country_v2.csv'):
            if not os.path.isfile('../data/locations/brute_newspapers_to_country_v2.csv'):
                base_url = 'http://www.abyznewslinks.com/'

                def get_newspapers(url, country_name):

                    df = pd.DataFrame(columns=columns)

                    r = requests.get(url)

                    #Find newspaper links
                    soup = BeautifulSoup(r.text, 'html.parser')
                    divs = soup.find_all('div')[3:]
                    for div in divs:
                        news_links = div.find_all('a')
                        for a_news in news_links:
                            a_news_link = a_news.get('href')
                            if a_news_link is not None:
                                #Check whether it links to a page of the website with more newspapers instead of a newspaper webstes
                                if a_news_link[-3:] == 'htm' and a_news_link[:3] != 'htt' and a_news_link[:3] != 'www':
                                    df = df.append(get_newspapers(base_url + a_news.get('href'), country_name))
                                else:
                                    newspaper_name = a_news.text
                                    newspaper_url = a_news.get('href')
                                    news_df = pd.DataFrame([[country_name, newspaper_name, newspaper_url]], columns=columns)
                                    df = df.append(news_df)

                    return df

                r = requests.get(base_url + 'allco.htm')
                soup = BeautifulSoup(r.text, 'html.parser')
                countries = soup.find_all('table')[5].find_all('a')

                for a in countries:
                    #Get specific page
                    country_name = a.text

                    df = df.append(get_newspapers(base_url + a.get('href'), country_name))

                df.to_csv('../data/locations/brute_newspapers_to_country_v2.csv', index=False)
                df = df.drop_duplicates(subset=['Newspaper Url'], keep='first')
                df.to_csv('../data/locations/no_duplicate_brute_newspapers_to_country_v2.csv', index=False)
            else:
                if not os.path.isfile('../data_locations/no_duplicate_brute_newspapers_to_country_v2.csv'):
                    print('hi2')
                    df = pd.read_csv('../data/locations/brute_newspapers_to_country_v2.csv')
                    df = df.drop_duplicates(subset=['Newspaper Url'], keep='first')
                    df.to_csv('../data/locations/no_duplicate_brute_newspapers_to_country_v2.csv', index=False)
                else:
                    df = pd.read_csv('../data_locations/no_duplicate_brute_newspapers_to_country_v2.csv')
            
               
            df['Clean URL'] = df['Newspaper Url'].apply(lambda x: clean_url(x))
            df.to_csv('../data/locations/clean_url_to_country_v2.csv', index=False)
        else:
            df = pd.read_csv('../data/locations/clean_url_to_country_v2.csv')

        return df[["Clean URL", "Country name"]].set_index("Clean URL").to_dict().get("Country name")
        
    else:
        #If the file does not exist, fetch everything (takes ~ 16 hours)
        if not os.path.isfile('../data/locations/clean_url_to_country.csv'):

            #First get newspaper per country as referenced in https://www.thepaperboy.com/newspapers-by-country.cfm
            if not os.path.isfile('../data/locations/countries_news.csv'):
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

                    #United states has a different structure
                    if country_name != 'United States':
                        df = df.append(get_country_newspaper(country_name, base_url + a.get('href')))
                    else:
                        r = requests.get('https://www.thepaperboy.com/united-states/newspapers/country.cfm')
                        soup = BeautifulSoup(r.text, 'html.parser')

                        us_states = soup.find_all('a', class_='mediumlink')
                        for state in us_states:
                            df = df.append(get_country_newspaper(country_name, base_url + state.get('href')))

                df.to_csv('../data/locations/countries_news.csv')
                original_websites_df = df
            else:
                original_websites_df = pd.read_csv('../data/locations/countries_news.csv')

            def get_new_url(base_url):
                """ This function try to get a redirection url and return it otherwise return the base url
                """
                try:
                    response = requests.get(base_url, timeout=5)
                    if response.history:
                        return response.url
                    else:
                        return base_url
                except:
                    return base_url

            #As the website is not up to date, we get the new address of the newspapers which changed their address over time (But keep both for older news!). Basically we follow the previous link and get if there is a redirection
            if not os.path.isfile('../data/locations/revisited_website_url.csv'):
                for _ , row in original_websites_df.iterrows():
                    new_url = get_new_url(row['Newspaper Url'])
                    df = pd.DataFrame({'Country name' : [row['Country name']], 'New URL' : [new_url]})
                    with open('../data/locations/revisited_website_url.csv', 'a') as f:
                        df.to_csv(f, header=False)

            redirected_websites_df = pd.read_csv('../data/locations/revisited_website_url.csv', names=['Country name', 'New URL'])

            original_websites_df['Clean URL'] = original_websites_df['Newspaper Url'].apply(lambda x: clean_url(x))
            original_websites_df.to_csv('../data/locations/original_clean_url_to_country.csv', index=False)

            redirected_websites_df['Clean URL'] = redirected_websites_df['New URL'].apply(lambda x: clean_url(x))
            redirected_websites_df.to_csv('../data/locations/redirected_clean_url_to_country.csv', index=False)

            websites_df = original_websites_df[["Clean URL", "Country name"]].append(redirected_websites_df[["Clean URL", "Country name"]])
            websites_df.to_csv('../data/locations/clean_url_to_country.csv', index=False)

            return websites_df[["Clean URL", "Country name"]].set_index("Clean URL").to_dict().get("Country name")

        else:
            return pd.read_csv('../data/locations/clean_url_to_country.csv')[["Clean URL", "Country name"]].set_index("Clean URL").to_dict().get("Country name")




def get_tld_to_country_dict():
    """Get the country associated to a top level domain in the formt: {'TLD' : 'Country name'}
        This function is not sufficient on its own to get the country of every newspaper, please see get_countries_for_dataframe in data_cleaning.py
    """
    if not os.path.isfile('../data/locations/top_level_domain_to_country.csv'):
        r = requests.get('https://raw.githubusercontent.com/mledoze/countries/master/countries.json')

        #Get the mapping
        countries = [(c['name']['common'], c['tld']) for c in r.json()]
        tld_to_country = {}

        for c in countries:
            for domain in c[1]:
                if not domain in tld_to_country:
                    tld_to_country[domain] = c[0]
                    
        tld_to_country['.us'] = 'United States' #hardcoded otherwise it's not the good value

        with open('../data/locations/top_level_domain_to_country.csv', 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['tld', 'Country name'])
            for key, value in tld_to_country.items():
                writer.writerow([key, value])

    return pd.read_csv('../data/locations/top_level_domain_to_country.csv').set_index('tld').to_dict().get('Country name')