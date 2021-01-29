import discord
from discord.ext import commands
from discord.utils import get

import random
import tracemalloc
import time
import os
import json
from datetime import datetime

tracemalloc.start()

def get_prefix(client,message):
    with open('prefixes.json', 'r') as f:
        prefixes=json.load(f)
    return prefixes[str(message.guild.id)]

intents = discord.Intents.default() # Enable all intents except for members and presences
intents.members = True  # Subscribe to the privileged members intent.
client = commands.Bot(command_prefix=get_prefix, intents=intents)
client.remove_command('help')
Token = ''

m = {}

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes=json.load(f)
    prefixes[str(guild.id)]="`"
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f)

@client.event
async def on_ready():
    print("Logged in as: " + client.user.name + "\n")
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers!"))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="`support | `hlp | https//bit.ly/SpectralS"))

@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes=json.load(f)
    prefixes[str(ctx.message.guild.id)]=prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes,f)
    await ctx.send(f"Prefix changed to {prefix}.")

"""
async def on_message(msg):
    print("Someone has send a message.")
    if str(msg.channel.type) == "private":
        user_id = msg.author.id
        target = await client.fetch_user(user_id)
        await target.send("Modmail is comming soon to this bot, for now this DM that you sent is not getting forwarded anywhere.")
    if "[AFK]" in msg.author.nick:
        newnickl = msg.author.nick.split("] ")
        print(newnickl)
        newnick = newnickl[-1]
        newnicks = str(newnick)
        await msg.author.edit(nick=newnicks)
        await msg.channel.send("You are no longer AFK.")
"""
"""
    global m
    with open("users.json", "r") as j:
        m = json.load(j)
        j.close()
    if len(m) == 0:
        m = {}
        for member in client.get_guild(785552568256299028):
            m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}
"""

@client.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms.')

@client.command(aliases=['help'])
@commands.has_permissions(administrator=True)
async def hlp(ctx):
    #await ctx.send('Help page not finished!')
    embed = discord.Embed(
        title="Commands",
        description=f"```hlp```Displays most of the bot commands.\n```suggestsetup [<Suggestion Channel ID>]```**ALPHA** sets up suggestions in a specific channel.\n```suggest [<suggestion>]```**Suggestions have to be setup for this!** Embeds a suggestion in the suggestion channel.\n```purge [<number of messages>]``` Deletes a specific amount of recent messages from the channel the command was sent in.\n```flip``` Flips a coin and randomly outputs wither 'heads' or 'tails'\n```8ball [<question>]```Integrated 8 ball that answers your question.\n```kick [<user>]``` Kicks a user from the server. \n```calc [<first number>] [<+, -, *, or / >] [<second number>]``` Outputs the answer of the math operation the command sender has input.\n```ping``` Outputs the latency/ping from your device to the bot.\n```servers```Outputs the number of servers the bot it in.\n```setprefix [<prefix>]```Changes the bot's prefix.\n```ticket```Creates a temporary channel that only Admins and the ticket creator has access to.\n```ticketclose```Closes the ticket, must be used in the ticket channel you want to close.\n```slowmode [<seconds>]```Sets the slowmode of the channel that the command was sent in to a specific amount of time.\n```warn [<member>]```Warns a member of the server.\n```warnings [<member>] [<amount>]``` Depending if the second command argument is set, it either changes the warnings of a server member or displays the warnings of a server member.\n```setjoinchannel [<Channel Mention>]```Sets the channel of which the join message gets sent to.\n\n**There are more commands than the ones that are listed, but they are in the beta or alpha versions.**\n*The suggest feature is the only alpha feature listed.*",
        colour=discord.Colour.purple()
    )
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def settings(ctx):
    await ctx.send('Settings not finished!')

@client.command()
@commands.has_permissions(administrator=True)
async def info(ctx):
    await ctx.send('Version: 0.1 Beta. By: Spectre CA.')

