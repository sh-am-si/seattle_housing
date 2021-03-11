import csv
import pandas as pd
import numpy as np
import datetime
import functools

import os
import os.path

import urllib.request

__all__ = ['PrepareData', 'get_equal_samples']


def get_equal_samples(X, column, mult_coef=1):
    
    """
    Creates equal samples according to (categorical, hopefully) values of X[column]
    TODO: should be fetched to np.ndarray
    TODO: redo it as an generator that will remember used indices and yield new ones
    """

    assert isinstance(X, pd.DataFrame)
    assert column in X.columns

    unique_items = X[column].unique()

    assert len(unique_items) > 1

    indices = [X[X[column] == item].index for item in unique_items] # can be simplified using parameters of the unique function
    indices.sort(key=lambda x: len(x))

    res = [np.array(indices[0])] + [np.random.choice(indices[i], min(mult_coef * len(indices[0]), len(indices[i])), replace=False) for i in range(1, len(indices)) ]
    res = functools.reduce(lambda x, y: np.concatenate((x, y)), res)
    res.sort()
    return X.iloc[res, :]

def get_criminal_activity_file(filename='data/seattle_criminal_history.csv'):
    """
    if the csv-file of criminal activities doesn't exist, it creates it
    this function doesn't varify its compliteness, however as it should be used only once there is no special need for it
    """
    path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(path):
        url = 'https://data.seattle.gov/api/views/tazs-3rd5/rows.csv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B'
        urllib.request.urlretrieve(url , filename)
    else:
        print(f'file {filename} exists')

def haversine_np(lon1, lat1, lon2, lat2):
    """
    https://stackoverflow.com/questions/29545704/fast-haversine-approximation-python-pandas/29546836#29546836

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def get_km_to_degree(dist=0.3):
    """
    the dullest way of getting spherical degrees from distance 
    df - seattle housing db 
    seattle_lat, seattle_long = df['lat'].mean(), df['long'].mean() - center of our data
    """

    dist_lat, dist_long = 0, 0

    seattle_lat, seattle_long = 47.56005251931708, -122.21389640494147

    while haversine_np(lon1=-122.21389640494147,
                       lat1=47.56005251931708,
                       lon2=-122.21389640494147,
                       lat2=47.56005251931708 + dist_lat) < dist:
        dist_lat += 0.0001
    
    while haversine_np(lon1=-122.21389640494147,
                       lat1=47.56005251931708,
                       lon2=-122.21389640494147 + dist_long,
                       lat2=47.56005251931708) < dist:
        dist_long += 0.0001

    return dist_lat, dist_long


def extend_df_by_criminal_activities(df, dist_lat, dist_long):

    assert 'lat' in df.columns
    assert 'long' in df.columns

    cdf = pd.read_csv('data/seattle_criminal_history.csv', sep=';', header = 0)
    cdf = cdf[cdf['Crime Against Category'].isin(['SOCIETY','PROPERTY', 'PERSON'])]
    cdf['Report DateTime'] = pd.to_datetime(cdf['Report DateTime'])
    cdf = cdf[cdf['Report DateTime'] < df['date'].max()]

    if 'criminal_activities' not in df.columns:
        df['criminal_activities'] = df.apply(lambda row: cdf[
            (row['long'] - dist_long < cdf['Longitude']) &
            (cdf['Longitude'] < row['long'] + dist_long) &
            (row['lat'] - dist_lat < cdf['Latitude']) &
            (cdf['Latitude'] < row['lat'] + dist_lat)].shape[0], axis=1)

        df.to_csv('data/house_ext.csv', index=False)
    else:
        print('column \'Crime Against Category\' already exists')
    

class PrepareData:

    def __init__(self):
        print('PrepareData constructor')
        filename1 = 'data/house_ext.csv'
        filename2 = 'data/house.csv'
        
        if os.path.isfile(os.path.join(os.getcwd(), filename1)):
            self.df = pd.read_csv(os.path.join(os.getcwd(), filename1),  header=0)
            print(f'DataFrame created from {filename1}')
        elif os.path.isfile(os.path.join(os.getcwd(), filename2)): 
            self.df = pd.read_csv(os.path.join(os.getcwd(), filename2),  header=0)
            print(f'DataFrame created from {filename2}')
        else:
            self.df = None
            print(f'files {filename2} and {filename1} don\'t exist')
        

if __name__ == '__main__':

    # get_criminal_activity_file()

    # data = PrepareData()
    # df = data.df

    # print(df.info())
    # print(df.describe())

    # extend_df_by_criminal_activities(df, *get_km_to_degree(dist=0.3))

    N = 321234
    df = pd.DataFrame({
        'a' : np.random.choice(list('qwerty'), N, replace=True),
        'b' : np.random.choice([0, 1], N, replace=True, p=[0.89, 0.11]),
    })
    print(df['b'].value_counts())
    Y = get_equal_samples(X=df, column='b', mult_coef=1)

    print(Y['b'].value_counts())
    print(Y['a'].value_counts())



        

