"""
Experiment to find data files that have more than one data series.
"""

import os
import pandas as pd

path = '../output/csv/'

l = [x for x in sorted(os.listdir(path)) if x.endswith('.csv')]

multiseries = []

for file in l:
    df = pd.read_csv(f'{path}-{file}', sep=';')
    if len(df.columns) > 2:
        multiseries.append(file)
        print(file)
x = 12, 12



