import re
import time
from bs4 import BeautifulSoup
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

main_csv = "All Hours CEWT.csv"

# find the last recorded date in AllHours.csv and convert to datetime object
last_date = datetime.date(2022, 5, 1)
try:
    with open(main_csv, "r") as csv_file:
        last_line = csv_file.readlines()[-1].split(",")[0]
        last_date = datetime.date(int(last_line[:4]), int(
            last_line[5:7]), int(last_line[8:]))
except:
    pass


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://apps.iu.edu/kpme-prd/Clock.do")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys("REDACTED")
password.send_keys("REDACTED")

driver.find_element(By.NAME, "_eventId_proceed").click()
driver.implicitly_wait(500)

driver.find_element(By.XPATH, "//a[text()='Time Detail']").click()

hours_dict = {}

while True:
    # get the current page source and create a soup object from it
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")

    # find the beginning of the 2 week period by checking the current selected week in the drop down
    date_string = soup.find_all(
        "option", {"selected": "selected"})[1].contents[0][0:10]
    month, day, year = date_string[0:2], date_string[3:5], date_string[6:10]
    this_date = datetime.date(int(year), int(month), int(day))

    # check if we have already recorded 2 weeks after this page's date; then no need to do this one again
    if last_date - this_date > datetime.timedelta(days=14):
        break

    # finds the names of the jobs
    assignment_tags = soup.find_all(
        "td", {"class": re.compile(r"assignment[0-9]")})

    # finds if Cox is present in that week's jobs
    cewt_assignment_name = ""
    for tag in assignment_tags:
        text = tag.get_text()
        try:
            float(text)
        except ValueError as e:
            if "CEWT" in tag.get_text():
                cewt_assignment_name = tag.get_text()

    # compiling the hours over the period into a list of lists (or list of 0's if no Cox)
    if cewt_assignment_name == "":
        hour_list = [0.0]*14
    else:
        hour_list = [[float(sib.get_text()) if sib.get_text() != '' else 0.0 for sib in soup.find_all(
            "td", text=cewt_assignment_name)[0].next_siblings if sib.get_text() != "\n"][j] for j in [x for x in range(15) if x != 7]]

    # generating a dictionary of dates and hours for each date using BeautifulSoup functionality
    current_dict = dict(zip([datetime.date(int(year), int(month), int(
        day))+datetime.timedelta(days=i) for i in range(14)], hour_list))

    # creating an individual csv for each 2 week period
    # we will call it "Hours [first day of the period]"
    #csv_filename = "2WeeksCSV_CEWT/Hours "+str(min(current_dict.keys()))+".csv"

    # writing to the csv for individual periods
    # with open(csv_filename, "w", newline='') as csv_file:
    #     writer = csv.writer(csv_file)
    #     writer.writerow(["Date", cewt_assignment_name])
    #     for date, hours in current_dict.items():
    #         writer.writerow([date, hours])

    # appending to our dictionary storing overall hours acquired from each file
    hours_dict.update(current_dict)

    # check if we can no longer go back
    if len(driver.find_elements(By.XPATH, "//button[@title='Previous']")) == 0:
        break
    driver.find_element(By.XPATH, "//button[@title='Previous']").click()

# delete the last 14 lines, because there is a chance they have changed
try:
    f = open(main_csv, "r+")
    lines = f.readlines()
    for i in range(14):
        if(lines != []):
            lines.pop()
    f = open(main_csv, "w+")
    f.writelines(lines)
    f.close()
except:
    pass


# writing to the csv for overall hours
with open(main_csv, "a", newline='') as csv_file:
    writer = csv.writer(csv_file)
    for date in sorted(hours_dict.keys()):
        writer.writerow([date, hours_dict[date]])
