import datetime
import os

import pandas as pd
from tqdm import tqdm

from clean_data import cleaned_columns, country_to_cca3, dict_countries_to_cca3
from high_level_fetch import get_cleaned_month

final_column_names = ['Day', 'EventCode', 'Source_CountryCode', 'Target_CountryCode',
                      'Target_Lat', 'Target_Long', 'Target_GeoType', 'IsRootEvent',
                      'QuadClass', 'GoldsteinScale', 'AvgTone', 'NumMentions',
                      'NumSources', 'NumArticles']


def load_data():
    """This function loads all the data cleaned from 03/01/201 to 12/12/2017.
        In most cases, only this function should be called
    """
    if not os.path.isfile('../data/final_data.csv'):
        # fetching
        print(
            "If you see this and you are not expecting to download and clean all the data, please verify you have the file final_data.csv in the folder data")

        print("Fetching and cleaning GDELT 2.0 Translingual data...")
        start_date = datetime.datetime(2015, 3, 1)
        end_date = datetime.datetime(2017, 12, 1)

        n_months = (end_date - start_date).days * 12 // 365

        df = pd.DataFrame(columns=cleaned_columns)

        for i in tqdm(range(n_months)):
            index = start_date.month - 1 + i

            from_month = index % 12 + 1
            from_year = start_date.year + index // 12

            df = df.append(get_cleaned_month(from_month, from_year))

        print("End fetching")
        print("Finalising cleaning...")
        # Country cleaning

        df.columns = ['EventCode', 'Target_CountryCode_2', 'Target_Lat', 'Target_Long',
                      'IsRootEvent', 'QuadClass', 'GoldsteinScale', 'AvgTone',
                      'NumMentions', 'NumSources', 'NumArticles', 'Target_GeoType',
                      'Day', 'Target_CountryCode', 'Source_CountryName', 'Target_CountryName']

        df['Source_CountryCode'] = df['Source_CountryName'].apply(lambda x: country_to_cca3(x, dict_countries_to_cca3))

        discard_mask = df['Source_CountryCode'] != 'DISCARDED'

        df = df[discard_mask]
        df = df[final_column_names]

        print("End cleaning")
        print("Writing...")

        with open('../data/final_data.csv', 'w', encoding='utf-8') as f:
            df.to_csv(f, encoding='utf-8')
        print("End load")
        return df
    else:
        print("Reading data from file...")
        return pd.read_csv("../data/final_data.csv")
