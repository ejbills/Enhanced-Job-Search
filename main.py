import discord

from web_scrape.web_scraper import scrape
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

token = config.get('BOT', 'token')

link = 'https://www.google.com/search?q=new+grad+software+engineer+california&ibp=htl;jobs#htivrt=jobs&fpstate=tldetail&htichips=date_posted:3days'

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content == '!job':
            jobs_returned = scrape(link, 3)

            await message.channel.send(jobs_returned)
            # for job in jobs_returned:
            #     await message.channel.send(job)


MyClient().run(token)
