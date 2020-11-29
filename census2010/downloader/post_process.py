"""
Census 2010
===========

Parser
------

Parser sub-package provides tools to:
- read an HTML table downloaded from Russian Statistics website as a
pandas dataframe
- identify metadata for an HTML file (indicator-oblast pair)
- filter out irrelevant data
- save the filtered dataset as a pandas-compatible CSV/feather file
"""

import os

from bs4 import BeautifulSoup
import pandas as pd
from typing import List


def _format_html(filename: str) -> None:
    """
    Add formatting headers/footers to downloaded raw HTML.
    """
    header = (
        r"<html><head><meta charset='UTF-8'></head><style>"
        r"body {font-family: Arial, sans-serif;background-color: #eeeeee;}"
        r".bL0 {color: black; font-weight: bold;}"
        r".bL1 {color: gray; font-weight: normal; font-size: 8pt;}"
        r".bL2 {color: #006666; font-size: 10pt; padding-left: 20px;}"
        r"</style><table>"
    )
    footer = r"</table></html>"
    with open(filename, 'r') as source_html:
        html_str = source_html.read()
    with open(filename, 'w') as dest_html:
        dest_html.write(header + html_str + footer)

def _scan_dir(html_dir: str) -> List[str]:
    """
    Scan a directory with saved html tables and return their filenames
    as a list of strings.
    """
    f_l = os.listdir(html_dir)
    filenames = sorted([x for x in f_l if x.endswith('.html')])
    return filenames

def _get_num_of_data_points(html_fn: str) -> str:
    """
    Open a downloaded HTML file and determine from it's contents whether
    the data is on rayon or muni level or error in data.
    """
    with open(html_fn, 'r') as html_f:
        html_str = html_f.read()
    soup = BeautifulSoup(html_str, 'html.parser')
    data_cells = 0
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            try:
                float(cell.text.replace(',', '.'))
                data_cells += 1
                break
            except ValueError:
                pass
    return data_cells

def extract_metadata(directory: str) -> pd.DataFrame():
    """Parse filenames for metadata - region code, indicator_code."""
    directory = directory if directory.endswith('/') else directory + '/'
    file_list = _scan_dir(directory)
    meta = []
    ok2 = file_list[0][:2]
    print(ok2)
    for x in file_list:
        meta.append([x[:2], x[3:-5], _get_num_of_data_points(directory + x)])
        if x[:2] != ok2:
            ok2 = x[:2]
            print(ok2)
    cols = {"street_network": "str", "nat_ch_perc": "natch1",
            "nat_ch_total": "natch2",
            "gender_age_gr": "ag", "migration": "migr", "ethnicity": "ethn",
            "workers_by_occ": "workers", "wages_by_occ": "wages",
            "wages_govt": "wgovt", "ungasified": "ungas",
            "total_housing": "t_h", "deter_housing": "det_h",
            "subsidies": "subs", "doctors": "doct", "nurses": "nurs",
            "elderly": "eld", "kindergarten": "kindg", "schools": "schools",
            "schoolchildren": "sch_ch", "total_new_housing": "t_n_h",
            "indiv_new_housing": "ind_h", "ndfl": "ndfl", "households":"hh"}
    df = pd.DataFrame(meta, columns=['ok2', 'ind', 'data'])
    df_p = df.pivot(index='ok2', columns='ind', values='data')
    df_p.columns = pd.Series(df_p.columns).replace(cols)
    cols = list(df_p.columns)
    cols.remove('str')
    cols.insert(0, 'str')
    df_n = df_p[cols]
    df_n = df_n.fillna('-')
    return df_n

def format_folder(folder:str):
    """Format a folder of downloaded html tables to a viewable state."""
    htmls = _scan_dir(folder)
    for html in htmls:
        _format_html(f'{folder}/{html}'.replace('//','/'))

def _import_html(filename: str) -> pd.DataFrame:
    """Read a downloaded (& formatted) HTML table into a DataFrame."""
    with open(filename, 'r') as html_file:
        html_str = html_file.read()
    soup = BeautifulSoup(html_str, features='lxml')
    rows = soup.find_all('tr')
    cells = [[x.text for x in row.find_all('td')] for row in rows]
    classes = [row.find('td')['class'][0] for row in rows]
    data = [x[1] for x in zip(classes, cells) if x[0]=='TblBok']
    cols = [f'd{x}' if x!=0 else 'muni'
            for x in range(max([len(x) for x in data]))]
    df = pd.DataFrame(data, columns=cols).fillna('')
    df.index = df.muni
    df.drop('muni', axis=1, inplace=True)
    return df

def _delete_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Find and delete rows where all data columns are empty in a 
       DataFrame in an imported format."""
    cols = list(df.columns)
    return df.loc[df[cols].sum(axis=1) != '']

def _df_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Convert value columns to numeric."""
    replacements = {'': '0', ' ': '0', '\xa0': '0', '-': '0'}
    df_num = df.copy().replace(replacements)
    df_num.replace(',', '.', regex=True, inplace=True)
    cols = list(df_num.columns)
    df_num[cols] = df_num[cols].apply(pd.to_numeric)
    return df_num

def html_to_csv(in_filename: str, out_filename: str):
    """Import an html table, clean it up and save as a csv."""
    df = _import_html(in_filename)
    dfr = _delete_empty_rows(df)
    dfn = _df_to_numeric(dfr)
    dfn.to_csv(out_filename, sep=';')

def html_folder_to_csv_folder(html_folder: str, csv_folder: str):
    """Load every html table from a folder, save it as csv to another
    folder."""
    l = os.listdir(html_folder)
    html = sorted([x for x in l if x.endswith('.html')])
    try:
        os.makedirs(csv_folder)
    except FileExistsError:
        pass
    for html_fn in html:
        print(html_fn)
        csv_fn = csv_folder + '/' + html_fn.split('.')[0] + '.csv'
        html_to_csv(f'{html_folder}/{html_fn}', csv_fn)





