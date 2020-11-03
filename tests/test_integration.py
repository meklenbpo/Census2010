"""
Integration test suite for Census 2010 project.
"""

import census2010


def test_integrate():
    """Test that running the whole of the process actually works."""
    html_01_wages = census2010.download('01', 'wages')
    html_99_wages = census2010.download('99', 'wages')
    html_99_total_female_pop = census2010.download('99', 'total_female_pop')
    prsd_01_wages = census2010.parse(html_01_wages)
    prsd_99_wages = census2010.parse(html_99_wages)
    prsd_99_total_female_pop = census2010.parse(html_99_total_female_pop)
    merged = census2010.merge([prsd_01_wages,
                               prsd_99_wages,
                               prsd_99_total_female_pop])
    geocoded = census2010.geocode(merged, 'OK2', 'Muni')
    census2010.format_to_excel(geocoded, './formatted.xlsx')
    # if the whole of the process didn't raise any exceptions, it passes
    assert True
