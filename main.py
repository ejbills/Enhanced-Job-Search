import discord
from discord.ext import commands
from configparser import ConfigParser

from web_scrape.web_scraper import scrape

config = ConfigParser()
config.read("config.ini")

job_bot = commands.Bot(command_prefix='!')

token = config.get('BOT', 'token')

google_job_link = 'https://www.google.com/search?q={}&ibp=htl;jobs#htivrt=jobs&fpstate=tldetail&htichips=date_posted:3days'


class EnhancedJobSearch(commands.Bot):
    async def on_ready(ctx):
        if job_bot.is_ready():
            print('Logged on as {0}!'.format(ctx.user))

    @job_bot.command()
    async def job(ctx, *args):
        temp_link = str(args[1]).replace(" ", "+")

        if args[0] == 'google':
            jobs_returned = scrape(google_job_link.format(temp_link), 3)

            await ctx.send(jobs_returned)


job_bot.run(token)
