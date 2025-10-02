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
        self.has_split = False  # AJOUTÉ : pour savoir si le joueur a splitté
        self.hand_finished = [False]  # AJOUTÉ : pour savoir si chaque main est terminée

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
    
    def hit(self, hand_index=None):
        """
        tire une carte et l'ajoute à sa main - MODIFIÉ : peut spécifier la main
        """
        if hand_index is None:
            hand_index = self.current_hand
        
        card = self.shoe.deck.pop()
        self.shoe.cards_used += 1
        self.hands[hand_index].append(card)
        return card

    def stand(self):
        """
        Le joueur reste avec sa main actuelle - MODIFIÉ : gère le split
        """
        if self.has_split:
            self.hand_finished[self.current_hand] = True
            # Passer à la main suivante si elle existe et n'est pas terminée
            if self.current_hand < len(self.hands) - 1:
                self.current_hand += 1
                return "next_hand"
            else:
                return "all_hands_finished"
        return "stand"

    def double(self, amount, hand_index=None):
        """
        Double la mise et tire une seule carte - MODIFIÉ : gère le split
        """
        if hand_index is None:
            hand_index = self.current_hand
            
        if amount <= self.wallet:
            self.wallet -= amount
            self.current_bet *= 2 if not self.has_split else 1  # Ne double que pour la main courante si split
            self.hit(hand_index)
            
            if self.has_split:
                self.hand_finished[hand_index] = True
                # Passer à la main suivante si elle existe
                if self.current_hand < len(self.hands) - 1:
                    self.current_hand += 1
                    return "next_hand"
                else:
                    return "all_hands_finished"
            
            return True
        return False

    def split(self, amount):
        """
        Sépare une paire en deux mains - CORRIGÉ
        """
        if amount <= self.wallet and self.can_split():
            self.wallet -= amount
            current_hand = self.hands[self.current_hand]

            # Séparer les cartes
            second_card = current_hand.pop()
            self.hands.append([second_card])
            self.hand_finished.append(False)

            # Distribuer une nouvelle carte à chaque main
            self.hit(0)  # Nouvelle carte pour la première main
            self.hit(1)  # Nouvelle carte pour la deuxième main
            
            self.has_split = True
            self.current_hand = 0  # Commencer par la première main
            return True
        return False

    def get_hand_value(self, hand_index=None):
        """
        Calcule la valeur d'une main en gérant les As
        """
        if hand_index is None:
            hand_index = self.current_hand
        
        if hand_index >= len(self.hands):
            return 0
            
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
        
        if hand_index >= len(self.hands):
            return False
            
        hand = self.hands[hand_index]
        return len(hand) == 2 and self.get_hand_value(hand_index) == 21

    def can_split(self):
        """
        Vérifie si le joueur peut séparer sa main
        """
        if self.has_split:  # Pas de re-split
            return False
            
        hand = self.hands[self.current_hand]
        return len(hand) == 2 and hand[0] == hand[1] and len(self.hands) == 1

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
        self.has_split = False  # AJOUTÉ
        self.hand_finished = [False]  # AJOUTÉ

    def win(self, amount):
        """
        Ajoute les gains au portefeuille
        """
        self.wallet += amount

    def is_current_hand_finished(self):
        """
        AJOUTÉ : Vérifie si la main courante est terminée
        """
        if not self.has_split:
            return False
        return self.current_hand < len(self.hand_finished) and self.hand_finished[self.current_hand]

    def all_hands_finished(self):
        """
        AJOUTÉ : Vérifie si toutes les mains sont terminées
        """
        if not self.has_split:
            return False
        return all(self.hand_finished)


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
        self.hole_card_drawn = False

    def hit(self):
        """
        Tire une carte
        """
        card = self.shoe.deck.pop()
        self.shoe.cards_used += 1
        self.hand.append(card)
        return card
    
    def draw_hole_card(self):
        """
        Tire la carte cachée (deuxième carte) du croupier
        """
        if not self.hole_card_drawn and len(self.hand) == 1:
            self.hit()
            self.hole_card_drawn = True

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
        self.hole_card_drawn = False


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
        self.initial_size = len(self.deck)
        self.cards_used = 0
        
        self.red_card_position = random.randint(
            int(self.initial_size * 0.70),
            int(self.initial_size * 0.85)
        )

    def should_shuffle(self):
        """
        Vérifie si on a atteint la position de la carte rouge
        """
        return self.cards_used >= self.red_card_position

    def shuffle(self):
        """
        Remélange le paquet
        """
        self.deck = cards * self.num_decks
        random.shuffle(self.deck)
        self.initial_size = len(self.deck)
        self.cards_used = 0
        
        self.red_card_position = random.randint(
            int(self.initial_size * 0.70),
            int(self.initial_size * 0.85)
        )
    
    def get_remaining_cards(self):
        """
        Retourne le nombre de cartes restantes
        """
        return len(self.deck)
    
    def get_red_card_position(self):
        """
        Retourne la position de la carte rouge
        """
        return self.red_card_position
    
    def get_cards_used(self):
        """
        Retourne le nombre de cartes utilisées depuis le début
        """
        return self.cards_used


