import random


class Player():
    """
    Un joueur peut hit, stand, double ou split. 
    Il a un porte feuille (min 0) et une mise (min 0,1). 

    Il a besoin du deck 
    """
    def __init__(self, wallet, deck):
        self.name = "Joueur"
        self.wallet = wallet
        self.hands = [[]]
        self.current_hand = 0
        self.shoe = deck
        self.current_bet = 0
        self.insurance_bet = 0
        self.has_blackjack = False
        self.is_busted = False

    def bet(self, amount):
        """
        return un float
        """
        if amount <= self.wallet:
            self.wallet -= amount
            self.current_bet = amount
            return True
        return False

    def assurance(self, amount):
        """
        Prend l'assurance (la moitié de la mise)
        """
        insurance_amount = amount / 2
        if insurance_amount <= self.wallet:
            self.wallet -= insurance_amount
            self.insurance_bet = insurance_amount
            return True
        return False
    
    def hit(self):
        """
        tire une carte et l'ajoute à sa main
        """
        card = self.shoe.deck.pop()
        self.hands[self.current_hand].append(card)
        return card

    def stand(self):
        """
        Le joueur reste avec sa main actuelle
        """
        return True

    def double(self, amount):
        """
        Double la mise et tire une seule carte
        """
        if amount <= self.wallet:
            self.wallet -= amount
            self.current_bet *= 2
            self.hit()
            return True
        return False

    def split(self, amount):
        """
        Sépare une paire en deux mains
        """
        if amount <= self.wallet:
            self.wallet -= amount
            current_hand = self.hands[self.current_hand]

            second_card = current_hand.pop()
            self.hands.append([second_card])

            current_hand.append(self.shoe.deck.pop())
            self.hands[-1].append(self.shoe.deck.pop())
            return True
        return False

    def get_hand_value(self, hand_index=None):
        """
        Calcule la valeur d'une main en gérant les As
        """
        if hand_index is None:
            hand_index = self.current_hand
        
        hand = self.hands[hand_index]
        value = sum(hand)
        aces = hand.count(11)
        
        # Convertit les As de 11 à 1 si nécessaire
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
            
        return value

    def is_hand_busted(self, hand_index=None):
        """
        Vérifie si une main dépasse 21
        """
        return self.get_hand_value(hand_index) > 21

    def has_hand_blackjack(self, hand_index=None):
        """
        Vérifie si une main est un blackjack (21 avec 2 cartes)
        """
        if hand_index is None:
            hand_index = self.current_hand
        
        hand = self.hands[hand_index]
        return len(hand) == 2 and self.get_hand_value(hand_index) == 21

    def can_split(self):
        """
        Vérifie si le joueur peut séparer sa main
        """
        hand = self.hands[self.current_hand]
        return len(hand) == 2 and hand[0] == hand[1]

    def reset_hand(self):
        """
        Remet à zéro la main du joueur pour une nouvelle partie
        """
        self.hands = [[]]
        self.current_hand = 0
        self.current_bet = 0
        self.insurance_bet = 0
        self.has_blackjack = False
        self.is_busted = False

    def win(self, amount):
        """
        Ajoute les gains au portefeuille
        """
        self.wallet += amount


class Croupier():
    """
    Le croupier tire automatiquement jusqu'à 17 minimum
    """
    def __init__(self, deck):
        self.name = "Croupier"
        self.hand = []
        self.shoe = deck
        self.has_blackjack = False
        self.is_busted = False

    def hit(self):
        """
        Tire une carte
        """
        card = self.shoe.deck.pop()
        self.hand.append(card)
        return card

    def get_hand_value(self):
        """
        Calcule la valeur de la main du croupier
        """
        value = sum(self.hand)
        aces = self.hand.count(11)
        
        # Convertit les As de 11 à 1 si nécessaire
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
            
        return value

    def should_hit(self):
        """
        Détermine si le croupier doit tirer (< 17)
        """
        return self.get_hand_value() < 17

    def is_hand_busted(self):
        """
        Vérifie si le croupier dépasse 21
        """
        return self.get_hand_value() > 21

    def has_hand_blackjack(self):
        """
        Vérifie si le croupier a un blackjack
        """
        return len(self.hand) == 2 and self.get_hand_value() == 21

    def get_visible_card(self):
        """
        Retourne la première carte visible du croupier
        """
        return self.hand[0] if self.hand else None

    def has_ace_showing(self):
        """
        Vérifie si le croupier montre un As (pour l'assurance)
        """
        return len(self.hand) > 0 and self.hand[0] == 11

    def reset_hand(self):
        """
        Remet à zéro la main du croupier
        """
        self.hand = []
        self.has_blackjack = False
        self.is_busted = False


cards = [
    11,11,11,11,
    2,2,2,2,
    3,3,3,3,
    4,4,4,4,
    5,5,5,5,
    6,6,6,6,
    7,7,7,7,
    8,8,8,8,
    9,9,9,9,
    10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10
]


