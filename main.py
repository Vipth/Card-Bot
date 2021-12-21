"""
Song that have been left:
Rick Ashelys "Never Going to Give You Up"
Smash Mouth "All Star"
(This list is unfinished, but you can help by add to it.)
"""

import json
from discord.ext import commands
from Games.Card_Games import Games
from Commands.Economy import Economy
from Commands.Util import Info
from Commands.Admin import Admin
from Commands.Fun import Fun

def main():
    file = open('config/config.json')
    config = json.load(file)
    token = config['token']

    bot = commands.Bot(command_prefix="!", case_insensitive=True)

    @bot.event
    async def on_ready():
        print(f"successfully logged in as {bot.user}")

    bot.add_cog(Games(bot))
    bot.add_cog(Economy(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(Admin(bot))

    bot.run(token)

if __name__ == '__main__':
    main()