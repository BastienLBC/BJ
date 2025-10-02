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

    def bet(self,amount):
        """
        return un float
        """
        self.wallet -= amount

    
    def assurance(self,amount):
        """"""
        self.bet(amount / 2)
    
    def hit(self):
        """
        tire une carte et l'ajoute à sa main
        """
        card = self.shoe.deck.pop()
        self.hands[self.current_hand].append(card)

    def stand(self):
        """"""
        return True

    def double(self, amount):
        self.bet(amount)
        self.hit()
        

    def split(self,amount):
        self.bet(amount)
        current_hand = self.hands[self.current_hand]

        second_card = current_hand.pop()
        self.hands.append([second_card])

        current_hand.append(self.shoe.deck.pop())
        self.hands[-1].append(self.shoe.deck.pop())


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
        self.red_card = random.randint(
            int(long*0.70),
            int(long*0.85)
        )

class Croupier():
    pass