from discord.ext import commands
from LocalLibs import dbhandler as dbh
from replit import db

# Economy Commands
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='give', aliases=['pay'])
    async def give(self, ctx, *args):
        """
        Transfers money between the players. `!give @Vipth 500`
        """
        author = str(ctx.author.id)
        mentioned = str(args[0][2:-1])
        amount = args[1]

        if dbh.check_exist(author) == False:
            return await ctx.send("You are not in database. use `!register` to register an account with the bot.")

        if dbh.check_exist(mentioned) == False:
            return await ctx.send("That user is not in the database.")

        if args == None:
            return await ctx.send("Enter a user and an amount!")

        # Try to convert the second argument to an integer.
        try:
            amount = int(amount)
            if amount < 1:
                return await ctx.send("Invalid Amount.")
            if amount > db[author]['Money']:
                return await ctx.send(f"You only have ${db[author]['Money']}")
                
        except ValueError:
            return await ctx.send("Invalid amount.")

        # Transfer money between users.
        db[author]['Money'] -= amount
        db[mentioned]['Money'] += amount
        return await ctx.send(f"You have sent <@{mentioned}> ${amount}")
        
        

    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, args=None):
        """
        Returns the user's money to chat.
        """
        if args == None:
            # If args are empty, set the args to the author's ID
            args = str(ctx.author.id)
        else:
            # If the author pings a user in the command, then we set args to that user's ID
            args = str(args[2:-1])
        exists = dbh.check_exist(args)
        
        if exists == True:
            return await ctx.send(f"${db[args]['Money']}")
        else:
            return await ctx.send("Player not in database. use `!register` to register an account with the bot.")