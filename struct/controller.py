from struct.model import BlackjackGame
from struct.view import BlackjackView


class BlackjackController:
    """
    Contrôleur pour gérer les interactions entre le modèle et la vue
    """
    def __init__(self):
        self.game = BlackjackGame()
        self.view = BlackjackView()
        self.current_bet = 0
        self.setup_callbacks()
        
    def setup_callbacks(self):
        """
        Configure les callbacks entre la vue et le contrôleur
        """
        callbacks = {
            'hit': self.on_hit,
            'stand': self.on_stand,
            'double': self.on_double,
            'split': self.on_split,
            'insurance': self.on_insurance,
            'new_game': self.on_new_game,
            'bet': self.on_bet
        }
        self.view.set_callbacks(callbacks)
    
    def on_bet(self, bet_amount):
        """
        Gère le placement d'une mise et le début d'une nouvelle manche
        """
        if bet_amount > self.game.player.wallet:
            self.view.show_message("Fonds insuffisants!", "red")
            return
        
        if bet_amount < 1:
            self.view.show_message("La mise minimum est de 1€!", "red")
            return
        
        self.current_bet = bet_amount
        result = self.game.start_new_round(bet_amount)
        
        if result == "shuffle":
            self.view.show_shuffle_message()
            # Recommencer après remélange
            result = self.game.start_new_round(bet_amount)
        
        if result == "insufficient_funds":
            self.view.show_message("Fonds insuffisants!", "red")
            return
        
        # Vérifier les blackjacks
        blackjack_result = self.game.check_blackjacks()
        
        if blackjack_result == "tie_blackjack":
            self.view.show_message("Égalité! Blackjack des deux côtés!", "yellow")
        elif blackjack_result == "player_blackjack":
            self.view.show_message("Blackjack! Vous gagnez!", "green")
        elif blackjack_result == "dealer_blackjack":
            self.view.show_message("Le croupier a un Blackjack. Vous perdez.", "red")
        else:
            # Vérifier l'assurance si le croupier montre un As
            if self.game.can_take_insurance():
                self.view.show_message("Le croupier montre un As. Voulez-vous prendre l'assurance?", "orange")
            else:
                self.view.show_message("À votre tour! Tirez ou restez.", "white")
        
        self.update_view()
    
    def on_hit(self):
        """
        Gère l'action de tirer une carte
        """
        result = self.game.player_hit()
        
        if result == "player_bust":
            self.view.show_message("Bust! Vous avez dépassé 21. Vous perdez.", "red")
        else:
            player_value = self.game.player.get_hand_value()
            if player_value == 21:
                self.view.show_message("21! Parfait!", "green")
            else:
                self.view.show_message(f"Valeur actuelle: {player_value}", "white")
        
        self.update_view()
    
    def on_stand(self):
        """
        Gère l'action de rester
        """
        self.view.show_message("Vous restez. Tour du croupier...", "white")
        self.update_view()
        
        # Le croupier joue automatiquement
        result = self.game.player_stand()
        self._handle_game_result(result)
        self.update_view()
    
    def on_double(self):
        """
        Gère l'action de doubler
        """
        if self.game.player.wallet < self.current_bet:
            self.view.show_message("Fonds insuffisants pour doubler!", "red")
            return
        
        result = self.game.player_double()
        
        if result == "insufficient_funds":
            self.view.show_message("Fonds insuffisants pour doubler!", "red")
        elif result == "player_bust":
            self.view.show_message("Bust après avoir doublé! Vous perdez.", "red")
        else:
            self.view.show_message("Vous avez doublé. Tour du croupier...", "white")
            self.update_view()
            # Attendre un peu avant que le croupier joue
            self.view.root.after(1000, lambda: self._dealer_plays_after_double(result))
            return
        
        self.update_view()
    
    def _dealer_plays_after_double(self, result):
        """
        Le croupier joue après que le joueur ait doublé
        """
        if result != "player_bust":
            final_result = self.game.dealer_play()
            self._handle_game_result(final_result)
        self.update_view()
    
    def on_split(self):
        """
        Gère l'action de séparer (non implémentée dans cette version simple)
        """
        self.view.show_message("Split non implémenté dans cette version.", "orange")
    
    def on_insurance(self):
        """
        Gère l'action de prendre l'assurance
        """
        if self.game.can_take_insurance():
            insurance_amount = self.current_bet / 2
            if self.game.player.wallet >= insurance_amount:
                self.game.take_insurance()
                self.view.show_message(f"Assurance prise pour {insurance_amount}€", "yellow")
            else:
                self.view.show_message("Fonds insuffisants pour l'assurance!", "red")
        else:
            self.view.show_message("Assurance non disponible.", "red")
        
        self.update_view()
    
    def on_new_game(self):
        """
        Démarre une nouvelle partie
        """
        if self.game.player.wallet <= 0:
            self.view.show_game_over("Game Over! Vous n'avez plus d'argent.")
            return
        
        self.view.show_message("Placez votre mise pour la prochaine manche.", "white")
        self.update_view()
    
    def _handle_game_result(self, result):
        """
        Gère les résultats de fin de manche
        """
        if result == "dealer_bust":
            self.view.show_message("Le croupier bust! Vous gagnez!", "green")
        elif result == "player_wins":
            self.view.show_message("Vous gagnez!", "green")
        elif result == "dealer_wins":
            self.view.show_message("Le croupier gagne. Vous perdez.", "red")
        elif result == "tie":
            self.view.show_message("Égalité! Vous récupérez votre mise.", "yellow")
    
    def update_view(self):
        """
        Met à jour la vue avec l'état actuel du jeu
        """
        game_state = self.game.get_game_state()
        self.view.update_display(game_state)
        
        # Vérifier si le joueur n'a plus d'argent
        if game_state['player_wallet'] <= 0 and game_state['round_over']:
            self.view.root.after(2000, lambda: self.view.show_game_over("Game Over! Vous n'avez plus d'argent."))
    
    def run(self):
        """
        Lance le jeu
        """
        # Initialiser l'affichage
        self.update_view()
        
        # Lancer l'interface graphique
        self.view.run()


def play():
    """
    Fonction principale pour lancer une partie de Blackjack
    """
    controller = BlackjackController()
    controller.run()


if __name__ == "__main__":
    play()
