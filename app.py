import copy

from web_scrape.web_scraper import scrape
from supporting.states import states

from flask import Flask, render_template, request

app = Flask(__name__)

consultancy_firms = {0: 'tata', 1: 'infosys', 2: 'revature', 3: 'cybercoders'}


# Root domain
@app.route("/")
def index():
    return render_template("index.html", location_list=states)


# Execute query request with search() function with the given job title, then switch to /searched directory
@app.route("/searched", methods=["POST"])
def searched():
    query = request.form["job-title"]
    shorthand_location = request.form["location"]
    config = request.form.get("consultancy-filter")

    search(query, shorthand_location, config)

    temp_jobs_list = copy.copy(Job.jobs_list) # Handles stacked results being returned
    Job.jobs_list.clear()

    total_jobs = len(temp_jobs_list)

    return render_template("index.html", jobs_list=temp_jobs_list, total_jobs=total_jobs, location_list=states)


def search(job_title, shorthand_location, config):
    jobs_returned = scrape(job_title, shorthand_location)

    for job in jobs_returned:
        if str(config) == 'no':
            if job[0].lower() not in consultancy_firms.values():
                obj = Job(job[0], job[1], job[2], job[3], Job.jobs_list)
                obj.add()
        else:
            obj = Job(job[0], job[1], job[2], job[3], Job.jobs_list)
            obj.add()


class Job:
    company = ""
    job_title = ""
    company_location = ""
    url = ""
    jobs_list = []

    def __init__(self, company, job_title, company_location, url, jobs_list):
        self.company = company
        self.job_title = job_title
        self.company_location = company_location
        self.url = url
        self.jobs_list = jobs_list

    def add(self):
        self.jobs_list.append(self)


app.run()  # Execute Flask when running program, (CTRL + C) to exit
