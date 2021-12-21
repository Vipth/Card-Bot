from discord.ext import commands
from replit import db
from LocalLibs import dbhandler as dbh

# Utility Commands
class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='stats')
    async def stats(self, ctx):
        """
        Return the user's stats from the database to chat.
        """
        if dbh.check_exist(str(ctx.author.id)) == True:
            # Inital string that is edited in the loop below.
            stats_string = ''

            # Iterates through the user's stats and add's them to a string that will be sent by the bot to the chat.
            for key in db[str(ctx.author.id)]:
                stats_string = stats_string + (f"{key}: {db[str(ctx.author.id)][key]}\n")
            await ctx.send(stats_string)
        else:
            return await ctx.send("Player not in database. use `!register` to register an account with the bot.")

    @commands.command(name='register', aliases=['reg'])
    async def register(self, ctx):
        """
        Register's the user to the database.
        """
        id = str(ctx.author.id)
        if dbh.check_exist(id) == False:
            dbh.create_user(id)
            await ctx.send(f"You have registered an account!")
        else:
            await ctx.send("You're already registered!")