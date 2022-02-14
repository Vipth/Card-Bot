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
        # This need to be rest after every beting phase which I believe I have fixed
        self.highest_bet = 0

        # The function for betting
        async def betting(player_list, dealer):
            # Could it be player_list that causing the issue?
            for user in player_list:

                def check(msg):
                    return msg.author.id == user.id and msg.channel == ctx.channel

                will_fold = False
                await ctx.send(f"<@{user.id}>, Would you like to pass, bet, raise, or fold?")
                msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                bet = None

                if msg.content.lower() == "pass":
                    if self.highest_bet == 0:
                        pass
                    else:
                        bet = self.highest_bet
                        db[str(user.id)]['Money'] -= bet
                        dealer.prize_pool += bet
                        return

                if msg.content.lower() == "bet":
                    if self.highest_bet == 0:
                        await ctx.send("Enter the amount you would like to bet:")
                        bet = await self.bot.wait_for('message', check=check, timeout=120.0)
                        while int(bet.content) < 0 or bet == None or type(bet) == str:
                            await ctx.send("Please enter a valid amount:")
                            bet = await self.bot.wait_for('message', check=check, timeout=120.0)
                        self.highest_bet = int(bet.content)
                        player_list[user].highest_bet = int(bet.content)
                        db[str(user.id)]['Money'] -= int(bet.content)
                        dealer.prize_pool += int(bet.content)
                    else:
                        bet = self.highest_bet
                        db[str(user.id)]['Money'] -= bet
                        dealer.prize_pool += bet
                        player_list[user].highest_bet = bet                    

                if msg.content.lower() == 'raise':
                    await ctx.send("Enter the amount you would like to raise to:")
                    bet = await self.bot.wait_for('message', check=check, timeout=120.0)
                    while int(bet.content) < self.highest_bet or bet == None or type(bet) == str:
                        await ctx.send("Please enter a valid amount:")
                        bet = await self.bot.wait_for('message', check=check, timeout=120.0)

                    self.highest_bet = int(bet.content)
                    db[str(user.id)]['Money'] -= int(bet.content)
                    dealer.prize_pool += int(bet.content)
                    player_list[user].highest_bet = int(bet.content)
                    for player in player_list:
                        if user != player:
                            def check_two(msg):
                                return msg.author.id == player.id and msg.channel == ctx.channel
                            await ctx.send(f"<@{player.id}> do you want to stay or fold?")
                            confirmation = await self.bot.wait_for('message', check=check_two, timeout=120.0)
                            if confirmation.content.lower() == "stay":
                                raise_money = self.highest_bet - player_list[player].highest_bet
                                db[str(player.id)]['Money'] -= raise_money
                                dealer.prize_pool += raise_money
                            elif confirmation.content.lower() == "fold":
                                will_fold = True
                                user_to_fold = player
                                print(user_to_fold)

                if msg.content.lower() == 'fold':
                    await ctx.send(f"<@{user.id}> has folded.")
                    db[user.id]['Losses'] += 1
                    del player_list[user]
                    return
                
                if will_fold == True:
                    await ctx.send(f"<@{user_to_fold.id}> has folded.")
                    db[user.id]['Losses'] += 1
                    del player_list[user_to_fold]
                    return

        buy_in = 25 # Default is 25

        # This is the emote the bot uses to get the players that want to play the game
        ticket = "🎟️"

        # Create the Game Handler
        GH = Game_Handler()

        # Create the Dealer
        Dealer = GH.Dealer()

        # Get players and add them to a list
        x = await ctx.send(f"{ctx.author.mention} has created a game of texas holdem! react to join the game. (Buy in: ${buy_in})")
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
            if dbh.check_exist(str(user.id)) == False:
                dbh.create_user(user.id)
                print(f"Added {user.id} / {user.name}#{user.discriminator} to the database.")

        # Check if the player can afford the buy-in
        cant_play = ''
        for user in users:
            if db[str(user.id)]['Money'] < buy_in:
                users.remove(user)
                cant_play += f"{user.name}, "
        cant_play = cant_play[0:-2]
        if len(cant_play) >= 1:
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

            # For "testing" puroses 
            """
            players[player].hand =  {
                "Clubs": {'Ace' : 1},
                "Diamonds": {'Ace': 1},
                "Spades": {},
                "Hearts": {}
            }
            """

            await player.send(f"Your hand: {CH.format_cards(players[player])}")


        # First betting
        if len(players) > 1:
            await betting(players, Dealer)
            Dealer.deal_cards(river, 3)
            await ctx.send(CH.format_cards(river))
            Dealer.deal_cards(discard, 1)

            # Second betting
            if len(players) > 1:
                await betting(players, Dealer)
                Dealer.deal_cards(river, 1)
                await ctx.send(CH.format_cards(river))
                Dealer.deal_cards(discard, 1)

                # Third betting
                if len(players) > 1:
                    await betting(players, Dealer)
                    Dealer.deal_cards(river, 1)
                    await ctx.send(CH.format_cards(river))
                    Dealer.deal_cards(discard, 1)
                else:
                    await ctx.send(f"<@{user.id}> is the winner!")
                    db[str(user.id)]['Money'] += Dealer.prize_pool
                    Dealer.prize_pool = 0

            else:
                await ctx.send(f"<@{user.id}> is the winner!")
                db[str(user.id)]['Money'] += Dealer.prize_pool
                Dealer.prize_pool = 0

        else:
            await ctx.send("Not Enough Players.")
 
        if len(players) > 1:
          for player in players:
            await ctx.send(f"{player}'s hand: {CH.format_cards(players[player])}")

        river = CH.format_cards(river)
        for i, v in enumerate(players):
            hand = CH.format_cards(players[v])
            player = players[v]
            if CH.royal_flush(hand, river):
                players[v].hand_value += 9
            elif CH.straight_flush(hand, river):
                players[v].hand_value += 8
            elif CH.four_of_kind(player, hand, river):
                players[v].hand_value += 7
            elif CH.full_house(hand, river):
                players[v].hand_value += 6
            elif CH.flush(hand, river):
                players[v].hand_value += 5
            elif CH.straight(hand, river):
                players[v].hand_value += 4
            elif CH.three_of_kind(player, hand, river):
                players[v].hand_value += 3
            elif CH.two_pair(player, hand, river):
                players[v].hand_value += 2
            elif CH.pair(player, hand, river):
                players[v].hand_value += 1
            else:
                players[v].hand_value += 0

            players[v].hand_value += CH.high_card(hand, river)

        hand_values = {}
        for player in players:
            hand_values.update({players[player]: players[player].hand_value})

        highest_value_holder = []
        for i, v in enumerate(hand_values):
            for x, y in enumerate(hand_values):
                if i != x and (y not in highest_value_holder and v not in highest_value_holder) and (v != y):
                    if v.hand_value > y.hand_value:
                        highest_value_holder.append(v)
                    elif v.hand_value < y.hand_value:
                        highest_value_holder.append(y)
                    else:
                        highest_value_holder.append(v)
                        highest_value_holder.append(y)


        if len(highest_value_holder) > 1:
            message = 'The Winners Are: '
            for i, v in enumerate(highest_value_holder):
                message += (f"<@{v.name}>" + ", ")
            message = message[:-2] + "!"
            await ctx.send(message)
            for i in range(len(highest_value_holder)):
                db[str(highest_value_holder[i].name)]['Money'] += (round(Dealer.prize_pool, 2) / len(highest_value_holder))
                db[str(highest_value_holder[i].name)]['Total Winnings'] += (round(Dealer.prize_pool, 2) / len(highest_value_holder))
                db[str(highest_value_holder[i].name)]['Wins'] += 1

            Dealer.prize_pool = 0

        elif len(highest_value_holder) == 1:
            await ctx.send(f"<@{highest_value_holder[0].name}> is the winner!")
            db[str(highest_value_holder[0].name)]['Money'] += Dealer.prize_pool
            db[str(highest_value_holder[i].name)]['Total Winnings'] += Dealer.prize_pool
            db[str(highest_value_holder[i].name)]['Wins'] += 1
            Dealer.prize_pool = 0