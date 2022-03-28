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

username.send_keys("put username here")
password.send_keys("put password here")

driver.find_element(By.NAME, "_eventId_proceed").click()
driver.implicitly_wait(10)

driver.find_element(By.XPATH, "//a[text()='Time Detail']").click()

html_files = [driver.page_source]

while True:
    driver.find_element(By.XPATH, "//button[@title='Previous']").click()
    html_files.append(driver.page_source)

    if len(driver.find_elements(By.XPATH, "//button[@title='Previous']")) == 0:
        break


hours_dict = {}

years = [2021, 2022]

# we iterate over each file
# for file in files:
for html_file in html_files:
    # using BeautifulSoup to read through the file
    content = html_file
    soup = BeautifulSoup(content, "lxml")

    # finding the first date that appears in the file; this is the beginning of the 2 week period
    date_string = soup.find("tr", {"class": "ui-state-default"}
                            ).contents[3].get_text()[3:]

    # generating a dictionary of dates and hours for each date using BeautifulSoup functionality
    current_dict = dict(zip([datetime.date((years[0] if int(date_string[0:2]) > 7 else years[1]), int(date_string[0:2]), int(
        date_string[3:5]))+datetime.timedelta(days=i) for i in range(14)], [float(tag.get_text())
                                                                            for i, tag in enumerate(soup.find_all("td", string="Worked Hours:")[0].next_siblings) if (i != 15 and tag.get_text() != "\n")]))

    # creating an individual csv for each 2 week period
    # we will call it "Hours [first day of the period]"
    csv_filename = "Hours "+str(min(current_dict.keys()))+".csv"

    # writing to the csv for individual periods
    with open(csv_filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for date, hours in current_dict.items():
            writer.writerow([date, hours])

    # appending to our dictionary storing overall hours acquired from each file
    hours_dict.update(current_dict)

# writing to the csv for overall hours
with open("All Hours.csv", "w", newline='') as csv_file:
    writer = csv.writer(csv_file)
    for date in sorted(hours_dict.keys()):
        writer.writerow([date, hours_dict[date]])
