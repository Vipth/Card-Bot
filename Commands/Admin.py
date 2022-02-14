from discord.ext import commands
from LocalLibs import dbhandler as dbh
from replit import db

# Dev discord Ids 
developers = ['228706397272014859', '491709222472515594']

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command(name='cleardb', aliases=['cleardatabase', 'resetdb'])
    async def cleardb(self, ctx):
        if str(ctx.author.id) not in developers:
            return await ctx.send("Invalid Permission.")
        await ctx.send(dbh.wipe_database())
            
    @commands.command(name='reset')
    async def reset(self, ctx, args):
        """
        Dev command to reset a player's data.
        """
        if str(ctx.author.id) not in developers:
            return await ctx.send("Invalid Permission.")
        
        if args == None:
            return await ctx.send("Please specify a player to reset.")
        else:
            args = str(args[2:-1])
            if dbh.check_exist(args) == True:
                del db[args]
                await ctx.send(f"<@{args}>'s data has been wiped.")
            else:
                await ctx.send("User not in database.")

    @commands.command(name='forceregister')
    async def forceregister(self, ctx, args):

        if str(ctx.author.id) not in developers:
            return await ctx.send("c")

        mentioned = args[2:-1]

        if dbh.check_exist(mentioned) == False:
            dbh.create_user(mentioned)
            await ctx.send("Registered user.")
        else:
            await ctx.send("User already registered.")

    @commands.command(name='spawnmoney', aliases=['grant'])
    async def spawnmoney(self, ctx, *args):
        if str(ctx.author.id) not in developers:
            return await ctx.send("No money printer for you")
        
        db[str(ctx.author.id)]['Money'] += int(args[0])