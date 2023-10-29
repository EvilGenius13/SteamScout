# Steam Game Watchlist Bot

The Steam Game Watchlist Bot is a Discord bot written in Python that allows users to interact with the Steam API to retrieve information about games, add games to a watchlist, and manage their watchlist.

## Features

- Check detailed information about a game using its app ID.
- Add games to your watchlist by specifying their app IDs.
- View your watchlist to keep track of the games you're interested in.
- Find games in your watchlist by searching for their names.
- Remove games from your watchlist by specifying their app IDs.
- Help command to explain how to use each bot command.

## Usage
**BOT COMMANDS*
- `*check <app_id>`: Fetches detailed information about a game using its app ID from the Steam API.

- `*add <app_id>`: Adds a game to your watchlist by specifying its app ID.

- `*watchlist`: Displays your current watchlist of games.

- `*find <game_name>`: Finds a game in your watchlist by searching for its name and fetches information from Steam.

- `*remove <app_id>`: Removes a game from your watchlist by specifying its app ID.

- `*commands`: Provides information about the available bot commands and their usage.

### Installation
- Install the required packages using `pip install -r requirements.txt`.
- Create a .env file in the root directory and add your bot token in the following format:
```python
DISCORD_TOKEN=<your_token_here>
```
- Run the bot using `python main.py`.
