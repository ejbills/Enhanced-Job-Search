import re
import requests

from bs4 import BeautifulSoup

def scrape(url, iterations):
    counter = 0
    
    jobs = []

    session = requests.Session()
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ('
                                                       'KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})

    soup = BeautifulSoup(response.text, 'html.parser')

    # Finds game title element by "name" attribute
    title = soup.findAll("div", {"class": re.compile('.*BjJfJf PUpOsf.*')}, limit=iterations)
    company = soup.findAll("div", {"class": re.compile('.*vNEEBe.*')}, limit=iterations)
    posted_date = soup.findAll("span", {"class": re.compile('.*SuWscb.*')}, limit=iterations)
    links = soup.find_all("a", {"href": True})

    for i in range(iterations):
        job = []
        job.append(company[i].text if company[i] else 'No company found')
        job.append(title[i].text if title[i] else 'No job title found')
        job.append(posted_date[i].text if posted_date[i] else 'No job post date found')
        
        jobs.append(job)

    for link in links:
        if link.get('title') and counter < iterations:
            if 'Apply on' in link.get('title'):
                jobs[counter].append(link.get('href') if len(link.text) > 1 else 'No job link found')

                counter += 1

    return jobs
