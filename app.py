import copy

from web_scrape.web_scraper import scrape
from flask import Flask, render_template, request

app = Flask(__name__)


# Root domain
@app.route("/")
def index():
    return render_template("index.html")


# Execute query request with search() function with the given job title, then switch to /searched directory
@app.route("/searched", methods=["POST"])
def searched():
    query = request.form["job-title"]

    search(query)

    temp_jobs_list = copy.copy(Job.jobs_list) # Handles stacked results being returned
    Job.jobs_list.clear()

    return render_template("index.html", jobs_list=temp_jobs_list)


def search(job_title):
    jobs_returned = scrape(job_title, 10)

    for job in jobs_returned:
        obj = Job(job[0], job[1], job[2], job[3], Job.jobs_list)
        obj.add()


class Job:
    company = ""
    job_title = ""
    date = ""
    url = ""
    jobs_list = []

    def __init__(self, company, job_title, date, url, jobs_list):
        self.company = company
        self.job_title = job_title
        self.date = date
        self.url = url
        self.jobs_list = jobs_list

    def add(self):
        self.jobs_list.append(self)


app.run()  # Execute Flask when running program, (CTRL + C) to exit
