from random import choice

class Game_Handler:
    """
    Tool to assist in building card games\n
    Dealer Class:
    ---
    `Holds the deck of cards and deals with card disribution.`
    Player Class:
    ---
    `Object that stores the player variables.`
    Card Hierarchy:
    ---
    `Checks to see what type of hand the player has`
    """

    class Dealer:
        """
        Holds the deck of cards and deals with card disribution.

        Functions:
        ---
        `random_card()` - `Selects a random card within the deck.`
        `deal_cards(player, cards=2)` - `Deals an amount, cards, to a player.`
        """
        def __init__(self):
            self.Dealer = Game_Handler.Dealer
            # We'll store the buy in money within the Dealer class.
            self.prize_pool = 0
            # This is the deck of cards. 1 means the card is in the deck, 0 means the card is somewhere else.
            self.Deck = {
            "Clubs": {
                "Ace": 1,
                "Two": 1,
                "Three": 1,
                "Four": 1,
                "Five": 1,
                "Six": 1,
                "Seven": 1,
                "Eight": 1,
                "Nine": 1,
                "Ten": 1,
                "Jack": 1,
                "Queen": 1,
                "King": 1
            },
            "Diamonds": {
                "Ace": 1,
                "Two": 1,
                "Three": 1,
                "Four": 1,
                "Five": 1,
                "Six": 1,
                "Seven": 1,
                "Eight": 1,
                "Nine": 1,
                "Ten": 1,
                "Jack": 1,
                "Queen": 1,
                "King": 1
            },
            "Spades": {
                "Ace": 1,
                "Two": 1,
                "Three": 1,
                "Four": 1,
                "Five": 1,
                "Six": 1,
                "Seven": 1,
                "Eight": 1,
                "Nine": 1,
                "Ten": 1,
                "Jack": 1,
                "Queen": 1,
                "King": 1
            },
            "Hearts": {
                "Ace": 1,
                "Two": 1,
                "Three": 1,
                "Four": 1,
                "Five": 1,
                "Six": 1,
                "Seven": 1,
                "Eight": 1,
                "Nine": 1,
                "Ten": 1,
                "Jack": 1,
                "Queen": 1,
                "King": 1
            }
        }

        def random_card(self):
            """Selects a random card from the deck."""
            # Creates a list containing the suites with cards left.
            active_suites = []
            for suite in self.Deck:
                suite_total = 0
                for card in self.Deck[suite]:
                    suite_total += self.Deck[suite][card]
                if suite_total > 0:
                    active_suites.append(suite)

            # Picks a suite from the list created above.
            self.suite = choice(active_suites)

            # Creates a list of active cards from the suite chosen from above.
            active_cards_in_list = []
            for card in self.Deck[self.suite]:
                if self.Deck[self.suite][card] == 1:
                    active_cards_in_list.append(card)
            
            # Picks a card from the list created above.
            self.card = choice(active_cards_in_list)

            # Removes card from Deck
            self.Deck[self.suite][self.card] = 0

            # Returns the card that has been chosen.
            return self.suite, self.card

        def deal_cards(self, player, cards=2):
            """Deals cards."""
            for _ in range(cards):
                suite, card = self.random_card()
                player.hand[suite].update({card: 1})
            
    class Player:
        """
        Object that stores the player variables.
        Functions:
        ---
        `play_card(player, card: tuple)` - `Transfers a card to another player object.`\n
        `get_cards()` - `Returns a neater dictionary only containing the cards in the player hand.`
        """
        def __init__(self, player_name):
            self.name = player_name
            self.hand = {
                "Clubs": {},
                "Diamonds": {},
                "Spades": {},
                "Hearts": {}
            }
            self.hand_value = 0
            
        def play_card(self, player, card: tuple):
            """
            Transfers a card to another player object.\n
            Recieves the card in the tuple format: (Suite, Card). `Ex:("Hearts", "Ace")`.
            """
            suite, card = card[0], card[1]
            if self.hand[suite][card] == 1:
                self.hand[suite].update({card: 0})
                player.hand[suite].update({card: 1})
            else:
                print(f"Card does not exist within {self.name}'s hand.")

    class Card_Hierarchy:

        def format_cards(self, player, high_ace=False):

            cards = dict()
            hand = player.hand
            # Updates the active suites in the cards dictionary.
            for suite in hand:
                suite_total = 0
                for card in hand[suite]:
                    suite_total += hand[suite][card]
                if suite_total > 0:
                    cards.update({suite: {}})
            
            # Updates the active cards to the proper suite in the cards dictionary.
            for suite in hand:
                for card in hand[suite]:
                    if hand[suite][card] == 1:
                        cards[suite].update({card: 1})
            hand = cards

            suite = list(hand.keys())
            cards_list = []
            card = ''
            if len(suite) == 1:
                for i in range(len(suite) + 1):
                    card_s = suite[0]
                    card = card + f'{list(hand[card_s])[i]} of '
                    card = card + f'{str(suite[0])}'
                    cards_list.append(card)
                    card = ''
            else:
                for i in range(len(suite)):
                    for x in range(len(hand[suite[i]])):
                        card_s = suite[i]
                        card = card + f'{list(hand[card_s])[x]} of '
                        card = card + f'{str(suite[i])}'
                        cards_list.append(card)
                        card = ''
            
            formatted_cards = []
            for i, v in enumerate(cards_list):
                card = ''
                if "Ace" in v:
                    if high_ace == True:
                        card = f'{v.split()[2][0]}14'
                        formatted_cards.append(card)
                    else:
                        card = f'{v.split()[2][0]}1'
                        formatted_cards.append(card)
                elif "Two" in cards_list[i]:
                    card = f'{v.split()[2][0]}2'
                    formatted_cards.append(card)
                elif "Three" in cards_list[i]:
                    card = f'{v.split()[2][0]}3'
                    formatted_cards.append(card)
                elif "Four" in cards_list[i]:
                    card = f'{v.split()[2][0]}4'
                    formatted_cards.append(card)
                elif "Five" in cards_list[i]:
                    card = f'{v.split()[2][0]}5'
                    formatted_cards.append(card)
                elif "Six" in cards_list[i]:
                    card = f'{v.split()[2][0]}6'
                    formatted_cards.append(card)
                elif "Seven" in cards_list[i]:
                    card = f'{v.split()[2][0]}7'
                    formatted_cards.append(card)
                elif "Eight" in cards_list[i]:
                    card = f'{v.split()[2][0]}8'
                    formatted_cards.append(card)
                elif "Nine" in cards_list[i]:
                    card = f'{v.split()[2][0]}9'
                    formatted_cards.append(card)
                elif "Ten" in cards_list[i]:
                    card = f'{v.split()[2][0]}10'
                    formatted_cards.append(card)
                elif "Jack" in cards_list[i]:
                    card = f'{v.split()[2][0]}11'
                    formatted_cards.append(card)
                elif "Queen" in cards_list[i]:
                    card = f'{v.split()[2][0]}12'
                    formatted_cards.append(card)
                elif "King" in cards_list[i]:
                    card = f'{v.split()[2][0]}13'
                    formatted_cards.append(card)
                card = ''
            return formatted_cards

        def pair(self, hand, river):

            # Pair in hand
            if hand[0][1:] == hand[1][1:]:
                return True

            # Pair in hand + river
            for i in range(len(hand)):
                for x in range(len(river)):
                    if hand[i][1:] == river[x][1:]:
                        return True

            # Pair in river
            for x in range(len(river)):
                for y in range(len(river)):
                    y += 1
                    if x + y >= len(river):
                        return False
                    z = x + y
                    if river[x][1:] == river[z][1:]:
                        return True

            return False

        def two_pair(self, hand, river):
            # Copy all cards to a separate list
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(v)
            for _, v in enumerate(river):
                all_cards.append(v)

            # Compare cards
            amount_of_pairs = 0
            indices_to_avoid = []
            for i in range(len(all_cards)):
                card_one = all_cards[i]
                for j in range(len(all_cards)):
                    card_two = all_cards[j]
                    if i != j:
                        if i not in indices_to_avoid and j not in indices_to_avoid:
                            if card_one[1:] == card_two[1:]:
                                indices_to_avoid.append(i)
                                indices_to_avoid.append(j)
                                amount_of_pairs += 1
            if amount_of_pairs >= 2:
                return True
            return False

        def three_of_kind(self, hand, river):
            # Copy all cards to a separate list
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(int(v[1:]))
            for _, v in enumerate(river):
                all_cards.append(int(v[1:]))
            print(all_cards)

            # Compare cards
            for i in range(len(all_cards)):
                card_one = all_cards[i]
                for j in range(len(all_cards)):
                    card_two = all_cards[j]
                    for k in range(len(all_cards)):
                        card_three = all_cards[k]
                        #It is working where it find the three of a kinds
                        if i != j and i != k and j != k: 
                            if card_one == card_two and card_one == card_three:
                                return True

            return False

        def straight(self, hand, river):
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(int(v[1:]))
            for _, v in enumerate(river):
                all_cards.append(int(v[1:]))

            for i in range(len(all_cards)):
                card_one = all_cards[i]
                for j in range(len(all_cards)):
                    card_two = all_cards[j]
                    for k in range(len(all_cards)):
                        card_three = all_cards[k]
                        for x in range(len(all_cards)):
                            card_four = all_cards[x]
                            for z in range(len(all_cards)):
                                card_five = all_cards[z]
                                if (i != j and i != k and i != x and i != z) and (j != k and j != x and j != z) and (x != z and  k != x) and (k != z ):
                                            if card_one + 1 == card_two and card_two +1 == card_three and card_three + 1 == card_four and card_four + 1 == card_five:
                                                print(card_one, card_two, card_three, card_four, card_five)
                                                return True
                                            #This if statment makes ace works for 1, 2, 3, 4, 5
                                            if card_one == 14 and card_two == 2 and card_three == 3 and card_four == 4 and card_five == 5:
                                                return True
            return False

        def flush(self, hand, river):
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(v)
            for _, v in enumerate(river):
                all_cards.append(v)

            for i in range(len(all_cards)):
                card_one = all_cards[i][0:1]
                for j in range(len(all_cards)):
                    card_two = all_cards[j][0:1]
                    for k in range(len(all_cards)):
                        card_three = all_cards[k][0:1]
                        for x in range(len(all_cards)):
                            card_four = all_cards[x][0:1]
                            for z in range(len(all_cards)):
                                card_five = all_cards[z][0:1]
                                if (i != j and i != k and i != x and i != z) and (j != k and j != x and j != z) and (x != z and  k != x) and (k != z ):
                                            if (card_one == card_two) and (card_two == card_three) and (card_three == card_four) and (card_four == card_five):
                                                return True
            return False

        def full_house(self, hand, river):
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(int(v[1:]))
            for _, v in enumerate(river):
                all_cards.append(int(v[1:]))

            for i in range(len(all_cards)):
                card_one = all_cards[i]
                for j in range(len(all_cards)):
                    card_two = all_cards[j]
                    for k in range(len(all_cards)):
                        card_three = all_cards[k]
                        for x in range(len(all_cards)):
                            card_four = all_cards[x]
                            for z in range(len(all_cards)):
                                card_five = all_cards[z]
                                if (i != j and i != k and i != x and i != z) and (j != k and j != x and j != z) and (x != z and  k != x) and (k != z ):
                                    if (card_one == card_two) and (card_two == card_three) and (card_four == card_five):
                                        return True
            return False

        # When ahead a did four of a kind since it would be easy so now we have royal flush and straight flush - H.D.
        def four_of_kind(self, hand, river):
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(int(v[1:]))
            for _, v in enumerate(river):
                all_cards.append(int(v[1:]))

            for i in range(len(all_cards)):
                card_one = all_cards[i]
                for j in range(len(all_cards)):
                    card_two = all_cards[j]
                    for k in range(len(all_cards)):
                        card_three = all_cards[k]
                        for x in range(len(all_cards)):
                            card_four = all_cards[x]
                            if i != j and i != k and i !=x and j != k and j != x and k != x: 
                                if card_one == card_two and card_one == card_three and card_one == card_four:
                                    return True

            return False

        # Taking a shot at doing straight flush and I think I did it correctly - H.D.
        def straight_flush(self, hand, river):
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(v)
            for _, v in enumerate(river):
                all_cards.append(v)

            for i in range(len(all_cards)):
                card_one = all_cards[i]
                for j in range(len(all_cards)):
                    card_two = all_cards[j]
                    for k in range(len(all_cards)):
                        card_three = all_cards[k]
                        for x in range(len(all_cards)):
                            card_four = all_cards[x]
                            for z in range(len(all_cards)):
                                card_five = all_cards[z]
                                if (i != j and i != k and i != x and i != z) and (j != k and j != x and j != z) and (x != z and  k != x) and (k != z ):  
                                    if (card_one[0:1] == card_two[0:1]) and (card_two[0:1] == card_three[0:1]) and (card_three[0:1] == card_four[0:1]) and (card_four[0:1] == card_five[0:1]):

                                        if int(card_one[1:]) + 1 == int(card_two[1:]) and int(card_two[1:]) +1 == int(card_three[1:]) and int(card_three[1:]) + 1 == int(card_four[1:]) and int(card_four[1:]) + 1 == int(card_five[1:]):
                                                return True
                                            #This if statment makes ace works for 1, 2, 3, 4, 5
                                        if card_one[1:] == "14" and card_two[1:] == "2" and card_three[1:] == "3" and card_four[1:] == "4" and card_five[1:] == "5":
                                            return True
            return False

        # Got this ready don't know if there are any bugs though - H.D.
        def royal_flush(self, hand, river):
            all_cards = []
            for _, v in enumerate(hand):
                all_cards.append(v)
            for _, v in enumerate(river):
                all_cards.append(v)

            for i in range(len(all_cards)):
                card_one = all_cards[i]
                for j in range(len(all_cards)):
                    card_two = all_cards[j]
                    for k in range(len(all_cards)):
                        card_three = all_cards[k]
                        for x in range(len(all_cards)):
                            card_four = all_cards[x]
                            for z in range(len(all_cards)):
                                card_five = all_cards[z]
                                if (i != j and i != k and i != x and i != z) and (j != k and j != x and j != z) and (x != z and  k != x) and (k != z ):  
                                    if (card_one[0:1] == card_two[0:1]) and (card_two[0:1] == card_three[0:1]) and (card_three[0:1] == card_four[0:1]) and (card_four[0:1] == card_five[0:1]):
                                        if card_one[1:] == "14" and card_two[1:] == "13" and card_three[1:] == "12" and card_four[1:] == "11" and card_five[1:] == "10":
                                            return True

            return False