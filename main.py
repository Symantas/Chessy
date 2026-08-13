import discord
import os
import aiohttp 
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Hello!')
    

@bot.command(name='exit')
async def exiting(ctx):
    await ctx.send('exiting...')
    await bot.close()
    

@bot.command(name='stats')
async def show_player_stats(ctx, arg):
    stats_url = f"https://api.chess.com/pub/player/{arg}/stats"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(stats_url) as response:
            data = await response.json()
            
            embed = discord.Embed( 
                title=f"Chess.com Stats for {arg}",
                description="Stats are pulled from live Rapid rating",
                color=discord.Color.green()                    
            )
            
            embed.add_field(
                name="Rapid ⏱️",
                value=str(data['chess_rapid']['last']['rating']),
                inline=True
            )
            
            await ctx.send(embed=embed)
            
            
bot.run(TOKEN)