@client.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, roll: discord.Role, user: discord.Member):
    try:
        await user.add_roles(roll)
        await ctx.send(f'Added {roll} to {user}.')
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.send('Member not found.')
"""
@client.command(pass_context=True, aliases=['j', 'joi'])
@commands.has_permissions(administrator=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@client.command(pass_context=True, aliases=['l', 'lea', 'leav'])
@commands.has_permissions(administrator=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I have to be in a voice channel to disconnect dum dum!")

@client.command(pass_context=True, aliases=['pla', 'p', 'ply', 'pl'])
@commands.has_permissions(administrator=True)
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file.")
    except PermissionError:
        print("Trying to delete song file, but it's being played.")
        ctx.send("ERROR: Music playing!")
        return

    await ctx.send("Getting everything ready now.")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
    }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading song now.\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f'Renamed File: {file}\n')
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f'{name} has finished playing.'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.3

    nname = name.rsplit("-", 2)
    await ctx.send(f'Playing {nname}')
    print('playing song')
"""
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    if reason != None:
        await ctx.send(f"{member} has been kicked from the server. Reason: {reason}")
    if reason == None:
        await ctx.send(f"{member} has been kicked from the server. For an unspecified reason.")

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    if reason != None:
        await ctx.send(f"{member} has been banned from the server. Reason: {reason}")
    if reason == None:
        await ctx.send(f"{member} has been banned from the server. For an unspecified reason.")

@client.command(aliases=['8ball', 'eightball', 'ball8'])
async def _8ball(ctx, *, question=None):
    if question != None:
        responses = ['It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes - definitely',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    "Don't count on it.",
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Very doubtful.']
        embed = discord.Embed(
            title="8 Ball",
            description=f"Question: {question}\nAnswer: {random.choice(responses)}",
            colour=discord.Colour.purple()
            )
        await ctx.send(embed=embed)
    elif question == None:
        await ctx.send("You must enter a question for this to work!")

@client.command(aliases=['ht', 'coin', 'flip'])
@commands.has_permissions(administrator=True)
async def coinflip(ctx):
    possibilities = ['heads',
                     'tails']
    choice = random.choice(possibilities)
    if choice == 'heads':
        print('heads')
        embed = discord.Embed(
            title="Heads!",
            description="The bot chose heads!",
            colour=discord.Colour.red()
        )
    elif choice == 'tails':
        print('tails')
        embed = discord.Embed(
            title="Tails!",
            description="The bot chose tails!",
            colour=discord.Colour.blue()
        )
    await ctx.send(embed=embed)
"""
@client.command(aliases=['numgen', 'randnumgen', 'rand'])
@commands.has_permissions(administrator=True)
async def randnum(ctx, min=None, max=None):
    if min != None and max != None:
        numrand = random.randint(min, max)
        embed = discord.Embed(
            title="Number generator: ",
            description=f"Your number is {numrand}!",
            colour=discord.Colour.orange())

        await ctx.send(embed=embed)

    else:
        if min == None:
            await ctx.send(f"Invalid syntax use it like this: ```randnum <min> <max>``")
        elif max == None:
            await ctx.send(f"Invalid syntax use it like this: ```randnum <min> <max>``")


@client.command()
@commands.has_permissions(administrator=True)
async def createpoll(ctx, *, message):
    embed = discord.Embed(title="Poll",
                          description=message,
                          colour=discord.Colour.red())
    global msg
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('<:greencheck:787740481508343836>')
    await msg.add_reaction('<:redx:787740501242806302>')
    global ynpollmessage
    ynpollmessage = msg.id
    print(msg.id)
    print(ynpollmessage)


@client.command()
@commands.has_permissions(administrator=True)
async def endpoll(ctx):
    print('Poll ended')
    print(ynpollresults)
    embed = discord.Embed(title="Poll Ended",
                          description=f"Votes: {ynpollresults}",
                          colour=discord.Colour.red()

    )

    await ctx.channel.send(embed=embed)
"""
"""
@client.event
async def on_raw_reaction_add(payload):
    global noresults
    global yesresults
    message_id = payload.message_id
    if message_id == msg.id:
        print('Someone voted')
        if payload.emoji.id == 787740481508343836:
            yesresults = + 1
            print('Someone voted yes')
        elif payload.emoji.id == 787740501242806302:
            noresults = + 1
            print('Someone voted no')
    global ynpollresults
    ynpollresults = f"No: {noresults - 1}, Yes: {yesresults}."
"""
@client.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, amount):
    await ctx.channel.purge(limit=int(amount)+1)

@client.command()
async def servers(ctx):
    await ctx.send(f"Spectral bot is in {len(client.guilds)} servers.")


