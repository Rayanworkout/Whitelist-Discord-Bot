import asyncio
from operator import itemgetter
from os import path
from random import choice

import discord
import requests
from discord.ext import commands, tasks
from discord.ext.commands.errors import (CheckFailure, CommandNotFound,
                                         MissingRequiredArgument)

from logger import Logger

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", help_command=None, case_insensitive=True, intents=intents)
bdd = Logger()


##############################################################################################################

def checkAuthorized(ctx):
    """Defining discord IDs authorized for
    admin commands"""
    return ctx.message.author.id in ["ADMINS IDS LIST IN INT FORMAT"]


@bot.command()
@commands.check(checkAuthorized)
async def db(ctx):
    if path.exists("whitelist.csv"):
        await ctx.author.send(file=discord.File("whitelist.csv"))
    
    if path.exists("db.db"):
        await ctx.author.send(file=discord.File("db.db"))
    await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    """Custom error handler, for the selected exceptions
    not appearing in the terminal, or sending msg when arg is mandatory"""

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(
            description="You need to specify something after the command !  :x:",
            color=discord.Colour.blue(),
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, (CheckFailure, CommandNotFound)):
        pass

##############################################################################################################

# DECLARING CONSTANTS FOR AN EASIER SETUP

SECRET_WORD = "we are blobz"
PRIVATE_SECRET_WORD = " hello finley"

GM_COUNT = 20
RESPONSE_COUNT = 35
MEME_COUNT = 2
REACTION_COUNT = 15
HELP_COUNT = 3
TROPHY_LVL = 12
TROPHY_NUMBER = 6
DM_DELAY = 900 # 900 SECONDS

BOT_ID = "YOUR BOT ID"
BOT_TOKEN = "YOUR BOT TOKEN"
GUILD_ID = 965910044833095690
ANNOUNCEMENTS_CHANNEL = "CHANNEL ID"
BOTS_COMMAND_CHANNEL = "CHANNEL ID"
MY_TROPHIES_CHANNEL = "CHANNEL ID"
GM_CHANNEL = "CHANNEL ID"
MEME_CHANNEL = "CHANNEL ID"
SECRET_CHANNEL = "CHANNEL ID"
LEADERBOARD_CHANNEL = "CHANNEL ID"

##############################################################################################################    

@bot.event
async def on_ready():
    print("Blobz Ready ...")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Blobz Blobz"))


@bot.command()
async def helpMe(ctx):
    if ctx.guild and ctx.channel.id == BOTS_COMMAND_CHANNEL:
        count = bdd.increment("help", ctx.author.id, str(ctx.author))
        
        embed = discord.Embed(
            description=choice(["**Nothing to see here ...**",
                                "**You're being annoying anon !**",
                                "** * *Blob... BlobBlobBlob* *...**",
                                "**Probably eating something …**",
                                "**Stop calling ser. Blob's busy.**",
                                "** * *Mochi Mochi ?* * **",
                                "**Listening to 50Blobz …**",
                                "**Humans say I'm not smart, and they get my Blob in the face**",
                                "** …you ! But it can’t be. You’re dead. You… * *Bloblbolboblbolbob* * **",
                                "**Oh… what happened ?**",
                                ("**These days, it seems there is dread everywhere, whether it be war or Blobz."
                                "But I beg you – here, today, put such fears aside. Enjoy yourselves !**"),
                                "**Ahhh… gotcha ! Oh, Human, you should see the look on your face ! * *BLOB ! BLOB ! BLOB !* * **",
                                "** You are carrying too much to be able to run**",
                                "**The save game is corrupt and cannot be loaded * *Blob* * **",
                                "**Those who shirk their duties will get an extra Blobing. Do I make make myself clear ?**",
                                "** What do you need ?**",
                                "**Finley is tired now. Go bother somebody else**",
                                "**Finley once walked to High Hrothgar. So many steps, he lost count.**",
                                "**Finley is done talking.**"]),
            color=discord.Colour.blue(),
        )
        await ctx.reply(embed=embed)
        
        if count and count[0] == HELP_COUNT:
            bdd.increment("trophies", ctx.author.id, str(ctx.author), value=2)
            embed = discord.Embed(
                description='**Good job human ! * *BlobBlob* * You just won the *"All Thumbs"* trophy !   :trophy:**',
                color=discord.Colour.blue(),
            )
            
            await asyncio.sleep(DM_DELAY)
            await ctx.author.send(embed=embed)

