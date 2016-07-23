#!/usr/bin/env python
#coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def plot(fname, columns_type='time', index='steps'):
    #matplotlib.style.use('fivethirtyeight')
    #[u'dark_background', u'bmh', u'grayscale', u'ggplot', u'fivethirtyeight']
    #pd.options.display.mpl_style = 'default'
    df = pd.read_csv(fname, sep=';')
    grp = df.groupby(index)
    #mean = grp.mean()
    data = grp.mean().filter(regex=columns_type)
    #data = mean.loc[:, columns]
    #data = mean.filter(columns_type)
    #norm_data = (data - data.mean()) / data.std()
    #norm_data.plot(kind='bar')
    data.plot(kind='bar')
    matplotlib.pyplot.show()

def fuse(fname='a_'):
    sep = ';'
    extension='.csv'
    h_names = ['h1', 'h2', 'h3', 'h4', 'h5']
    types = 'time|nodes'
    dfs = []
    for h in h_names:
        dfs.append(pd.read_csv(fname+h+extension, sep=sep))

    # add to dfT the state and steps columns from the h_5 datafile
    dfT = dfs[-1][['state', 'steps']]
    for df in dfs:
        dfT[df.filter(regex=types).columns] = df.filter(regex=types)
    dfT.to_csv(fname+'star.csv', sep=sep, index=False)

if __name__ == '__main__':
    folder = 'data'

    subfolders = ['a', 'a_tree', 'ida']
    #subfolders = ['ida']

    for sf in subfolders:
        fuse(folder + '/' + sf + '/' + sf + '_')

    fnames = ['a_star.csv', 'a_tree_star.csv', 'ida_star.csv']
    #fnames = ['ida_star.csv']

    types = ['time', 'nodes']
    for sf, name in zip(subfolders, fnames):
        for tp in types:
            plot(folder + '/' + sf + '/' + name, tp)

