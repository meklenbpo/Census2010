"""
An attempt at uniform augmentation algorythm.
"""

import pandas as pd


def _add_rayons(df: pd.DataFrame) -> pd.DataFrame:
    """Add a column with rayon information to an indicator.

    `ind` is an indicator DataFrame that has at least the following fields:
    - `muni`: str - textual description of municipality (same as gks.ru),
    - `d1`: numeric - actual values of indicator per municipality.
    Some indicators have additional `d{x}` columns - these are not allowed,
    the indicator must be "flattened", before it can be added rayon-level 
    values (because it is not clear which value column to take as rayon value).

    Assumptions:
    1. indicator has both rayon-level and municipality-level records (though,
       the function will work without the municipality-level (rayon-only ind.)
    2. rayon-level records are marked by certain strings (see flags dict.)
    """
    ind = df.copy()
    ind['rayon'] = ''
    ind['rayon_v'] = 0
    flags = ['муниципальный', 'Городские округа']
    for n in ind.index:
        curr_muni = ind.loc[n, 'muni']
        curr_value = ind.loc[n, 'd1']
        if any([flag in curr_muni for flag in flags]):
            ind.loc[n, 'rayon'] = curr_muni
            ind.loc[n, 'rayon_v'] = curr_value
        else:
            ind.loc[n, 'rayon'] = ind.loc[n-1, 'rayon']
            ind.loc[n, 'rayon_v'] = ind.loc[n-1, 'rayon_v']
    # Flatten "Городские округа"
    ind.loc[ind.rayon.str.contains('Городские округа'), 'rayon_v'] = ind.d1
    ind.loc[ind.rayon.str.contains('Городские округа'), 'rayon'] = ind.muni
    return ind


def update_indicator(src_ind: pd.DataFrame, 
                     helper_ind: pd.DataFrame) -> pd.DataFrame:
    """
    Increase detailisation of source indicator based on helper indicator.

    Assumptions:
    1. Both indicators are for the same oblast.
    2. The distribution of values between indicators is similar.
    """
    hlp_ray = _add_rayons(helper_ind)
    hlp_ray['ratio'] = hlp_ray.d1 / hlp_ray.rayon_v
    src_m = hlp_ray.merge(src_ind, how='left', left_on='rayon', 
                          right_on='muni', suffixes=('', '_src'))
    src_m.drop(['d1', 'rayon_v', 'muni_src'], axis=1, inplace=True)
    src_m['d1'] = round(src_m.ratio * src_m.d1_src, 1)
    src_m.drop(['d1_src', 'ratio', 'rayon'], axis=1, inplace=True)
    return src_m

def augment_file(src_filename: str, helper_filename: str,
                 target_filename: str) -> None:
    """Load indicator file and augment it on helper indicator file."""
    src_df = pd.read_csv(src_filename, sep=';')
    hlp_df = pd.read_csv(helper_filename, sep=';')
    aug_df = update_indicator(src_df, hlp_df)
    aug_df.to_csv(target_filename, sep=';', index=False)


def main():
    """Test script running function."""
    try:
        src_fn = 'output/csv/14_wages_govt.csv'
        hlp_fn = 'output/augm/14_augm_wages_muni.csv'
        src_df = pd.read_csv(src_fn, sep=';')
        hlp_df = pd.read_csv(hlp_fn, sep=';')
        wg14a = update_indicator(src_df, hlp_df)
    except:
        return 1
    return 0

if __name__ == '__main__':
    exit(main())
