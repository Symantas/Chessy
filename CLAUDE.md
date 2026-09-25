# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Chessy is a Discord chess bot written in Python using `discord.py`. The whole bot currently lives in `main.py`.

## Running

There is no dependency manifest, build step, linter config, or test suite yet. Dependencies (inferred from imports):

```bash
pip install discord.py aiohttp python-dotenv
```

The bot reads `DISCORD_TOKEN` from the environment, loaded via `python-dotenv` from a `.env` file in the repo root (`.env` is gitignored). Run it with:

```bash
python main.py
```

The Discord application must have the **Message Content** privileged intent enabled, since the bot sets `intents.message_content = True`.

## Architecture

- A single `commands.Bot` instance with command prefix `$`; commands are registered with `@bot.command(name=...)` decorators in `main.py`, and `bot.run(TOKEN)` at module level starts the bot (so importing `main.py` launches it).
- Commands: `$hello` (greeting), `$exit` (closes the bot — no permission check), `$stats <username>` (fetches player stats from the public Chess.com API and replies with an embed).
- External data comes from the Chess.com public API (`https://api.chess.com/pub/player/{username}/stats`), fetched with `aiohttp` inside the command handler. Only the rapid rating (`data['chess_rapid']['last']['rating']`) is shown; there is no handling yet for unknown users, HTTP errors, or players without a rapid rating.

## How to work with me

- I'm learning. Don't create or edit files unless I explicitly say "implement" or "edit".
- When I ask how to do something: suggest 2–3 approaches with trade-offs and point to relevant docs. Don't write the full solution.
- Discord plumbing and boilerplate: OK to write when I ask.
- Analysis code (Stockfish, blunder detection, pattern finding): hints and review only. I write it.
- When I share code I wrote: review it, explain what's wrong and why, but don't rewrite it.

## Project notes

- discord.py is async: never call blocking code (e.g. Stockfish) directly in a command handler.
- Never commit the bot token or .env.
- Stockfish is installed at: TODO (path not set yet)
