# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## How to work with me (learning mode)

I'm building this project to learn. Follow these rules unless I explicitly say otherwise for a specific task:

- **Don't write feature code for me.** Explain the concept, point to the relevant API or docs, and let me write it. Only write code directly when it's pure boilerplate (config files, `requirements.txt`, imports, repetitive setup) or when I ask for it explicitly.
- **Guide with questions and hints first.** When I'm stuck, give the smallest nudge that unblocks me: a question, a hint, or the name of the function or concept to look up. Escalate to a fuller explanation only if I'm still stuck.
- **Review, don't rewrite.** When I share code, point out bugs, edge cases and better approaches, and explain *why*. Let me make the fix myself.
- **Explain trade-offs.** When there are several ways to do something, lay out the options and their trade-offs briefly and let me choose.
- **Small illustrative snippets are OK** (a few lines that show how an unfamiliar library call works), as long as they aren't the actual solution pasted into place.

## Project

Chessy is a Discord chess bot written in Python with `discord.py`. The whole bot currently lives in `main.py`.

## Running

There is no requirements file, build step, linter config or test suite yet. Dependencies are installed by hand:

```
pip install discord.py python-dotenv aiohttp
python main.py
```

The bot reads `DISCORD_TOKEN` from a `.env` file in the repo root, loaded with `python-dotenv`. `.env` is gitignored. The bot needs the **Message Content** privileged intent turned on in the Discord developer portal, because `main.py` sets `intents.message_content = True`.

## Architecture

- A single `commands.Bot` with the command prefix `$`. Commands are registered with `@bot.command(name=...)` decorators in `main.py`. There are no cogs or extensions yet.
- `bot.run(TOKEN)` at the bottom of the module blocks. New commands must be defined above that line.
- Chess data comes from the public Chess.com API (`https://api.chess.com/pub/player/{username}/...`). Calls go through `aiohttp`, never a blocking HTTP library, so the event loop keeps running.
- Current commands: `$hello`, `$exit`, which shuts the bot down with `bot.close()` and has no permission check, and `$stats <username>`. `$stats` is still in progress: it fetches the stats JSON and only prints it to the console. Nothing is sent back to Discord yet.

## Planned features

- **`$analyse <username>`**: analyse the user's last game (or last 5 games) with the Stockfish engine and report their most common blunders and ways to improve. Relevant building blocks:
  - Chess.com endpoints: `/pub/player/{username}/games/archives` lists the monthly archive URLs, and each archive returns games with PGN.
  - The `python-chess` library can parse PGN and drive a local Stockfish binary over UCI. Its `chess.engine` module has an asyncio API, which matters because blocking engine calls would freeze the bot.
  - Engine analysis is slow. Think about analysis depth or time limits, and how the bot stays responsive while analysing (for example, send a "working on it" message first).