##############################################################################################################

@bot.command()
@commands.check(checkAuthorized)
async def WhoIsWL(ctx):
    embed = discord.Embed(
    description=bdd.fetch_whitelisted(),
    color=discord.Colour.blue(),)
    
    await ctx.author.send(embed=embed)
    await ctx.message.delete()

@bot.command()
@commands.check(checkAuthorized)
async def whitelist(ctx, user_id):
    user_id = int(user_id)
    name = str(bot.get_user(user_id))
    
    guild = bot.get_guild(GUILD_ID)
    role = discord.utils.get(guild.roles, id=965911625624322078)
    member = guild.get_member(user_id)
    
    if not member:
        embed = discord.Embed(
        description="**An error occured, try again.**",
        color=discord.Colour.blue(),)
        await ctx.author.send(embed=embed)
        await ctx.message.delete()
        return f"Error whitelisting {user_id}."
        
    await member.add_roles(role, atomic=True)    
    
    embed = discord.Embed(
    description=bdd.whitelist(user_id, name),
    color=discord.Colour.blue(),)
    
    await ctx.author.send(embed=embed)
    await ctx.message.delete()


@bot.command()
@commands.check(checkAuthorized)
async def removeWL(ctx, user_id):
    user_id = int(user_id)
    name = str(bot.get_user(user_id))
    
    guild = bot.get_guild(GUILD_ID)
    role = discord.utils.get(guild.roles, id="WHITELIST ROLE")
    member = guild.get_member(user_id)
    
    if not member:
        embed = discord.Embed(
        description="**An error occured, try again.**",
        color=discord.Colour.blue(),)
        await ctx.author.send(embed=embed)
        await ctx.message.delete()
        return f"Error whitelisting {user_id}."
    
    await member.remove_roles(role, atomic=True) 

    embed = discord.Embed(
    description=bdd.remove_whitelist(user_id, name),
    color=discord.Colour.blue(),)
    
    await ctx.author.send(embed=embed)
    await ctx.message.delete()

@bot.command()
@commands.check(checkAuthorized)
async def giveTrophy(ctx, user_id):
    user_id = int(user_id)
    name = str(bot.get_user(user_id))
    
    bdd.increment("trophies", user_id, name)
    
    embed = discord.Embed(
    description="Successfully added 1 trophy to {}".format(name),
    color=discord.Colour.blue(),)
    
    await ctx.author.send(embed=embed)
    await ctx.message.delete()

##############################################################################################################


