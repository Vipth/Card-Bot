import asyncio, discord, random
from LocalLibs.gameLib import Game_Handler
from LocalLibs import dbhandler as dbh
from discord.ext import commands
from replit import db

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='texasholdem', aliases=['thold'])
    async def texashold(self, ctx):
        """A game of Texas Holdem. Include the amount of players as a command argument."""
        CH = Game_Handler.Card_Hierarchy()
        self.highest_bet = 0

        # The function for betting 
        async def betting(user, dealer):
            def check(msg):
                return msg.author.id == user.id and msg.channel == ctx.channel
                
            await ctx.send(f"<@{user.id}>, Would you like to bet, raise, or fold?")
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            bet = None

            if msg.content.lower() == "bet":
                if self.highest_bet == 0:
                    await ctx.send("Enter the amount you would like to bet:")
                    bet = await self.bot.wait_for('message', check=check, timeout=120.0)
                    while int(bet.content) < 0 or bet == None or type(bet) == str:
                        await ctx.send("Please enter a valid amount:")
                        bet = await self.bot.wait_for('message', check=check, timeout=120.0)
                    self.highest_bet = int(bet.content)
                else:
                    bet = self.highest_bet
                db[str(user.id)]['Money'] -= int(bet.content)
                dealer.prize_pool += int(bet.content)

            if msg.content.lower() == 'raise':
                await ctx.send("Enter the amount you would like to raise to:")
                bet = await self.bot.wait_for('message', check=check, timeout=120.0)
                while int(bet.content) < self.highest_bet or bet == None or type(bet) == str:
                    await ctx.send("Please enter a valid amount:")
                    bet = await self.bot.wait_for('message', check=check, timeout=120.0)

                self.highest_bet = int(bet.content)
                db[str(user.id)]['Money'] -= int(bet.content)
                dealer.prize_pool += int(bet.content)


            if msg.content.lower() == 'fold':
                await ctx.send(f"<@{user.id}> has folded.")
                del players[user]
                return

        # The loop that bets and gives cards to the
        async def betshow(amount):
            if len(players) > 1:
              for player in list(players): 
                await betting(player, Dealer)
              Dealer.deal_cards(river, amount)
              await ctx.send(CH.format_cards(river))
              Dealer.deal_cards(discard, 1)
            else:
              await ctx.send("player is the winner")
              db[str(user.id)]['Money'] += Dealer.prize_pool
              Dealer.prize_pool = 0

        # Buy in variable
        buy_in = 25 # Default is 25

        # This is the emote the bot uses to get the players that want to play the game
        ticket = "🎟️"

        # Create the Game Handler
        GH = Game_Handler()

        # Create the Dealer
        Dealer = GH.Dealer()

        # Get players and add them to a list
        x = await ctx.send(f"{ctx.author.mention} has created a game of texas holdem! react to join the game.")
        await x.add_reaction(ticket)
        message = discord.utils.get(self.bot.cached_messages, id=x.id)
        await asyncio.sleep(5)
        # Creates a set to store the user variables
        users = []
        # Gets the channel that the invitation message was sent to
        channel = self.bot.get_channel(x.channel.id)
        # Gets the ID of the invitation message
        message = await channel.fetch_message(x.id)
        # Iterates through the reactions on the invitation message sent by the bot
        for reaction in message.reactions:
            # Iterates through the user list of everyone who reacted
            async for user in reaction.users():
                # Checks to make sure the user isn't a bot and that they reacted with the ticket emote
                if user.bot == False and reaction.emoji == ticket:
                    # Adds them to the list of users who want to play the game.
                    users.append(user)

        # Ensures the user exists in the database, and adds them if they're not.
        for user in users:
            id = str(user.id)
            if dbh.check_exist(id) == False:
                dbh.create_user(id)
                print(f"Added {id} / {user.name}#{user.discriminator} to the database.")

        # Check if the player can afford the buy-in
        cant_play = ''
        for user in users:
            id = str(user.id)
            if db[id]['Money'] < buy_in:
                users.remove(user)
                cant_play += f"{user.name}, "
        cant_play = cant_play[0:-2]
        if len(cant_play) != 1:
            await ctx.send(f"The following users can't afford the buy-in: {cant_play}")
            continue_game = await ctx.send("Do you wish to continue with the game?")
            await continue_game.add_reaction('✔️')
            await continue_game.add_reaction('❌')
            await asyncio.sleep(5)
            x = discord.utils.get(self.bot.cached_messages, id=continue_game.id)
            channel = self.bot.get_channel(x.channel.id)
            message = await channel.fetch_message(x.id)
            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.bot == False:
                        if user.id == ctx.author.id:
                            if reaction.emoji == '✔️':
                                continue
                            else:
                                return await ctx.send("Game Stopped.")

        # Yoinks but in Cash
        for user in users:
            db[str(user.id)]['Money'] -= buy_in
            Dealer.prize_pool += buy_in
 
        # Shuffle the players so the playing order is randomized.
        random.shuffle(users)

        # Player dictionary to store player objects
        players = {}
        river = GH.Player("River")
        discard = GH.Player("Discard")

        # Add all players to a dictionary and convert them to player objects with the Game_Handler
        for i, v in enumerate(users):
            players.update({(v): GH.Player(v.id)})
        # Iterate through each player, give them their cards, then DM them their hand
        for player in players:
            Dealer.deal_cards(players[player])
            await player.send(f"Your hand: {CH.format_cards(players[player])}")

        while len(players) > 2:
          await betshow(3)
          await betshow(1)
          await betshow(1)
          break 
        else:
          await ctx.send("The game ended")
 
        if len(players) > 1:
          for player in players:
            await ctx.send(f"{player}'s hand: {CH.format_cards(players[player])}")
          await ctx.send(CH.format_cards(river))
        
        for i, v in enumerate(players):
            hand = CH.format_cards(players[v])
            river = CH.format_cards(river)
            if CH.royal_flush(hand, river):
                players[v].hand_value = 10
            elif CH.straight_flush(hand, river):
                players[v].hand_value = 9
            elif CH.four_of_kind(hand, river):
                players[v].hand_value = 8
            elif CH.full_house(hand, river):
                players[v].hand_value = 7
            elif CH.flush(hand, river):
                players[v].hand_value = 6
            elif CH.straight(hand, river):
                players[v].hand_value = 5
            elif CH.three_of_kind(hand, river):
                players[v].hand_value = 4
            elif CH.two_pair(hand, river):
                players[v].hand_value = 3
            elif CH.pair(hand, river):
                players[v].hand_value = 2
        
        # we need to compare the values to this some how
        pl = []
        for v in range(len(players)):
            pl.append(players)
        print(pl)

        for i, v in enumerate(players):
            player_one = players[v].hand_value
            for j, k in enumerate(players):
                player_two = players[k].hand_value
                if len(pl) == 1:
                    break
                if i != j:
                    if player_one > player_two:
                        del pl[j]

        players = pl
        await ctx.send(f"{player}'s is the winner")
        db[str(user.id)]['Money'] += Dealer.prize_pool
        Dealer.prize_pool = 0