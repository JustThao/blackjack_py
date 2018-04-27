import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck():

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        # card passed in
        # from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        # values from global dictionary
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value >= 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Place your bet: \n"))
        except ValueError:
            print("Please only numbers")
        else:
            if chips.bet > chips.total:
                print("Sorry, you only have " + chips.total + " left")
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while playing:
        player_decision = input("Do you want to hit or stand? h or s: \n")
        if player_decision[0].lower() == "h":
            hit(deck, hand)
            for card in hand.cards:
                print(card)
            print(player_hand.value)
        elif player_decision[0].lower() == "s":
            print("stand, dealer is playing")
            playing = False
        else:
            print("only h or s")
            continue


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    print("Bust Player")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Player wins, Dealer busted")
    chips.win_bet


def dealer_wins(player, dealer, chips):
    print("Dealer wins, Player busted")
    chips.lose_bet


def push(player, dealer):
    print("Player and Dealer tie")


def play_again():
    return input("Do you want to play again? y or n \n").lower().startswith("y")


while True:
    # Print an opening statement
    print("Welcome to Console Blackjack")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            dealer_wins(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        else:
            while dealer_hand.value < 17:
                dealer_hand.add_card(deck.deal())

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
            player_wins(player_hand, dealer_hand, player_chips)
            player_chips.win_bet()
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
            player_chips.win_bet()
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
            player_chips.lose_bet()
        else:
            push(player_hand, dealer_hand)

    # Inform Player of their chips total
    print(f"You have {player_chips.total} left")
    # Ask to play again
    if not play_again():
        break
    else:
        playing = True
