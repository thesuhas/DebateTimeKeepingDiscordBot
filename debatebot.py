import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='.')
client.remove_command('help')

# Creating a debate class
class Debate:
    def __init__(self, status=False, format="NA", reply="NA", speaker='PM', restart = False, speech = False):
        self.status = status
        self.format = format
        self.reply = reply
        self.speaker = speaker
        self.restart = restart
        self.speech = False

def make_sleep():
    async def sleep(delay, result=None, *, loop=None):
        coro = asyncio.sleep(delay, result=result, loop=loop)
        task = asyncio.ensure_future(coro)
        sleep.tasks.add(task)
        try:
            return await task
        except asyncio.CancelledError:
            return result
        finally:
            sleep.tasks.remove(task)

    sleep.tasks = set()
    sleep.cancel_all = lambda: sum(task.cancel() for task in sleep.tasks)
    return sleep

@client.event
async def on_ready():
    print("Bot is ready")
    global deb
    global speakers
    deb = Debate()
    speakers = {'BP': ['PM', 'LO', 'DPM', 'DLO', 'MG', 'OG', 'GW', 'OW'], 'AP': ['PM', 'LO', 'DPM', 'DLO', 'GW', 'OW']}

@client.command(aliases=['h', "help"])
async def _help(ctx):
    author = ctx.message.author
    help_e = discord.Embed(color=discord.Color.green())
    name = "`.start` to start a debate\n`.format {format}` to set the debate format\n`.speech` to start a speech\n`.restart` to restart a speech\n`.stop` to stop a speech before time has elapsed\n`.end` to end a debate before it has finished\n`.status` to check the status of a debate"
    format = "Formats available are AP and BP\n"
    time = "Speaker time is 7:20 per person"
    poi = "POIs can be asked from the 1st minute till the 6th minute"
    help_e.add_field(name='Commands', value=name, inline=False)
    help_e.add_field(name='Formats', value=format)
    help_e.add_field(name="Speaker Time", value=time)
    help_e.add_field(name='POIs', value=poi)
    await author.send(embed=help_e)

@client.command()
async def start(ctx):
    global deb
    if deb.status == False:
        deb.status = True
        await ctx.send(f"Debate has been started by {ctx.author.mention}")
        asyncio.sleep(1)
        await ctx.send("Please set the format with `.format {format}`")
    elif deb.status == True:
        await ctx.send("A debate is already going on")    

@client.command()
async def format(ctx, format):
    global deb
    # If debate has started
    if deb.status == True:
        # If format has not been set yet
        if deb.format == 'NA':
            deb.format = format
            await ctx.send(f"Debate format set to {format} by {ctx.author.mention}")
        else:
            await ctx.send(f"Debate format has already been set to {deb.format}")
    else:
        await ctx.send("Debate has not started yet. Please start with `.start`")

@client.command()
async def end(ctx):
    global deb
    # If debate has not ended yet
    if deb.status == True:
        # Resets all parameters
        deb.status = False
        deb.format = 'NA'
        deb.reply = 'NA'
        deb.speaker = 'PM'
        deb.restart = False
        deb.speech = False
        # If a speech is going on, stop all timers
        if deb.speech == True:
            sleep.cancel_all()
            await asyncio.wait(sleep.tasks)
        await ctx.send(f"Debate has been ended by {ctx.author.mention}")
    else:
        await ctx.send("No debate going on to end")

@client.command()
async def speech(ctx):
    global deb
    global speakers
    # If speech has been restarted
    if deb.restart == True:
        deb.restart = False
    # If debate has started
    if (deb.status == True):
        # If format has been set
        if (deb.format != 'NA'):
            # If a speech has not been started
            if deb.speech == False:
                await ctx.send(f"I now invite the {deb.speaker} for their speech")
                deb.speech = True
                index = speakers[deb.format].index(deb.speaker)
                await sleep(60)
                if deb.status == True and deb.restart == False:
                    await ctx.send("POIs can be asked")
                    await sleep(5 * 60)
                    if deb.status == True and deb.restart == False:
                        await ctx.send("No more POIs")
                        await sleep(80)
                        if deb.status == True and deb.restart == False:
                            await ctx.send("Time up!")
                            # Need to set speech to false after speech is done
                            deb.speech = False
                # If it is not the last speaker
                if (deb.status == True) and deb.restart == False:
                    if index != len(speakers[deb.format]) - 1:
                        deb.speaker = speakers[deb.format][index + 1]
                    elif index == len(speakers[deb.format]) - 1:
                        deb.status = False
                        deb.speaker = 'PM'
                        deb.format = 'NA'
                        deb.reply = 'NA'
                        await ctx.send("The debate has finished")
            else:
                await ctx.send(f"{deb.speaker} has already started their speech")
        else:
            await ctx.send("The format has not been set. Please set it with `.format`")
    else:
        await ctx.send("The debate has not started. Please set it with `.start`")

@client.command()
async def restart(ctx):
    global deb
    # Can only restart a speech if a speech is going on
    if deb.speech == True:
        deb.restart = True
        deb.speech = False
        sleep.cancel_all()
        await asyncio.wait(sleep.tasks)
        await ctx.send(f"The {deb.speaker} may restart their speech")
    else:
        await ctx.send("No one is speaking")

@client.command()
async def restart_status(ctx):
    global deb
    await ctx.send(deb.restart)

@client.command()
async def stop(ctx):
    global deb
    global speakers
    # Speech can be stopped only if one is going on
    if deb.speech == True:
        deb.restart = True
        deb.speech = False
        sleep.cancel_all()
        index = speakers[deb.format].index(deb.speaker)
        await asyncio.wait(sleep.tasks)
        if index != len(speakers[deb.format]) - 1:
            await ctx.send(f"{deb.speaker} has finished their speech")
            deb.speaker = speakers[deb.format][index + 1]
        elif index == len(speakers[deb.format]) - 1:
            deb.status = False
            deb.speaker = 'PM'
            deb.format = 'NA'
            deb.reply = 'NA'
            await ctx.send("The debate has finished")
        
@client.command()
async def status(ctx):
    global deb
    if deb.status == True:
        embed = discord.Embed(title = 'Debate Status', colour = discord.Colour.blue(), description="Started")
        if deb.format != 'NA':
            embed.add_field(name='Format', value=deb.format)
            embed.add_field(name='Speaker', value=deb.speaker)
        else:
            embed.add_field(name='Format', value='To Be Set')
        await ctx.message.author.send(embed=embed)
    else:
        embed = discord.Embed(title='Debate Status', colour=discord.Colour.red(), description='Finished/Has not started')
        await ctx.message.author.send(embed=embed)


sleep = make_sleep()
client.run('NzUyODg5MzI2Mzc0ODc5MjU2.X1eM0w._JppyqlGEnZqDop2prNeJtYnPJs')