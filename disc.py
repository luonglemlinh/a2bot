
import discord
from discord.ext import commands
import os
import asyncio
import json
from datetime import datetime
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
with open("token.txt") as f:
    token=f.read()

@bot.event
async def on_ready():
    print("bot is ready to use")
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print(f"failed to sync: {e}")

@bot.tree.command(name="hello",description="Says hello back to the person who typed the command.")
async def hello(interactions:discord.Interaction):
    await interactions.response.send_message(f"Heya {interactions.user.mention}!",ephemeral=False)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1309154321081958445)  
    if channel:  
        await channel.send(f"Hello, {member.mention}!")
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1309154321081958445)  
    if channel:  
        await channel.send(f"goodbye, {member.mention}!")

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello,{ctx.author.mention}")
@bot.command()
async def goodbye(ctx):
    await ctx.send("https://tenor.com/view/kitty-highkitten-mdmacat-cat-happykitty-gif-17268330459933875989")

@bot.command()
async def embed(ctx):
    embed_msg=discord.Embed(title="Title ",description="Description ",color=discord.Color.green())
    embed_msg.set_author(name="Footer text",icon_url=ctx.author.avatar)
    embed_msg.set_thumbnail(url=ctx.author.avatar)
    embed_msg.add_field(name="Name of field",value="Value of field",inline=False)
    embed_msg.set_image(url=ctx.guild.icon)
    embed_msg.set_footer(text="Footer text",icon_url=ctx.author.avatar)
    await ctx.send(embed=embed_msg)

@bot.command()
async def ping(ctx):
    ping_embed=discord.Embed(title="Ping",description="Latency in ms",color=discord.Color.blurple())
    ping_embed.add_field(name=f"{bot.user.name}'s Latency(ms): ",value=f"{round(bot.latency*1000)}ms",inline = False)
    ping_embed.set_footer(text=f"Requested by {ctx.author.name}.",icon_url=ctx.author.avatar)
    await ctx.send(embed=ping_embed)

def get_unexpiredcodes():
    with open("giftcodes.json") as file:
        gc = json.load(file)
        unexpired= [
            code["code"]
            for code in gc
            if code["status"] == "active" and code["expiry_date"]=="never" or datetime.strptime(code["expiry_date"], "%Y-%m-%d") > datetime.now()
        ]
        return unexpired
          
@bot.tree.command(name="giftcodes", description="Shows unexpired giftcodes")
async def giftcode(interaction: discord.Interaction):
    allowed_channel_id=1311900462429110332
    if interaction.channel_id != allowed_channel_id:
        await interaction.response.send_message(f"This command can only be used in <#{allowed_channel_id}>.",ephemeral=False)
    return
 
    codes = get_unexpiredcodes()  
    if codes:
        await interaction.response.send_message(f"Unexpired giftcodes:\n" + "\n".join(codes),ephemeral=False)
    else:
        await interaction.response.send_message("No giftcodes available",ephemeral=True)

bot.run(token)