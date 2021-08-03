# import libraries
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# format url
def get_url(position, location):
    # generate url from position and location
    template = 'https://uk.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

url = get_url('senior analyst', 'london')

# create session
s = requests.Session()
response = s.get(url)
print(response)

soup = BeautifulSoup(response.content, 'html.parser')
cards = soup.find_all('div', class_='job_seen_beacon')
card = cards[0]



# get position
job_title = card.h2.text
print(job_title)

# get company
company = card.find('span', class_='companyName').text.lstrip('New')
print(company)

# get frequency
new = card.find('span', class_='label').text.strip()
print(new)

# get url
atag = card.find('a')
job_url = 'https://uk.indeed.com' + atag.get('href')
print(job_url)

# get job location
job_loc = card.find('div', class_='companyLocation').text.strip()
print(job_loc)

# get summary
jd = card.find('div', class_='job-snippet').text.strip('\n')
print(jd)