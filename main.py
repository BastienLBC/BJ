from struct.model import Player, Deck

if __name__ == "__main__":
    deck = Deck()
    player = Player(wallet=1000, deck=deck)

    player.hit()
    player.hit()
    player.hit()
    print(f"main : {player.hand}")
    # print(deck.deck)
    # print(len(deck.deck))
    print(deck.red_card)