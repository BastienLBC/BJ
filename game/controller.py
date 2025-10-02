from game.model import BlackjackGame
from game.view import BlackjackView


class BlackjackController:
    """
    Contrôleur simple pour gérer le jeu de Blackjack
    """
    def __init__(self):
        self.game = BlackjackGame()
        self.view = BlackjackView()
        self.setup_callbacks()
        
    def setup_callbacks(self):
        """
        Configure les callbacks entre la vue et le contrôleur
        """
        callbacks = {
            'hit': self.on_hit,
            'stand': self.on_stand,
            'double': self.on_double,
            'insurance': self.on_insurance,
            'bet': self.on_bet,
            'split': self.on_split  # AJOUTÉ : callback pour le split
        }
        self.view.set_callbacks(callbacks)
    
    def on_bet(self, bet_amount):
        """
        Gère le placement d'une mise et le début d'une nouvelle manche
        """
        if bet_amount > self.game.player.wallet:
            self.view.show_message("Fonds insuffisants!", "#F44336")
            return
        
        if bet_amount < 1:
            self.view.show_message("La mise minimum est de 1€!", "#F44336")
            return
        
        # Démarrer une nouvelle manche
        result = self.game.start_new_round(bet_amount)
        
        if result == "game_over":
            self.view.show_game_over("Partie terminée ! La carte rouge a été atteinte.")
            return
        
        if result == "shuffle":
            self.view.show_shuffle_message()
            result = self.game.start_new_round(bet_amount)
        
        if result == "insufficient_funds":
            self.view.show_message("Fonds insuffisants!", "#F44336")
            return
        
        if result in ["tie_blackjack", "player_blackjack", "dealer_blackjack"]:
            if result == "tie_blackjack":
                self.view.show_message("Égalité! Blackjack des deux côtés!", "#FFD700")
            elif result == "player_blackjack":
                self.view.show_message("Blackjack! Vous gagnez!", "#4CAF50")
            elif result == "dealer_blackjack":
                self.view.show_message("Le croupier a un Blackjack. Vous perdez.", "#F44336")
        else:
            if self.game.can_take_insurance():
                self.view.show_message("Le croupier montre un As. Assurance?", "#FF9800")
            else:
                if self.game.should_end_after_round:
                    self.view.show_message("La carte rouge a été atteinte. Le jeu va se terminer après ce round.", "#FF9800")
                else:
                    self.view.show_message("À votre tour! Tirez ou restez.", "#FFD700")
        
        self.update_view()
    
    def on_hit(self):
        """
        Gère l'action de tirer une carte - MODIFIÉ pour le split
        """
        result = self.game.player_hit()
        
        if result == "player_bust":
            self.view.show_message("Bust! Vous avez dépassé 21. Vous perdez.", "#F44336")
        elif result == "next_hand":
            hand_num = self.game.player.current_hand + 1
            self.view.show_message(f"Main {hand_num} - À vous de jouer!", "#FFD700")
        elif result == "all_hands_finished":
            self.view.show_message("Toutes les mains sont terminées. Tour du croupier...", "#FFD700")
            self._handle_split_results(result)
        else:
            player_value = self.game.player.get_hand_value()
            if player_value == 21:
                self.view.show_message("21! Parfait!", "#4CAF50")
            else:
                hand_message = ""
                if self.game.player.has_split:
                    hand_num = self.game.player.current_hand + 1
                    hand_message = f"Main {hand_num} - "
                self.view.show_message(f"{hand_message}Valeur actuelle: {player_value}", "#FFD700")
        
        self.update_view()
    
    def on_stand(self):
        """
        Gère l'action de rester - MODIFIÉ pour le split
        """
        if self.game.player.has_split:
            hand_num = self.game.player.current_hand + 1
            self.view.show_message(f"Main {hand_num} - Vous restez.", "#FFD700")
        else:
            self.view.show_message("Vous restez. Tour du croupier...", "#FFD700")
            
        self.update_view()
        
        result = self.game.player_stand()
        
        if result == "next_hand":
            hand_num = self.game.player.current_hand + 1
            self.view.show_message(f"Main {hand_num} - À vous de jouer!", "#FFD700")
        else:
            self._handle_game_result(result)
            
        self.update_view()
    
    def on_double(self):
        """
        Gère l'action de doubler - MODIFIÉ pour le split
        """
        bet_amount = self.game.player.current_bet
        if self.game.player.wallet < bet_amount:
            self.view.show_message("Fonds insuffisants pour doubler!", "#F44336")
            return
        
        result = self.game.player_double()
        
        if result == "insufficient_funds":
            self.view.show_message("Fonds insuffisants pour doubler!", "#F44336")
        elif result == "next_hand":
            hand_num = self.game.player.current_hand + 1
            self.view.show_message(f"Main {self.game.player.current_hand} doublée. Main {hand_num} - À vous!", "#FFD700")
        elif result == "all_hands_finished":
            self.view.show_message("Toutes les mains sont terminées. Tour du croupier...", "#FFD700")
            self._handle_split_results(result)
        elif result == "player_bust":
            if self.game.player.has_split:
                self.view.show_message("Bust sur cette main après avoir doublé!", "#F44336")
            else:
                self.view.show_message("Bust après avoir doublé! Vous perdez.", "#F44336")
        else:
            self.view.show_message("Vous avez doublé. Tour du croupier...", "#FFD700")
            self._handle_game_result(result)
        
        self.update_view()
    
    def on_insurance(self):
        """
        Gère l'action de prendre l'assurance
        """
        if self.game.player.insurance_bet > 0:
            self.view.show_message("Assurance déjà prise!", "#F44336")
            return
            
        if self.game.can_take_insurance():
            insurance_amount = self.game.player.current_bet / 2
            if self.game.player.wallet >= insurance_amount:
                self.game.take_insurance()
                self.view.show_message(f"Assurance prise pour {insurance_amount}€", "#FFD700")
            else:
                self.view.show_message("Fonds insuffisants pour l'assurance!", "#F44336")
        else:
            self.view.show_message("Assurance non disponible.", "#F44336")
        
        self.update_view()
    
    def on_split(self):
        """
        AJOUTÉ : Gère l'action de splitter
        """
        if self.game.player.wallet < self.game.player.current_bet:
            self.view.show_message("Fonds insuffisants pour splitter!", "#F44336")
            return
            
        result = self.game.player_split()
        
        if result == "split_success":
            self.view.show_message("Main splittée! Main 1 - À vous de jouer!", "#4CAF50")
        else:
            self.view.show_message("Impossible de splitter!", "#F44336")
        
        self.update_view()
    
    def _handle_game_result(self, result):
        """
        Gère les résultats de fin de manche - MODIFIÉ pour le split
        """
        if result.startswith("split_results_"):
            self._handle_split_results(result)
        else:
            if result == "dealer_bust":
                self.view.show_message("Le croupier bust! Vous gagnez!", "#4CAF50")
            elif result == "player_wins":
                self.view.show_message("Vous gagnez!", "#4CAF50")
            elif result == "dealer_wins":
                self.view.show_message("Le croupier gagne. Vous perdez.", "#F44336")
            elif result == "tie":
                self.view.show_message("Égalité! Vous récupérez votre mise.", "#FFD700")
    
    def _handle_split_results(self, result):
        """
        AJOUTÉ : Gère les résultats des mains splittées
        """
        if result.startswith("split_results_"):
            results = result.replace("split_results_", "").split("-")
            message_parts = []
            
            for i, hand_result in enumerate(results):
                hand_num = i + 1
                if hand_result == "win":
                    message_parts.append(f"Main {hand_num}: Gagnée!")
                elif hand_result == "lose":
                    message_parts.append(f"Main {hand_num}: Perdue")
                elif hand_result == "tie":
                    message_parts.append(f"Main {hand_num}: Égalité")
                elif hand_result == "bust":
                    message_parts.append(f"Main {hand_num}: Bust")
            
            final_message = " | ".join(message_parts)
            self.view.show_message(final_message, "#FFD700")
        else:
            # Toutes les mains sont bust
            self.view.show_message("Toutes vos mains ont bust! Vous perdez.", "#F44336")
    
    def update_view(self):
        """
        Met à jour la vue avec l'état actuel du jeu
        """
        game_state = self.game.get_game_state()
        self.view.update_display(game_state)
        
        # Vérifier si le joueur n'a plus d'argent
        if game_state['player_wallet'] <= 0 and game_state['round_over']:
            self.view.show_game_over("Game Over! Vous n'avez plus d'argent.")
    
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