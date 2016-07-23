#!/usr/bin/env python
#coding: utf-8

import pandas as pd
import sys

def write_missing_states(fname):
    sep = ';'
    df = pd.read_csv(fname, sep=sep)

    df = df[pd.isnull(df['steps'])]
    df = df['state']

    df.to_csv(fname+'_missing.txt', sep=sep, index=False)

def replace_with_nan(fname, threshold=1e6):
    sep = ';'
    df = pd.read_csv(fname, sep=sep)

    column_name = df.filter(regex='nodes').columns[0]
    df.loc[df[column_name] > threshold, df.columns[1:]] = 'NaN'
    df.to_csv(fname, sep=sep, index=False)


if __name__ == '__main__':
    fname = sys.argv[2]
    if sys.argv[1] == 'write':
        write_missing_states(fname)
    elif sys.argv[1] == 'replace':
        replace_with_nan(fname)

