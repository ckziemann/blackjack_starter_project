import random


class Card:
    def __init__(self, card, value, suit, color):
        self.card = card
        self.value = value
        self.suit = suit
        self.color = color

    def __str__(self):
        return f'{self.card} of {self.suit}'


class Deck:
    def __init__(self):
        self.cards = []
        card_number = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        self.colors = ["Red", "Black"]
        iterations = range(13)
        for n in iterations:
            for s in ["Spades", "Clubs"]:
                self.cards.append(Card(card_number[n], values[n], s, "Black"))
        for n in iterations:
            for s in ["Diamonds", "Hearts"]:
                self.cards.append(Card(card_number[n], values[n], s, "Red"))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


class Shoe:
    def __init__(self, decks):
        self.decks = decks
        self.cards = []
        for deck in self.decks:
            self.cards.extend(deck.cards)

    def new_shoe(self):
        print('*' * 80)
        print('NEW SHOE')
        print('*' * 80)
        print()
        self.cards = []
        deck_list = []
        for j in range(self.decks):
            deck_j = Deck()
            deck_list.append(deck_j)
        new_shoe = Shoe(deck_list)
        random.shuffle(new_shoe.cards)
        for deck in self.decks:
            self.cards.extend(deck.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            self.new_shoe()
        return self.cards.pop()


class Player:
    def __init__(self, player_name, chips, bet_size):
        self.player_name = player_name
        self.chips = chips
        self.bet_size = bet_size
        self.games_played = 0
        self.winnings = 0
        self.hand = []
        self.hand_score = 0
        self.stay = False

    def print_balance(self):
        print(f'{self.player_name} current balance = {self.chips}. {self.winnings} '
              f'chips won(lost) in {self.games_played} games played')

    def print_hand(self):
        for card in self.hand:
            print(card)

    def update_player_hand_value(self):
        self.hand_score = 0
        for card in self.hand:
            self.hand_score += card.value
        for card in self.hand:
            if card.value == 1:
                if self.hand_score + 10 <= 21:
                    self.hand_score += 10
        return self.hand_score


def player_stay(player):
    player.stay = True


class Blackjack:
    def __init__(self):
        self.players = []
        self.dealer_hand = []
        self.dealer_score = 0
        deck_list = []
        for j in range(6):
            deck_j = Deck()
            deck_list.append(deck_j)
        self.shoe = Shoe(deck_list)
        random.shuffle(self.shoe.cards)

    def new_shoe(self):
        deck_list = []
        for j in range(6):
            deck_j = Deck()
            deck_list.append(deck_j)
        new_shoe = Shoe(deck_list)
        random.shuffle(new_shoe.cards)
        self.shoe = new_shoe

    def dealer_hit(self):
        self.dealer_hand.append(self.shoe.draw_card())
        self.update_dealer_hand_value()

    def update_dealer_hand_value(self):
        self.dealer_score = 0
        for card in self.dealer_hand:
            self.dealer_score += card.value
        for card in self.dealer_hand:
            if card.value == 1:
                if self.dealer_score + 10 <= 21:
                    self.dealer_score += 10
        return self.dealer_score

    def player_hit(self, player):
        player.hand.append(self.shoe.draw_card())
        print(player.hand[-1])
        player.update_player_hand_value()

    def prompt_player(self, player):
        response = input("hit or stay? (h/s) ")
        if response == 'h':
            self.player_hit(player)
        elif response == 's':
            player.stay = True
        else:
            print("please enter 'h' or 's'")

    def evaluate_winners(self, player):
        player.games_played += 1
        if player.hand_score > 21:
            print(f'{player.player_name}: you bust')
            player.winnings -= player.bet_size
            player.chips -= player.bet_size
        elif self.dealer_score > 21:
            print(f'{player.player_name}: dealer bust, you win')
            player.winnings += player.bet_size
            player.chips += player.bet_size
        elif player.hand_score == self.dealer_score:
            print(f'{player.player_name}: you push')
        elif player.hand_score > self.dealer_score:
            print(f'{player.player_name}: you win')
            player.winnings += player.bet_size
            player.chips += player.bet_size
        elif player.hand_score < self.dealer_score:
            print(f'{player.player_name}: you lose')
            player.winnings -= player.bet_size
            player.chips -= player.bet_size
        else:
            'condition not defined'

    def start_round(self):
        self.dealer_hand = [self.shoe.draw_card(), self.shoe.draw_card()]
        self.update_dealer_hand_value()
        for player in self.players:
            player.stay = False
            player.hand = [self.shoe.draw_card(), self.shoe.draw_card()]
            player.update_player_hand_value()
        print(f'Dealer shows: {self.dealer_hand[0]}')
        for player in self.players:
            print()
            print(f'{player.player_name} hand:')
            player.print_hand()
            while player.hand_score < 21 and player.stay is not True:
                self.prompt_player(player)
        print()
        print(f'Dealer shows: {self.dealer_hand[0]}, {self.dealer_hand[1]}')
        while self.dealer_score < 17:
            self.dealer_hit()
            print(f'Dealer shows: {self.dealer_hand[-1]}')
        print()
        for player in self.players:
            self.evaluate_winners(player)
            print()


player1 = Player("Carter", 500, 50)
player2 = Player("Casey", 500, 50)
table1_players = [player1, player2]
table1 = Blackjack()
table1.players = table1_players
table1.start_round()
for table1_player in table1_players:
    table1_player.print_balance()
