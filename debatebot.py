import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='.')
client.remove_command('help')

@client.event
async def on_ready():
    print("Bot is ready")

@client.command(aliases=['h', "help"])
async def _help(ctx):
    author = ctx.message.author
    help_e = discord.Embed(title='Debate Time Keeper Bot', color=discord.Color.green())
    name = ".start to start a debate\n.format {format} to set the debate format\n"
    format = "Formats are AP and BP\nIf AP, .reply to set if reply (Y/N)\n"
    time = "Speaker time is 7:20 per person"
    help_e.add_field(name='Description', value=name, inline=False)
    help_e.add_field(name='Formats', value=format)
    help_e.add_field(name="Speaker Time", value=time)
    await author.send(embed=help_e)

client.run('NzUyODg5MzI2Mzc0ODc5MjU2.X1eM0w.7-oN3tzEguiGTDxfsyYNr6p53sU')