import re
import time
from bs4 import BeautifulSoup
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://apps.iu.edu/kpme-prd/Clock.do")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys("nmriddle")
password.send_keys("IUapplication2020")

driver.find_element(By.NAME, "_eventId_proceed").click()
driver.implicitly_wait(500)

driver.find_element(By.XPATH, "//a[text()='Time Detail']").click()

html_files = [driver.page_source]

num = 0

while True:
    driver.find_element(By.XPATH, "//button[@title='Previous']").click()
    html_files.append(driver.page_source)

    num += 1
    # if num == 5:
    #     break
    if len(driver.find_elements(By.XPATH, "//button[@title='Previous']")) == 0:
        break

print("1")
print(len(html_files))
hours_dict = {}


# we iterate over each file
# for file in files:
for html_file in html_files:
    # using BeautifulSoup to read through the file
    content = html_file
    soup = BeautifulSoup(content, "lxml")

    print("bruh")

    # finds the names of the jobs
    assignment_tags = soup.find_all(
        "td", {"class": re.compile(r"assignment[0-9]")})

    # finds if Cox is present in that week's jobs
    cox_assignment_name = ""
    for tag in assignment_tags:
        text = tag.get_text()
        try:
            float(text)
        except ValueError as e:
            if "Cox" in tag.get_text():
                cox_assignment_name = tag.get_text()

    # finding the first date that appears in the file; this is the beginning of the 2 week period
    date_string = soup.find_all(
        "option", {"selected": "selected"})[1].contents[0][0:10]
    month, day, year = date_string[0:2], date_string[3:5], date_string[6:10]

    # compiling the hours for each job over the period into a list of lists (or list of 0's if no Cox)
    if cox_assignment_name == "":
        hour_list = [0.0]*14
    else:
        hour_list = [[float(sib.get_text()) if sib.get_text() != '' else 0.0 for sib in soup.find_all(
            "td", text=cox_assignment_name)[0].next_siblings if sib.get_text() != "\n"][j] for j in [x for x in range(15) if x != 7]]

    # generating a dictionary of dates and hours for each date using BeautifulSoup functionality
    current_dict = dict(zip([datetime.date(int(year), int(month), int(
        day))+datetime.timedelta(days=i) for i in range(14)], hour_list))

    # creating an individual csv for each 2 week period
    # we will call it "Hours [first day of the period]"
    csv_filename = "2WeeksCSV/Hours "+str(min(current_dict.keys()))+".csv"

    # writing to the csv for individual periods
    with open(csv_filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Date", cox_assignment_name])
        for date, hours in current_dict.items():
            writer.writerow([date, hours])

    # appending to our dictionary storing overall hours acquired from each file
    hours_dict.update(current_dict)

# writing to the csv for overall hours
with open("All Hours.csv", "w", newline='') as csv_file:
    writer = csv.writer(csv_file)
    for date in sorted(hours_dict.keys()):
        writer.writerow([date, hours_dict[date]])
