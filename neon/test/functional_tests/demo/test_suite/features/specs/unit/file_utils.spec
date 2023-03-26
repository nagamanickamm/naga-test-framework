# File Utilities
==================
tag: Common_utils

## Read a config file from specific location
--------------------------------------------

tags: unit

* Read config file "/test_suite/resources/config/sample.config"
* Validate configuration file

## Read csv file for step data
------------------------------

tags: unit

table: test_suite/resources/csv/read_csv_test.csv

* Read <scenario> with "/test_suite/resources/csv/read_csv_test.csv"
* Each <scenario> row should be a dictionary


## Get Current Working Directory relative to the file
------------------------------------------------------

tags: unit

* Get current working directory
* Returned the working directory path