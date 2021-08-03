# import libraries
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# format url

baseUrl = 'https://uk.indeed.com'

def get_url(position, location):
    # generate url from position and location
    template = baseUrl + '/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

# Extract job data from a single record
def get_record(card):
    # get position
    try:
        job_title = card.h2.text.strip().lstrip('new')
    except AttributeError:
        job_title = ''
    # get company
    try:
        company = card.find('span', class_='companyName').text.strip('\n')
    except AttributeError:
        company = ''
    # get frequency
    try:
        new = card.find('span', class_='label').text.strip()
    except AttributeError:
        new = ''
    # get url
    try:
        atag = card.find('a')
        job_url = baseUrl + atag.get('href')
    except AttributeError:
        job_url = ''
    # get job location
    try:
        job_loc = card.find('div', class_='companyLocation').text.strip()
    except AttributeError:
        job_loc = ''
    # get summary
    try:
        jd = card.find('div', class_='job-snippet').text.strip('\n')
    except AttributeError:
        jd = ''
    # get salary
    try:
        salary = card.find('span', class_='salary-snippet').text
    except AttributeError:
        salary = ''
    # get rating
    try:
        rating = card.find('span', class_='ratingNumber').text.strip()
    except AttributeError:
        rating = ''
    # get post date
    try:
        post_date = card.find('span', class_='date').text.strip()
    except AttributeError:
        post_date = ''
    today = datetime.today().strftime('%Y-%m-%d')

    record = (job_title, company, new, job_url, job_loc, jd, salary, rating, post_date, today)

    return record

def main(position, location):
    # run main program
    records = []
    url = get_url(position, location)

    # extract the job data
    while True:
        # create session
        s = requests.Session()
        response = s.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all('div', class_='job_seen_beacon')

        for card in cards:
            record = get_record(card)
            records.append(record)
            time.sleep(1.5)

        # pagination
        try:
            url = baseUrl + soup.find('a', attrs={'aria-label': "Next"}).get('href')
        except AttributeError:
            break

    # save the job data
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_title', 'company', 'new', 'job_url', 'job_loc', 'jd', 'salary','rating', 'post_date', 'today'])
        writer.writerows(records)

# run the main program
main('senior analyst', 'london')
