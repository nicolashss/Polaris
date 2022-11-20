# V 1.0.5
# By LuX


# Modules 
# ----------------------

import discord
import json
from discord.ext import commands, tasks
from random import choice
import asyncio
import aiohttp
from discord.ext.commands import Bot
from discord import Game
import requests
import os 
import random
from discord import Intents
import random
import os
import requests

# ----------------------

bot = commands.Bot(command_prefix=".", description="Developed by LuX", intents=Intents.all())
intents = discord.Intents.default()
intents.members = True
couleurs = [0x00ff36, 0xeb7807, 0xf47fff, 0x11100d, 0xe6493f, 0x00e9ff]

bot.ticket_configs = {}

# Tickets
# ---------------------------------------------------------------------------

@bot.event
async def on_ready():
    print("___________________________________________Le bot est connecté.___________________________________________")

@bot.event
async def on_message(message):
    # await bot.handler.propagate(message)
    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def delete(ctx, nombre: int):
    print(f"Suppression de {nombre} messages")
    list_suppr = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in list_suppr:
        await message.delete()
    embed = discord.Embed(description=f"{nombre} messages ont été supprimés.", color=0x0089ff)
    await ctx.send(embed=embed)

# Bienvenue

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(1005098550625062934)
    print(f"{member} a joint le seveur {member.guild.name}")
    embed = discord.Embed(title="《 Welcome to xLuX.xyz 》", description=f"**Hey** {member.mention}\n✅  | Don't hesitate to read the rules of {member.guild.name}! And on those, I wish you a good time on our discord :)", color=random.choice(couleurs))
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="《 xLuX.xyz | By xLuX 》")
    await channel.send(embed=embed)
    role = discord.utils.get(member.guild.roles, name = "Members")
    await member.add_roles(role)

# Commande de modération :

@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} was banned for the following reason: {reason}.")
    
# ---------------------------------------------------------------------------

@commands.has_permissions(ban_members=True)
@bot.command()
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} was unban.")
            return

    await ctx.send(f"The user {user} is not in the list of bans.")

# ---------------------------------------------------------------------------

@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} was kicked.")

# ---------------------------------------------------------------------------


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

# ---------------------------------------------------------------------------

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)


@commands.has_permissions(manage_messages=True)
@bot.command()
async def mute(ctx, member : discord.Member, *, reason = ""):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} was muted!")

@commands.has_permissions(manage_messages=True)
@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = ""):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} was unmute!")

bot.run(token)