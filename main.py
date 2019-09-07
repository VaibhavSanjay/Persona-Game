import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
from keep_alive import keep_alive
import os
import calendar
import datetime
import random
import math
import pytz
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from collections import OrderedDict
#from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS 
from steamwebapi import profiles
from urllib.parse import urlparse
import squarify
import re
import wolframalpha

def set_up_user_directory():
  import sys
  import site
  # this makes it work
  if not os.path.exists(site.USER_SITE):
    os.makedirs(site.USER_SITE)
    # since I'm installing with --user, packages
    # should be installed here,
    #so make sure it's on the path
    sys.path.insert(0, site.USER_SITE)

def install(package):
  set_up_user_directory()
  from pip._internal import main
  main(['install', package, "--upgrade"])

install("git+git://github.com/AWConant/jikanpy.git")

from jikanpy import Jikan
'''
import spotipy
import spotipy.util as util
print(spotipy.VERSION)
scope = 'user-read-currently-playing user-modify-playback-state'

token = util.prompt_for_user_token("9in0kmec0w7c94fn8tofp0mc0", scope)
if token:
  sp = spotipy.Spotify(auth=token)
  print(sp.current_user_playing_track())
else:
  print ("Can't get token")
'''


'''
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# track id: 3tX27xdHUiQpamL8RCTNXA
sp.user_playlist_add_tracks("9in0kmec0w7c94fn8tofp0mc0?si=rlwnEKGYQfmV4wk4k4XmfA", "0WQmOp058GX6eQS8uqv4er", ["3tX27xdHUiQpamL8RCTNXA"])
'''
'''
# Here, we're just importing both Beautiful Soup and the Requests library
page_link = 'https://eprp.fandom.com/wiki/Special:WikiActivity'
# this is the url that we've already determined is safe and legal to scrape from.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'cache-control': 'private, max-age=0, no-cache'
}
page_response = requests.get(page_link, timeout=5, headers=headers)
# here, we fetch the content from the url, using the requests library
page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

update_list = []
updates = page_content.find(id="myhome-activityfeed")
result1 = updates.findAll("cite")
result2 = updates.findAll("strong")
for i in range(0, len(result1)):
  update_list.append(result1[i].get_text())
  update_list.append(result2[i].get_text())
'''

Client = discord.Client()
client = commands.Bot(command_prefix = "rp!") # The prefix for starting commands will be "rp!". For example "rp!games"
client.remove_command('help') # To create a custom help command

hehe = { # The dictionary that provides data to firebase so that the database can be accessed.
  "type": os.environ.get("TYPE"), # All of these collect info from the environment variables. This is because some of this information must be hidden to keep the database private
  "project_id": os.environ.get("PROJECTID"),
  "private_key_id": os.environ.get("PRIVATEKEYID"),
  "private_key": os.environ.get('PRIVATEKEY').replace('\\n', '\n'),
  "client_email": os.environ.get("CLIENTEMAIL"),
  "client_id": os.environ.get("CLIENTID"),
  "auth_uri": os.environ.get("AUTHURI"),
  "token_uri": os.environ.get("TOKENURI"),
  "auth_provider_x509_cert_url": os.environ.get("AUTHPROVIDER"),
  "client_x509_cert_url": os.environ.get("CLIENTX")
}
# Fetch the service account key JSON file contents
cred = credentials.Certificate(hehe)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://personarp-91339.firebaseio.com/'
})

'''
Database is set up as follows:
personarp
  characters
    (Discord ids)
      arca -> str
      bonus -> str
      desc -> str
      elem -> str
      imag -> str
      level -> str
      name -> str
      pers -> str
      ranks -> str
      side -> str
  shops
    (All Shops Names) -> Link
  steam
    (Discord ids) -> str (Steam id #)
  users
    (Discord ids) -> List (Messages sent each day)
    server -> List (Messages sent each day)
  websites
    (Names of Site) -> Link
  wordclouds
    (Discord ids) -> str (All words said)
    server -> str (All words said)
'''


STAT_FILE_CONST = 11 # A constant that represents the number of lines of data in the file with character stats
skillFile = open("skills.txt", "r").readlines() # The file with all elements and moves
statFile = [] # A file that will contain stats of all characters
reqFile = [] # Will contain all of the requests to level up and buy stuff
helpFile = open("help.txt", "r").readlines() # Contains all the lines that will be used in the help command
siteFile = [] # A file with all of the websites that are stored
statusFile = open("status.txt", "r").readlines() # A file with all of the status affects
shopsFile = [] # Contains all of the links to the shops
ranksFile = open("ranks.txt", "r").readlines() # Contains all of the ranks that can be reached for secret stats
guideFile = open("help2.txt", "r").readlines() # A file with a guide to how to use the bot for the persona game
combatFile = open("combat.txt", "r").readlines() # A file with combat help

with open("reqlvl.txt", "r") as f:
  reqFile = f.readlines()

# Turn the stats database data into a list
data = db.reference("characters").get()
statFile.append(str(len(data)))
for key, value in data.items():
  statFile.append(key)
  statFile.append(value["name"])
  statFile.append(value["desc"])
  statFile.append(value["elem"])
  statFile.append(value["level"])
  statFile.append(value["bonus"])
  statFile.append(value["imag"])
  statFile.append(value["arca"])
  statFile.append(value["pers"])
  statFile.append(value["side"])
  statFile.append(value["ranks"])

# Turn the websites database data into a list
data = db.reference("websites").get()
siteFile.append(str(len(data)))
for key, value in data.items():
  siteFile.append(value)
  siteFile.append(key)

# Turn the shhops database data into a list
data = db.reference("shops").get()
shopsFile.append(str(len(data)))
for key, value in data.items():
  shopsFile.append(key)
  shopsFile.append(value)

# Strip whitespace
for i in range(len(skillFile)):
  skillFile[i] = skillFile[i].rstrip()
for k in range(len(reqFile)):
  reqFile[k] = reqFile[k].rstrip()
for b in range(len(statusFile)):
  statusFile[b] = statusFile[b].rstrip()
for a in range(len(ranksFile)):
  ranksFile[a] = ranksFile[a].rstrip()
for j in range(len(guideFile)):
  guideFile[j] = guideFile[j].rstrip()
for m in range(len(helpFile)):
  helpFile[m] = helpFile[m].rstrip()

mod_list = [274755261883744256, 362226117341609984] # List of people who can do mod commands
talk_user = None # Visit rp!talk
talk_channel = None # Visit rp!talk
mults = {"Miniscule": 0.5, "Light": 1.0, "Medium": 1.67, "Heavy": 2.33, "Severe": 3.0, "Colossal/Grave": 3.67} # Attack multipliers
elem_emotes = [":fire:", ":shaved_ice:", ":cloud_lightning:", ":dash:", ":boom:", "<:smart:546833109539094528>", ":angel:", ":smiling_imp:"] # Specific emotes for each element
flags = {"Neutral" : "https://cdn.discordapp.com/attachments/570799295159336962/583747727066923008/1280px-Flag_of_Japan.png", "Loyalist" : "https://cdn.discordapp.com/attachments/559563885829554226/583142995646218260/image0.jpg", "Survivalist" : "https://cdn.discordapp.com/attachments/559563885829554226/583144010290298881/Survivalist_Flag.png"} # Flags for each side in the war
lvl_rank = ['0'] # Gives an emoji corresponding to level, kind of like a "rank". Each index is a level and the corresponding rank at the level is in the index
bruiser_hp = [0] # List of hp for a bruiser at each level
bruiser_sp = [0] # List of sp for a bruiser at each level
arc_hp = [0] # List of hp for an arcanist at each level
arc_sp = [0] # List of sp for an arcanist at each level
exp_val = [0] # Experience needed to level up at this level
str_val = [0] # Strength at this number of str points
end_val = [0] # Endurance at this number of end points
agi_val = [0] # Agility at this number of agi points
luc_val = [0] # Luck at this number of luc points
arc_cur_hp = 104.5 # Helpful counters to be added to in the loop
arc_cur_sp = 36
str_cur = 30
agi_cur = 70
luc_cur = 8
for i in range(1, 34):
  arc_hp.append(int(arc_cur_hp)) # Add current values
  arc_sp.append(arc_cur_sp)
  str_val.append(str_cur)

  if (i % 2 == 1): # Alternating adding to strength
    str_cur += 5
  else:
    str_cur += 3

  # To add to the ranks at each level
  if (i <= 5):
    lvl_rank.append('<:akkosmug:557742653370925067>')
  elif (i <= 10):
    lvl_rank.append('<:trucysmile:536105440140984331>')
  elif (i <= 15):
    lvl_rank.append('<:monikaS:509887910867238914>')
  elif(i <= 20):
    lvl_rank.append('<:bigbrain:490748484169891841>')
  elif(i <= 25):
    lvl_rank.append('<:dip:573728403757465610>')
  elif(i <= 30):
    lvl_rank.append('<:akkogun:551969541874253824>')
  elif(i <= 32):
    lvl_rank.append('<:akkohuh:546438940799008770>')
  else:
    lvl_rank.append('<:dokihug:537798999701454850>')

  # These are the equations that are used to calculate the amount of each stat at each level
  bruiser_hp.append(int((1/20)*(i**2) + 3.5*i + 112))
  bruiser_sp.append(int((1/57)*(i**2) + 2*i + 28))
  end_val.append(int((1/5)*(i**2) + 0.9*i - 0.5))
  exp_val.append(int(8*(0.2*math.sin(i) + 2.1*math.sqrt(i) - 1)))

  arc_cur_hp += 3.5
  arc_cur_sp += 4

for j in range(1, 34): # Another loop needed for these guys
  agi_val.append(agi_cur)
  luc_val.append(luc_cur)
  if (j % 3 == 2):
    agi_cur += 1
    luc_cur += 1

exp_val[33] = 0 # Max level

calc_mem = OrderedDict() # Memory for calc. See rp!calc

