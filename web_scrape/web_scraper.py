import re
import requests
from bs4 import BeautifulSoup

from supporting.states import states_dict

job_boards = ['https://www.indeed.com/jobs?q={}&l={}&start={}',
              'https://www.glassdoor.com/Job/{}-jobs-SRCH_KO0,17_IP{}.htm']

def scrape(search_query, shorthand_location):
    jobs = []

    selected_location = states_dict[shorthand_location]

    for job_board in job_boards:
        page_count = 0
        pages = []

        indeed_query = True if 'indeed' in job_board else False
        temp_query = search_query.replace(" ", "%20" if indeed_query else '-')

        session = requests.Session()
        response = session.get(job_board.format(temp_query, selected_location, '00' if indeed_query else '1'),
                               headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ('
                                                      'KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})

        soup = BeautifulSoup(response.text, 'html.parser')

        # Dynamically returns all page numbers
        pages_returned = soup.findAll("span", {"class": re.compile(r'pn')}) if indeed_query \
            else soup.findAll("div", {"data-test": re.compile(r'page-x-of-y')})

        # Calculates page numbers for indeed URL
        for i in range(len(pages_returned)):
            if indeed_query:
                if page_count == 0:
                    pages.append('00')
                    page_count += 10

                pages.append(str(page_count))
                page_count += 10
            else:
                for i in range(1, int(pages_returned[i].text.split()[-1]) - 20):
                    pages.append(i)

        for page in pages:
            response = session.get(job_board.format(temp_query, selected_location, page),
                                   headers={
                                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ('
                                                     'KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})

            soup = BeautifulSoup(response.text, 'html.parser')

            company = soup.findAll("span", {"class": re.compile(r'companyName')})
            title = soup.findAll("span", {"title": re.compile(r'.*')})
            company_location = soup.findAll("div", {"class": re.compile(r'companyLocation')})
            link = soup.findAll("a", {"class": re.compile(r'jcs-JobTitle')})

            for i in range(len(company)):
                job = [company[i].text if company[i] else 'No company found',
                       title[i].text if title[i] else 'No job title found',
                       company_location[i].text if company_location[i] else 'No job location found',
                       'https://indeed.com' + link[i].get('href') if link[i] else 'No job link found']

                jobs.append(job)

    return jobs
