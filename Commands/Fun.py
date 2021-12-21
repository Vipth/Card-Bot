from discord.ext import commands
import asyncio, discord

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rnr', aliases=['rick'])
    async def rick(self, ctx, args=None):
        #this sets up for the embed by make the title, description, link, and the default color. - Hank
        embed = discord.Embed(title="github link", description="Take you to the github page for the bot some that if you are curoius you can look at it",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        if args != None:
            await ctx.send(f"<@{args[2:-1]}>")
            print(args)
        await ctx.send(embed=embed)
        await asyncio.sleep(25)
        await ctx.send(file=discord.File('Funny_Img/RickRoll.png')) 