@client.command()
async def calc(ctx, on=None, dmas=None, tn=None):

    if on == None:
        error = True
        await ctx.send("INVALID SYNTAX! \nMake sure that your command looks like this:\nSyntax: ``calc [first number] [operation] [second number]``\nExample: ``calc 6 * 6``")
    elif dmas == None:
        error = True
        await ctx.send("INVALID SYNTAX! \nMake sure that your command looks like this:\nSyntax: ``calc [first number] [operation] [second number]``\nExample: ``calc 6 * 6``")
    elif tn == None:
        error = True
        await ctx.send("INVALID SYNTAX! \nMake sure that your command looks like this:\nSyntax: ``calc [first number] [operation] [second number]``\nExample: ``calc 6 * 6``")
    else:
        error = False

    if error == False:
        if dmas == "-":
            result = int(on) - int(tn)
            #await ctx.send(f"Your answer is {result}")
        elif dmas == "+":
            result = int(on) + int(tn)
            #await ctx.send(f"Your answer is {result}")
        elif dmas == "/":
            result = int(on) / int(tn)
            #await ctx.send(f"Your answer is {result}")
        elif dmas == "x":
            result = int(on) * int(tn)
            #await ctx.send(f"Your answer is {result}")
        elif dmas == "*":
            result = int(on) * int(tn)
            #await ctx.send(f"Your answer is {result}")

        else:
            await ctx.send(f"'{dmas}' is not a valid operator please use '+, -, /, * or x'")
            result = None
        if result != None:
            embed = discord.Embed(
                title="Calculator",
                description=f"The calculator has calculated your result.\nYour result is....\n{result}!",
                colour=discord.Colour.blue()
            )
            await ctx.send(embed=embed)
"""
        elif on == none:
            #await ctx.send("Make sure your command is structured like: ```calc [first number] [operation] [second number]```")
        elif dmas == none:
            #await ctx.send("Make sure your command is structured like: ```calc [first number] [operation] [second number]```")
        elif tn == none:
            #await ctx.send("Make sure your command is structured like: ```calc [first number] [operation] [second number]```")
        """

"""
@client.event
async def on_message(msg):
    if str(msg.channel.type) == "private":
        user_id = msg.author.id
        target = await client.fetch_user(user_id)
        await target.send("Modmail is comming soon to this bot, for now this DM that you sent is not getting forwarded anywhere.")

@client.command()
async def reactionrole(ctx, channelid, msgid, emoji, roleid):
    channel=client.get_channel(id=channelid)
    message=channel.fetch_message(msgid)
    global gotemoji
    gotemoji=emoji
    message.add_reaction(emoji)
    global role
    role = client.guilds.get_role(roleid)

@client.event
async def on_raw_reaction_add():
    print("test")
"""