class Deck():
    def __init__(self):
        self.num_decks = random.choice([6,8])
        self.deck = cards * self.num_decks
        random.shuffle(self.deck)
        
        long = len(self.deck)
        self.red_card_position = random.randint(
            int(long*0.70),
            int(long*0.85)
        )

    def should_shuffle(self):
        """
        Vérifie si on a atteint la carte rouge
        """
        return len(self.deck) <= self.red_card_position

    def shuffle(self):
        """
        Remélange le paquet
        """
        self.deck = cards * self.num_decks
        random.shuffle(self.deck)
        
        long = len(self.deck)
        self.red_card_position = random.randint(
            int(long*0.70),
            int(long*0.85)
        )


class BlackjackGame():
    """
    Gère la logique d'une partie de Blackjack
    """
    def __init__(self, player_wallet=1000):
        self.deck = Deck()
        self.player = Player(player_wallet, self.deck)
        self.dealer = Croupier(self.deck)
        self.game_over = False
        self.round_over = False

    def start_new_round(self, bet_amount):
        """
        Commence une nouvelle manche
        """
        if self.deck.should_shuffle():
            self.deck.shuffle()
            return "shuffle"  # Signal pour indiquer qu'il faut remélanger
        
        # Reset des mains
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.round_over = False
        
        # Mise du joueur
        if not self.player.bet(bet_amount):
            return "insufficient_funds"
        
        # Distribution initiale
        self.player.hit()  # Première carte joueur
        self.dealer.hit()  # Première carte croupier
        self.player.hit()  # Deuxième carte joueur
        self.dealer.hit()  # Deuxième carte croupier (cachée)
        
        return "round_started"

    def can_take_insurance(self):
        """
        Vérifie si le joueur peut prendre l'assurance
        """
        return self.dealer.has_ace_showing() and self.player.wallet >= self.player.current_bet / 2

    def take_insurance(self):
        """
        Le joueur prend l'assurance
        """
        return self.player.assurance(self.player.current_bet)

    def check_blackjacks(self):
        """
        Vérifie les blackjacks au début du tour
        """
        player_bj = self.player.has_hand_blackjack()
        dealer_bj = self.dealer.has_hand_blackjack()
        
        if player_bj and dealer_bj:
            # Égalité blackjack
            self.player.win(self.player.current_bet)  # Récupère sa mise
            if self.player.insurance_bet > 0:
                self.player.win(self.player.insurance_bet * 3)  # Gain assurance 2:1
            self.round_over = True
            return "tie_blackjack"
        elif player_bj:
            # Blackjack joueur - CORRIGÉ : x2 au lieu de x2.5
            self.player.win(self.player.current_bet * 2)
            self.round_over = True
            return "player_blackjack"
        elif dealer_bj:
            # Blackjack croupier
            if self.player.insurance_bet > 0:
                self.player.win(self.player.insurance_bet * 3)  # Gain assurance 2:1
            self.round_over = True
            return "dealer_blackjack"
        
        # Pas d'assurance si pas de blackjack croupier
        if self.player.insurance_bet > 0 and not dealer_bj:
            pass  # Perte de l'assurance
        
        return "continue"

    def player_hit(self):
        """
        Le joueur tire une carte
        """
        self.player.hit()
        if self.player.is_hand_busted():
            self.round_over = True
            return "player_bust"
        return "continue"

    def player_stand(self):
        """
        Le joueur reste, c'est au tour du croupier
        """
        return self.dealer_play()

    def player_double(self):
        """
        Le joueur double sa mise
        """
        if self.player.double(self.player.current_bet):
            if self.player.is_hand_busted():
                self.round_over = True
                return "player_bust"
            return self.dealer_play()
        return "insufficient_funds"

    def dealer_play(self):
        """
        Le croupier joue selon les règles (tire jusqu'à 17)
        """
        while self.dealer.should_hit():
            self.dealer.hit()
        
        if self.dealer.is_hand_busted():
            # Croupier bust, joueur gagne
            self.player.win(self.player.current_bet * 2)
            self.round_over = True
            return "dealer_bust"
        
        # Comparaison des mains
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()
        
        if player_value > dealer_value:
            # Joueur gagne
            self.player.win(self.player.current_bet * 2)
            self.round_over = True
            return "player_wins"
        elif player_value < dealer_value:
            # Croupier gagne
            self.round_over = True
            return "dealer_wins"
        else:
            # Égalité
            self.player.win(self.player.current_bet)  # Récupère sa mise
            self.round_over = True
            return "tie"

    def get_game_state(self):
        """
        Retourne l'état actuel du jeu
        """
        return {
            'player_hand': self.player.hands[0],
            'player_value': self.player.get_hand_value(),
            'dealer_hand': self.dealer.hand,
            'dealer_visible_card': self.dealer.get_visible_card(),
            'dealer_value': self.dealer.get_hand_value(),
            'player_wallet': self.player.wallet,
            'current_bet': self.player.current_bet,
            'insurance_bet': self.player.insurance_bet,
            'round_over': self.round_over,
            'can_take_insurance': self.can_take_insurance(),
            'can_double': len(self.player.hands[0]) == 2 and self.player.wallet >= self.player.current_bet,
            'can_split': self.player.can_split() and self.player.wallet >= self.player.current_bet
        }