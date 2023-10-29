import discord
import os
from discord.ext import commands
import requests
import json

from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def save_watchlist(watchlist_data):
  with open('watchlist.json', 'w') as f:
    json.dump(watchlist_data, f)

def load_watchlist():
  try:
    with open('watchlist.json', 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return []

@bot.event 
async def on_ready():
  print("Bot is ready")

@bot.command()
async def check(ctx, arg):
    try:
        response = requests.get(f'https://store.steampowered.com/api/appdetails?appids={arg}')
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error_message = f'Error: {e}'
        await ctx.send(error_message)
        return

    data = response.json()
  
    if arg in data:
        game_data = data[arg]['data']
        game_name = game_data.get('name', 'Name not found')
        header_image = game_data.get('header_image', 'Image not found')

        price_overview = game_data.get('price_overview', None)
        if price_overview:
            final_formatted = price_overview.get('final_formatted', 'Final price not found')
            discount = price_overview.get('discount_percent', 'No current discount')
            description = game_data.get('short_description', 'No description found')
        else:
            final_formatted = 'Price not listed'
            discount = '0'
            description = 'No description found'
            release_date = 'No release date found'

        release_date_data = game_data.get('release_date', {})
        is_coming_soon = release_date_data.get('coming_soon', False)
        release_date = release_date_data.get('date', 'No release date found')

        embed = discord.Embed(title=f'Game Name: {game_name}')
        if is_coming_soon:
            embed.add_field(name='Release Date', value='Coming Soon', inline=True)
        else:
            embed.add_field(name='Release Date', value=release_date, inline=True)
        embed.add_field(name='Description', value=description, inline=False)
        embed.set_image(url=header_image)
        embed.add_field(name='Current Price', value=final_formatted, inline=True)
        embed.add_field(name='Discount', value=f'**{discount}%**', inline=True)
        

        await ctx.send(embed=embed)
    else:
        await ctx.send('Game not found')

@bot.command()
async def add(ctx, arg):
    try:
      response = requests.get(f'https://store.steampowered.com/api/appdetails?appids={arg}')
      response.raise_for_status()
    except requests.exceptions.RequestException as e:
      error_message = f'Error: {e}'
      await ctx.send(error_message)
      return
    
    data = response.json()

    if arg in data:
       game_data = data[arg]['data']
       game_name = game_data.get('name', 'Name not found')

       watchlist = load_watchlist()

       watchlist.append({'app_id': arg, 'game_name': game_name})

       save_watchlist(watchlist)

       await ctx.send(f'Added {game_name} to watchlist')
    else:
        await ctx.send('Game not found')

@bot.command()
async def watchlist(ctx):
    watchlist = load_watchlist()

    if not watchlist:
       await ctx.send('Watchlist is empty')
       return

    watchlist_text = '\n'.join([f"App ID: {item['app_id']} | Game Name: {item['game_name']}" for item in watchlist])
    await ctx.send(f'**Watchlist**:\n{watchlist_text}')

@bot.command()
async def find(ctx, *, arg):
   watchlist = load_watchlist()

   matching_games = [item for item in watchlist if arg.lower() in item['game_name'].lower()]

   if not matching_games:
        await ctx.send('No matching games found in the watchlist. Try adding it with the `add` command')
        return
   
   first_matching_game = matching_games[0]
   app_id = first_matching_game['app_id']

   try:
      response = requests.get(f'https://store.steampowered.com/api/appdetails?appids={app_id}')
      response.raise_for_status()
   except requests.exceptions.RequestException as e:
      error_message = f'Error: {e}'
      await ctx.send(error_message)
      return
  
   data = response.json()
  
   if app_id in data:
        game_data = data[app_id]['data']
        game_name = game_data.get('name', 'Name not found')
        header_image = game_data.get('header_image', 'Image not found')

        # Extract price information from price_overview
        price_overview = game_data.get('price_overview', None)
        if price_overview:
            final_formatted = price_overview.get('final_formatted', 'Final price not found')
            discount = price_overview.get('discount_percent', 'No current discount')
            description = game_data.get('short_description', 'No description found')
        else:
            final_formatted = 'Price not listed'
            discount = '0'
            description = 'No description found'
            release_date = 'No release date found'

        release_date_data = game_data.get('release_date', {})
        is_coming_soon = release_date_data.get('coming_soon', False)
        release_date = release_date_data.get('date', 'No release date found')

        embed = discord.Embed(title=f'Game Name: {game_name}', color=0x00ff00)
        if is_coming_soon:
            embed.add_field(name='Release Date', value='Coming Soon', inline=True)
        else:
            embed.add_field(name='Release Date', value=release_date, inline=True)
        embed.add_field(name='Description', value=description, inline=False)
        embed.set_image(url=header_image)
        embed.add_field(name='Current Price', value=final_formatted, inline=True)
        embed.add_field(name='Discount', value=f'**{discount}%**', inline=True)
        
        await ctx.send(embed=embed)
   else:
        await ctx.send('Game not found in the Steam store.')

@bot.command()
async def remove(ctx, app_id: int):
    watchlist = load_watchlist()

    # Find the index of the game with the given app ID in the watchlist
    index_to_remove = None
    for i, item in enumerate(watchlist):
        if item['app_id'] == str(app_id):
            index_to_remove = i
            break

    if index_to_remove is not None:
        # Remove the game from the watchlist
        removed_game = watchlist.pop(index_to_remove)
        save_watchlist(watchlist)
        await ctx.send(f'Removed game with App ID {app_id} from the watchlist: {removed_game["game_name"]}')
    else:
        await ctx.send(f'Game with App ID {app_id} not found in the watchlist.')

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Steam Game Watchlist Bot Help", color=0x00ff00)

    embed.add_field(
        name="*check <app_id>",
        value="Fetches information about a game with the specified app ID from Steam.",
        inline=False,
    )

    embed.add_field(
        name="*add <app_id>",
        value="Adds a game with the specified app ID to the watchlist.",
        inline=False,
    )

    embed.add_field(
        name="*watchlist",
        value="Displays the current watchlist of games.",
        inline=False,
    )

    embed.add_field(
        name="*find <game_name>",
        value="Finds a game in the watchlist by name and fetches its information from Steam.",
        inline=False,
    )

    embed.add_field(
        name="*remove <app_id>",
        value="Removes a game with the specified app ID from the watchlist.",
        inline=False,
    )

    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)