@bot.event
async def on_message(message):
    
    if message.guild:  
        if message.reference and message.author.id != BOT_ID:
            count =  bdd.increment("responses", message.author.id, str(message.author))
            if count and count[0] == RESPONSE_COUNT:
                    embed = discord.Embed(
                    description='** * *Eating Bloberries* * Oh hey human ! you\'ve won the *"One For All"* trophy ! 🏆**',
                    color=discord.Colour.blue(),)
                    
                    await asyncio.sleep(DM_DELAY)
                    await message.author.send(embed=embed)
                    
                    bdd.increment("trophies", message.author.id, str(message.author))
        
        if message.content.strip().lower() == "gm" and message.author.id != BOT_ID and message.channel.id == GM_CHANNEL:
            count = bdd.increment("gm", message.author.id, str(message.author))
            gn = bdd.check("gn", message.author.id)
            if count and count[0] == GM_COUNT and gn and gn[0] == GM_COUNT:
                embed = discord.Embed(
                description='** * *Blobing a Zoot* * Congrats human you\'ve won the *"Tea Time"* trophy ! 🏆  Share it to Blob frens**',
                color=discord.Colour.blue(),)
                
                await asyncio.sleep(DM_DELAY)
                await message.author.send(embed=embed)
                bdd.increment("gm", message.author.id, str(message.author))
                bdd.increment("trophies", message.author.id, str(message.author))
        
        
        if message.content.strip().lower() == "gn" and message.author.id != BOT_ID and message.channel.id == GM_CHANNEL:
            bdd.increment("gn", message.author.id, str(message.author))
        
        
        if SECRET_WORD in message.content.lower() and message.author.id != BOT_ID:
            count = bdd.increment("secret_word", message.author.id, str(message.author))
            if count and count[0] == 2:
                bdd.increment("trophies", message.author.id, str(message.author))
                embed = discord.Embed(
                description='** * *Eating Bloberries* *  Oh hey human ! you\'ve won the *"One For All"* trophy !  :trophy:**',
                color=discord.Colour.blue(),)
                
                await asyncio.sleep(DM_DELAY)
                await message.author.send(embed=embed)
        
        if message.channel.id == SECRET_CHANNEL and message.author.id != BOT_ID:
            already_trophy = bdd.check("secret_channel_trophy", message.author.id)
            if not already_trophy or already_trophy[0] == 0:
                bdd.increment("trophies", message.author.id, str(message.author))
                bdd.increment("secret_channel_trophy", message.author.id, str(message.author))
                
        if message.channel.id == MEME_CHANNEL and message.author.id != BOT_ID:
            if message.attachments:
                count = bdd.increment("memes", message.author.id, str(message.author))
                if count and count[0] == MEME_COUNT:
                    bdd.increment("trophies", message.author.id, str(message.author))
                    embed = discord.Embed(
                    description='** * *Blobing dance moves* * Huuuuuuuuman… 🎶 … Come get your trophy … 🎶 You\'ve just won the *"Artist"* trophy 🏆 !**',
                    color=discord.Colour.blue(),)
                    
                    await asyncio.sleep(DM_DELAY)
                    await message.author.send(embed=embed)
    
    elif not message.guild and PRIVATE_SECRET_WORD in message.content.lower():
        check = bdd.check("private_secret_word", message.author.id)
        if not check or check[0] == 0:
            bdd.increment("private_secret_word", message.author.id, str(message.author))
            bdd.increment("trophies", message.author.id, str(message.author), value=2)
            
            embed = discord.Embed(
            description='**By the Blobz ! You just found the secret word ! There is your reward : *"Stalker"* trophy 🏆**',
            color=discord.Colour.blue(),)
                
            await message.author.send(embed=embed)
            
    
    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    """Trophy after X reactions"""
    # Checking if reaction is made in the right channel and not in DM
    if reaction.message.channel.id == ANNOUNCEMENTS_CHANNEL:
        reactions_check = bdd.check("reactions", user.id)
        
        if not reactions_check or reactions_check[0] < REACTION_COUNT:
            # Fetching last message where reaction was made
            last_msg = bdd.check("msg_reactions", user.id)
            if not last_msg or last_msg[0] == 0:
                bdd.increment("reactions", user.id, user.name)
                bdd.increment("msg_reactions", user.id, user.name, str(reaction.message.id))
            
            # Adding a reaction if the msg is a different one
            elif last_msg and int(last_msg[0]) != reaction.message.id:
                bdd.increment("msg_reactions", user.id, user.name, str(reaction.message.id))
                bdd.increment("reactions", user.id, user.name)
                count = bdd.check("reactions", user.id)
                
                # Sending the trophy if it reaches the count
                if count and count[0] == REACTION_COUNT:
                    bdd.increment("trophies", user.id, user.name)
                    
                    embed = discord.Embed(
                    description="**Congratulations, you won the *enjoyooor* trophy !**",
                    color=discord.Colour.blue(),)

                    await asyncio.sleep(DM_DELAY)
                    await user.send(embed=embed)

@bot.command()
async def myTrophies(ctx):
    if ctx.channel.id == MY_TROPHIES_CHANNEL:
        trophies = bdd.check("trophies", ctx.author.id)
        if trophies and trophies[0]:
            numb = "trophy" if trophies[0] == 1 else "trophies"
            embed = discord.Embed(
            description=f'**You currently have {trophies[0]}/6 {numb}  :trophy:**',
            color=discord.Colour.blue(),)
        
        elif not trophies or not trophies[0]:
            embed = discord.Embed(
            description="**You don't have any trophy so far, find'em all !  :trophy:**",
            color=discord.Colour.blue(),)
            
        await ctx.reply(embed=embed)

