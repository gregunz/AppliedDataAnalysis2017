# -*- coding: utf-8 -*-

import datetime
import io
import os
import zipfile

import pandas as pd
import requests

data_directory = "../data"
gdelt_directory = "{}/gdelt".format(data_directory)

"""
Construct a string of all quarters of hours in a day (e.g. '143000', '174500')
"""
all_quarters_per_day = [str(h * 100 + q * 15).zfill(4) + "00" for h in range(24) for q in range(4)]


def load_column_names(v='2'):
    """Load the column names for the gdelt data given a version

        Keyword arguments:
        v -- version of gdelt data ('1' or '2')
    """
    path = "{}/gdelt_column_names_v{}.csv".format(data_directory, v)
    return pd.read_csv(path, header=None).T.values.tolist()[0]


def get_filenames(date, translingual=False, v='2'):
    """Construct filenames (local or on the Gdelt server) of gdelt files for a given day

        Keyword arguments:
        date -- the given day
        translingual -- whether we want the translingual data or not
        v -- version of gdelt data ('1' or '2')
    """
    trans_ext = ""
    if translingual:
        trans_ext = ".translation"
    if v == '1':
        return ["{:%Y%m%d}{}.export.CSV".format(date, trans_ext)]
    if v == '2':
        return ["{:%Y%m%d}{}{}.export.CSV".format(date, q, trans_ext) for q in all_quarters_per_day]
    raise ValueError("Version {} does NOT exist".format(v))


def get_file_paths(date, translingual=False, v='2'):
    """Construct filepaths (local) of gdelt files for a given day

        Keyword arguments:
        date -- the given day
        translingual -- whether we want the translingual data or not
        v -- version of gdelt data ('1' or '2')
    """
    return ["{d}/{f}".format(d=gdelt_directory, f=f) for f in get_filenames(date, translingual=translingual, v=v)]


def create_df(path_or_buffer, v='2'):
    """Construct a dataframe given a path or a buffer to the Gdelt data

        Keyword arguments:
        path_or_buffer -- path or buffer for the dataframe data
        v -- version of gdelt data ('1' or '2')
    """
    column_names = load_column_names(v=v)
    return pd.read_csv(
        path_or_buffer, sep="\t", header=None, usecols=range(len(column_names)),
        names=column_names, index_col=0, dtype={'EventCode': 'object'}, encoding='utf-8'
    )


def load_df(date, translingual=False, v='2'):
    """Load a dataframe (locally) for a given day

        Keyword arguments:
        date -- the given day
        translingual -- whether we want the translingual data or not
        v -- version of gdelt data ('1' or '2')
    """
    return pd.concat(
        [create_df(path, v=v) for path in get_file_paths(date, translingual=translingual, v=v) if os.path.isfile(path)])


def download_df(date, translingual=False, should_save=True, v='2'):
    """Download a dataframe for a given day

        Keyword arguments:
        date -- the given day
        translingual -- whether we want the translingual data or not
        should_save -- whether we want to save the gdelt file locally
        v -- version of gdelt data ('1' or '2')
    """
    if v == '1':
        base_url = "http://data.gdeltproject.org/events/"
    elif v == '2':
        base_url = 'http://data.gdeltproject.org/gdeltv2/'
    else:
        raise ValueError("Version {} does NOT exist".format(v))

    filenames = get_filenames(date, translingual=translingual, v=v)
    dfs = []
    for filename in filenames:
        r = requests.get('{}{}.zip'.format(base_url, filename))
        if r.status_code != 200:
            print("File not found on server {} : {}.zip".format(base_url, filename))
        else:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            if should_save:
                z.extract(filename, gdelt_directory)
            dfs.append(create_df(z.open(filename), v=v))

    if len(dfs) == 0:
        return pd.DataFrame(columns=load_column_names(v=v))
    else:
        return pd.concat(dfs)


def fetch_df(from_date, to_date=None, translingual=False, should_save=True, v='2'):
    """Fetch a dataframe files for a given day or sequence of days.
       It will fetch locally first and download if not available.

        Keyword arguments:
        from_date -- the given day or the start of the sequence of days (inclusive)
        to_date -- the end of the sequence of days (exclusive)
        translingual -- whether we want the translingual data or not
        should_save -- whether we want to save the gdelt file locally (if downloaded)
        v -- version of gdelt data ('1' or '2')
    """
    if to_date != None:
        dfs = []
        for delta in range((to_date - from_date).days):
            date = from_date + datetime.timedelta(days=delta)
            df = fetch_df(date, to_date=None, translingual=translingual, should_save=should_save, v=v)
            dfs.append(df)
        return pd.concat(dfs)
    else:
        try:
            return load_df(from_date, translingual=translingual, v=v)
        except:
            print("downloading files...")
            return download_df(from_date, translingual=translingual, should_save=should_save, v=v)