class BlackjackGame():
    """
    Gère la logique d'une partie de Blackjack
    """
    def __init__(self, player_wallet=1000):
        self.deck = Deck()
        self.player = Player(player_wallet, self.deck)
        self.dealer = Croupier(self.deck)
        self.game_over = False
        self.round_over = True
        self.should_end_after_round = False

    def start_new_round(self, bet_amount):
        """
        Commence une nouvelle manche
        """
        if self.should_end_after_round:
            return "game_over"
            
        shuffle_needed = False
        if self.deck.should_shuffle():
            self.deck.shuffle()
            shuffle_needed = True
            
        # Reset des mains
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.round_over = False
        
        # Mise du joueur
        if not self.player.bet(bet_amount):
            return "insufficient_funds"
        
        # Distribution initiale
        self.player.hit()
        self.dealer.hit()
        self.player.hit()
        
        # Vérifier si on a atteint la carte rouge APRÈS la distribution
        if self.deck.should_shuffle() and not shuffle_needed:
            self.should_end_after_round = True
        
        # Vérifier le blackjack du joueur seulement
        if self.player.has_hand_blackjack():
            self.dealer.draw_hole_card()
            return self.check_blackjacks()
        
        return "round_started" if not shuffle_needed else "shuffle"

    def can_take_insurance(self):
        """
        Vérifie si le joueur peut prendre l'assurance
        """
        return (self.dealer.has_ace_showing() and 
                self.player.wallet >= self.player.current_bet / 2 and
                self.player.insurance_bet == 0 and
                not self.round_over)

    def take_insurance(self):
        """
        Le joueur prend l'assurance
        """
        return self.player.assurance(self.player.current_bet)

    def check_blackjacks(self):
        """
        Vérifie les blackjacks
        """
        player_bj = self.player.has_hand_blackjack()
        dealer_bj = self.dealer.has_hand_blackjack()
        
        if player_bj and dealer_bj:
            self.player.win(self.player.current_bet)
            if self.player.insurance_bet > 0:
                self.player.win(self.player.insurance_bet * 3)
            self.round_over = True
            return "tie_blackjack"
        elif player_bj:
            self.player.win(self.player.current_bet * 2)
            self.round_over = True
            return "player_blackjack"
        elif dealer_bj:
            if self.player.insurance_bet > 0:
                self.player.win(self.player.insurance_bet * 3)
            self.round_over = True
            return "dealer_blackjack"
        
        return "continue"

    def player_hit(self):
        """
        Le joueur tire une carte
        """
        self.player.hit()
        if self.player.is_hand_busted():
            if self.player.has_split:
                self.player.hand_finished[self.player.current_hand] = True
                # Vérifier s'il y a une main suivante
                if self.player.current_hand < len(self.player.hands) - 1:
                    self.player.current_hand += 1
                    return "next_hand"
                else:
                    self.round_over = True
                    return "all_hands_finished"
            else:
                self.round_over = True
                return "player_bust"
        return "continue"

    def player_stand(self):
        """
        Le joueur reste
        """
        result = self.player.stand()
        
        if result == "next_hand":
            return "next_hand"
        elif result == "all_hands_finished" or result == "stand":
            # Tirer la carte cachée du croupier
            self.dealer.draw_hole_card()
            return self.dealer_play()
        
        return "continue"

    def player_double(self):
        """
        Le joueur double sa mise
        """
        bet_amount = self.player.current_bet if not self.player.has_split else self.player.current_bet
        
        if self.player.wallet < bet_amount:
            return "insufficient_funds"
            
        result = self.player.double(bet_amount)
        
        if not result:
            return "insufficient_funds"
            
        # Vérifier si bust
        if self.player.is_hand_busted():
            if result == "next_hand":
                return "next_hand"
            elif result == "all_hands_finished":
                self.round_over = True
                return "all_hands_finished"
            else:
                self.round_over = True
                return "player_bust"
        
        if result == "next_hand":
            return "next_hand"
        elif result == "all_hands_finished" or result == True:
            # Tirer la carte cachée du croupier
            self.dealer.draw_hole_card()
            return self.dealer_play()
            
        return "continue"

    def player_split(self):
        """
        AJOUTÉ : Le joueur sépare sa main
        """
        if not self.player.can_split() or self.player.wallet < self.player.current_bet:
            return "cannot_split"
            
        success = self.player.split(self.player.current_bet)
        if success:
            return "split_success"
        return "cannot_split"

    def dealer_play(self):
        """
        Le croupier joue selon les règles
        """
        while self.dealer.should_hit():
            self.dealer.hit()
        
        self.round_over = True
        
        # Calculer les résultats pour chaque main
        if self.player.has_split:
            return self._calculate_split_results()
        else:
            return self._calculate_single_hand_result()

    def _calculate_single_hand_result(self):
        """
        AJOUTÉ : Calcule le résultat pour une seule main
        """
        if self.dealer.is_hand_busted():
            self.player.win(self.player.current_bet * 2)
            return "dealer_bust"
        
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()
        
        if player_value > dealer_value:
            self.player.win(self.player.current_bet * 2)
            return "player_wins"
        elif player_value < dealer_value:
            return "dealer_wins"
        else:
            self.player.win(self.player.current_bet)
            return "tie"

    def _calculate_split_results(self):
        """
        AJOUTÉ : Calcule les résultats pour les mains splittées
        """
        results = []
        bet_per_hand = self.player.current_bet
        
        for i in range(len(self.player.hands)):
            if self.player.is_hand_busted(i):
                results.append("bust")
            elif self.dealer.is_hand_busted():
                self.player.win(bet_per_hand * 2)
                results.append("win")
            else:
                player_value = self.player.get_hand_value(i)
                dealer_value = self.dealer.get_hand_value()
                
                if player_value > dealer_value:
                    self.player.win(bet_per_hand * 2)
                    results.append("win")
                elif player_value < dealer_value:
                    results.append("lose")
                else:
                    self.player.win(bet_per_hand)
                    results.append("tie")
        
        return f"split_results_{'-'.join(results)}"

    def get_game_state(self):
        """
        Retourne l'état actuel du jeu - MODIFIÉ pour le split
        """
        return {
            'player_hand': self.player.hands[0],
            'player_hands': self.player.hands,  # AJOUTÉ : toutes les mains
            'current_hand_index': self.player.current_hand,  # AJOUTÉ
            'has_split': self.player.has_split,  # AJOUTÉ
            'hand_finished': self.player.hand_finished,  # AJOUTÉ
            'player_value': self.player.get_hand_value(),
            'dealer_hand': self.dealer.hand,
            'dealer_visible_card': self.dealer.get_visible_card(),
            'dealer_value': self.dealer.get_hand_value(),
            'player_wallet': self.player.wallet,
            'current_bet': self.player.current_bet,
            'insurance_bet': self.player.insurance_bet,
            'round_over': self.round_over,
            'can_take_insurance': self.can_take_insurance(),
            'can_double': (len(self.player.hands[self.player.current_hand]) == 2 and 
                          self.player.wallet >= self.player.current_bet and
                          not self.round_over and
                          not self.player.is_current_hand_finished()),
            'can_split': (self.player.can_split() and 
                         self.player.wallet >= self.player.current_bet and
                         not self.round_over),
            'deck_remaining': self.deck.get_remaining_cards(),
            'red_card_position': self.deck.get_red_card_position(),
            'cards_used': self.deck.get_cards_used(),
            'should_end_after_round': self.should_end_after_round
        }