from source.poker_items import Card, Deck, Hand


class Round(object):
    def __init__(self, dealer_turn, players_points, players_number=2, cards_in_hand_number=2, deal_amount=50,
                 raise_size=25):
        # Round parameters
        self.player_turn = dealer_turn
        self.deal_amount = deal_amount
        self.players_points = players_points
        self.raise_size = raise_size

        # Initialization
        self.bank = 0
        self.curr_bet = 0
        self.board = Hand()
        self.winner = 0

        # Prepare items
        self.deck = Deck()  # Make deck
        self.deck.shuffle()  # Shuffle
        self.hands = []  # Make two hands

        # Deal cards to players
        for i in range(players_number):
            curr_hand = Hand()
            for j in range(cards_in_hand_number):
                curr_hand.add_card(self.deck.get_card())
            self.hands.append(curr_hand)

        # Deal two first cards to board
        for i in range(2):
            self.board.add_card(self.deck.get_card())

    def play(self):
        # Deal points by dealer
        self.bank = self.deal_amount
        self.curr_bet = self.deal_amount
        self.players_points[self.player_turn] -= self.deal_amount

        # Deal points by second player
        self.bank = self.deal_amount / 2
        self.players_points[1 - self.player_turn] -= self.deal_amount / 2

    def take_action(self, curr_player, action):
        # 0 - pass
        # 1 - call
        # 2 - raise
        if action == 0:
            self.players_points[1 - curr_player] += self.bank
            return 1 - self.player_turn, self.players_points
        elif action == 1:
            self.players_points[curr_player] -= self.curr_bet - self.curr_bet
        elif action == 2:
            self.bank += self.raise_size
            self.curr_bet += self.raise_size
            self.players_points[curr_player] -= self.raise_size

    def summarize(self):
        if self.hands[0].better_than(self.hands[1], self.board):
            self.winner = 0
            self.players_points[self.winner] += self.bank
        elif self.hands[0].worse_than(self.hands[1], self.board):
            self.winner = 1
            self.players_points[self.winner] += self.bank
        elif self.hands[0].equal_to(self.hands[1], self.board):
            self.winner = 2
            self.players_points[0] += self.bank / 2
            self.players_points[1] += self.bank / 2

        return self.winner, self.players_points


class Game(object):
    def __init__(self):
        # Game settings
        players_number = 2
        cards_in_hand_number = 2
        self.points = [1000, 1000]  # Players points at the beginning

        # Prepare items
        self.deck = Deck()  # Make deck
        self.deck.shuffle()  # Shuffle
        self.hands = []  # Make two hands

        # Statistics
        self.winning_history = []
        self.points_history = []

    def reset(self):
        self.__init__()

    def add_round(self, winner, players_points):
        self.winning_history.append(winner)
        self.points_history.append((players_points[0], players_points[1]))