import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp 
import asyncio
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '$',intents=intents)




@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Hello!')
    
@bot.command(name='exit')
async def exiting(ctx):
    await ctx.send('exiting...')
    await bot.close()
    

@bot.command(name='stats')
async def show_player_stats(ctx,arg):
    stats_url = f"https://api.chess.com/pub/player/{arg}/stats"
    headers = {'User-Agent': 'Chessy Discord bot'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(stats_url) as response:
            if response.status != 200:
                await ctx.send(f"Couldn't find a Chess.com player called **{arg}**.")
                return
            data = await response.json()

    rapid = data.get('chess_rapid')
    if rapid is None:
        await ctx.send(f"**{arg}** hasn't played any rated rapid games.")
        return

    record = rapid['record']
    embed = discord.Embed(
        title=f"{arg}'s Rapid Stats",
        url=f"https://www.chess.com/member/{arg}",
        color=discord.Color.green(),
    )
    embed.add_field(name='Current', value=rapid['last']['rating'], inline=True)
    embed.add_field(name='Best', value=rapid['best']['rating'], inline=True)
    embed.add_field(name='Record (W/L/D)', value=f"{record['win']} / {record['loss']} / {record['draw']}", inline=False)
    embed.set_footer(text='Data from Chess.com')
    await ctx.send(embed=embed)

            

        
    
    
bot.run(TOKEN)    
