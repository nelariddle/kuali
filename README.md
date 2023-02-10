# kuali

## Purpose

Kuali Time only allows you to see 2 weeks' worth of hours at a time, so I wrote this web scraper so that I could generate a csv of my hours for the entire year and generate my own plots and insights into my hours.

## Contents

- scraper.py: the python file that does all of the web navigation and scraping
- scraper_CEWT.py: the python file that does all of the web navigation and scraping
- practice folder: HTML manually downloaded from Kuali that I used to practice the scraping code on
- All Hours Cox.csv: the resultant csv from running the python file consisting of all dates and hours taken off Kuali Time for Cox only
- All Hours CEWT.csv: the resultant csv from running the python file consisting of all dates and hours taken off Kuali Time for CEWT only
- other csv files: the code also records each 2 week period in its own csv

## Notes

You must have downloaded the latest version of ChromeDriver for the program to function. I'd recommend storing it in Program Files (x86), the path I reference in the code.
