"""
Unit tests suite for Downloader sub-package.
"""

import pytest

import census2010.downloader as cd


def test_get_template_args():
    """Test how template is caluclated."""
    with pytest.raises(ValueError):
        _templ = cd.templates.get_template('', '')

def test_get_template_default_template():
    """
    Test how template is calculated when there are no customizations.
    """
    templ = cd.templates.get_template('street_network', '01')
    assert templ == {'munr': '*', 'tippos': '*', 'oktmo': '*', 'god': '2010',
                     'period': 'значение показателя за год'}

def test_get_template_customized_indicator():
    """
    Test how template is calculated when indicator customizations
    override default template.
    """
    templ = cd.templates.get_template('natural_change', '01')
    assert templ == {'munr': '*', 'tippos': '*', 'oktmo': '*', 'god': '2012',
                     'period': 'значение показателя за год'}

def test_get_template_custom_region_template():
    """
    Test how template is calculated when there are customizations on
    region level.
    """
    templ = cd.templates.get_template('natural_change', '99')
    assert templ == {'munr': '*', 'tippos': '*', 'oktmo': '*', 'god': '2012',
                     'period': 'январь-март'}