data_ids = [] # IDs to be stored for the rp!talkdata command

days_recorded = len(db.reference("users/server").get()) # Total days recorded for rp!talkdata command

# Called when bot is ready
@client.event
async def on_ready():
  utc_now = pytz.utc.localize(datetime.datetime.utcnow()) # Get now
  est_now = utc_now.astimezone(pytz.timezone("America/New_York")) # Get est
  activity = discord.Game(name="Persona: Unity") # Set status of bot
  await client.change_presence(activity=activity)
  print("Bot is ready @ " + est_now.strftime("%Y-%m-%d %H:%M:%S")) # Ready message
  #await check_wiki_updates()

# Help command. Gives what bot can do.
@client.command(name = 'help', pass_context = True)
async def help(ctx, Name = None):
  page = 0
  if (Name):
    embed = discord.Embed(title="Commands", description=helpFile[0])
    for i in range(1, len(helpFile), 2):
      if (Name.lower() in helpFile[i].lower()):
        embed.add_field(name=helpFile[i], value=helpFile[i+1])
    await ctx.send(embed=embed)
  else:
    help_dic = dict()
    for i in range(1, len(helpFile), 2):
      parts = helpFile[i].split(" - ")
      help_dic.setdefault(parts[0], []).append(parts[1])

    embed = discord.Embed(title="All Commands", description=helpFile[0])
    for key, value in help_dic.items():
      embed.add_field(name=key, value=", ".join(value))

    await ctx.send(embed=embed)

# Guide for using this bot in the game
@client.command(name = 'guide', pass_context = True)
async def guide(ctx, Name = None):
  embed = discord.Embed(title=guideFile[0], description=guideFile[1])
  if (Name == None): # Send entire guide
    for i in range(2, len(guideFile), 2):
      embed.add_field(name=guideFile[i], value=guideFile[i+1])
    await ctx.send(embed=embed)
  else:
    for i in range(2, len(guideFile), 2): # Look Section titled with Name
      if Name.lower() in guideFile[i].lower():
        embed.add_field(name=guideFile[i], value=guideFile[i+1])
        await ctx.send(embed=embed)
        return
    await ctx.send("Could not find that part of the guide")

# A command used to find attacks of an element and status effects.
@client.command(name = 'library', pass_context = True)
async def library(ctx, *args):
    if (len(args) < 1): # Invalid nubmer of args
      await ctx.send("Specify an element.")
    elif (len(args) == 1): # An element or a status effect
      Arg = args[0].lower() # Get element name
      i = find_element(Arg, True) # Find the element in skillFile
      if i == -1: # Not an element
        j = find_status(Arg, True) # Find element in statusFile
        if j == -1: # Not a status either
          await ctx.send("Could not find an element or status effect with that name.")
          return
        lineNum = j*3 # jth status effect is located on the j*3 'th line
        embed = discord.Embed(title=statusFile[lineNum], description=statusFile[lineNum+1] + " ***Moves That Inflict This Status Effect:***")
        move_list = statusFile[lineNum + 2].split("-") # List of all moves that deal this effect
        for move in move_list: # Add each move into a list
          embed.add_field(name=":arrow_forward:  ", value="  **" + move + "**", inline=False)
        await ctx.send(embed=embed)
      else:
        lineNum = i*49 # ith element is located on the i*49 'th line
        embed = discord.Embed(title = skillFile[lineNum] + elem_emotes[i], description = skillFile[lineNum + 3]) # Title and Description
        embed.add_field(name = "**Type: **", value = skillFile[lineNum + 1] + "/" + skillFile[lineNum + 2], inline = False) # Type of fighter with this element
        interactions = skillFile[lineNum + 4].split() # Absorbs/Blocks/Resists/Weak
        embed.add_field(name = "**Absorbs: **", value = interactions[0], inline = True)
        embed.add_field(name = "**Block: **", value = interactions[1], inline = True)
        embed.add_field(name = "**Resists: **", value = interactions[2], inline = True)
        embed.add_field(name = "**Weak: **", value = interactions[3], inline = True)
        for j in range(11): # All moves
          lineNum2 = lineNum + 5 + j * 4 # Line with name of the move
          embed.add_field(name = "*" + skillFile[lineNum2 + 1] + ", level " + skillFile[lineNum2] + "*", value = "*" + skillFile[lineNum2 +2 ] + "*\n" + "`Cost: " + skillFile[lineNum2 + 3] + "`", inline = False)
        await ctx.send(embed = embed)
    elif (len(args) >= 2): # An element and the name of a move
      Elem = args[0].lower()
      Move = args[1].lower()
      i = find_element(Elem, True) # Find the element
      if i == -1:
        await ctx.send("Could not find that element.")
      else:
        lineNum = i*49 + 6 # Line with the first move of the element
        Found = False
        while(Found == False and lineNum < i*49 + 50): # Loop through each line
          if (Move in skillFile[lineNum].lower()): # If the move name given is part of the move on the line
            Found = True
            break # Found the move, we can break
          else:
            lineNum += 4 # Each move contains 4 lines of info, so we skip the lines that don't have the move name
        if (Found == False):
          await ctx.send("Could not find that move.")
        else:
          embed = discord.Embed(title = skillFile[lineNum], description = skillFile[lineNum + 1])
          embed.add_field(name = "Level: ", value = skillFile[lineNum - 1], inline = True) 
          embed.add_field(name = "Cost: ", value = skillFile[lineNum + 2], inline = True)  
          await ctx.send(embed = embed) 

# Function to give the amount of exp needed to go to the next level 
@client.command(name = 'expstats', pass_context = True)
async def expstats(ctx, lvl):
  try:
    int(lvl) # if it's not an int, then bad data
  except Exception:
    await ctx.send("Grrr.... :angry:")
    return
  embed = discord.Embed(title="XP For Next Level")
  for i in range(int(lvl) - 2, int(lvl) + 3): # 2 back and 2 in front
    if (i > 0 and i < 33):
      embed.add_field(name="Level " + str(i) + ":", value=str(exp_val[i]) + "XP", inline=False)
    elif(i == 33):
      embed.add_field(name="Level " + str(i) + ":", value=":rainbow_flag:XP", inline=False)
  await ctx.send(embed=embed)

# A command designed to show all of the stats of a player. No data left out.
@client.command(name = 'stats', pass_context = True)      
async def stats(ctx, *args):
  i = 0 # i reprresents which number the player is in the order on the database
  if (len(args) == 0): # Stats of the person who did the command
    i = find_player(mention_to_id(ctx.message.author.mention))
  elif (len(args) == 1): # Stats of the person in the arg (FName, LName, or @mention)
    i = find_player(mention_to_id(args[0]))
  else: # Stats of the person in 2 args (FName LName)
    i = find_player((args[0] + " " + args[1]).strip())
  if i == -1:
      await ctx.send("This player has not created a character. use `rp!createchar` to create one.")
  else:
    line = STAT_FILE_CONST*i + 1 # Line with the id of the person whos stats we are looking for
    userString = statFile[line] # User id
    mentioned_user = await client.fetch_user(userString) # Get a user from the id
    embed = discord.Embed(title=statFile[line + 1] + ", " + statFile[line+9], description="*"+statFile[line + 2]+"*") # Name, Side *Description*
    embed.set_thumbnail(url=flags[statFile[line+9]]) # Flag based on side
    embed.set_author(name=str(mentioned_user) + "'s character", icon_url=mentioned_user.avatar_url) # User's character with user's pfp
    embed.add_field(name="Element: ", value=statFile[line + 3] + elem_emotes[find_element(statFile[line + 3])], inline=False) # Element
    level = int(statFile[line + 4])
    embed.add_field(name=lvl_rank[level] + " Level " + str(level), value=str(exp_val[level]) + "XP Needed For Next Level", inline=False) # Level
    stats = statFile[line + 5].split() # Line with all of point stats
    embed.add_field(name="Arcana: ", value=statFile[line + 7], inline=True) # Arcana
    embed.add_field(name="Persona: ", value=statFile[line + 8], inline=True) # Persona
    if (isBruiser(statFile[line + 3])): # Find hp and sp based on whether element is bruiser or not
      embed.add_field(name = "Total HP: ", value = str(bruiser_hp[int(level)]), inline = True)
      embed.add_field(name = "Total SP: ", value = str(bruiser_sp[int(level)]), inline = True)
    else:
      embed.add_field(name = "Total HP: ", value = str(arc_hp[int(level)]), inline = True)
      embed.add_field(name = "Total SP: ", value = str(arc_sp[int(level)]), inline = True)
    # All of point stat data listed below
    embed.add_field(name="SAP: ", value=str(str_val[int(stats[0])]) + " (" + stats[0] + ")", inline=True)
    embed.add_field(name="MAP/MR: ", value=str(str_val[int(stats[1])]) + "/" + str(end_val[int(stats[1])]) + " (" + stats[1] + ")", inline=True)
    embed.add_field(name="ACC/EVA: ", value=str(agi_val[int(stats[3])]) + "%/" + str(agi_val[int(stats[3])] - 65) + "%" + " (" + stats[3] + ")", inline=True)
    embed.add_field(name="PR: ", value=str(end_val[int(stats[2])]) + " (" + stats[2] + ")" , inline=True)
    embed.add_field(name="CRT/CEVA: ", value=str(luc_val[int(stats[4])]) + "%/" + str(luc_val[int(stats[4])] - 6) + "%" + " (" + stats[4] + ")", inline=True)
    stats = statFile[line + 10].split()
    # Secret stats listed below. Only name of level is given (Not the number)
    embed.add_field(name="Knowledge", value=find_rank("kno", stats[0]), inline=True)
    embed.add_field(name="Guts", value=find_rank("gut", stats[1]), inline=True)
    embed.add_field(name="Proficiency", value=find_rank("pro", stats[2]), inline=True)
    embed.add_field(name="Kindness", value=find_rank("kin", stats[3]), inline=True)
    embed.add_field(name="Charm", value=find_rank("cha", stats[4]), inline=True)
    embed.set_image(url=statFile[line + 6]) # Image of character that was given
    await ctx.send(embed=embed)

