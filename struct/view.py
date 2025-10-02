import customtkinter as ctk
from tkinter import messagebox


class BlackjackView:
    """
    Interface graphique pour le jeu de Blackjack avec CustomTkinter
    """
    def __init__(self):
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("Blackjack Game")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Variables pour les callbacks du controller
        self.on_hit_callback = None
        self.on_stand_callback = None
        self.on_double_callback = None
        self.on_split_callback = None
        self.on_insurance_callback = None
        self.on_new_game_callback = None
        self.on_bet_callback = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """
        Crée l'interface utilisateur
        """
        # Titre
        title_label = ctk.CTkLabel(
            self.root, 
            text="♠️ BLACKJACK ♠️", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Zone d'informations du croupier
        self.dealer_frame = ctk.CTkFrame(self.root)
        self.dealer_frame.pack(pady=10, padx=20, fill="x")
        
        dealer_title = ctk.CTkLabel(
            self.dealer_frame, 
            text="Croupier", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        dealer_title.pack(pady=10)
        
        self.dealer_cards_label = ctk.CTkLabel(
            self.dealer_frame, 
            text="Cartes: []", 
            font=ctk.CTkFont(size=16)
        )
        self.dealer_cards_label.pack()
        
        self.dealer_value_label = ctk.CTkLabel(
            self.dealer_frame, 
            text="Valeur: 0", 
            font=ctk.CTkFont(size=16)
        )
        self.dealer_value_label.pack(pady=(0, 10))
        
        # Zone d'informations du joueur
        self.player_frame = ctk.CTkFrame(self.root)
        self.player_frame.pack(pady=10, padx=20, fill="x")
        
        player_title = ctk.CTkLabel(
            self.player_frame, 
            text="Joueur", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        player_title.pack(pady=10)
        
        self.player_cards_label = ctk.CTkLabel(
            self.player_frame, 
            text="Cartes: []", 
            font=ctk.CTkFont(size=16)
        )
        self.player_cards_label.pack()
        
        self.player_value_label = ctk.CTkLabel(
            self.player_frame, 
            text="Valeur: 0", 
            font=ctk.CTkFont(size=16)
        )
        self.player_value_label.pack()
        
        # Informations sur l'argent et les mises
        info_frame = ctk.CTkFrame(self.player_frame)
        info_frame.pack(pady=10, fill="x")
        
        self.wallet_label = ctk.CTkLabel(
            info_frame, 
            text="Portefeuille: 1000€", 
            font=ctk.CTkFont(size=14)
        )
        self.wallet_label.pack(side="left", padx=10)
        
        self.bet_label = ctk.CTkLabel(
            info_frame, 
            text="Mise: 0€", 
            font=ctk.CTkFont(size=14)
        )
        self.bet_label.pack(side="right", padx=10)
        
        # Zone de mise
        self.bet_frame = ctk.CTkFrame(self.root)
        self.bet_frame.pack(pady=10, padx=20, fill="x")
        
        bet_title = ctk.CTkLabel(
            self.bet_frame, 
            text="Placer une mise", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        bet_title.pack(pady=10)
        
        bet_input_frame = ctk.CTkFrame(self.bet_frame)
        bet_input_frame.pack(pady=10)
        
        self.bet_entry = ctk.CTkEntry(
            bet_input_frame, 
            placeholder_text="Montant de la mise",
            width=200
        )
        self.bet_entry.pack(side="left", padx=5)
        
        self.deal_button = ctk.CTkButton(
            bet_input_frame, 
            text="Distribuer",
            command=self._on_bet_clicked,
            width=100
        )
        self.deal_button.pack(side="left", padx=5)
        
        # Boutons de mise rapide
        quick_bet_frame = ctk.CTkFrame(self.bet_frame)
        quick_bet_frame.pack(pady=5)
        
        quick_bet_amounts = [10, 25, 50, 100]
        for amount in quick_bet_amounts:
            btn = ctk.CTkButton(
                quick_bet_frame,
                text=f"{amount}€",
                command=lambda a=amount: self._set_bet_amount(a),
                width=60
            )
            btn.pack(side="left", padx=2)
        
        # Zone des actions de jeu
        self.game_frame = ctk.CTkFrame(self.root)
        self.game_frame.pack(pady=10, padx=20, fill="x")
        
        game_title = ctk.CTkLabel(
            self.game_frame, 
            text="Actions de jeu", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        game_title.pack(pady=10)
        
        # Première rangée de boutons
        buttons_frame1 = ctk.CTkFrame(self.game_frame)
        buttons_frame1.pack(pady=5)
        
        self.hit_button = ctk.CTkButton(
            buttons_frame1, 
            text="Tirer (Hit)",
            command=self._on_hit_clicked,
            state="disabled"
        )
        self.hit_button.pack(side="left", padx=5)
        
        self.stand_button = ctk.CTkButton(
            buttons_frame1, 
            text="Rester (Stand)",
            command=self._on_stand_clicked,
            state="disabled"
        )
        self.stand_button.pack(side="left", padx=5)
        
        self.double_button = ctk.CTkButton(
            buttons_frame1, 
            text="Doubler",
            command=self._on_double_clicked,
            state="disabled"
        )
        self.double_button.pack(side="left", padx=5)
        
        # Deuxième rangée de boutons
        buttons_frame2 = ctk.CTkFrame(self.game_frame)
        buttons_frame2.pack(pady=5)
        
        self.insurance_button = ctk.CTkButton(
            buttons_frame2, 
            text="Assurance",
            command=self._on_insurance_clicked,
            state="disabled"
        )
        self.insurance_button.pack(side="left", padx=5)
        
        self.split_button = ctk.CTkButton(
            buttons_frame2, 
            text="Séparer (Split)",
            command=self._on_split_clicked,
            state="disabled"
        )
        self.split_button.pack(side="left", padx=5)
        
        self.new_game_button = ctk.CTkButton(
            buttons_frame2, 
            text="Nouvelle partie",
            command=self._on_new_game_clicked,
            state="disabled"
        )
        self.new_game_button.pack(side="left", padx=5)
        
        # Zone des messages
        self.message_frame = ctk.CTkFrame(self.root)
        self.message_frame.pack(pady=10, padx=20, fill="x")
        
        self.message_label = ctk.CTkLabel(
            self.message_frame, 
            text="Placez votre mise pour commencer", 
            font=ctk.CTkFont(size=16),
            text_color="yellow"
        )
        self.message_label.pack(pady=15)
        
    def _set_bet_amount(self, amount):
        """
        Définit le montant de la mise dans l'entrée
        """
        self.bet_entry.delete(0, "end")
        self.bet_entry.insert(0, str(amount))
        
    def _on_bet_clicked(self):
        """
        Gère le clic sur le bouton de mise
        """
        try:
            bet_amount = float(self.bet_entry.get())
            if bet_amount <= 0:
                self.show_message("La mise doit être positive!", "red")
                return
            if self.on_bet_callback:
                self.on_bet_callback(bet_amount)
        except ValueError:
            self.show_message("Veuillez entrer un montant valide!", "red")
    
    def _on_hit_clicked(self):
        if self.on_hit_callback:
            self.on_hit_callback()
    
    def _on_stand_clicked(self):
        if self.on_stand_callback:
            self.on_stand_callback()
    
    def _on_double_clicked(self):
        if self.on_double_callback:
            self.on_double_callback()
    
    def _on_split_clicked(self):
        if self.on_split_callback:
            self.on_split_callback()
    
    def _on_insurance_clicked(self):
        if self.on_insurance_callback:
            self.on_insurance_callback()
    
    def _on_new_game_clicked(self):
        if self.on_new_game_callback:
            self.on_new_game_callback()
    
    def update_display(self, game_state):
        """
        Met à jour l'affichage avec l'état actuel du jeu
        """
        # Mise à jour des cartes et valeurs du joueur
        player_cards = game_state['player_hand']
        player_value = game_state['player_value']
        self.player_cards_label.configure(text=f"Cartes: {player_cards}")
        self.player_value_label.configure(text=f"Valeur: {player_value}")
        
        # Mise à jour des cartes du croupier
        dealer_cards = game_state['dealer_hand']
        if game_state['round_over']:
            # Montrer toutes les cartes du croupier
            dealer_value = game_state['dealer_value']
            self.dealer_cards_label.configure(text=f"Cartes: {dealer_cards}")
            self.dealer_value_label.configure(text=f"Valeur: {dealer_value}")
        else:
            # Cacher la deuxième carte du croupier
            if len(dealer_cards) >= 2:
                visible_cards = [dealer_cards[0], "?¿?"]
                self.dealer_cards_label.configure(text=f"Cartes: {visible_cards}")
                self.dealer_value_label.configure(text=f"Valeur: {dealer_cards[0] if dealer_cards[0] != 11 else '1/11'} + ?")
            else:
                self.dealer_cards_label.configure(text=f"Cartes: {dealer_cards}")
                self.dealer_value_label.configure(text=f"Valeur: {game_state['dealer_value']}")
        
        # Mise à jour des informations financières
        self.wallet_label.configure(text=f"Portefeuille: {game_state['player_wallet']}€")
        self.bet_label.configure(text=f"Mise: {game_state['current_bet']}€")
        
        # État des boutons
        if game_state['round_over']:
            self._disable_game_buttons()
            self.new_game_button.configure(state="normal")
        else:
            self._enable_game_buttons()
            self.new_game_button.configure(state="disabled")
            
            # Boutons spéciaux
            if game_state['can_take_insurance']:
                self.insurance_button.configure(state="normal")
            else:
                self.insurance_button.configure(state="disabled")
                
            if game_state['can_double']:
                self.double_button.configure(state="normal")
            else:
                self.double_button.configure(state="disabled")
                
            if game_state['can_split']:
                self.split_button.configure(state="normal")
            else:
                self.split_button.configure(state="disabled")
    
    def _enable_game_buttons(self):
        """
        Active les boutons de jeu
        """
        self.hit_button.configure(state="normal")
        self.stand_button.configure(state="normal")
        self.deal_button.configure(state="disabled")
        
    def _disable_game_buttons(self):
        """
        Désactive les boutons de jeu
        """
        self.hit_button.configure(state="disabled")
        self.stand_button.configure(state="disabled")
        self.double_button.configure(state="disabled")
        self.split_button.configure(state="disabled")
        self.insurance_button.configure(state="disabled")
        self.deal_button.configure(state="normal")
    
    def show_message(self, message, color="white"):
        """
        Affiche un message à l'utilisateur
        """
        self.message_label.configure(text=message, text_color=color)
    
    def show_shuffle_message(self):
        """
        Affiche un message de remélange
        """
        messagebox.showinfo("Remélange", "Le paquet va être remélangé!")
    
    def show_game_over(self, message):
        """
        Affiche un message de fin de partie
        """
        messagebox.showinfo("Fin de partie", message)
    
    def set_callbacks(self, callbacks):
        """
        Définit les callbacks pour les actions
        """
        self.on_hit_callback = callbacks.get('hit')
        self.on_stand_callback = callbacks.get('stand')
        self.on_double_callback = callbacks.get('double')
        self.on_split_callback = callbacks.get('split')
        self.on_insurance_callback = callbacks.get('insurance')
        self.on_new_game_callback = callbacks.get('new_game')
        self.on_bet_callback = callbacks.get('bet')
    
    def run(self):
        """
        Lance la boucle principale de l'interface
        """
        self.root.mainloop()
    
    def close(self):
        """
        Ferme l'interface
        """
        self.root.destroy()
