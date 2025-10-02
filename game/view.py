import customtkinter as ctk
from tkinter import messagebox


class BlackjackView:
    """
    Interface graphique simple pour le jeu de Blackjack
    """
    def __init__(self):
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("♠️ Blackjack ♠️")
        self.root.geometry("800x600")
        self.root.configure(fg_color="#1a1a1a")
        
        # Variables pour les callbacks du controller
        self.on_hit_callback = None
        self.on_stand_callback = None
        self.on_double_callback = None
        self.on_insurance_callback = None
        self.on_bet_callback = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """
        Crée l'interface utilisateur simple
        """
        # Frame principal avec couleur verte
        main_frame = ctk.CTkFrame(self.root, fg_color="#2d5016")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            main_frame, 
            text="♠️ BLACKJACK ♠️", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#90EE90"
        )
        title_label.pack(pady=20)
        
        # Zone portefeuille
        self.wallet_label = ctk.CTkLabel(
            main_frame, 
            text="💰 Portefeuille: 1000€", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFD700"
        )
        self.wallet_label.pack(pady=10)
        
        # Zone de mise
        bet_frame = ctk.CTkFrame(main_frame, fg_color="#1a3d0a")
        bet_frame.pack(pady=20, padx=20, fill="x")
        
        bet_title = ctk.CTkLabel(
            bet_frame, 
            text="💵 Placer votre mise", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#90EE90"
        )
        bet_title.pack(pady=10)
        
        # Champ de saisie + bouton
        bet_input_frame = ctk.CTkFrame(bet_frame, fg_color="transparent")
        bet_input_frame.pack(pady=10)
        
        self.bet_entry = ctk.CTkEntry(
            bet_input_frame, 
            placeholder_text="Montant en €",
            width=150,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.bet_entry.pack(side="left", padx=5)
        
        self.deal_button = ctk.CTkButton(
            bet_input_frame, 
            text="Distribuer",
            command=self._on_bet_clicked,
            width=120,
            height=35,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.deal_button.pack(side="left", padx=5)
        
        # Zone d'informations du croupier
        dealer_frame = ctk.CTkFrame(main_frame, fg_color="#1a3d0a")
        dealer_frame.pack(pady=10, padx=20, fill="x")
        
        dealer_title = ctk.CTkLabel(
            dealer_frame, 
            text="🎩 Croupier", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFD700"
        )
        dealer_title.pack(pady=5)
        
        self.dealer_cards_label = ctk.CTkLabel(
            dealer_frame, 
            text="Cartes: []", 
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.dealer_cards_label.pack()
        
        self.dealer_value_label = ctk.CTkLabel(
            dealer_frame, 
            text="Valeur: 0", 
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.dealer_value_label.pack(pady=(0, 10))
        
        # Zone d'informations du joueur
        player_frame = ctk.CTkFrame(main_frame, fg_color="#1a3d0a")
        player_frame.pack(pady=10, padx=20, fill="x")
        
        player_title = ctk.CTkLabel(
            player_frame, 
            text="👤 Vous", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#90EE90"
        )
        player_title.pack(pady=5)
        
        self.player_cards_label = ctk.CTkLabel(
            player_frame, 
            text="Cartes: []", 
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.player_cards_label.pack()
        
        self.player_value_label = ctk.CTkLabel(
            player_frame, 
            text="Valeur: 0", 
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.player_value_label.pack(pady=(0, 10))
        
        # Zone des boutons d'action
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        self.hit_button = ctk.CTkButton(
            buttons_frame, 
            text="Tirer (Hit)",
            command=self._on_hit_clicked,
            state="disabled",
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.hit_button.pack(side="left", padx=5)
        
        self.stand_button = ctk.CTkButton(
            buttons_frame, 
            text="Rester (Stand)",
            command=self._on_stand_clicked,
            state="disabled",
            width=100,
            fg_color="#FF9800",
            hover_color="#e68900"
        )
        self.stand_button.pack(side="left", padx=5)
        
        self.double_button = ctk.CTkButton(
            buttons_frame, 
            text="Doubler",
            command=self._on_double_clicked,
            state="disabled",
            width=100,
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )
        self.double_button.pack(side="left", padx=5)
        
        self.insurance_button = ctk.CTkButton(
            buttons_frame, 
            text="Assurance",
            command=self._on_insurance_clicked,
            state="disabled",
            width=100,
            fg_color="#9C27B0",
            hover_color="#7B1FA2"
        )
        self.insurance_button.pack(side="left", padx=5)
        
        # Zone des messages
        self.message_label = ctk.CTkLabel(
            main_frame, 
            text="Placez votre mise pour commencer", 
            font=ctk.CTkFont(size=16),
            text_color="#FFD700"
        )
        self.message_label.pack(pady=20)
        
    def set_callbacks(self, callbacks):
        """
        Définit les callbacks pour les actions
        """
        self.on_hit_callback = callbacks.get('hit')
        self.on_stand_callback = callbacks.get('stand')
        self.on_double_callback = callbacks.get('double')
        self.on_insurance_callback = callbacks.get('insurance')
        self.on_bet_callback = callbacks.get('bet')
        
    def _on_bet_clicked(self):
        """
        Gère le clic sur le bouton de mise
        """
        try:
            bet_amount = float(self.bet_entry.get())
            if bet_amount <= 0:
                self.show_message("La mise doit être positive!", "#F44336")
                return
            if self.on_bet_callback:
                self.on_bet_callback(bet_amount)
        except ValueError:
            self.show_message("Veuillez entrer un montant valide!", "#F44336")
    
    def _on_hit_clicked(self):
        if self.on_hit_callback:
            self.on_hit_callback()
    
    def _on_stand_clicked(self):
        if self.on_stand_callback:
            self.on_stand_callback()
    
    def _on_double_clicked(self):
        if self.on_double_callback:
            self.on_double_callback()
    
    def _on_insurance_clicked(self):
        if self.on_insurance_callback:
            self.on_insurance_callback()
    
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
                visible_cards = [dealer_cards[0], "??"]
                self.dealer_cards_label.configure(text=f"Cartes: {visible_cards}")
                visible_value = dealer_cards[0] if dealer_cards[0] != 11 else '1/11'
                self.dealer_value_label.configure(text=f"Valeur: {visible_value} + ?")
            else:
                self.dealer_cards_label.configure(text=f"Cartes: {dealer_cards}")
                self.dealer_value_label.configure(text=f"Valeur: {game_state['dealer_value']}")
        
        # Mise à jour du portefeuille
        self.wallet_label.configure(text=f"💰 Portefeuille: {game_state['player_wallet']}€")
        
        # État des boutons
        if game_state['round_over']:
            self._disable_game_buttons()
            self.deal_button.configure(state="normal")
            self.bet_entry.configure(state="normal")
        else:
            self._enable_game_buttons()
            self.deal_button.configure(state="disabled")
            self.bet_entry.configure(state="disabled")
            
            # Boutons spéciaux
            if game_state['can_take_insurance']:
                self.insurance_button.configure(state="normal")
            else:
                self.insurance_button.configure(state="disabled")
                
            if game_state['can_double']:
                self.double_button.configure(state="normal")
            else:
                self.double_button.configure(state="disabled")
    
    def _enable_game_buttons(self):
        """
        Active les boutons de jeu
        """
        self.hit_button.configure(state="normal")
        self.stand_button.configure(state="normal")
        
    def _disable_game_buttons(self):
        """
        Désactive les boutons de jeu
        """
        self.hit_button.configure(state="disabled")
        self.stand_button.configure(state="disabled")
        self.double_button.configure(state="disabled")
        self.insurance_button.configure(state="disabled")
    
    def show_message(self, message, color="#FFD700"):
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