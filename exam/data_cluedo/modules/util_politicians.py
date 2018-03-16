import ipywidgets as widgets
from IPython.display import display

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import ttest_ind


def evaluate(df, party, politicians, economy, outliers, part):
    print(politicians.value)
    print(economy.value)
    print(outliers.value)
    if outliers.value=="Exclude":
        df = df[(np.abs(stats.zscore(df)) < 2.5).all(axis=1)]
    pol_column = politicians.value
    econ_column = economy.value
    df.plot.scatter(x=pol_column,y=econ_column)
    plt.show()
    corr, p_val = stats.pearsonr(df[pol_column], df[econ_column])
    print('Correlation', corr, 'P-value', p_val)
    if corr < 0:
        print('Part', part, ':', party, 'have a negative impact on the economy!')
    else:
        print('Part', part, ':', party, 'have a positive impact on the economy!')
    if p_val < 0.05:
        print('By achieving a p-value of less than 0.05, your result is publishable!')
    else:
        print('Try again to see if you can find a lower p-value.')
    return p_val, corr


def toggle_display(party='Democrats'):
    style = {'description_width': 'initial'}

    if party == 'Democrats':
        print('Analyzing Party: Democrats')
        politicians = widgets.ToggleButtons(
            options=['Dem_Presidents', 'Dem_Governors'],
            description='Choose politicians to include:', style=style,
            disabled=False,
            button_style='',
        )
        display(politicians)
    else:
        print('Analyzing Party: Republicans')
        politicians = widgets.ToggleButtons(
            options=['Rep_Presidents', 'Rep_Governors'],
            description='Politicians to include:', style=style,
            disabled=False,
            button_style='', 
        )
        display(politicians)

    economy = widgets.ToggleButtons(
        options=['GDP', 'Employment'],
        description='Measure of economic performance:', style=style,
        disabled=False,
        button_style='', 
    )
    display(economy)
    
    outliers = widgets.ToggleButtons(
        options=['Include', 'Exclude'],
        description='Include or exclude outliers:', style=style,
        disabled=False,
        button_style='', 
    )
    display(outliers)
    
    return politicians, economy, outliers
