Census 2010
===========


Census 2010 is a project by Kantynent where we are required to deliver a table of socio-demographic indicators for Russia to the customer.

The table has a predefined format where every row corresponds to a single municipality (some rows are also aggregate on rayon and/or region level (a region is an oblast or republic or kray or other top (ADM1) level division unit in Russia)) and every column corresponds to a single indicator.


Downloading source data
-----------------------

Most indicators are obtained from Russian statistical office web-site (municipality level statistical database). A few additional sources that we will use are our own produced raster maps of age-groups and households structure distributions (in fact those are as well derived from Russian statistical office, so in theory can be reproduced from scratch).

As such our first concern is to download all source data from the Russian statistics web-site. To achieve this, we implement the `downloader` module.

The result of the downloader module working will be a directory of raw HTML files, each containing a table (in HTML markup). It is important that every HTML file is named in a uniform fashion and contains the following metadata:
- `region` - a 2-digit OKTMO code of the region.
- `indicator` - a predefined short alphanumeric code of the indicator that was downloaded.
Inidcator and region codes are standardized in the special sub-module of the downloader module - `config.py`.


Importing from outside
----------------------

Two indicators (that are required by the final table format) cannot be downloaded from rosstat.gov.ru. Instead they need to be imported from file system (`data` predefined folder). Import settings and formatting rules are implemented in the `importer` module.


Post-processing downloaded data
-------------------------------

In order to make downloaded (and imported) data convenient to work with we introduce a number of post-processing filters:
- proper HTML - will add a valid HTML header (including encoding metadata, table header tag etc.), footer and an embedded CSS stylesheet.
- pandas csv - will extract valuable information from HTML table, standardize it and save as a pandas-readable CSV format DataFrame.

Post-processing is implemented as `post-processing` module.


Inclusion pipeline
------------------

At this point (once the post-processing module has done its job) we have a folder of files that can be identified by their region/indicator codes in a well-formed, readable CSV format. However, not all of them can be imported into the final table as they are. Different region/indicator pairs have different problems that prevent them from being imported:
- some region/indicator combinations have no data at all and as such are not even present as files (e.g. 40_ndfl doesn't exist as Saint Petersburg have failed to publish the personal tax statistics.
- data is limited:
  - where data _is_ available sometimes it is only present on rayon-level
  - alternatively data may be present on municipal level, but not all municiaplities are present in the list
- some tables are malformed (e.g. 64 - Sakhalinskaya oblast, but maybe others too) and need reformatting before they can be imported
- some tables have more than one data series (columns). For example - age/gender groups have a separate column for each of the groups, ethnicity data has a separate column for each ethnicity, nurses and doctors data have separate state/private columns and an additional aggregate column. Some of those columns can be imported into the final table as they are, some need to recalculated, some even interpolated.
- many tables are downloaded at years different from 2010, so they need to be adjusted to the target year.

In order to make all data series ready for importing we implement `parser` module with the following functionality:

1. if a data file exists - skip, else if the file doesn't exist - also skip
2. if the data is detailed - skip, else if the data is limited - `augment` the data file
3. if the data is well-formed - skip, else if the data is malformed - `reformat` the data file
4. if the data file has exactly one data series - skip, else if the data has more than one series:
   - if data = 'ethnicity' or 'age groups' - `split` data to sub-indicators (each with a single series)
   - else if data = 'wages' or 'workers' - `recalculate wages` and workers into a single series
   - else if data = 'doctors' or 'nurses' - `filter` redundant columns
5. if data year is 2010 - `move to the ready folder`, 
   - else if data year != 2010 & if data year is acceptable - `move to the ready folder`, else - `shift` data to 2010 and move to the ready folder

Marked above are functions that need to be implemented in the `parser` module.

Once the above functionality have been implemented and parser has done its job, we will have a folder of single-series indicators, part of which can be directly included into the final table, and the other part is ready to be put on a map and interpolated.


Interpolation
-------------

There are a number of indicators that do not have municipality level detail, but still need to be included together with the rest of the table. We have chosen to interpolate those series geographically and then collect the interpolated values through zonal statistics. The following indicators need interpolation treatment:
- age / gender groups
- ethnicity
- households (data obtained outside rosstat.gov.ru)
- wages

Interpolation process consists of the following stages:
1. geocoding (i.e. assigning geographic coordinates for every value in the interpolated data series)
2. creating raster (through IDW, kriging whatever else)
3. collecting values

The above is implemented as `geocoder`, `interpolator` and `collector` sub-modules.


Geography
---------

An important part of interpolation process is preparing the geographic datasets - municipality polygons and municipality population centers (points). These two datasets are used by all three sub-modules of the interpolator module. Moreover, they are part of the deliverable of this project as agreed with the customer.

Although preparing geographic datasets is in large part a manual or semi-manual process, the parts that can be programmatically automated are implemented as the `geography` module.


Merging
-------

After interpolation stage we now have all data series ready for inclusion in the final table. Some of them come directly from parsing stage and some from interpolating stage. Both variants should be uniform and available as single CSV-files, each featuring an index and a single data series (column).

To merge all of the data series together into a final table stub we implement `merger` module.


Formatting
----------

Once we have all the data series uniformly merged into a single dataframe, we can finalize it by programmatically formatting the data into an Microsoft Excel document. This functionality is implemented in `formatter` module.


Deploy
------

Once the ready table has been formatted it can be deployed to the customer. Deploy is carried out by FTP and is implemented in `deploy` module.

At this stage the project may be considered complete.
