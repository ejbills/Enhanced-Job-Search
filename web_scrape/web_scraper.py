import re
import requests
from bs4 import BeautifulSoup

indeed_link = 'https://www.indeed.com/jobs?q={}&l=California&start={}'


def scrape(search_query, iterations):
    counter = 0
    page_count = 0
    jobs = []
    pages = []

    temp_query = search_query.replace(" ", "%20")

    session = requests.Session()
    response = session.get(indeed_link.format(temp_query, '00'),
                           headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ('
                                                  'KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})

    soup = BeautifulSoup(response.text, 'html.parser')

    pages_returned = soup.findAll("span", {"class": re.compile(r'pn')})  # Dynamically returns all page numbers

    for i in range(len(pages_returned)):  # Calculates page number for indeed URL
        if page_count == 0:
            pages.append('00')
            page_count += 10

        pages.append(str(page_count))
        page_count += 10

    for page in pages:
        response = session.get(indeed_link.format(temp_query, page),
                               headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ('
                                                      'KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.findAll("span", {"title": re.compile(r'.*')}, limit=iterations)
        company = soup.findAll("span", {"class": re.compile(r'companyName')}, limit=iterations)
        posted_date = soup.findAll("span", {"class": re.compile(r'date')}, limit=iterations)
        links = soup.find_all("a", {"class": re.compile(r'tapItem')}, {"href": True})

        try:
            for i in range(iterations):
                job = []

                job.append(company[i].text if company[i] else 'No company found')
                job.append(title[i].text if title[i] else 'No job title found')
                job.append(posted_date[i].text if posted_date[i] else 'No job post date found')

                jobs.append(job)
        except: # No more job results found, pass
            pass

        for link in links:
            jobs[counter].append('https://indeed.com' + link.get('href'))
            counter += 1

    return jobs
