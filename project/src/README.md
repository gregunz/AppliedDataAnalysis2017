## Data Pipeline
This pipeline sums up all the data processing done before visualition. This includes data **acquisition**, data **cleaning** and data **augmentation**.
![data_pipeline_img]

1. We download the data from the [Gdelt website][gdelt_download_link]. There are a file every 15 minutes (96 per day). Some powerful functions in [fetch_gdelt_data.py] makes the download easy. By providing a date (or range of dates) we can automatically download every files and save them.
2. We load all the files into a single dataframes, this is directly done in [fetch_gdelt_data.py] after the download. (Note: if a file is already downloaded, it will load it automatically from storage)
3. In our project we only need a few columns, hence we keep only the ones we need for our project ('EventCode', 'SOURCEURL', 'ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long', 'IsRootEvent', 'QuadClass', 'GoldsteinScale', 'AvgTone', 'NumMentions', 'NumSources', 'NumArticles', 'ActionGeo_Type', 'Day'), please refer to the [Gdelt Codebook][gdelt_event_codebook] for the details about each field. This is done in the [clean_data.py] file.
4. When some values are missing or invalid (e.g. not geographic position), we remove the row (done in the [clean_data.py] file as well).
5. 'ActionGeo_CountryCode' do NOT use the ISO 3166-1 country codes. Hence, to be more consistent we find the correct country using the latitude and longitude and construct a mapping of their country codes to the ISO ones. This is done in [fetch_locations.py].
6. For each event we have a source URL of the article from which the event comes from. Unfortunately we don't have the country from which the article comes from. For this reason use this [database][paperboy] and make use of the top level domain (tld) names which represent a country to determine it. All this is done in [fetch_source_country.py]


Summary of what each file does :

### [Milestone_02.ipynb] -- (jupyter notebook)
- Show our progress up to the Milestone_02

### [clean_data.py] -- (python code functions)
- Filter data we don't use
- Clean the Gdelt data

### [download_all_gdelt_data.ipynb] -- (jupyter notebook)
- Download all the Gdelt Events (2.0) data (200k files = 100GB uncompressed)

### [fetch_gdelt_data.py] -- (python code functions)
- Download/Save/Load Gdelt data given dates

### [fetch_location.py] -- (python code functions)
- Find all Actions country in a dataframe using longitude and latitute

### [fetch_source_country.py] -- (python code functions)
- Find the country of the sources (newspapers/websites) 


[data_pipeline_img]: https://raw.githubusercontent.com/gregunz/ada2017/master/project/data/images/data_pipeline.png "data pipeline"
[gdelt_download_link]: http://data.gdeltproject.org/gdeltv2/masterfilelist.txt
[gdelt_event_codebook]: https://github.com/gregunz/ada2017/blob/master/project/data/pdf/GDELT-Event_Codebook-V2.0.pdf
[paperboy]: https://www.thepaperboy.com/newspapers-by-country.cfm

[Milestone_02.ipynb]: https://github.com/gregunz/ada2017/blob/master/project/src/Milestone_02.ipynb
[clean_data.py]: https://github.com/gregunz/ada2017/blob/master/project/src/clean_data.py
[download_all_gdelt_data.ipynb]: https://github.com/gregunz/ada2017/blob/master/project/src/download_all_gdelt_data.ipynb
[fetch_gdelt_data.py]: https://github.com/gregunz/ada2017/blob/master/project/src/fetch_gdelt_data.py
[fetch_location.py]: https://github.com/gregunz/ada2017/blob/master/project/src/fetch_location.py
[fetch_source_country.py]: https://github.com/gregunz/ada2017/blob/master/project/src/fetch_source_country.py
[clean_data.py]: https://github.com/gregunz/ada2017/blob/master/project/src/clean_data.py
