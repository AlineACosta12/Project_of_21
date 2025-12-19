import random

class Game21:
    def __init__(self):
        # Start immediately with a fresh round
        self.player_wins = 0  # simple stats tracker
        self.dealer_wins = 0
        self.pushes = 0
        self.new_round()

    # ROUND MANAGEMENT AND SETUP
    def new_round(self):
        """
        Prepares for a new round
        Suggested process:
        - Create and shuffle a new deck
        - Reset card pointer
        - Empty both hands
        - Reset whether the dealer's hidden card has been revealed
        """
        self.deck = self.create_deck()
        random.shuffle(self.deck)

        # Instead of removing cards from the deck,
        # we keep an index of the "next card" to deal.
        self.deck_position = 0

        # Hands start empty; cards will be dealt after UI calls deal_initial_cards()
        self.player_hand = []
        self.dealer_hand = []

        # The first dealer card starts hidden until Stand is pressed
        self.dealer_hidden_revealed = False

    def deal_initial_cards(self):
        """
        Deal two cards each to player and dealer.
        """
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

    # DECK AND CARD DRAWING

    def create_deck(self):
        """
        Create a standard 52-card deck represented as text strings, e.g.:
        'A♠', '10♥', 'K♦'.

        Ranks: A, 2–10, J, Q, K
        Suits: spades, hearts, diamonds, clubs (with unicode symbols)
        """
        ranks = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    def draw_card(self):
        """
        Return the next card in the shuffled deck.
        """
        card = self.deck[self.deck_position]
        self.deck_position += 1
        return card

    # HAND VALUES + ACE HANDLING

    def card_value(self, card):
        """
        Convert a card string into its numeric value.

        Rules:
        - Number cards = their number (2–10)
        - J, Q, K = 10
        - A is normally 11, may later count as 1 if needed
        """
        rank = card[:-1]  # everything except the suit symbol

        if rank in ["J", "Q", "K"]:
            return 10

        if rank == "A":
            return 11  # Initially treat Ace as 11

        # Otherwise it's a number from 2 to 10
        return int(rank)

    def hand_total(self, hand):
        """
        Calculates the best possible total for a hand.
        Aces are counted as 11 unless this would bust the hand,
        in which case they are reduced to 1.

        Suggested Process:
        1. Count all Aces as 11 initially.
        2. If total > 21, subtract 10 for each Ace, so it effectively makes them = 1
        """
        total = 0
        aces = 0

        for card in hand:
            value = self.card_value(card)
            total += value
            rank = card[:-1]
            if rank == "A":
                aces += 1

        # Adjust Aces from 11 to 1 as needed to avoid busting
        while total > 21 and aces > 0:
            total -= 10  # turn one Ace from 11 to 1
            aces -= 1
        return total

    # PLAYER ACTIONS

    def player_hit(self):
        # TODO: Add one card to the player's hand and return it, so the UI can display the card. Remove pass when complete.
        card = self.draw_card()
        self.player_hand.append(card)
        return card

    def player_total(self):
        # TODO: Return the player's total. Remove pass when complete.
        return self.hand_total(self.player_hand)

    # DEALER ACTIONS
    def reveal_dealer_card(self):
        # TODO: Called when the player presses Stand. After this, the UI should show both dealer cards. Remove pass when complete.
        self.dealer_hidden_revealed = True

    def dealer_total(self):
        # TODO: Return the dealer's total. Remove pass when complete.
        return self.hand_total(self.dealer_hand)

    def play_dealer_turn(self):
        # TODO: Dealer must hit until their total is 17 or more, then stand.  Remove pass when complete.
        # Dealer draws until total >= 17
        while self.dealer_total() < 17:
            self.dealer_hand.append(self.draw_card())

    # WINNER DETERMINATION

    def decide_winner(self):
        # TODO: Decide the outcome of the round.
        """
        Example: return the following text messages:
        - "Player busts. Dealer wins!"
        - "Dealer busts. Player wins!"
        - "Player wins!"
        - "Dealer wins!"
        - "Push (tie)."
        """
        player_total = self.player_total()
        dealer_total = self.dealer_total()

        # Player busts
        if player_total > 21:
            self.dealer_wins += 1
            return "Player busts. Dealer wins!"

        # Dealer busts
        if dealer_total > 21:
            self.player_wins += 1
            return "Dealer busts. Player wins!"

        # Neither busts – compare totals
        if player_total > dealer_total:
            self.player_wins += 1
            return "Player wins!"
        elif dealer_total > player_total:
            self.dealer_wins += 1
            return "Dealer wins!"
        else:
            self.pushes += 1
            return "Push (tie)."