# Creates a character for a user and holds the data in the database
@client.command(name = 'createchar', pass_context = True)      
async def createchar(ctx):
  def check1(m): # Check if message made by the one who initiated command
    return m.author == ctx.message.author

  def check2(m): # Check if the element could be found
    return check1(m) and (find_element(m.content) != -1 or m.content.lower() == "cancel")

  def check3(m): # Check if a valid side is given
    return check1(m) and (m.content.lower() == "loyalist" or m.content.lower() == "survivalist" or m.content.lower() == "neutral" or m.content.lower() == "cancel")

  def check4(m): # Check if the answer is yes or no
    return check1(m) and (m.content.lower() == "yes" or m.content.lower() == "no")

  # A function written to receive a message
  async def getmsg(num):
    try:
      if (num == 1):
        msg = await client.wait_for('message', check=check1, timeout=30.0)
      if (num == 2):
        msg = await client.wait_for('message', check=check2, timeout=30.0)
      if (num == 3):
        msg = await client.wait_for('message', check=check3, timeout=30.0)
      if (num == 4):
        msg = await client.wait_for('message', check=check4, timeout=30.0)
    except asyncio.TimeoutError: # If the message times out
      await ctx.send("Timed out.")
      return "cancel"
    else:
      return msg.content

  j = find_player(mention_to_id(ctx.message.author.mention)) # If the player made a character, finds their position
  cur_level = ""
  cur_bonus = ""
  cur_ranks = ""
  keep = True # Whether to keep point stats
  if (j != -1): # A character for this user exists
    await ctx.send("You already have a character, are you sure you want to overwrite them?")
    if ((await getmsg(4)).lower() == "yes"):
      await ctx.send("Would you still like to keep your old stats?")
      if ((await getmsg(4)).lower() == "yes"):
        await ctx.send("You keep the stats, but now you will start the creation process.")
        # Set stats to what they are when things are rewritten
        cur_level = statFile[j*STAT_FILE_CONST + 5]
        cur_bonus = statFile[j*STAT_FILE_CONST + 6]
        cur_ranks = statFile[j*STAT_FILE_CONST + 11]
      else:
        await ctx.send("Ok, but just for reference, the bonus stats you had (including the starting stats) are:")
        keep = False # We are not keeping old stats
        await ctx.send(statFile[STAT_FILE_CONST*j + 6])
    else:
      await ctx.send("Ok then.")
      return

  # Now follows a series of questions that the user must answer to store their data
  await ctx.send("You are about to go through the process of adding your character data for this bot to use. If at any time you wish to stop, type cancel and the bot will stop. Waiting for over 30 seconds without writing your answer will also cause the process to cancel.")
  await ctx.send("Type cancel to stop, or anything else to proceed:")
  Confirm = (await getmsg(1)).title()
  if Confirm.lower() == "cancel":
    return

  await ctx.send("What is your character's name?")
  Name = (await getmsg(1)).title()
  if (Name.lower() == "cancel"):
    return
  await ctx.send("What is your character's element?")
  Elem = (await getmsg(2)).title() # Check if element exists
  if (Elem.lower() == "cancel"):
    return
  await ctx.send("Give a description of your character. (You can use multiple sentences but **do not** use SHIFT+ENTER to create multiple lines.")
  Desc = (await getmsg(1))
  if (Desc.lower() == "cancel"):
    return
  await ctx.send("What Arcana does your character represent?")
  Arca = (await getmsg(1)).title()
  if (Arca.lower() == "cancel"):
    return
  await ctx.send("What is the name of your character's Persona?")
  Pers = (await getmsg(1)).title()
  if (Pers.lower() == "cancel"):
    return
  await ctx.send("What side is your character on? (loyalist, survivalist or neutral)")
  Side = (await getmsg(3)).title() # Check if a valid side is given
  if (Side.lower() == "cancel"):
    return
  await ctx.send("Send an image of your character and their persona!")
  Imag = await getmsg(1)
  if (Imag.lower() == "cancel"):
    return

  if (j != -1): # This user already made a character
    line = STAT_FILE_CONST*j
    statFile[line + 1] = mention_to_id(ctx.message.author.mention) # Get users id
    statFile[line + 2] = Name
    statFile[line + 3] = Desc
    statFile[line + 4] = Elem
    if (keep): # If we a re keeping old stats
      statFile[line + 5] = cur_level
      statFile[line + 6] = cur_bonus
      statFile[line + 11] = cur_ranks
    else:
      statFile[line + 5] = "1" # Everyone starts as level 1
      if (isBruiser(Elem)):
        statFile[line + 6] = "3 1 2 2 1" # Base stats for bruiser
      else:
        statFile[line + 6] = "1 3 1 2 2" # Base stats for non bruiser
      statFile[line + 11] = "0 0 0 0 0" # Secret stats
    statFile[line + 7] = Imag
    statFile[line + 8] = Arca
    statFile[line + 9] = Pers
    statFile[line + 10] = Side

    # Set everything into the database
    ref = db.reference("characters/" + mention_to_id(ctx.message.author.mention))
    ref.update({
      'name': statFile[line + 2],
      'desc': statFile[line + 3],
      'elem': statFile[line + 4],
      'level': statFile[line + 5],
      'bonus': statFile[line + 6],
      'imag': statFile[line + 7],
      'arca': statFile[line + 8],
      'pers': statFile[line + 9],
      'side': statFile[line + 10],
      'ranks': statFile[line + 11]
    })
  else:
    statFile.append(mention_to_id(ctx.message.author.mention))
    statFile.append(Name)
    statFile.append(Desc)
    statFile.append(Elem)
    statFile.append("1") # Everyone starts at level 1
    if (isBruiser(Elem)):
      statFile.append("3 1 2 2 1") # Base stats for bruiser
    else:
      statFile.append("1 3 1 2 2") # Base stats for non bruiser
    statFile.append(Imag)
    statFile.append(Arca)
    statFile.append(Pers)
    statFile.append(Side)
    statFile.append("0 0 0 0 0") # Secret stats
    statFile[0] = str(int(statFile[0]) + 1)

    # Set everything into the database
    ref = db.reference("characters")
    ref.child(mention_to_id(ctx.message.author.mention)).set({
      'name': Name,
      'desc': Desc,
      'elem': Elem,
      'level': "1",
      'bonus': "3 1 2 2 1" if isBruiser(Elem) else "1 3 1 2 2",
      'imag': Imag,
      'arca': Arca,
      'pers': Pers,
      'side': Side,
      'ranks': "0 0 0 0 0"
    })
    
  outF = open("stats.txt", 'w')
  for line in statFile:
    outF.write(line)
    outF.write("\n")
  outF.close()

  await ctx.send("Your character has been created! Use `rp!stats` to check your stats!")

# Get stats for each different class at each level
@client.command(name = 'lvlstats', pass_context = True)      
async def lvlstats(ctx, level):
  embed = discord.Embed(title="Level " + level + " stats")
  embed.add_field(name="Bruiser: ", value=str(int(bruiser_hp[int(level)])) + "/" + str(int(bruiser_sp[int(level)])), inline=False)
  embed.add_field(name="Arcanist: ", value=str(int(arc_hp[int(level)])) + "/" + str(int(arc_sp[int(level)])), inline=False)
  embed.add_field(name="Healer: ", value=str(int(arc_hp[int(level)])) + "/" + str(int(arc_sp[int(level)])), inline=False)
  await ctx.send(embed=embed)

# Get stats for each point stat at every number of points
@client.command(name = 'ptstats', pass_context = True)      
async def ptstats(ctx, level):
  embed = discord.Embed(title=level + " point stats")
  embed.add_field(name="SAP & MAP: ", value=str(str_val[int(level)]), inline=False)
  embed.add_field(name="PR & MR: ", value=str(end_val[int(level)]), inline=False)
  embed.add_field(name="ACC/EVA: ", value=str(agi_val[int(level)]) + "%/" + str(agi_val[int(level)] - 65) + "%", inline=False)
  embed.add_field(name="CRT/CEVA: ", value=str(luc_val[int(level)]) + "%/" + str(luc_val[int(level)] - 6) + "%", inline=False)
  await ctx.send(embed=embed)

# The command used to level up a character
@client.command(name = 'lvlup', pass_context = True)      
async def lvlup(ctx, user = None, lvl = "-1", *args):
  if (not ctx.message.author.id in mod_list): # You cannot level someone up without having a mod permission
    await ctx.send("You don't have permission.")
    return
  if (user == None): # You have to specify a user to level up
    await ctx.send("Please specify a user.")
    return
  i = find_player(mention_to_id(user)) # Try and find the user
  if (i == -1):
    await ctx.send("This user has not created a character.")
    return
  
  bonus = [] # Bonuses for stats
  if (lvl != "-1"): # Leveling up to a specific level
    if (len(args) != 5): # In writing the specific level you want to go to, you also have to specify the point stats
      await ctx.send("Send the point values of the five stats in order after the level as arguments.")
      return
    for thing in args:
      try: # Checking if its an integer
        int(thing)
      except Exception:
        await ctx.send("Send integers only.")
        return
    statFile[STAT_FILE_CONST*i + 6] = " ".join(args) # Join the args into a string with them seperated by spaces
    statFile[STAT_FILE_CONST*i + 5] = str(max(1, min(33, int(lvl)))) # Set the level to the level given
  else: # Regular level up
    statFile[STAT_FILE_CONST*i + 5] = str(int(statFile[STAT_FILE_CONST*i + 5]) + 1) # Change level by 1
    if (isBruiser(statFile[STAT_FILE_CONST*i + 4])):
      for j in range(0, 3):
        bonus.append(bruiser_level()) # Create a list of stats to level up for a bruiser
    else:
      for k in range(0, 3):
        bonus.append(arc_level()) # Create a list of stats to level up for an arcanist or healer
    cur_bonus = statFile[STAT_FILE_CONST*i + 6].split() # The bonuses already gotten
    for a in range(0, 3):
      cur_bonus[bonus[a]] = str(int(cur_bonus[bonus[a]]) + 1) # Added the bonus stats to what is already had
    statFile[STAT_FILE_CONST*i + 6] = " ".join(cur_bonus) # Join together again with spaces in between

  # Update everything into the database
  ref = db.reference("characters/" + mention_to_id(statFile[STAT_FILE_CONST*i + 1]))
  ref.update({
      "bonus": statFile[STAT_FILE_CONST*i + 6],
      "level": statFile[STAT_FILE_CONST*i + 5]
  })
  userString = statFile[STAT_FILE_CONST*i + 1] # User being leveled up
  tag = await client.fetch_user(int(userString))
  # Removing a request from the user to level up
  for j in range(0, len(reqFile), 3):
    if reqFile[j] == userString and reqFile[j + 2] == "0":
      reqFile.pop(j) # Remove the three lines representing the request
      reqFile.pop(j)
      reqFile.pop(j)

  await ctx.send("<a:gifmenacing:550916104034189323> Congratulations " + tag.mention + ", you leveled up! <a:gifmenacing:550916104034189323>")
  if (lvl == "-1"): # Regular level up means we tell the user what stats they got in the bonus
    await ctx.send("Your bonus points went toward " + point_def(bonus[0]) + ", " + point_def(bonus[1]) + " and " + point_def(bonus[2]))

