#importing required libraries
import datetime as dt
from enum import Flag
from os import error
import random
import re
import aiohttp
import discord
from discord import channel
import giphy_client
import requests
import swaglyrics.cli as swaglyrics
import config

from discord import embeds
from random import choice
from typing import Optional
from aiohttp.client import request
from discord import Embed
from discord import Spotify
from discord.ext import commands, tasks
from discord.ext.commands.core import has_permissions
from discord.ext.commands import Context
from discord_components import *
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash import SlashCommand
from giphy_client.rest import ApiException

#API keys and some random variables

unsplash = ""
weather_key = ""
base_url = "http://api.openweathermap.org/data/2.5/weather?"
astrowebsite = "https://astrobot.me"

client = commands.Bot(command_prefix=commands.when_mentioned_or(','), intents=discord.Intents.all())
client.remove_command('help')

def split_on_paragraph(string: str):
    splitted = []
    buffer = ""
    for s in string.split("\n\n"):
        s += "\n\n"
        if len(buffer) + len(s) > 1024:
            splitted.append(buffer)
            buffer = ""
        buffer += s
    return splitted

slash = SlashCommand(client, sync_commands=True)

guild_ids = [817040371325468684]

@client.event
async def on_ready():
    print('Astro is connected to Discord')
    DiscordComponents(client)
    status = discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers!")
    await client.change_presence(status=discord.Status.idle, activity=status)