@client.command()
@commands.has_permissions(administrator=True)
async def suggestsetup(ctx, channel=None):
    if channel:
        global schannel
        schannelint = int(channel)
        try:
            with open('suggestions.json', 'r') as myfile:
                datag = myfile.read()
            obj = json.loads(datag)
            suggestionchannel=str(obj[str(ctx.message.guild.id)])
            await ctx.send("Suggestions are already setup!")
            return
        except:
            datatostore = {
                f"{ctx.message.guild.id}": f"{channel}"
            }
            """
            with open('suggestions.json', 'w') as f:
                json.dump(datatostore, f)
                """
            with open(r"suggestions.json", "r+") as file:
                data = json.load(file)
                data.update(datatostore)
                file.seek(0)
                json.dump(data, file)
        schannel = ctx.guild.get_channel(channel_id=schannelint)
        embed=discord.Embed(
            title="Suggestions Setup",
            description=f"Suggestions have now been setup on this server.\n\nSuggestions set up by: {ctx.author}",
            colour=discord.Colour.blue()
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await schannel.send(embed=embed)

    else:
        await ctx.send("Make sure that your command is structured like this: ```suggestsetup {Suggestion Channel ID}``` \nHow to get a channel ID: \nGo to account settings, then navigate to appearance and their should be a switch to turn on developer mode. Turn it on, right click on the channel you wish to get the ID for and select 'Copy ID'. The channel ID should be copied to your clipboard.")

@client.command()
@commands.has_permissions(administrator=True)
async def suggest(ctx, *, suggestion=None):
    if suggestion:
        try:
            embed = discord.Embed(
                title="Suggestion",
                description=f"A suggestion has been made: \n{suggestion}\n\nSuggestion sent by: {ctx.author}",
                colour=discord.Colour.blue()
            )
            embed.set_thumbnail(url=ctx.author.avatar_url)
            with open('suggestions.json', 'r') as myfile:
                datag = myfile.read()
            obj = json.loads(datag)
            suggestionchannel=str(obj[str(ctx.message.guild.id)])
            schannel = ctx.guild.get_channel(channel_id=int(suggestionchannel))
            sentsuggestion=await schannel.send(embed=embed)
            await sentsuggestion.add_reaction('<:Check:802178065709924383>')
            await sentsuggestion.add_reaction('<:RX:802178164054163496>')
            await ctx.message.delete()
        except:
            await ctx.send("Their has been an error with making your suggestion. Please contact the server admin or owner about this issue. If you are an admin or owner please set up suggestions again. This error occurs when the bot restarts, and the error will be fixed in the near future.")
    else:
        await ctx.send("Make sure you have input your suggestion after the command: ```suggest {suggestion}```")

@client.command()
async def afk(ctx):
    if "[AFK]" in ctx.author.nick:
        newnickl=ctx.author.nick.split("] ")
        print(newnickl)
        newnick = newnickl[-1]
        newnicks = str(newnick)
        await ctx.author.edit(nick=newnicks)
        await ctx.send("You are no longer AFK.")
    else:
        newnick = f"[AFK] {ctx.author.nick}"
        await ctx.author.edit(nick=newnick)
        await ctx.send("You are now AFK.")

"""
@client.command(aliases=['numguess', 'guess', 'guessthenumber'])
@commands.has_permissions(administrator=True)
async def guessnum(ctx, startnum=None, endnum=None, num=None):
    if num != None:
        if endnum != None:
            if startnum != None:
                ctx.delete()
                
                global gnum
                gnum=int(num)
                global gsnum
                gsnum=int(startnum)
                global genum
                genum=int(endnum)
                global ispoll
                ispoll=True
                
                embed = discord.Embed(
                    title="Guess the number!",
                    description=f"Try to guess the number chosen number:\nTo play guess a number between {startnum} and {endnum}. To guess, type `numanswer <[Your Answer]>>.",
                    colour=discord.Colour.dark_purple()
                )
                ctx.send(embed=embed)
                
@client.command()
async def numanswer(ctx, answer=None):
    if ispoll==True:
        if answer != None:
            
"""
@client.command()
@commands.has_permissions(administrator=True)
async def spectralsupporthlppg(ctx):
    embed = discord.Embed(
        title="Commands",
        description=f"```hlp```Displays most of the bot commands.\n```suggestsetup [<Suggestion Channel ID>]```**ALPHA** sets up suggestions in a specific channel.\n```suggest [<suggestion>]```**Suggestions have to be setup for this!** Embeds a suggestion in the suggestion channel.\n```purge [<number of messages>]``` Deletes a specific amount of recent messages from the channel the command was sent in.\n```flip``` Flips a coin and randomly outputs wither 'heads' or 'tails'\n```kick [<user>]``` Kicks a user from the server. \n```calc [<first number>] [<+, -, *, or / >] [<second number>]``` Outputs the answer of the math operation the command sender has input.\n```ping``` Outputs the latency/ping from your device to the bot.\n```servers```Outputs the number of servers the bot it in.\n```ticket```Creates a temporary channel that only Admins and the ticket creator has access to.\n```ticketclose```Closes the ticket, must be used in the ticket channel you want to close.\n**There are more commands than the ones that are listed, but they are in the beta or alpha versions.**\n*The suggest feature is the only alpha feature listed.*",
        colour=discord.Colour.purple()
    )
    await ctx.send(embed=embed)

@client.command(aliases=['sup', 'server', 'feedback'])
async def support(ctx):
    embed = discord.Embed(
        title="Support and Feedback",
        description=f"**All resources are in the Spectral Bot Support and Feedback server. Join to get support or resources, also join to give feedback: **https://discord.gg/qmMpyBh99e\n`hlp for commands.",
        colour=discord.Colour.purple()
    )
    await ctx.send(embed=embed)

@client.command()
async def ticket(ctx):
    ticketchannel=await ctx.message.guild.create_text_channel(f'TICKET-{ctx.message.author}')
    await ticketchannel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ticketchannel.set_permissions(ctx.message.author, view_channel=True)
    await ticketchannel.set_permissions(ctx.message.author, send_messages=True)
    await ticketchannel.set_permissions(ctx.message.author, embed_links=True)
    await ticketchannel.set_permissions(ctx.message.author, attach_files=True)
    await ticketchannel.send("``ticketclose`` command to close the ticket.")
    await ctx.message.delete()



@client.command()
async def ticketclose(ctx):
    if ctx.message.channel.name.startswith("ticket"):
        await ctx.message.channel.delete()
    else:
        await ctx.send("You can only use this command in a ticket channel!")


@client.command(aliases=['sm'])
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode for this channel to {seconds} seconds!")


@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, user:discord.Member, *, reason=None):
    try:
        with open('warnings.json', 'r') as f:
            prefixes=json.load(f)
        warnings = prefixes[f"{str(ctx.guild.id)}, {str(user.id)}"]
        newwarnings=warnings+1
        with open('warnings.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[f"{str(ctx.message.guild.id)}, {str(user.id)}"] = newwarnings
        with open('warnings.json', 'w') as f:
            json.dump(prefixes, f)
        embed = discord.Embed(
            title="Warned",
            description=f"{user} has been warned. They now have {newwarnings} warnings.\n\nWarned by: {ctx.message.author}.\n\nReason: {reason}.",
            colour=discord.Colour.red()
        )
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    except:
        with open('warnings.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[f"{str(ctx.guild.id)}, {user.id}"] = 1
        with open('warnings.json', 'w') as f:
            json.dump(prefixes, f)
        embed = discord.Embed(
            title="Warned",
            description=f"{user} has been warned. This is their first warning.\n\nWarned by: {ctx.message.author}.\n\nReason: {reason}.",
            colour=discord.Colour.red()
        )
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def warnings(ctx, user:discord.Member, amount:int=None):
    if amount==None:
        try:
            with open('warnings.json', 'r') as f:
                prefixes = json.load(f)
            warnings = prefixes[f"{str(ctx.guild.id)}, {str(user.id)}"]
            await ctx.send(f"{user.mention} has {warnings} warnings.")
        except:
            await ctx.send(f"{user.mention} doesn't have any warnings.")
    else:
        try:
            with open('warnings.json', 'r') as f:
                prefixes = json.load(f)
            warnings = prefixes[f"{str(ctx.guild.id)}, {str(user.id)}"]
            newwarnings = amount
            with open('warnings.json', 'r') as f:
                prefixes = json.load(f)
            prefixes[f"{str(ctx.message.guild.id)}, {str(user.id)}"] = newwarnings
            with open('warnings.json', 'w') as f:
                json.dump(prefixes, f)
            embed = discord.Embed(
                title="Warnings Changed",
                description=f"{user}'s warnings have been changed. They now have {newwarnings} warnings.\n\nWarnings changed by: {ctx.message.author}.",
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

        except:
            with open('warnings.json', 'r') as f:
                prefixes = json.load(f)
            prefixes[f"{str(ctx.guild.id)}, {user.id}"] = amount
            with open('warnings.json', 'w') as f:
                json.dump(prefixes, f)
            embed = discord.Embed(
                title="Warnings Changed",
                description=f"{user}'s warnings have been changed. They now have {newwarnings} warnings.\n\nWarnings changed by: {ctx.message.author}.",
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)


@client.command()
async def time(ctx, timezone=None):

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    await ctx.send("The current time (central time) is "+current_time)

@client.command()
@commands.has_permissions(administrator=True)
async def setjoinchannel(ctx, channel: discord.TextChannel):
    with open('joinchannel.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.message.guild.id)] = channel.id
    with open('joinchannel.json', 'w') as f:
        json.dump(prefixes, f)

@client.command()
async def yeet(ctx):
    await ctx.send("https://tenor.com/bf63y.gif")

@client.event
async def on_member_join(member):
    try:
        with open('joinchannel.json', 'r') as f:
            prefixes = json.load(f)
        jchannelid = prefixes[f"{str(member.guild.id)}"]
        jchannel= member.guild.get_channel(int(jchannelid))
        embed = discord.Embed(
            title=f"{member} has joined the server!",
            description=f"{member.mention} has joined the server! Make sure to welcome them!",
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=member.avatar_url)
        await jchannel.send(embed=embed)
        print(jchannel.id)
    except:
        print("No Join channel")


client.run('My Token')