# When you need to request a level up
@client.command(name = 'reqlvl', pass_context = True)      
async def reqlvl(ctx):
  for j in range(0, len(reqFile), 3): # Check if a level up was already requested
    if reqFile[j] == ctx.message.author and reqFile[j + 2] == "0":
      await ctx.send("You have already requested a level up. Wait for it to be granted.")
      return
  if(find_player(mention_to_id(ctx.message.author.mention)) == -1): # Check if this is a player
    await ctx.send("You are not a user right now. Become one with `rp!createchar`")
    return
  reqFile.append(str(ctx.message.author.id)) # Append id
  reqFile.append("@ " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Append time requested
  reqFile.append("0") # Append a zero to represent this as a level up request

  # Write to the file
  outF = open("reqlvl.txt", 'w')
  for line in reqFile:
    outF.write(line)
    outF.write("\n")
  outF.close()

  await ctx.send("Level up requested. <a:trucyexcited:566040963567321108>")

# Request to buy a certain item from the store
@client.command(name = 'reqbuy', pass_context = True)      
async def reqbuy(ctx, *args):
  if(find_player(mention_to_id(ctx.message.author.mention)) == -1): # Player not found
    await ctx.send("You are not a user right now. Become one with `rp!createchar`")
    return
  if(not args): # No args passed
    await ctx.send("Specify the items you want to buy.")
    return
  reqFile.append(str(ctx.message.author.id)) # Player id
  reqFile.append("@ " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Time requested
  reqFile.append(", ".join(args)) # All the things that were requested to buy

  # Write to the file
  outF = open("reqlvl.txt", 'w')
  for line in reqFile:
    outF.write(line)
    outF.write("\n")
  outF.close()

  await ctx.send("Items requested! :shopping_cart: ")

# Delete all of the buy requests
@client.command(name = 'reqbuydel', pass_context = True)      
async def reqbuydel(ctx):
  if not ctx.message.author.id in mod_list: # A mod only command
    await ctx.send("You don't have permission.")
    return
  for j in range(0, len(reqFile), 3): # Delete the lines representing the buy
    if reqFile[j + 2] != "0": # If it ends in 0, it represents a level up request
      reqFile.pop(j)
      reqFile.pop(j)
      reqFile.pop(j)

  # Write to file
  outF = open("reqlvl.txt", 'w')
  for line in reqFile:
    outF.write(line)
    outF.write("\n")
  outF.close()

  await ctx.send("Shop requests deleted.")
  
# Get this list of things that were requested
@client.command(name = 'reqlist', pass_context = True)      
async def reqlist(ctx):
  embed = discord.Embed(title="temp")
  if (len(reqFile) == 0): # Nothing is requested
    embed = discord.Embed(title="All Requests", description="Empty. All caught up!")
  else: # Some stuff is requested
    embed = discord.Embed(title="All Requests")
    for i in range(0, len(reqFile), 3): # Look at the head of each request
      user_id = reqFile[i]
      a = find_player(user_id)
      tag = await client.fetch_user(user_id) # Get the user
      if (reqFile[i + 2] == "0"): # This is a level up request
        embed.add_field(name=str(tag) + ", " + statFile[STAT_FILE_CONST*a + 2] + " to level " + str(int(statFile[STAT_FILE_CONST*a + 5]) + 1), value=reqFile[i+1], inline = False)
      else: # This is a shop buy request
        embed.add_field(name=str(tag) + ", " + statFile[STAT_FILE_CONST*a + 2] + " bought *" + reqFile[i + 2] + "*", value=reqFile[i+1], inline = False)
    embed.set_footer(text="Time is in UTC")
  await ctx.send(embed=embed)

# Delete the entire request list
@client.command(name = 'reqlistdel', pass_context = True)      
async def reqlistdel(ctx):
  if not ctx.message.author.id in mod_list: # Only mods can do this
    await ctx.send("You don't have permission.")
    return
  for i in range(0, len(reqFile)):
    reqFile.pop(0) # Delete each item
  await ctx.send("Request List Deleted.")

# List all of the players who registered
@client.command(name = 'allplayers', pass_context = True)      
async def allplayers(ctx):
  embed = discord.Embed(title="All Players Listed", description="Player Count: " + statFile[0])
  for i in range(0, int(statFile[0])): # Loop goes through each player
    userString = statFile[STAT_FILE_CONST*i + 1] # User id
    user = await client.fetch_user(userString) # Find the user
    embed.add_field(name=user, value=statFile[STAT_FILE_CONST*i + 2], inline=False) # Write the user and the name of their character
  await ctx.send(embed=embed)

# Add a link that can be searched for
@client.command(name = 'addlink', pass_context = True)      
async def addlink(ctx, link, *args):
  if link in siteFile: # Link is in the file with all the sites
    await ctx.send("This link has already been added.")
    return
  siteFile.append(link) # Add the link
  siteFile.append(" ".join(args).title()) # Add the title
  siteFile[0] = str(int(siteFile[0]) + 1) # ADd 1 to the number of sites added

  # Update database
  ref = db.reference("websites")
  ref.child(" ".join(args).title()).set(link)

  await ctx.send("Website added! ID = " + str(int(siteFile[0])) + " <a:trucybounce:542845961890824222>")

# Search for a link
@client.command(name = 'search', pass_context = True)   
async def search(ctx, *args):
  site_list = []
  for i in range(2, len(siteFile), 2): # Look through each title
    for word in args: # Each word in the argument
      if word.lower() in siteFile[i].lower(): # Check keywords
        site_list.append(i) # Add the index
        break
        
  embed = discord.Embed()
  if not site_list: # Nothing found
    embed = discord.Embed(title="Search Results", description="No results for " + " ".join(args) + " <a:revivebro:567571082970923008>")
  else: # Stuff found
    embed = discord.Embed(title="Search Results", description=str(len(site_list)) + " results found for " + " ".join(args))
    for site in site_list: # For everything found
      embed.add_field(name=siteFile[site], value=siteFile[site - 1] + "\n" + "Remove ID = " + str(site/2), inline=False) # Add the title and site, along with a number representing its id
  await ctx.send(embed=embed)

# Removes a link from the search
@client.command(name = 'removelink', pass_context = True)   
async def removelink(ctx, id):
  try: # Check if the number entered is valid
    if (int(id) > int(siteFile[0])):
      await ctx.send("No link has this ID")
      return
  except ValueError:
    await ctx.send("Please type a number <:emauh:559193530187382788>")
    return
  
  # Take off the title and the link
  siteFile.pop(int(id)*2 - 1)
  name = siteFile.pop(int(id)*2 - 1)
  siteFile[0] = str(int(siteFile[0]) - 1) # Lower the number of links by 1

  db.reference("websites/" + name).delete() # Delete from the database

  await ctx.send("Link removed! <a:haram:563065825947549744>")

# List of all of the links
@client.command(name = 'linklist', pass_context = True)   
async def linklist(ctx):
  embed = discord.Embed(title = "All Links")
  for i in range(1, len(siteFile), 2): # Loop through and add each title and link
    embed.add_field(name=siteFile[i+1], value=siteFile[i] + "\n" + "Remove ID = " + str((i + 1)/2), inline=False)
  await ctx.send(embed=embed)

# Add a shop to the list of shops
@client.command(name = 'addshop', pass_context = True)   
async def addshop(ctx, link, *args):
  if (ctx.message.author.id in mod_list): # Only for mods
    if (link in shopsFile): # Check if the shop is already in
      await ctx.send("That shop has already been added")
      return

    # Add the shop
    shopsFile.append((" ".join(args)).title())
    shopsFile.append(link)
    shopsFile[0] = str(int(shopsFile[0]) + 1) # Add 1 to number of shops

    # Add shop to the database
    ref = db.reference("shops")
    ref.child((" ".join(args)).title()).set(link)

    await ctx.send("Shop added!")
  else:
    await ctx.send("You don't have permission, bro :flushed:")

# Search for a shop or display all shops
@client.command(name = 'shops', pass_context = True)   
async def shops(ctx, name = None):
  if (name == None): # No args, list all shops
    embed = discord.Embed(title="All Shops", description="All the shops that can be visited. Please do not visit shops that you do not know about. Thank you! <:SmileChamp:587464108799033355>")
    for i in range(1, int(shopsFile[0])*2, 2): # Loop through the title of each shop
      embed.add_field(name=shopsFile[i], value=shopsFile[i + 1])
    await ctx.send(embed=embed)
  else: # A shop was provided as an arg
    Found = False
    for i in range(1, int(shopsFile[0])*2, 2): # Loop through the title of each shop
      if (name.lower() in shopsFile[i].lower()): # The arg searched for is in the shop name
        Found = True
        break # We found the index so break
    if (Found): # If a shop was found
      embed = discord.Embed(title=shopsFile[i], description=shopsFile[i + 1])
      await ctx.send(embed=embed)
    else:
      await ctx.send("Could not find that shop. :shrug:")

# Remove a shop from the list of shops
@client.command(name = 'removeshop', pass_context = True)   
async def removeshop(ctx, name = None):
    if (name == None): # No args, invalid
      await ctx.send("Please specify the shop to delete.")
      return
    for i in range(1, int(shopsFile[0])*2, 2): # Loop through each shop and search for the one that should be removed
      if (name.lower() == shopsFile[i].lower()):
        Found = True
        break # The shop was found so break
    if (Found):
      name = shopsFile.pop(i) # The name of the shop that was removed
      shopsFile.pop(i) # Pop the link as well
      shopsFile[0] = str(int(shopsFile[0]) - 1) # Decrement the number of shops

      db.reference("shops/" + name).delete()

      await ctx.send("Shop Removed!")
    else:
      await ctx.send("Could not find that shop. :shrug:")

# The number of points needed for a rank stat (secret stat)
@client.command(name = 'rankstats', pass_context = True)   
async def rankstats(ctx, Name = None):
  if (not ctx.message.author.id in mod_list): # This is info for only mods
    await ctx.send("You do not have permission.")
  if (Name == None): # No args, invalid
    await ctx.send("Please supply the name of a stat")
    return
  for i in range(0, len(ranksFile), 6): # Look at each rank in the file
    if Name.lower() == ranksFile[i].lower()[:min(len(Name), len(ranksFile[i].lower()))]: # Same as if name is something that ranksFile[i] starts with
      embed = discord.Embed(title=ranksFile[i])
      for j in range(1, 6): # Look at each individual level
        line = ranksFile[i+j].split()
        embed.add_field(name=line[0], value=line[1] + " pts") # Send the points needed
      await ctx.message.author.send(embed=embed)
      await ctx.send("Sent to DMs!")
      return
  await ctx.send("Could not find that stat.")

# Add rank stat points to a player
@client.command(name = 'addrank', pass_context = True)   
async def addrank(ctx, stat = None, num = None, *args):
  if (ctx.message.author.id not in mod_list): # Only for mods
    await ctx.send("You don't have permission.")
    return
  if (stat == None): # The stat to increase is None
    await ctx.send("Please specify the stat to increase by an amount and the player to add the stat to.")
    return
  if (num == None): # The amount to increase it by is None
    await ctx.send("Please specify the amount to increase by and the player to add the stat to.")
    return
  if (len(args) == 0): # The name of the player to add the stats to
    await ctx.send("Please specify the player to add the stat to.")
    return
  stats = ["knowledge", "guts", "proficiency", "kindness", "charm"]
  j = find_player(" ".join(args)) # j is the player that was found
  if (j == -1): # Player not found
    await ctx.send("This player has not registered. Use `rp!createchar` to register with the bot.")
    return
  rankLine = statFile[STAT_FILE_CONST*j + 11].split() # The line with all of the players stats
  start = ""
  end = ""
  Found = False
  for i in range(0, 5):
    if stat.lower() == stats[i].lower()[:min(len(stat), len(stats[i].lower()))]: # The stat being added to is equal to the front part of the actual stat
      start = find_rank(stats[i], rankLine[i]) # Find the rank for a certain stat and point amount
      rankLine[i] = str(int(rankLine[i]) + int(num)) # Add the amount to the rank
      end = find_rank(stats[i], rankLine[i]) # The rank after adding the points
      Found = True
      break # We can break because we added and found the rank
  if (not Found):
    await ctx.send("Could not find that stat.")
    return
  statFile[STAT_FILE_CONST*j + 11] = " ".join(rankLine) # New value for the points
  db.reference("characters/" + statFile[STAT_FILE_CONST*j + 1]).update({
    'ranks': statFile[STAT_FILE_CONST*j + 11]
  })
  await ctx.send("Rank Updated!")
  if (start != end): # If the player leveld up in rank
    user = await client.fetch_user(statFile[STAT_FILE_CONST*j + 1])
    await ctx.send("Congratulations " + user.mention + ", your character's " + stats[i].title() + " leveled up to " + end.title() + "!")

# A command to show the games that everyone in the server is playing
@client.command(name = 'games', pass_context = True)   
async def games(ctx):
  embed = discord.Embed(title="Players online")
  # A function to add a user to the list of users that will be displayed
  def add(user):
    act = user.activity # The user's activity
    if (act != None and act.name == "Attorney Online 2"):
      playing = datetime.datetime.utcnow() - act.start
      hours = playing.seconds // 3600
      minutes = (playing.seconds - hours * 3600) // 60
      name = act.state[11:] 
      embed.add_field(name=str(user), value="Playing as ||" + name + "|| in __" + act.details + "__ for " + str(hours) + " hours and " + str(minutes) + " minutes.")
    elif (act != None):
      if (act.start != None):
        playing = datetime.datetime.utcnow() - act.start
        hours = playing.seconds // 3600
        minutes = (playing.seconds - hours * 3600) // 60 
        embed.add_field(name=str(user), value="Playing __" + act.name + "__ for " + str(hours) + " hours and " + str(minutes) + " minutes.")
      else:
        embed.add_field(name=str(user), value="Playing __" + act.name + "__")

  eurae_law = client.get_guild(490714402287386626)
  for i in eurae_law.members:
    if (not i.bot):
      add(i)
  
  await ctx.send(embed=embed)

@client.command(name = 'talk', pass_context = True)   
async def talk(ctx, chan = "490732477766172692"):
  def che(msg):
    return msg.author == ctx.message.author and msg.channel == ctx.message.channel

  if ctx.message.author.id not in mod_list: return
  await ctx.send("You wanna have a little fun, huh. Fine. (Type 'stop' to stop this nonsense)")

  channel = None
  try:
    channel = client.get_channel(int(chan))
  except Exception:
    eurae_law = client.get_guild(490714402287386626)
    channel = discord.utils.find(lambda m: chan in m.name, eurae_law.channels)

  global talk_user
  talk_user = ctx.message.channel
  global talk_channel 
  talk_channel = channel

  async with channel.typing():
    await ctx.send("Type:")
    inp = await client.wait_for("message", check=che)
    while(inp.content != "stop"):
      await channel.send(inp.content)
      await ctx.send("Type:")
      inp = await client.wait_for("message", check=che)
  talk_user = None
  talk_channel = None

@client.event
async def on_message(message):
  if(client.user.mentioned_in(message) and not message.mention_everyone and talk_user == None):
    await message.channel.send("<a:trucybounce:542845961890824222>")
  if (talk_user != None):
    if (message.channel == talk_channel and message.author != client.user):
      await talk_user.send(str(message.author) + ": " + message.content)
  '''
  #Fix this for new people who say stuff
  if str(message.author.id) in db.reference("users").get().keys():
    ref = db.reference("users/" + str(message.author.id))
    length = len(ref.get())
    db.reference("users/" + str(message.author.id)).update({
      length - 1 : ref.get()[length - 1] + 1
    })
  else:
    ref = db.reference("users").child(str(message.author.id)).set({
      0 : 1
    })

  ref = db.reference("users/server")
  length = len(ref.get())
  ref.update({
    length - 1 : ref.get()[length - 1] + 1
  })

  
  now = datetime.datetime.utcnow()
  #update the times variable in the database
  ref = db.reference("users/times/" + str(now.hour))
  ref.update({
    now.minute : ref.get()[now.minute] + 1
  })

  if (message.content[:3] != "rp!" and not message.author.bot):
    words = remove_links(message.content)
    if str(message.author.id) in db.reference("wordclouds").get().keys():
      ref = db.reference("wordclouds")
      added = ""
      if (len(ref.child(str(message.author.id)).get().split(" ")) > 1000):
        added = ref.child(str(message.author.id)).get().split(" ", 1)[1] + words.replace("\n", " ")
      else:
        added = ref.child(str(message.author.id)).get() +  " " + words.replace("\n", " ")
      ref.update({
        str(message.author.id) : added
      })
    else:
      db.reference("wordclouds").update({
        str(message.author.id) : words.replace("\n", " ")
      })

    ref = db.reference("wordclouds")
    ref.update({
      "server" : ref.child("server").get().split(" ", 1)[1] + " " + words.replace("\n", " ")
    })
  
  ref = db.reference("channels")
  if str(message.channel.id) in ref.get().keys():
    sref = ref.child(str(message.channel.id))
    length = len(sref.get())
    sref.update({
      0 : sref.child("0").get() + 1,
      length - 1 : sref.get()[length - 1] + 1
    })
  else:
    ref.child(str(message.channel.id)).set({
      0 : 1,
      1 : 1
    })
  '''
  await client.process_commands(message)

def remove_links(value):
  words = value.split(" ")
  i = 0
  while i < len(words):
    if (urlparse(words[i]).scheme != "" and urlparse(words[i]).netloc != ""):
      del words[i]
    else:
      i += 1
  return " ".join(words)


@client.command(name = 'combathelp', pass_context = True)
async def combathelp(ctx, Name = None):
  embed = discord.Embed(title="Combat Help", description="Help for when you are in a fight.")
  if (Name == None):
    for i in range(0, len(combatFile), 2):
      embed.add_field(name=combatFile[i], value=combatFile[i+1])
    await ctx.send(embed=embed)
  else:
    for i in range(2, len(combatFile), 2):
      if Name.lower() in combatFile[i].lower():
        embed.add_field(name=combatFile[i], value=combatFile[i+1])
        await ctx.send(embed=embed)
        return
    await ctx.send("Could not find that part.")

@client.command(name = 'socialstats', pass_context = True)
async def secretstats(ctx, *args):
  if (ctx.message.author.id not in mod_list):
    await ctx.send("You do not have permission.")
    return
  i = 0
  if (len(args) == 0):
    i = find_player(mention_to_id(ctx.message.author.mention))
  elif (len(args) == 1):
    i = find_player(mention_to_id(args[0]))
  else:
    i = find_player((args[0] + " " + args[1]).strip())

  if (i == -1):
    await ctx.send("Could not find this player.")
    return

  stats = statFile[STAT_FILE_CONST*i + 11].split()
  embed = discord.Embed(title="Social Stats For " + statFile[STAT_FILE_CONST*i + 2])
  embed.add_field(name="Knowledge", value=stats[0], inline=False)
  embed.add_field(name="Guts", value=stats[1], inline=False)
  embed.add_field(name="Proficiency", value=stats[2], inline=False)
  embed.add_field(name="Kindness", value=stats[3], inline=False)
  embed.add_field(name="Charm", value=stats[4], inline=False)

  await ctx.message.author.send(embed=embed)
  await ctx.send("Sent to DMS!")

@client.command(name = 'calc', pass_context = True)
async def calc(ctx, *args):
  if (len(args) == 0):
    embed = discord.Embed(title = "Damage Multipliers", description = "Damage scales like this:")
    for key, value in mults.items():
      embed.add_field(name = key + ": ", value = "`" + str(value) + "x AP`", inline = False)
    await ctx.send(embed=embed) 
  if (len(args) == 1):
    embed = discord.Embed(title = "Damage Multipliers", description = "Damage scales like this:")
    for key, value in mults.items():
      if (args[0].lower() in key.lower()):
        embed.add_field(name = key + ": ", value = "`" + str(value) + "x AP`", inline = False)
        break
    await ctx.send(embed=embed)
  if (len(args) == 2):
    extra = ""
    dmg = 0
    try:
      dmg = int(args[1])
      extra = args[1] + " damage "
    except Exception:
      i = find_player(str(ctx.message.author.id))
      if (i == -1):
        await ctx.send("This player has not created a character.")
        return
      stats = statFile[STAT_FILE_CONST*i + 6].split()
      if (args[1].lower() == "sap"):
        dmg = str_val[int(stats[0])]
        extra = "SAP "
      else:
        dmg = str_val[int(stats[1])]
        extra = "MAP " 
    for key, value in mults.items():
      if args[0].lower() == key.lower()[:len(args[0])]:
        await ctx.send("Your " + extra + "attack does " + str(dmg) + " x " + str(value) + " damage = " + str(value*dmg) + " damage.")
        calc_mem[ctx.message.content] = value*dmg
        return
    await ctx.send("Couldn't find that type of attack.")
  if (len(args) == 3):
    i = find_player(str(args[2]))
    if (i == -1):
        await ctx.send("This player has not created a character.")
        return
    stats = statFile[STAT_FILE_CONST*i + 6].split()
    if (args[1].lower() == "sap"):
      dmg = str_val[int(stats[0])]
      extra = "SAP "
    else:
      dmg = str_val[int(stats[1])]
      extra = "MAP " 
    for key, value in mults.items():
      if args[0].lower() == key.lower()[:len(args[0])]:
        await ctx.send(statFile[STAT_FILE_CONST*i + 2] + "'s " + extra + "attack does " + str(dmg) + " x " + str(value) + " damage = " + str(value*dmg) + " damage.")
        calc_mem[ctx.message.content] = value*dmg
        return
    await ctx.send("Couldn't find that type of attack.")

@client.command(name = 'mem', pass_context = True)
async def mem(ctx, num = None):
  embed = discord.Embed(title="Memory")
  if (not calc_mem):
    embed.add_field(name="Nothing in memory", value = ":heavy_plus_sign:")
  try:
    embed.add_field(name=calc_mem.keys()[int(num)], value=calc_mem.keys()[int(num)])
    await ctx.send(embed=embed)
  except Exception:
    i = 1
    for key, value in calc_mem.items():
      embed.add_field(name=str(i) + ". " + key, value=value, inline=False)
      i += 1
    await ctx.send(embed=embed)

@client.command(name = 'clearmem', pass_context = True)
async def clearmem(ctx):
  calc_mem.clear()
  await ctx.send("Memory Cleared!")

@client.command(name = 'phys', pass_context = True)
async def phys(ctx, percent, h = None):
  if (h == None):
    i = find_player(str(ctx.message.author.id))
    if (i == -1):
      await ctx.send("You are not a player. Register with `rp!createchar`")
      return
    health = 0
    if (isBruiser(statFile[STAT_FILE_CONST*i + 4])):
      health = bruiser_hp[int(statFile[STAT_FILE_CONST*i + 5])]
    else:
      health = arc_hp[int(statFile[STAT_FILE_CONST*i + 5])]
    await ctx.send(percent + "% of your health is " + str(health * int(percent)/100))
    calc_mem[ctx.message.content] = health * int(percent)/100
  else:
    try:
      int(h)
      await ctx.send(percent + "% of your health is " + str(int(h) * int(percent)/100))
      calc_mem[ctx.message.content] = int(h) * int(percent)/100
    except Exception:
      i = find_player(h)
      if (i == -1):
        await ctx.send("This is not a player or a number.")
        return
      health = 0
      if (isBruiser(statFile[STAT_FILE_CONST*i + 4])):
        health = bruiser_hp[int(statFile[STAT_FILE_CONST*i + 5])]
      else:
        health = arc_hp[int(statFile[STAT_FILE_CONST*i + 5])]
      await ctx.send(percent + "% of " + statFile[STAT_FILE_CONST*i + 2] + "'s health is " + str(health * int(percent)/100))
      calc_mem[ctx.message.content] = health * int(percent)/100

@client.command(name = 'cstats', pass_context = True)
async def cstats(ctx, *args):
  i = 0
  if (len(args) == 0):
    i = find_player(mention_to_id(ctx.message.author.mention))
  elif (len(args) == 1):
    i = find_player(mention_to_id(args[0]))
  else:
    i = find_player((args[0] + " " + args[1]).strip())
  if i == -1:
      await ctx.send("This player has not created a character. use `rp!createchar` to create one.")
  else:
    line = STAT_FILE_CONST*i + 1
    userString = statFile[line]
    mentioned_user = await client.fetch_user(userString)
    embed = discord.Embed(title=statFile[line + 1])
    embed.set_author(name=str(mentioned_user) + "'s character", icon_url=mentioned_user.avatar_url)
    embed.set_thumbnail(url=statFile[line + 6])
    embed.add_field(name="Element: ", value=statFile[line + 3] + elem_emotes[find_element(statFile[line + 3])], inline=False)
    level = int(statFile[line + 4])
    embed.add_field(name=lvl_rank[level] + " Level " + str(level), value=str(exp_val[level]) + "XP Needed For Next Level", inline=False)
    stats = statFile[line + 5].split()
    if (isBruiser(statFile[line + 3])):
      embed.add_field(name = "Total HP: ", value = str(bruiser_hp[int(level)]), inline = True)
      embed.add_field(name = "Total SP: ", value = str(bruiser_sp[int(level)]), inline = True)
    else:
      embed.add_field(name = "Total HP: ", value = str(arc_hp[int(level)]), inline = True)
      embed.add_field(name = "Total SP: ", value = str(arc_sp[int(level)]), inline = True)
    embed.add_field(name="SAP: ", value=str(str_val[int(stats[0])]) + " (" + stats[0] + ")", inline=True)
    embed.add_field(name="MAP/MR: ", value=str(str_val[int(stats[1])]) + "/" + str(end_val[int(stats[1])]) + " (" + stats[1] + ")", inline=True)
    embed.add_field(name="ACC/EVA: ", value=str(agi_val[int(stats[3])]) + "%/" + str(agi_val[int(stats[3])] - 65) + "%" + " (" + stats[3] + ")", inline=True)
    embed.add_field(name="PR: ", value=str(end_val[int(stats[2])]) + " (" + stats[2] + ")" , inline=True)
    embed.add_field(name="CRT/CEVA: ", value=str(luc_val[int(stats[4])]) + "%/" + str(luc_val[int(stats[4])] - 6) + "%" + " (" + stats[4] + ")", inline=True)
    elemLine = find_element(statFile[line + 3])*49
    for a in range(elemLine + 5, elemLine + 49, 4):
      if (level >= int(skillFile[a])):
        embed.add_field(name="_ _", value="_ _", inline=False)
        embed.add_field(name=skillFile[a + 1], value=skillFile[a], inline=True)
        embed.add_field(name=skillFile[a + 3], value=skillFile[a + 2], inline=True)
    await ctx.send(embed=embed)

'''
@client.command(name = 'talkdata', pass_context = True)
async def talkdata(ctx, user = None):
  #random.randint(1, 100)
  look_id = ""
  name = ""
  if (user != None):
    name, look_id = await find_name(user)
  else:
    name = ctx.author.display_name
    look_id = str(ctx.message.author.id)
  
  if (name == None):
    await ctx.send("Could not find this user.")
    return
  plt.figure()
  await ctx.send("Checking if data was accessed...")
  if (look_id not in data_ids):
    data_ids.append(look_id)

  await ctx.send("Retrieving data...")
  for each_id in data_ids:
    get_values = db.reference("users").get().get(each_id)
    x_values = list(range(1, len(get_values) + 1))
    y_values = []
    y_values.append(get_values[0])
    for i in range(1, len(get_values)):
      y_values.append(y_values[i-1] + get_values[i])
    label_name = ""

    if (each_id == "server"):
      label_name = "Eurae's Law"
    else:
      label_name = (await client.fetch_user(each_id)).name

    if (each_id == look_id):
      plt.plot(x_values, y_values, c=(random.uniform(0.1, 0.4), random.uniform(0.1, 0.4), random.uniform(0.1, 0.4)), linewidth=5, label=label_name)
    else:
      plt.plot(x_values, y_values, c=(random.uniform(0.75, 0.9), random.uniform(0.75, 0.9), random.uniform(0.75, 0.9)), linewidth=5, label=label_name)
  
  await ctx.send("Compiling data to graph...")
  plt.title(name + "'s Data", fontsize=24)
  plt.xlabel("Days", fontsize=14)
  plt.ylabel("Messages Sent", fontsize=14)
  plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
  plt.savefig('squares_plot.png', bbox_inches='tight')
  img = discord.File('squares_plot.png', filename="squares_plot.png")
  await ctx.send("Data for `" + name + "`" , file=img)

@client.command(name = 'cleargraph', pass_context = True)
async def cleardata(ctx, user = None):
  global data_ids
  data_ids = []
  await ctx.send("Graph Cleared!")

@client.command(name = 'wordcloud', pass_context = True)
async def wordcloud(ctx, user = None):  
  look_id = ""
  name = ""
  if (user != None):
    name, look_id = await find_name(user)
    if (name == None):
      await ctx.send("User could not be found.")
      return
  else:
    name = ctx.author.display_name
    look_id = str(ctx.message.author.id)

  words = db.reference("wordclouds/" + look_id).get().replace("nigger", "").replace("faggot", "")
  stopwords = set(STOPWORDS)
  wordcloud = WordCloud(stopwords=stopwords, collocations=False).generate(words) 
  
  # plot the WordCloud image                        
  plt.figure(figsize = (8, 8), facecolor = None) 
  plt.imshow(wordcloud) 
  plt.axis("off") 
  plt.tight_layout(pad = 0) 
  plt.savefig('squares_plot.png', bbox_inches='tight')
  img = discord.File('squares_plot.png', filename="squares_plot.png")
  await ctx.send("Word Cloud for " + name, file=img)

@client.command(name = 'steamid', pass_context = True)
async def steamid(ctx, num = None):
  if (num == None):
    await ctx.send("Form: `rp!steamid <idnum>`")
    return
  
  db.reference("steam").update({
    str(ctx.message.author.id) : num
  })

  await ctx.send("Steam ID set!")
  '''

@client.command(name = 'steam', pass_context = True)
async def steam(ctx, user = None):
  name = ""
  look_id = ""
  if (user != None):
    name, look_id = await find_name(user)
    if name == None:
      await ctx.send("User could not be found")
      return
  else:
    name = ctx.author.display_name
    look_id = str(ctx.message.author.id)
  
  steam_id =  db.reference("steam/" + look_id).get()
  if (steam_id == None):
    await ctx.send("User has not attached steam id to profile. Use command `rp!steamid`")
    return

  user_profile = profiles.get_user_profile(steam_id)

  PersonaState = {0 : "Offline", 1 : "Online", 2 : "Busy", 3 : "Away", 4 : "Snooze", 5 : "Looking to Trade", 6 : "Looking to Play"}
  embed = discord.Embed(title="Steam Information For " + name,)
  embed.add_field(name="Level", value=user_profile.steamlevel, inline=True)
  if (user_profile.gameextrainfo != None): 
    embed.add_field(name="Playing Game", value = user_profile.gameextrainfo)
  else:
    embed.add_field(name="Playing Game", value = "*None*")
  embed.add_field(name="Status", value=PersonaState[user_profile._personastate])
  all_seconds = int(datetime.datetime.now().strftime("%s")) - user_profile.lastlogoff
  hours, minutes = seconds_to_time(all_seconds)
  embed.add_field(name="Last Online", value=str(hours) + " hours and " + str(minutes) + " minutes ago", inline=True)
  for game in user_profile.recentlyplayedgames:
    embed.add_field(name=game['name'], value="_ _", inline=False)
    hours, minutes = minutes_to_time(game['playtime_2weeks'])
    embed.add_field(name="Playtime Last Two Weeks", value=str(hours) + " hours and " + str(minutes) + " minutes", inline=True)
    hours, minutes = minutes_to_time(game['playtime_forever'])
    embed.add_field(name="Playtime All Time", value=str(hours) + " hours and " + str(minutes) + " minutes", inline=True)
  embed.set_author(name=user_profile.personaname, icon_url=user_profile.avatar)
  embed.set_thumbnail(url=user_profile.recentlyplayedgames[0]["img_logo_url"])
  embed.set_footer(text="Link: " + user_profile.profileurl)
  await ctx.send(embed=embed)

@client.command(name = 'channeldata', pass_context = True)
async def channeldata(ctx):
  plt.figure()
  data = db.reference("channels").get()
  sent = [x[0] for x in data.values()]
  names = [client.get_channel(int(x)).name for x in data.keys()]
  squarify.plot(sizes=sent, label=names, alpha=.7 )
  plt.axis('off')
  plt.savefig('squares_plot.png', bbox_inches='tight')
  img = discord.File('squares_plot.png', filename="squares_plot.png")
  await ctx.send("Channel Message Data", file=img)

  plt.figure()

  # Plot
  patches, text = plt.pie(sent, shadow=True, startangle=140)

  plt.legend(patches, names, loc="best")

  plt.tight_layout()
  plt.axis('equal')
  plt.savefig('squares_plot.png', bbox_inches='tight')
  img = discord.File('squares_plot.png', filename="squares_plot.png")
  await ctx.send("Channel Message Data", file=img)

@client.command(name = 'google', pass_context = True)
async def google(ctx, *args):
  query = " ".join(args)
  embed = discord.Embed(title='Results for search "' + query + '"')

  try: 
    from googlesearch import search 
  except ImportError:  
    print("No module named 'google' found") 

  await ctx.send("Searching...")
  async with ctx.channel.typing():
    for j in search(query, num=10, stop=5, pause=2): 
      page = requests.get(j)
      titles = re.findall(pattern=r'<title>(.*)</title>', string=page.text, flags=re.M|re.I)
      if titles:
        embed.add_field(name=titles[0][:50], value=j, inline=False)
      else:
        embed.add_field(name="Unknown", value=j)

  await ctx.send(embed=embed)

@client.command(name = 'animesearch', pass_context = True)
async def animesearch(ctx, stypearg, *args):
  jikan = Jikan()
  results = []
  stype = stypearg.lower()
  try:
    results = jikan.search(stype, " ".join(args))['results']
  except Exception:
    await ctx.send("No results found. (Remember that your first argument has to be anime, manga, or character)")
    return
  if (stype == "anime"):
    result = jikan.anime(results[0]['mal_id'])
    embed = discord.Embed(title=result['title'], description=result['synopsis'])
    embed.add_field(name="Type", value = result['type'])
    embed.add_field(name="Episodes", value = result['episodes'])
    embed.add_field(name="Score", value = result['score'])
    embed.add_field(name="Rating", value = result['rating'])
    if (result['aired']['from'] != None):
      embed.add_field(name="Started", value = result['aired']['from'][:10])
    else:
      embed.add_field(name="Started", value = "Hasn't Started")
    if (result['aired']['to'] != None):
      embed.add_field(name="Ended", value = result['aired']['to'][:10])
    else:
      embed.add_field(name="Ended", value = "Hasn't ended")
    if (result['broadcast'] != None):
      embed.add_field(name="Aires on", value=result['broadcast'])
    embed.set_thumbnail(url=result['image_url'])
    if (result['trailer_url'] != None):
      embed.add_field(name="Trailer", value=result['trailer_url'])
    embed.set_footer(text="Link: " + result['url'])
    await ctx.send(embed=embed)
  elif (stype == "manga"):
    result = jikan.manga(results[0]['mal_id'])
    embed = discord.Embed(title=result['title'], description=result['synopsis'])
    embed.add_field(name="Type", value = result['type'])
    embed.add_field(name="Chapters", value = result['chapters'])
    embed.add_field(name="Volumes", value = result['volumes'])
    embed.add_field(name="Score", value = result['score'])
    embed.add_field(name="Status", value = result['status'])
    if (result['published']['from'] != None):
      embed.add_field(name="Started", value = result['published']['from'][:10])
    else:
      embed.add_field(name="Started", value = "Hasn't Started")
    if (result['published']['to'] != None):
      embed.add_field(name="Ended", value = result['published']['to'][:10])
    else:
      embed.add_field(name="Ended", value = "Hasn't ended")
    embed.set_thumbnail(url=result['image_url'])
    embed.set_footer(text="Link: " + result['url'])
    await ctx.send(embed=embed)
  elif (stype == "character"):
    result = jikan.character(results[0]['mal_id'])
    embed = discord.Embed(title=result['name'] + "(" + result['name_kanji'] + ")", description=result['about'][:500])
    if (result['animeography']):
      embed.set_thumbnail(url=result["animeography"][0]["image_url"])
      for anime in result["animeography"]:
        embed.add_field(name="Anime Name", value=anime['name'], inline=False)
    elif (result['mangaography']):
      embed.set_thumbnail(url=result["mangaography"][0]["image_url"])
      for manga in result["mangaography"]:
        embed.add_field(name="Manga Name", value=manga['name'], inline=False)
    embed.set_image(url=result['url'])
    await ctx.send(embed=embed)

@client.command(name = 'animeupcoming', pass_context = True)
async def animeupcoming(ctx, day = None):
  jikan = Jikan()
  if (day == None or day.lower() == "today"):
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo')) # you could pass `timezone` object here
    weekday = now.weekday() 
    use_day = calendar.day_name[weekday]
  else:
    use_day = day
  try:
    scheduled = jikan.schedule(day=use_day.lower())
  except Exception:
    await ctx.send('Enter a valid day of the week or "today."')
    return

  embed = discord.Embed(title="Anime on " + use_day.title())
  for item in scheduled[use_day.lower()]:
    anime = jikan.anime(item['mal_id'])
    embed.add_field(name=anime['title'], value=anime['broadcast'])
  embed.set_thumbnail(url=scheduled[use_day.lower()][0]['image_url'])
  await ctx.send(embed=embed)

@client.command(name = 'alphaAI', pass_context = True)
async def alphaAI(ctx, priv_arg = "False"):
  alphaclient = wolframalpha.Client(os.environ.get("WOLFRAM_ALPHA_CLIENT_ID"))
  await ctx.send("Talk to the AI! Type cancel when you are finished.")

  priv = priv_arg.lower() in ("yes", "true", "t", "1")
  def check0(m):
    return not m.author.bot

  def check1(m): # Check if message made by the one who initiated command
    return m.author == ctx.message.author

  async def getmsg():
    try:
      if (priv):
        msg = await client.wait_for('message', check=check1, timeout=30.0)
      else:
        msg = await client.wait_for('message', check=check0, timeout=30.0)
    except asyncio.TimeoutError: # If the message times out
      await ctx.send("Timed out.")
      return "cancel"
    else:
      return msg.content

  q = await getmsg()
  while (q != "cancel"):
    res = alphaclient.query(q)
    embed = discord.Embed(title="Result in " + res['@timing'] + " seconds")
    if (res['@success'] == 'true'):
      for pod in res.pods:
        if (not None in pod.texts):
          embed.add_field(name=pod['@title'], value="/n".join(pod.texts))
    else:
      embed.add_field(name="Result", value="Unsuccessful")
    await ctx.send(embed=embed)
    q = await getmsg()

@client.command(name = 'react', pass_context = True)
async def react(ctx, message_link, *args):
  letters = "🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿".split(" ")
  numbers = ":zero: :one: :two: :three: :four: :five: :six: :seven: :eight: :nine:".split(" ")
  message_id = message_link.split("/")[-1]
  try:
    message = await ctx.message.channel.fetch_message(int(message_id))
    words = args
  except Exception:
    message = (await ctx.message.channel.history(limit=2).flatten())[1]
    orig_list = [message_link]
    words = orig_list + list(args)

  for word in words:
    if (len(message.reactions) == 20): # The bagel statement
      await ctx.send("No more space.")
      break
    if (word[0] == "<" and word[-1] == ">"):
      await message.add_reaction(client.get_emoji(int(word.split(":")[2][:-1])))
    else:
      for letter in word:
        if (ord(letter) - 97 >= 0 and ord(letter) - 97 <= 25):
          await message.add_reaction(letters[ord(letter) - 97])
        else:
          try:
            await message.add_reaction(letter)
          except:
            pass
  
def anime_in_day(anime, day):
  jikan = Jikan()
  for item in jikan.schedule()[day]:
    if (item["title"] == anime):
      return True
  return False

def seconds_to_time(all_seconds):
  hours = all_seconds // 3600
  minutes = (all_seconds - hours*3600) // 60
  return hours, minutes

def minutes_to_time(all_minutes):
  hours = all_minutes // 60
  minutes = all_minutes - hours*60
  return hours, minutes

async def find_name(user):
  name = ""
  look_id = ""
  if (user.lower() == "s" or user.lower() == "serv" or user.lower() == "server"):
    look_id = "server"
    name = "Eurae's Law"
  else:
    eurae_law = client.get_guild(490714402287386626)
    person = discord.utils.find(lambda m: user.lower() == m.display_name.lower(), eurae_law.members)
    if (person == None):
      person = discord.utils.find(lambda m: user.lower() == m.name.lower(), eurae_law.members)
    if (person == None):
      try:
        mention_user = await client.fetch_user(mention_to_id(user))
        name = mention_user.name
        look_id = str(mention_user.id)
      except Exception:
        return None, None
    else:
      name = person.name
      look_id = str(person.id)
  return name, look_id
    
def find_player(user):
  i = 0
  Found = False
  while (Found == False and i < int(statFile[0])):
    if (statFile[STAT_FILE_CONST*i + 1] == user or statFile[STAT_FILE_CONST*i + 2].lower() == user.lower() or statFile[STAT_FILE_CONST*i + 2].lower().split(" ")[0] == user.lower()):
      Found = True
    else:
      i += 1
  if not Found:
    return -1
  return i

def mention_to_id(mention):
  if (mention[0] != "<"):
    return mention
  a = mention[2:len(mention) - 1]
  if (a[0] == "!"):
    a = a[1:]
  return a

def find_element(elem, unexact = False):
  i = 0
  Found = False
  while (Found == False and i < 8):
    if unexact:
      if (elem.lower() == skillFile[i*49].lower()[:len(elem)]):
        Found = True
      else:
        i += 1
    else:
      if (skillFile[i*49].lower() == elem.lower()):
        Found = True
      else:
        i += 1
  if (Found == False):
    return -1
  return i

def isBruiser(elem):
  return skillFile[find_element(elem)*49 + 1] == "Bruiser"

def bruiser_level():
  num = random.randint(1, 100)
  if (num <= 30):
    return 0
  if (num <= 50):
    return 1
  if (num <= 70):
    return 2
  if (num <= 90):
    return 3
  return 4

def arc_level():
  num = random.randint(1, 100)
  if (num <= 10):
    return 0
  if (num <= 40):
    return 1
  if (num <= 60):
    return 2
  if (num <= 80):
    return 3
  return 4

def point_def(pts):
  if pts == 0:
    return "SAP"
  if pts == 1:
    return "MAP/MR"
  if pts == 2:
    return "END"
  if pts == 3:
    return "ACC/EVA"
  if pts == 4:
    return "CRT/CEVA"

def find_status(stat, unexact = False):
  i = 0
  Found = False
  while (Found == False and i < 13):
    if unexact:
      if (stat.lower() == statusFile[i*3].lower()[:len(stat)]):
        Found = True
      else:
        i += 1
    else:
      if (statusFile[i*3].lower() == stat.lower()):
        Found = True
      else:
        i += 1
  if (Found == False):
    return -1
  return i

def find_rank(rank, num):
  for i in range(0, len(statFile), 6):
    if rank.lower() == ranksFile[i].lower()[:len(rank)]:
      for j in range(1, 6):
        line = int(ranksFile[i+j].split()[1])
        if int(num) < line:
          return ranksFile[i+j - 1].split()[0]
      return ranksFile[i+5].split()[0]
  return "ERROR"

'''
async def check_wiki_updates():
  while True:
    pr = requests.get('https://eprp.fandom.com/wiki/Special:WikiActivity', timeout=5, headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'cache-control': 'private, max-age=0, no-cache'
    })
    # here, we fetch the content from the url, using the requests library
    pc = BeautifulSoup(pr.content, "html.parser")
    #we use the html parser to parse the url content and store it in a variable.
    updates = pc.find(id="myhome-activityfeed")
    r1 = updates.findAll("cite")
    r2 = updates.findAll("strong")
    if (len(r1) * 2 > len(update_list)):
      dif = len(r1) * 2 - len(update_list)
      update_list.clear()
      for i in range(0, len(r1)):
        update_list.append(r1[i].get_text())
        update_list.append(r2[i].get_text())
      channel = client.get_channel(570799295159336962)
      embed = discord.Embed(title="Update")
      for i in range(0, dif):
        embed.add_field(name=r2[i].get_text(), value=r1[i].get_text())
      await channel.send(embed=embed)
    await asyncio.sleep(60)
'''

def time_helper(i, j):
  if j < 10:
    return str(i) + ":0" + str(j)
  else:
    return str(i) + ":" + str(j)

async def update_graph():
  day = db.reference("users/day").get()
  while True:
    cur_time = datetime.datetime.now()
    if (cur_time.hour == 0 and cur_time.minute == 0 and day != cur_time.day):
      for key, value in db.reference("users").get().items():
        if (key == "day" or key == "time"):
          continue
        db.reference("users/" + key).update({
          len(value) : 0
        })

      for key2, value2 in db.reference("channels").get().items():
        db.reference("channels/" + key2).update({
          len(value2) : 0
        })

      lobby = client.get_channel(596491158872522752)
      plt.figure()

      times = [time_helper(i, j) for i in range(24) for j in range(0, 60, 30)]
      data = []
      for i in range(24):
        ref_list = db.reference("users/times/" + str(i)).get()
        sumN = 0
        for j in range(0, 30):
          sumN += ref_list[j]
        data.append(sumN)

        sumN = 0
        for k in range(30, 60):
          sumN += ref_list[k]
        data.append(sumN)
      
      plt.plot(times, data)
      plt.title("Server Data For Today", fontsize=24)
      plt.xlabel("Time", fontsize=14)
      plt.xticks([])
      plt.ylabel("Messages Sent", fontsize=14)
      plt.savefig('squares_plot.png', bbox_inches='tight')
      img = discord.File('squares_plot.png', filename="squares_plot.png")
      await lobby.send("Daily Data", file=img)

      for k in range(24):
        for m in range(60):
          db.reference("users/times/" + str(k)).update({
            m : 0
          })
      day = cur_time.day
      db.reference("users").update({
        "day" : day
      })
    else:
      await asyncio.sleep(15)

@client.command(name = 'temp', pass_context = True)
async def temp(ctx):
  lobby = client.get_channel(570799295159336962)
  plt.figure()

  times = [time_helper(i, j) for i in range(24) for j in range(0, 60, 30)]
  data = []
  for i in range(24):
    ref_list = db.reference("users/times/" + str(i)).get()
    sumN = 0
    for j in range(0, 30):
      sumN += ref_list[j]
    data.append(sumN)

    sumN = 0
    for k in range(30, 60):
      sumN += ref_list[k]
    data.append(sumN)
  
  plt.plot(times, data)
  plt.title("Server Data For Today", fontsize=24)
  plt.xlabel("Time", fontsize=14)
  plt.xticks([])
  plt.ylabel("Messages Sent", fontsize=14)
  plt.savefig('squares_plot.png', bbox_inches='tight')
  img = discord.File('squares_plot.png', filename="squares_plot.png")
  await lobby.send("Daily Data", file=img)

#client.loop.create_task(update_graph())

keep_alive()
TOKEN = os.environ.get("KEY")
client.run(TOKEN)
