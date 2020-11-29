"""
Census 2010
===========

Downloader
----------

Downloader subpackage provides tools to:
1. Go to Russian Statistics web-site
2. Follow down the link path to a specific indicator in specific oblast
3. Fill out data request form
4. Extract the HTML data
5. Save HTML to disk

Main functionality of the *downloader* module.
"""

from datetime import datetime
from importlib import reload
import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from census2010.utils import create_folder
from . import config
from . import post_process


# Request is a data object that holds a variety of attributes that allow
# for efficient downloading of the indicator/region pair.

class Request:
    """
    A class that stores all metadata necessary to pass through all steps
    in a download process.
    """
    def __init__(self, indicator_name: str, region: str):
        """
        Take indicator name and region OK2 code, calculate indicator
        code and template. Store all of that in the object.
        """
        reload(config)
        self.indicator_name = indicator_name
        self.indicator_code = config.templates[indicator_name]['id']
        self.region = region
        self.template = config._calc_template(indicator_name, region)
        self._set_availability()
    
    def _set_availability(self):
        """
        Determine dataset availability status and set the request
        availability flag.
        """
        if self.template['available'] == "yes":
            self.available = True
        else:
            self.available = False
        del self.template['available']

# Helper functions

# Browser operating functions

def _launch_browser(headless: bool):
    """Initialize a Selenium webdriver session and return a handler."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    return driver

def _check_box(chkbox_element):
    """
    Make sure a checkbox is checked regardless of it's initial state.
    """
    if not chkbox_element.is_selected():
        chkbox_element.click()

def _select_option(select_element, pref_option):
    """
    Fill out a `select` HTML element based on `pref_option` value.
    `pref_option` can be a string value or a list of string values that
    need to be selected.
    """
    pref_opts = pref_option if isinstance(pref_option, list) else [pref_option]
    options = select_element.find_elements_by_tag_name('option')
    for option in options:
        if option.text in pref_opts:
            if not option.is_selected():
                option.click()
        else:
            if option.is_selected():
                option.click()

# Request handlers:

def _load_region(driver, request: Request):
    """Go to a webpage that contains all indicators for a region."""
    ok2 = request.region
    url = f'https://rosstat.gov.ru/dbscripts/munst/munst{ok2}/DBInet.cgi'
    driver.get(url)

def _open_folder(driver, request: Request):
    """Open a folder (by indicator code), if not already open"""
    element = driver.find_element_by_name(request.indicator_code)
    if not element.is_displayed():
        while element.get_attribute('class') != 'list':
            element = element.find_element_by_xpath('..')
        folder_id = element.get_attribute('id')[:-1]
        driver.find_element_by_id(folder_id).click()

def _check_indicator(driver, request):
    """Check an indicator checkbox on a region page."""
    chk = driver.find_element_by_name(request.indicator_code)
    if not chk.is_selected():
        chk.click()

def _open_form(driver):
    """
    Given an indicator cehckbox is selected, click the button to load
    the attribute form.
    """
    button = driver.find_element_by_id('Knopka')
    button.click()

def _fill_form(driver, request):
    """Fill indicator form fields based on indicator template."""
    for key in request.template:
        if request.template[key] == '*':
            _check_box(driver.find_element_by_name(key+'_chk'))
        else:
            _select_option(driver.find_element_by_name(key), request.template[key])

def _manual_layout(driver, request):
    """Open manual layout section and fill it out."""
    manual = driver.find_elements_by_id('Manual')[0]
    manual.click()
    for key in request.template:
        name = '_' + key
        driver.find_elements_by_name(name)[1].click()
    # Format order of municiaplity-related columns
    driver.find_elements_by_name('_munr')[2].click()
    driver.find_elements_by_name('_tippos')[2].click()
    driver.find_elements_by_name('_oktmo')[2].click()
    _select_option(driver.find_element_by_name('a_munr'), '1')
    _select_option(driver.find_element_by_name('a_tippos'), '2')
    _select_option(driver.find_element_by_name('a_oktmo'), '3')

def _launch_table(driver):
    """Once the form has been filled out, launch the table."""
    launch_button = driver.find_element_by_name('STbl')
    launch_button.click()
    try:
        driver.switch_to.alert
        raise selenium.common.exceptions.UnexpectedAlertPresentException
    except selenium.common.exceptions.NoAlertPresentException:
        # No Alert is the happy flow
        driver.switch_to.window(driver.window_handles[-1])

def _evaluate_detail(driver):
    """
    Evaluate the detail level of the data table - is it 'rayon-level' or
    'municipality-level'.
    """
    rayon_cells = driver.find_elements_by_class_name('bL0')
    data_cells = driver.find_elements_by_class_name('bL2')
    if len(data_cells) / len(rayon_cells) < 1.5:
        raise ValueError

def _extract_table(driver):
    """Extract the table HTML and return it as a string."""
    out_table = driver.find_element_by_class_name('OutTbl')
    return out_table.get_attribute('innerHTML')

# All kinds of downloader functions:

def download(driver, indicator: str, region: str):
    """
    Run through the process of downloading a data table for a specified
    indicator and specified region.
    """
    request = Request(indicator, region)
    if not request.available:
        return (2, 'No data')
    try:
        _load_region(driver, request)
    except:
        return (1, 'Region not loaded')
    try:
        _open_folder(driver, request)
    except:
        return (1, 'Folder not found')
    try:
        _check_indicator(driver, request)
    except:
        return (1, 'Indicator not found')
    try:
        _open_form(driver)
    except:
        return (1, 'Form not loaded')
    try:
        _fill_form(driver, request)
    except:
        return (1, 'Form couldn\'t be filled out')
    try:
        _manual_layout(driver, request)
    except:
        return (1, 'Manual layout failed')
    try:
        _launch_table(driver)
    except selenium.common.exceptions.UnexpectedAlertPresentException:
        return (1, 'Alert prevented table from loading')
    try:
        html = _extract_table(driver)
    except:
        return (1, 'Failed to extract table')
    return (0, html)

def download_single(indicator_name: str, region_code: str, 
                    save_directory: str):
    """A convenience function to download a single indicator without a
    boilerplate to instantiate a browser."""
    driver = _launch_browser(False)
    code, result = download(driver, indicator_name, region_code)
    if code == 0:
        driver.quit()
        create_folder(save_directory)
        filename = f'{save_directory}/{region_code}_{indicator_name}.html'
        with open(filename, 'w') as html_file:
                html_file.write(result)
        dp = post_process._get_num_of_data_points(filename)
        print(f'Success {dp} dp.')
    elif code == 1:
        print(f'Error: {result}')
    elif code == 2:
        driver.quit()
        print(f'Skipped: {result}')

def download_region(region: str, save_directory: str):
    """Download all indicators for a specified region."""
    reload(config)
    create_folder(save_directory)
    for indicator in config.templates:
        driver  = _launch_browser(True)
        ex_code, result = download(driver, indicator, region)
        if ex_code == 0:
            filename = f'{save_directory}/{region}_{indicator}.html'
            with open(filename, 'w') as html_file:
                html_file.write(result)
            status = 'Success!'
            color = ''
        elif ex_code == 2:
            status = 'no data'
            color = '\033[90m'
        else:
            status = result
            color = '\033[31m'
        timestamp = datetime.now().strftime("%T")
        message = (color + timestamp +' - ' + region + ' - ' + indicator +
                   ' - ' + status + '\033[0m')
        print(message)
        driver.quit()

def download_range(save_directory: str, start: str = '01', end: str = '99'):
    """
    Consequently download every indicator for every oblast and save
    obtained tables as separate files to a specified folder.
    """
    reload(config)
    start_index = config.region_codes.index(start)
    end_index = config.region_codes.index(end) + 1
    for region in config.region_codes[start_index:end_index]:
        download_region(region, save_directory)

def download_indicator(indicator_name: str, save_directory: str,
                       start: str = '01', end: str = '99'):
    """
    Consequently download tables for a specified indicator across all
    regions.
    """
    reload(config)
    start_idx = config.region_codes.index(start)
    end_idx = config.region_codes.index(end) + 1
    for region in config.region_codes[start_idx:end_idx]:
        driver  = _launch_browser(True)
        ex_code, result = download(driver, indicator_name, region)
        if ex_code == 0:
            filename = f'{save_directory}/{region}_{indicator_name}.html'
            with open(filename, 'w') as html_file:
                html_file.write(result)
            status = 'Success!'
            color = '\033[90m'
        elif ex_code == 2:
            status = 'skipped'
            color = ''
        else:
            status = result
            color = '\033[31m'
        timestamp = datetime.now().strftime("%T")
        regidx = config.region_codes.index(region)
        message = (f'{timestamp} - {region} ({regidx}) - {indicator_name} - '
                   f'{status}')
        message = color + message + '\033[0m'
        print(message)
        driver.quit()

def download_all(save_directory: str, start: str = '01'):
    """
    Consequently download every indicator for every oblast and save
    obtained tables as separate files to a specified folder.
    """
    reload(config)
    start_index = config.region_codes.index(start)
    for region in config.region_codes[start_index:]:
        download_region(region, save_directory)