@client.command(help="Shows the latency of bot")
async def ping(ctx):
    if round(client.latency * 1000) <= 20:
        embed = discord.Embed(title="Fast AF Boi!!", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0x2ecc71, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    elif round(client.latency * 1000) <= 50:
        embed = discord.Embed(title="Not Fast Enough :')", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0xffd000, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    elif round(client.latency * 1000) <= 100:
        embed = discord.Embed(title="Your Wifi is Slow", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0xe67e22, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    else:
        embed = discord.Embed(title="Ouch, That's Slow", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0xe74c3c, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


@slash.slash(name='ping', description='Shows the latency of bot')
async def ping(ctx):
    if round(client.latency * 1000) <= 20:
        embed = discord.Embed(title="Fast AF Boi!!", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0x2ecc71)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    elif round(client.latency * 1000) <= 50:
        embed = discord.Embed(title="Not Fast Enough :')", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0xffd000)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    elif round(client.latency * 1000) <= 100:
        embed = discord.Embed(title="Your Wifi is Slow", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0xe67e22)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    else:
        embed = discord.Embed(title="Ouch, That's Slow", description=f"⌛ **{round(client.latency * 1000)}** ms!",
                              color=0xe74c3c)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


@client.command(aliases=['j'])
async def jumbo(ctx, emoji: discord.Emoji = None):
    if not emoji:
        await ctx.send("Please provide an emoji!")
    else:
        await ctx.send(emoji.url)


@client.command(aliases=['hey', 'hi', 'hy'])
async def hello(ctx):
    responses = ['Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.reply(choice(responses))

@slash.slash(name='hello', description='say hello to bot')
async def hello(ctx):
    responses = ['Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.reply(choice(responses))

@commands.has_permissions(manage_messages=True)
@has_permissions(manage_messages=True)
@client.command(alises=['purge', 'Purge', 'Clear', 'delete', 'Delete'])
async def clear(ctx, limit: Optional[int] = 1):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=limit)
    await ctx.send(f"**Deleted** {len(deleted):,} messages.", delete_after=6)
    pass

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("You don't have permission(s) to manage messages of this server")
        

@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(color=000000, title=f'{member.name} has been kicked', description=f'Reason - {reason}',
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/794595829238464523.gif?v=1')
    embed.set_footer(text=f"Kicked by {ctx.author}")
    await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please specify a valid user")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission(s) to kick members of this server")
    else:
        raise error


@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(color=000000, title=f'{member.name} has been banned', description=f'Reason - {reason}',
                          timestamp=ctx.message.created_at)
    embed.set_image(
        url='https://media4.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif')
    embed.set_footer(text=f"Banned by {ctx.author}")
    await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please specify a valid user")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission(s) to ban members of this server")
    else:
        raise error


client.launch_time = dt.datetime.utcnow()
@client.command()
async def uptime(ctx):
    delta_uptime = dt.datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.reply(f"I\'ve been up for {days}d, {hours}h, {minutes}m, {seconds}s")


determine_flip = [1, 0]
@client.command()
async def flipcoin(ctx):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(title="Flipped A Coin", description="**Heads**!", color=000000)
        embed.set_thumbnail(url="https://i.imgur.com/5QaWKpL.gif")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Flipped A Coin", description="**Tails**!", color=000000)
        embed.set_thumbnail(url="https://i.imgur.com/5QaWKpL.gif")
        embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)


@client.event
async def on_message(message):
    if message.content in [f'<@{client.user.id}', f'<@!{client.user.id}>']:
        embed = discord.Embed(title='Server Prefix', description=f'Hey {message.author.mention} my prefix in this server is `,`', color=000000)
        embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
        await message.channel.send(embed=embed)
    if isinstance(message.channel, discord.DMChannel):
        emb=discord.Embed(title=message.author, description=message.content)
        channel = client.get_channel(876874511130169394)
        await channel.send(embed=emb)
    await client.process_commands(message)


@client.command(aliases=['img'])
async def image(ctx, *, search):
    client.ses = aiohttp.ClientSession()
    search = search.replace(' ', '-')
    url = f'https://api.unsplash.com/photos/random/?query={search}&client_id={unsplash}'
    async with client.ses.get(url) as r:
        if r.status in range(200, 299):
            data = await r.json()
            url = data['urls']['regular']
            uname = data['user']['username']
            embed = discord.Embed(
                title='Here is your requested image',
                description=f"By [{uname}](https://unsplash.com/@{uname}?utm_source=astro-bot&utm_medium=referral) on Unsplash").set_image(
                url=url)
            await ctx.send(embed=embed)


@client.command()
async def bored(ctx):
    client.ses = aiohttp.ClientSession()
    url = 'https://www.boredapi.com/api/activity/'
    async with client.ses.get(url) as r:
        if r.status in range(200, 299):
            data = await r.json()
            activity = data['activity']
            type = data['type']
            participants = data['participants']
            embed = discord.Embed(
                title='Bored?', description='Here\'s something you can do', color=000000
            ).add_field(name=activity, value=f'Type - {type}\nNumber of participants - {participants}').set_thumbnail(
                url='https://media.tenor.com/images/9f0fc756b9383e86043bd7dfd6241766/tenor.gif')
            await ctx.send(embed=embed)


@client.command()
async def hoomangen(ctx, *, gender):
    client.ses = aiohttp.ClientSession()
    url = f'https://fakeface.rest/face/json?gender={gender}'
    async with client.ses.get(url) as r:
        if r.status in range(200, 299):
            data = await r.json()
            img = data['image_url']
            gender = data['gender']
            age = data['age']
            embed = discord.Embed(
                title='This Human Doesn\'t Exist', description='Displays an image of a person that doesn’t actually exist which are generated by a Deep Neural Network', color=000000
            ).set_image(url=img).add_field(name='Gender -', value=gender).add_field(name='Age -', value=age).set_footer(text="All the images are generated by thispersondoesnotexist.com and are provided for usage only as allowed by that project’s creators.")
            await ctx.send(embed=embed)

@client.command()
async def advice(ctx):
    client.ses = aiohttp.ClientSession()
    url = 'https://api.adviceslip.com/advice'
    async with client.ses.get(url) as r:
        if r.status in range(200, 299):
            data = await r.json(content_type=None)
            advic = data['slip']['advice']
            await ctx.send(f'Here\'s an advice for you - \n{advic}')


@client.command(pass_context=True)
async def gif(ctx, *, q='gif'):
    api_key = ''
    api_instance = giphy_client.DefaultApi()
    try:
        api_responce = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_responce.data)
        giff = random.choice(lst)
        emb = discord.Embed(title=f'<a:sparkles:852928271343419392> Results for {q}<a:sparkles:852928271343419392>')
        emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
        emb.set_thumbnail(url='https://i.imgur.com/BH4Mseg.png')
        await ctx.channel.send(embed=emb)

    except ApiException:
        await print("Exception when calling Api")


@client.command()
async def spotify(ctx, user: discord.Member = None):
    message = ctx.message
    if user is None:
        user = ctx.author
    spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if user.status == discord.Status.offline:
        await ctx.send(f'{user.display_name} is offline')
    else:
        if spotify_result is None:
            await ctx.send(f'{user.display_name} is not listening to Spotify right now.')
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(
                    title=f"<:spotify:854936708910940181> {user.display_name}'s Spotify",
                    description=f"Listening to [{activity.title}](https://open.spotify.com/track/{spotify_result.track_id})",
                    color=0x2ecc71)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                embed.set_footer(text=f"Requested by {ctx.author}")
                if ctx.author.mentioned_in(message):
                    await ctx.send('You dont have to mention yourself to see your Spotify, anyways -')
                await ctx.send(embed=embed,
                components=[
                        [
                    Button(style=ButtonStyle.URL, label="Open in Spotify", url=f"https://open.spotify.com/track/{spotify_result.track_id}"),
                    Button(label="Get lyrics")
                        ]
                    
                    ]
                )

    res = await client.wait_for("button_click")
    if res.channel == ctx.channel:
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content= "This feature will be availble soon, until then please use the `,lyrics` command.",
            ephemeral=False
        )

@client.command()
async def lyrics(ctx: Context, user: discord.Member = None):
    spotify: discord.Spotify
    ath: discord.Member = ctx.author
    if user is None:
        user = ctx.author
    spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if user.status == discord.Status.offline:
        await ctx.send(f'{user.display_name} is offline')
    else:
        if spotify_result is None:
            await ctx.send(f"{user.display_name} are not listening to Spotify right now.")
    
    for activity in user.activities:
        if isinstance(activity, discord.Spotify):
            spotify = activity
            break
    else:
        return
    await ctx.send("<a:loading:876031038281904148>", delete_after=1)    
    l = swaglyrics.lyrics(spotify.title, spotify.artist)
    l_splitted = split_on_paragraph(l)
    embed: discord.Embed = (discord.Embed(title=f"{activity.title} \nby {spotify.artist}", color=000000)
                            .set_footer(text=f"Requested by {ath.name}#{ath.discriminator}",
                                        icon_url=ath.avatar_url)).set_image(url=activity.album_cover_url)
    for idx, part in enumerate(l_splitted):
        embed.add_field(name=f"{idx+1}/{len(l_splitted)}", value=part, inline=False)
    await ctx.send(embed=embed,
    components=[
            Button(style=ButtonStyle.URL, label="Open in Spotify", url=f"https://open.spotify.com/track/{spotify.track_id}")
        ],
    )
    

@client.command()
async def salute(ctx):
    await ctx.send("<:salute:822099584762249246>")

@client.command()
async def hug(ctx, user: discord.Member = None):
    if user == None:
        await ctx.send('Mention the user you want to send hug to')

    elif user == ctx.author:
        await ctx.send(f'I\'ll hug you {ctx.author.display_name} ;-;')
        await ctx.send('https://tenor.com/view/bay-max-big-hero6-gif-5101373')

    elif user == client.user:
        responses = ['<:iosplead:854993979661484052> Thank You!!']
        await ctx.send(choice(responses))

    else:
        responses = [f'awww, you gave a hug to {user.display_name} <:iosplead:854993979661484052>',
                     'https://cdn.discordapp.com/emojis/803562963424378930.gif?v=1']
        await ctx.send(choice(responses))


@client.command(pass_context=True)
async def google(ctx, *, message: str):
    message = message.replace(' ', '+')
    embed = discord.Embed(title='Let Me Google That', colour=0xffffff, timestamp=ctx.message.created_at)
    embed.add_field(name='Results-',
                    value=f'<a:Sparkles:852918135296360448>https://letmegooglethat.com/?q={message}<a:Sparkles:852918135296360448>')
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/728473878946381934.gif')
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def duck(ctx, *, message: str):
    message = message.replace(' ', '+')
    embed = discord.Embed(color=0xe74c3c, title='DuckDuckGo')
    embed.add_field(name='Results -', value=f'https://duck.com/?q={message}')
    embed.set_thumbnail(url='https://i.imgur.com/fvjtJZK.png')
    embed.set_footer(text='DuckDuckGo. Privacy, Simplified.')
    await ctx.send(embed=embed)


@client.command()
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + weather_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            c_name = response.json()["name"]
            country_name = response.json()["sys"]["country"]

            z = x["weather"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {c_name}, {country_name}",
                              color=000000,
                              timestamp=ctx.message.created_at,)
            embed.add_field(name="Descripition", value=f"{weather_description}", inline=False)
            embed.add_field(name="Temperature", value=f"{current_temperature_celsiuis}°C", inline=False)
            embed.add_field(name="Humidity", value=f"{current_humidity}%", inline=False)
            embed.add_field(name="Atmospheric Pressure", value=f"{current_pressure}hPa", inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/851805970987876404/858786298927251486/weather_2.gif")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send("City not found.")


@client.command(aliases=['profilepic', 'pfp', 'av'])
async def avatar(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(title=f'{member.display_name}\'s Profile Picture', color=000000, timestamp=ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


format = "%a, %d %b %Y | %H:%M %ZGMT"
@client.command(aliases=['sinfo'])
async def serverinfo(ctx):
    id = str(ctx.guild.id)
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner.mention)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    created = str(ctx.guild.created_at.strftime(format))
    bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
    hoomans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
    icon = str(ctx.guild.icon_url)
    embed = discord.Embed(title=name + " Server Information", description=description, color=00000)
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    embed.add_field(name="Bots", value=bots, inline=True)
    embed.add_field(name="Hoomans", value=hoomans, inline=True)
    embed.add_field(name="Date Created", value=created, inline=True)
    await ctx.send(embed=embed)


@client.command(aliases=["ui"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    if member.status == discord.Status.online:
        embed = discord.Embed(colour=000000, timestamp=ctx.message.created_at, title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]

        banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
        embed.set_image(url=banner_url)
            

        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="ID:", value=member.id)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Status:", value="<:online:857264271980494849> Online")
        embed.add_field(name="Highest Role:", value=member.top_role.mention)

        await ctx.send(embed=embed)

    elif member.status == discord.Status.idle:
        embed = discord.Embed(colour=000000, timestamp=ctx.message.created_at, title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]

        banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
        embed.set_image(url=banner_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Status:", value="<:idle:857264271771697162> Idle")
        embed.add_field(name="Highest Role:", value=member.top_role.mention)

        await ctx.send(embed=embed)

    elif member.status == discord.Status.do_not_disturb:
        embed = discord.Embed(colour=000000, timestamp=ctx.message.created_at, title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]
        
        banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
        embed.set_image(url=banner_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Status:", value="<:dnd:857264251312144424> DND")
        embed.add_field(name="Highest Role:", value=member.top_role.mention)

        await ctx.send(embed=embed)


    else:
        embed = discord.Embed(colour=000000, timestamp=ctx.message.created_at, title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]

        banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
        embed.set_image(url=banner_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Status:", value="<:offline:857264271724118017> Offline")
        embed.add_field(name="Highest Role:", value=member.top_role.mention)

        await ctx.send(embed=embed)

@client.command()
async def vote(ctx):
    embed = discord.Embed(title="Vote Page", color=00000, timestamp=ctx.message.created_at)
    embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
    embed.add_field(name="Vote to help me grow faster", value='[Click here](https://discord.ly/astro-bot/upvote) to vote or use the new buttons.',
                    inline=False)
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed,
                components=[
                    [
            Button(style=ButtonStyle.URL, label="Vote On Discordbotlist", url="https://discord.ly/astro-bot/upvote"),
            Button(style=ButtonStyle.URL, label="Vote On Top.gg", url="https://top.gg/bot/841269196376637450/vote")
                ]
                ]
            )


@client.command(aliases=['si'])
async def serverinvite(ctx):
    invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)
    await ctx.author.send('Here is the invite link to server')
    await ctx.author.send(invitelink)
    embed = discord.Embed(title='Server Invite Link', color=00000, timestamp=ctx.message.created_at)
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
    embed.add_field(name='**Sent!**', value='I have sent this server invite link in your DMs', inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['i', 'Invite'])
async def invite(ctx):
    embed = discord.Embed(title='Invite Link', color=00000, timestamp=ctx.message.created_at)
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
    embed.add_field(name='To add me to your server',
                    value='[Click here](https://astrobot.me/invite) \n \n Or Scan the QR code given below.',
                    inline=False)
    embed.set_image(url="https://i.imgur.com/4C0DP3F.png")
    await ctx.send(embed=embed)


@client.command(name='dev', help='About the developer')
async def dev(ctx):
    embed = discord.Embed(title="Astrogeek", description="Astrogeek#0002", color=0x000000,
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(url="https://i.imgur.com/F1gdA28.png")
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    embed.add_field(name="Website", value='http://astro.taufeeq.team', inline=False)
    embed.add_field(name="Github", value='http://github.taufeeq.team', inline=False)
    embed.add_field(name="Instagram", value='http://insta.taufeeq.team', inline=False)
    embed.add_field(name="Mail", value='contact@taufeeq.team', inline=False)
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help Page", description="Support has arrived!", color=000000,
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(url="https://media.tenor.com/images/056dda4212a51107e1f80fa6ab035b55/tenor.gif")
    embed.add_field(name="For Detailed Documentation Visit", value="[Astro Bot Website](http://astrobot.me/commands)",
                    inline=False)
    embed.add_field(name="To Add Me To You Server",
                    value="[Use This Link](https://astrobot.me/invite)",
                    inline=False)
    embed.add_field(name="To See The List Of Commands", value="Use the ,commands command", inline=False)
    embed.add_field(name="To see the list of Music Commands", value="Use the ,mcommands or ,musiccommands",
                    inline=False)
    embed.add_field(name="Vote", value="[Vote to support me :)](https://discord.ly/astro-bot)", inline=False)
    embed.set_image(url='https://i.imgur.com/Gj1mLFo.png')
    await ctx.send(embed=embed, 
            components=[
            Button(style=ButtonStyle.URL, label="Astrobot Website", url=astrowebsite),
            Button(style=ButtonStyle.URL, label="Invite Me", url="https://astrobot.me/invite")
        ],
    )
    

@slash.slash(name="help", description="More slash commands coming soon")
async def help(ctx):
    embed = discord.Embed(title="Help Page", description="Support has arrived!", color=000000)
    embed.set_thumbnail(url="https://media.tenor.com/images/056dda4212a51107e1f80fa6ab035b55/tenor.gif")
    embed.add_field(name="For Detailed Documentation Visit", value="[Astro Bot Website](http://astrobot.me/commands)",
                    inline=False)
    embed.add_field(name="To Add Me To You Server",
                    value="[Use This Link](https://astrobot.me/invite)",
                    inline=False)
    embed.add_field(name="To See The List Of Commands", value="Use the ,commands command", inline=False)
    embed.add_field(name="To see the list of Music Commands", value="Use the ,mcommands or ,musiccommands",
                    inline=False)
    embed.add_field(name="Vote", value="[Vote to support me :)](https://discord.ly/astro-bot)", inline=False)
    embed.set_image(url='https://i.imgur.com/Gj1mLFo.png')
    await ctx.send(embed=embed)

#Astro meth

@client.command() 
async def add(ctx, *nums):
    operation = " + ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def sub(ctx, *nums): 
    operation = " - ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def multiply(ctx, *nums): 
    operation = " * ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def divide(ctx, *nums): 
    operation = " / ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')


@client.command()
async def dm(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send("Mention the user or provide user id of the user you want me to send a DM to.")

    else:
        embed=discord.Embed(title=f"Sure, What do you want me to send to {member.display_name} ?", description="By using the DM command, you agree to the following [Terms and Conditions](https://astrobot.me/DM-Tos)")
        await ctx.send(embed=embed)
        def check(m):
            return m.author.id == ctx.author.id
        message = await client.wait_for('message', check=check)
        await ctx.send(f'Message sent to {member.display_name}!')
    
        await member.send(f"{ctx.author.mention} Sent a message - \n{message.content}")


@client.command()
@commands.is_owner()
async def bs(ctx):
    await ctx.channel.send(f"I'm in {len(client.guilds)} servers!")

@client.command()
@commands.is_owner()
async def servers(ctx):
    if ctx.guild.id == 855281187739402241:
        activeservers = client.guilds
        for guild in activeservers:
            await ctx.send(guild.name)
    else:
        return


@client.command()
async def commands(ctx):
    embed = discord.Embed(title="List Of Commands",
                          description="For detailed documentation on how to use commands visit [Astro Bot Website](https://astrobot.me)",
                          color=00000)
    embed.set_thumbnail(url="https://i.imgur.com/3fE2zQi.jpeg")
    embed.add_field(name="To see the list of Music Commands", value="```Use ,mcommands or ,musiccommands```",
                    inline=False)
    embed.add_field(name="Ping", value="Shows the latency of bot\n```,ping```", inline=False)
    embed.add_field(name="Hey", value="Say Hi to bot\n```,hi\n,hey\n,hy\n,hello```", inline=False)
    embed.add_field(name="Delete Multiple Messages",
                    value="Clears the number of messages provided by author\n\n*You need 'manage messages' permission to use this command*\n```,clear <number of messages>\n,Clear\n,purge\n,Purge\n,delete\n,Delete```",
                    inline=False)
    embed.add_field(name="Kick A User",
                    value="Kicks the the specified user from server\n\n*You need 'kick members' permission to use this command*\n```,kick <mention user>```",
                    inline=False)
    embed.add_field(name="Ban A User",
                    value="Bans the specified user from server\n\n*You need 'ban members' permission to use this command*\n```,ban <mention user>```",
                    inline=False)
    embed.add_field(name="Jumbo Emoji", value="Sends requested enlarged custom emoji\n```,jumbo <emoji>\n,j <emoji>```",
                    inline=False)
    embed.add_field(name="Image", value="Sends a random image of your request\n```,image <search>\n,img <search>```",
                    inline=False)
    embed.add_field(name="Gif", value="Sends a random gif of your request\n```,gif <search>```", inline=False)
    embed.add_field(name="Spotify",
                    value="Shows the song details of the song a user is listening to on Spotify\n```,spotify```",
                    inline=False)
    embed.add_field(name="Welcome A User Using Bot", value="Welcomes a user\n```,welcome <mention user>```",
                    inline=False)
    embed.add_field(name="Print", value="Sends the requested output\n```,print <input>```", inline=False)
    embed.add_field(name="Hug", value="Send virtual hug to a user\n```,hug <mention user>```", inline=False)
    embed.add_field(name="Google", value="Let the bot google a query for you\n```,google <search>```", inline=False)
    embed.add_field(name="DuckDuckGo", value="Gives you results from DuckDuckGo\n```,duck <search>```", inline=False)
    embed.add_field(name="Avatar",
                    value="Sends the profile picture of the requested user\n```,avatar\n,av\n,profilepic\n,pfp```",
                    inline=False)
    embed.add_field(name="Server Info",
                    value="Sends information about the server the command is used in\n```,serverinfo or ,sinfo```",
                    inline=False)
    embed.add_field(name="User Info",
                    value="Sends the profile information of the requested user\n```,userinfo <mention user>\n,ui <mention user>```",
                    inline=False)
    embed.add_field(name="Vote For Bot", value="Vote for the  bot to support :)\n```,vote```", inline=False)
    embed.add_field(name="Server Invite Link", value="DMs you the server invite link\n```,serverinvite\n,si```",
                    inline=False)
    embed.add_field(name="Invite Bot",
                    value="Gives you the invite link to add bot to your own server\n```,invite\n,i\n,Invite```",
                    inline=False)
    embed.add_field(name="Dev Info", value="About the developer\n```,dev```", inline=False)
    embed.add_field(name="Help", value="All the usefull stuff in one place\n```,help```", inline=False)
    embed.set_image(url='https://i.imgur.com/Gj1mLFo.png')
    await ctx.send(embed=embed)


@client.command(aliases=['mcommands'])
async def musiccommands(ctx):
    embed = discord.Embed(title="Music Commands", description="List Of Music Commands", color=000000)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/822385499515125770/859081775561310238/849827273313878016.gif")
    embed.add_field(name="<:join:859077566824710224> Join",
                    value="Joins The Voice Channel You Are Currently In\n```,join```", inline=False)
    embed.add_field(name="<:play:859077290843177011> Play",
                    value="Plays Music \n [Or Adds It To The Queue If A Song Is Already Being Played]\n```,play or ,p```",
                    inline=False)
    embed.add_field(name="<:queue:859079092975435787> Queue",
                    value="Shows The List Of Songs That Will Be Played Next\n```,queue or ,q```", inline=False)
    embed.add_field(name="<:pause:859079093219622933> Pause", value="Pauses The Music Player\n```,pause```",
                    inline=False)
    embed.add_field(name="<:resume:859079093256454186> Resume", value="Resumes The Music Player\n```,resume```",
                    inline=False)
    embed.add_field(name="<:skip:859079684247650304> Skip", value="Skips The Song Which Is Being Played\n```,skip```",
                    inline=False)
    embed.add_field(name="<:now:859076865917321216> Now",
                    value="Shows Information About The Song Which Is Being Played\n```,now```", inline=False)
    embed.add_field(name="<:shuffle:859078541092847646> Shuffle", value="Shuffles The Queue\n```,shuffle```",
                    inline=False)
    embed.add_field(name="<:loop:859078541525778434> Loop", value="Plays One Song In Loop\n```,loop```", inline=False)
    embed.add_field(name="<:leave:859077637053349918> Leave", value="Leaves The Voice Channel\n```,leave```",
                    inline=False)
    embed.add_field(name="<:ping:859078541341884455> Music ping", value="Shows The Music Latency\n```,mping```",
                    inline=False)
    embed.set_image(url='https://i.imgur.com/Gj1mLFo.png')
    await ctx.send(embed=embed)  

client.run('TOKEN')