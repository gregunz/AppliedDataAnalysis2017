import datetime

import pandas as pd

from clean_data import clean_df, default_columns
from fetch_gdelt_data import fetch_df

min_year = 2015
max_year = 2017


def get_cleaned_month(month, year, country="none"):
    """ This function fetch the data of a whole month, clean them and return them as a dataframe

        Keyword arguments:
        month -- The desired month
        year -- The desired year
        country -- (Optional) Fetch only the data of a specific country
    """
    assert (year >= min_year & year < max_year), "Year not in range"
    assert (month >= 0 & month <= 12), "Month not in range"
    start = datetime.date(year, month, 1)
    end = datetime.date(year + (month // 12), (month + 1) % 12, 1)

    df = fetch_df(start, end, translingual=True)
    clean = clean_df(df)
    if (country != "none"):
        return clean[clean["Country_Source"] == country]
    else:
        return clean


def get_cleaned_year(year, country="none"):
    """ This function fetch the data of a whole year, clean them and return them as a dataframe

        Keyword arguments:
        year -- The desired year
        country -- (Optional) Fetch only the data of a specific country
    """
    assert (year >= min_year & year < max_year), "Year not in range"
    start = datetime.date(year, 1, 1)
    end = datetime.date(year + 1, 1, 1)
    df = fetch_df(start, end, translingual=True)
    clean = clean_df(df)

    if (country != "none"):
        return clean[clean["Country_Source"] == country]
    else:
        return clean


def get_cleaned_country(country):
    """ This function fetch all the data of a country, clean them and return them as a dataframe

        Keyword arguments:
        country -- The desired country
    """
    df = pd.DataFrame(columns=default_columns)
    for y in range(min_year, max_year + 1):
        df = df.append(get_cleaned_year(y, country))


def get_cleaned_separate_month(start_month, start_year, end_month, end_year, country="none"):
    """ This function fetch the data of a period, clean them and return them as a dataframe where the month of each news is specified

        Keyword arguments:
        start_month -- The starting month
        start_year -- The starting year
        end_month -- The ending month (including)
        end_year -- The ending year (including)
        country -- (Optional) Fetch only the data of a specific country
    """
    df = pd.DataFrame(columns=default_columns + ['Month'])

    for y in range(start_year, end_year + 1):
        if y == end_year:
            end_m = end_month
        else:
            end_m = 12

        for m in range(start_month, end_month + 1):
            df_m = get_cleaned_month(m, y, country)
            df_m['Month'] = m
            df = df.append(df_m)
