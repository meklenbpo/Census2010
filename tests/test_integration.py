"""
Integration test suite for Census 2010 project.
"""

import census2010


def test_integrate():
    """Test that running the whole of the process actually works."""
    # census2010.download_all('../data/html/')
    census2010.parse_all('../data/html/', '../data/parsed/')
    census2010.parse_census('../data/official_2010_Census_pop.xlsx', '../data/parsed/')
    census2010.calculate_households('../data/muni2010.gpkg', 'OKTMO',
                                    '../data/hhrasters/', '../data/parsed/')
    census2010.calculate_wages('../data/parsed/workers_by_occ.csv',
                               '../data/parsed/wages_by_occ.csv',
                               '../data/parsed/')
    census2010.merge('../data/parsed/', '../data/merged/merged.csv')
    census2010.geocode('../data/merged/merged.csv',
                       '../data/geocoded/geocoded.csv')
    census2010.format_to_excel('../data/geocoded/geocoded.csv',
                               '../data/ready/Census2010.xlsx')
    # if the whole of the process didn't raise any exceptions, it passes
    assert True
