import re
import time
from bs4 import BeautifulSoup
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


years = [2021, 2022]
hours_dict = {}


content = "hours3.html"
with open(content) as fp:
    soup = BeautifulSoup(fp, "lxml")


assignment_tags = soup.find_all(
    "td", {"class": re.compile(r"assignment[0-9]")})
assignment_names = []
cox_assignment_name = ""
for tag in assignment_tags:
    try:
        float(tag.get_text())
    except ValueError as e:
        assignment_names.append(tag.get_text())
        if "Cox" in tag.get_text():
            cox_assignment_name = tag.get_text()

print(cox_assignment_name)

print(assignment_names)


# print(assignment_tags)

# used if the user has multiple jobs within kuali
# num_jobs = 2
# job_titles = [soup.find_all(
#     "td", {"class": ("assignment"+str(i))})[0].get_text() for i in range(num_jobs)]

# finding the first date that appears in the file; this is the beginning of the 2 week period
date_string = soup.find_all(
    "option", {"selected": "selected"})[1].contents[0][0:10]
month, day, year = date_string[0:2], date_string[3:5], date_string[6:10]

if assignment_names == []:
    hour_list = [[0.0]*14]
else:
    hour_list = [[float(sib.get_text()) if sib.get_text() != '' else 0 for sib in soup.find_all(
        "td", text=cox_assignment_name)[0].next_siblings if sib.get_text() != "\n"][j] for j in [x for x in range(15) if x != 7]]
# print([float(sib.get_text()) if sib.get_text() != '' else 0 for sib in soup.find_all(
#     "td", {"class": "assignment1"})[0].next_siblings if sib.get_text() != "\n"])
# print([float(sib.get_text()) if sib.get_text() != '' else 0 for sib in soup.find_all(
#     "td", {"class": "assignment0"})[0].next_siblings if sib.get_text() != "\n"])

print(hour_list)

# print(zip(*hour_lists))


# generating a dictionary of dates and hours for each date using BeautifulSoup functionality
current_dict = dict(zip([datetime.date(int(year), int(month), int(
    day))+datetime.timedelta(days=i) for i in range(14)], hour_list))

# creating an individual csv for each 2 week period
# we will call it "Hours [first day of the period]"
csv_filename = "Hours "+str(min(current_dict.keys()))+".csv"

# writing to the csv for individual periods
with open(csv_filename, "w", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Date", *assignment_names])
    for date, hours in current_dict.items():
        writer.writerow([date, hours])

# appending to our dictionary storing overall hours acquired from each file
hours_dict.update(current_dict)

print(hours_dict)
