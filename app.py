from web_scrape.web_scraper import scrape
from flask import Flask, render_template, request

app = Flask(__name__)
job_link = 'https://www.google.com/search?q={}&ibp=htl;jobs#htivrt=jobs&fpstate=tldetail&htichips=date_posted:3days'
jobs_list = []  # Stores jobs found in the form of Job constructor

# Root domain
@app.route("/")
def index():
    return render_template("index.html")

# Execute query request with search() function with the given job title, then switch to /searched directory
@app.route("/searched", methods=["POST"])
def searched():
    query = request.form["job-title"]
    search(query)
    return render_template("index.html", jobs_list=jobs_list)

def search(job_title):
    temp_link = job_title.replace(" ", "+")

    jobs_returned = scrape(job_link.format(temp_link), 3)

    for job in jobs_returned:
        obj = Job(job[0], job[1], job[2], job[3])
        obj.add()

class Job:
    company = ""
    job_title = ""
    date = ""
    url = ""

    def __init__(self, company, job_title, date, url):
        self.company = company
        self.job_title = job_title
        self.date = date
        self.url = url

    def add(self):
        jobs_list.append(self)

app.run()  # Execute Flask when running program, (CTRL + C) to exit
