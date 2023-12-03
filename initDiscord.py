import datetime
import os
import time

from dateutil.parser import parse as dtparse
import discord
from discord.ext import commands
from dotenv import load_dotenv
import schedule

from get_events import get_list_event


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

intents = discord.Intents.all()
client = commands.Bot(command_prefix="?", intents=intents)

TIME1 = '%H:%M'
TIME2 = '%m/%d,%Y'


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break
        
    print(f'{client.user} has connected to:\n' + 
            f'{guild.name}(id: {guild.id})')
    schedule_track()

def schedule_track(): # Schedule message send
    schedule.every().day.at("7:00").do(on_time)
    
    while schedule.run_pending():
        time.sleep(1)

@client.event
async def on_time(event_number = 5): # Display events at 7am every day
    ctx = client.get_channel(1161636345245085748)
    
    await ctx.send("Displaying events...")
    
    # Day start time 
    start = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' = UTC
    # Day end time
    end = datetime.datetime.utcnow().replace(hour=23, minute=59,
    second=59, microsecond=0).isoformat() + 'Z'
    
    events = get_list_event(event_number, start, end)
    
    if len(events) == 0:  # If there are no events today
        embed = discord.Embed(title="No Events Found", color=0xf74f18,
        url="https://calendar.google.com/calendar/u/0/r?mode=week")
        await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(title="Todays Events", url="https://calendar.google.com/calendar/u/0/r?mode=week",
                                      description=f' {len(events)} events ', colour=0xf74f18)
        embed.set_thumbnail(url="https://img.icons8.com/fluent/48/000000/google-calendar--v2.png")
        
        for event in events:
            # set variables
            startdatetime = event["start_datetime"]
            enddatetime = event["end_datetime"]
            eventdescription = event["event_desc"]
            stime = datetime.datetime.strftime(dtparse(startdatetime),
            format=TIME1)
            etime = datetime.datetime.strftime(dtparse(enddatetime),
            format=TIME1)
            html_link = event["html_link"]
            title_description = event["eventtitle"]
            # embedding fields
            embed.add_field(name=f'{title_description} from {stime} to {etime}',
            value=f"[{eventdescription}]({html_link})", inline=False)
            embed.set_footer(text=
            f"For {datetime.datetime.strftime(dtparse(startdatetime), format=TIME2)}")
        
        await ctx.send(embed=embed)

    
@client.command() # Display events command
async def displayEvents(ctx, event_number):
    await ctx.send("Displaying events...")
    
    # Day start time 
    start = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' = UTC
    # Day end time
    end = datetime.datetime.utcnow().replace(hour=23, minute=59,
    second=59, microsecond=0).isoformat() + 'Z'
    
    events = get_list_event(event_number, start, end)
    
    if len(events) == 0:  # If there are no events today
        embed = discord.Embed(title="No Events Found", color=0xf74f18,
        url="https://calendar.google.com/calendar/u/0/r?mode=week")
        await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(title="Todays Events", url="https://calendar.google.com/calendar/u/0/r?mode=week",
                                      description=f' {len(events)} events ', colour=0xf74f18)
        embed.set_thumbnail(url="https://img.icons8.com/fluent/48/000000/google-calendar--v2.png")
        
        for event in events:
            # set variables
            startdatetime = event["start_datetime"]
            enddatetime = event["end_datetime"]
            eventdescription = event["event_desc"]
            stime = datetime.datetime.strftime(dtparse(startdatetime),
            format=TIME1)
            etime = datetime.datetime.strftime(dtparse(enddatetime),
            format=TIME1)
            html_link = event["html_link"]
            title_description = event["eventtitle"]
            # embedding fields
            embed.add_field(name=f'{title_description} from {stime} to {etime}',
            value=f"[{eventdescription}]({html_link})", inline=False)
            embed.set_footer(text=
            f"For {datetime.datetime.strftime(dtparse(startdatetime), format=TIME2)}")
        
        await ctx.send(embed=embed)

    
client.run(TOKEN)
