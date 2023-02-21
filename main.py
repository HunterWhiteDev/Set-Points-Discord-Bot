import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
from discord.utils import get
load_dotenv();

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents(messages=True, guilds=True, message_content=True, members=True)

client = discord.Client(intents=intents);
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f"{client.user} has connected to Discord!")
    print(f"{guild.name} (ID: {guild.id})")
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

async def removePreviousRoles(user: discord.Member):
    roles = user.roles;
    for role in roles:
        prevRole = str(role.name[0:7])
        if prevRole == "Points:": 
            # user.remove_roles(role)
            await user.remove_roles(role);
            print("user role removed")
            if(len(role.members) < 1):
                await role.delete()
                
async def addNewRole(ctx, user: discord.Member, points: int): 
    role = get(ctx.guild.roles, name=f"Points: {points}")
    if role == None: 
        await ctx.guild.create_role(name=f"Points: {points}", color=discord.Colour(0xFF6700))
        newRole = get(ctx.guild.roles, name=f"Points: {points}")
        await user.add_roles(newRole);
    else: 
        await user.add_roles(role);
        
        
async def getUserPoints(user):
    roles = user.roles;
    for role in roles:
        prevRole = str(role.name[0:7])
        points = str(role.name[8:len(role.name)])
        if prevRole == "Points:":
            return points

@bot.command(pass_context=True)
async def setPoints(ctx, user: discord.Member, points):
    author = ctx.author;
    if(str(author) == "VividElites#9979"):
      await removePreviousRoles(user=user);
      await addNewRole(ctx=ctx, user=user, points=points);
      await ctx.send(f"{user.mention} had their points set to {points}!");
    else:
     await ctx.send(f"{author.mention} tried to use a command they don't have access to everyone point and laugh <a:soypoint:1056030957209128971>")
     

#Adding and subtracting are works in progress
# @bot.command(pass_context=True)
# async def addPoints(ctx, user: discord.Member, points):
#     author = ctx.author;
#     if(str(author) == "VividElites#9979"):
#       oldPoints = await getUserPoints(user=user);
#       await removePreviousRoles(user=user);
#       if oldPoints == None:
#           await addNewRole(ctx=ctx, user=user, points=points)
#           await ctx.send(f"{user.mention} had {points} points added!");
#       else:
#         newPoints = int(oldPoints) + int(points);
#         await addNewRole(ctx=ctx, user=user, points=newPoints);
#         await ctx.send(f"{user.mention} had {points} added!");
#     else:
#      await ctx.send(f"{author.mention} tried to use a command they don't have access to everyone point and laugh <a:soypoint:1056030957209128971>")

# @bot.command(pass_context=True)
# async def subPoints(ctx, user: discord.Member, points):
#     author = ctx.author;
#     if(str(author) == "VividElites#9979"):
#       oldPoints = await getUserPoints(user=user);
#       await removePreviousRoles(user=user);
#       if oldPoints == None:
#           await addNewRole(ctx=ctx, user=user, points=points)
#           await ctx.send(f"{user.mention} had {points} points subtracted!");
#       else:
#         newPoints = int(oldPoints) + int(points);
#         await addNewRole(ctx=ctx, user=user, points=newPoints);
#         await ctx.send(f"{user.mention} had {points} subtracted!");
#     else:
#      await ctx.send(f"{author.mention} tried to use a command they don't have access to everyone point and laugh <a:soypoint:1056030957209128971>")




    

bot.run(TOKEN)