@bot.command()
async def soldOut(ctx):
    """Secret command"""
    if ctx.guild:
        bdd.increment("secret_command", ctx.author.id, str(ctx.author))
        count = bdd.check("secret_command", ctx.author.id)
        
        if count and count[0] == 1:
            bdd.increment("trophies", ctx.author.id, str(ctx.author), value=2)
            await ctx.message.delete()
            embed = discord.Embed(
            description='** * *Whispering confidential Blob things* * ... WOW HUMAN! you scared me! please take this *"SubBlobz"* trophy 🏆 and be quiet.**',
            color=discord.Colour.blue(),)
            
            await asyncio.sleep(DM_DELAY)
            await ctx.author.send(embed=embed)
    

##############################################################################################################

@tasks.loop(hours=7)
async def check_levels():
    """Regularly checking for users levels"""
    
    await bot.wait_until_ready()
    
    r = requests.get(f"https://mee6.xyz/api/plugins/levels/leaderboard/{GUILD_ID}").json()
    players = r["players"]
    levels = [(user["id"], user["level"], user["username"]) for user in players if user["level"] > TROPHY_LVL]
    
    for user_id, level, name in levels:
        if bdd.user_exists(user_id):
            if not bdd.check("lvl_trophy", user_id)[0]:
                bdd.increment("trophies", user_id, name)
                bdd.increment("lvl_trophy", user_id, name)
                
                embed = discord.Embed(
                description='** * *Doing Blob push-ups* * You\'ve got guts kid, there is your *"Reckless"* trophy" 🏆 ... * *Doing more Blob push-ups* * **',
                color=discord.Colour.blue(),)
                
                user = bot.get_user(int(user_id))
                await user.send(embed=embed)



@tasks.loop(hours=6)
async def check_members():
    """Regularly checking if a member has "Blobz" 
    in his discord name"""
    
    await bot.wait_until_ready()

    for member in bot.get_guild(GUILD_ID).members:
        if bdd.user_exists(member.id):
            if "blobz" in member.name.lower() and not bdd.check("name_trophy", member.id)[0]:
                bdd.increment("trophies", member.id, member.name)
                bdd.increment("name_trophy", member.id, member.name)
                
                embed = discord.Embed(
                description='** * *Flirting with a Blobie* * ... * *Still flirting* * ... Maybe we should go ... You won the *"Call me by your name"* trophy 🏆**',
                color=discord.Colour.blue(),)

                user = bot.get_user(member.id)
                await user.send(embed=embed)


@tasks.loop(hours=4)
async def check_trophies():
    """Regularly checking for users trophy
    and giving WL to those who got them all"""
    
    await bot.wait_until_ready()

    for member in bot.get_guild(GUILD_ID).members:
        if bdd.user_exists(member.id) and not bdd.check_wl(member.id):
            trophies = bdd.check("trophies", member.id)
            
            if trophies[0] == TROPHY_NUMBER:
                    guild = bot.get_guild(GUILD_ID)
                    role = discord.utils.get(guild.roles, id=965911625624322078)
        
                    await member.add_roles(role, atomic=True)
                    
                    print(f"WL role added to {member.name}.")


@tasks.loop(hours=5)
async def trophies_leaderboard():
    """Creating a leaderboard of trophies in an embed"""
    await bot.wait_until_ready()
    
    # Checking if the message currently exists
    channel = await bot.fetch_channel(LEADERBOARD_CHANNEL)
    try:
        msg = await channel.fetch_message(972957604751998996)
    except discord.errors.NotFound:
        msg = None
    
    if msg:
        data = list()
        for user, count in bdd.all_trophies():
            adj = "trophy" if count == 1 else "trophies"
            data.append(f"{count}**:trophy: {user} :arrow_forward: {count} {adj}**\n\n")
        
        data = sorted(data, key=itemgetter(0), reverse=True)
        data = "".join([elem[1:] for elem in data])
        
        new = discord.Embed(description=data,
                color=discord.Colour.blue(),)
        
        # Editing the old one with updated data
        await msg.edit(embed=new)
        print("Leaderboard updated.")
    
    elif not msg:
        print("Could not retrieve message.")


                
trophies_leaderboard.start()
check_trophies.start()
check_levels.start()
check_members.start()

bot.run(BOT_TOKEN)

