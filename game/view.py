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
        self.root.geometry("800x700")
        self.root.configure(fg_color="#000000")  # Noir
        
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
        # Frame principal avec couleur noire
        main_frame = ctk.CTkFrame(self.root, fg_color="#2d2d2d")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            main_frame, 
            text="♠️ BLACKJACK ♠️", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=20)
        
        # Zone portefeuille et mise actuelle
        info_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
        info_frame.pack(pady=10, padx=20, fill="x")
        
        self.wallet_label = ctk.CTkLabel(
            info_frame, 
            text="💰 Portefeuille: 1000€", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFD700"
        )
        self.wallet_label.pack(side="left", padx=20, pady=10)
        
        self.current_bet_label = ctk.CTkLabel(
            info_frame, 
            text="🎲 Mise actuelle: 0€", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#87CEEB"
        )
        self.current_bet_label.pack(side="right", padx=20, pady=10)
        
        # Zone du paquet - CORRIGÉ : affichage amélioré
        deck_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
        deck_frame.pack(pady=10, padx=20, fill="x")
        
        deck_title = ctk.CTkLabel(
            deck_frame, 
            text="🃏 Paquet", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        deck_title.pack(pady=5)
        
        self.deck_info_label = ctk.CTkLabel(
            deck_frame, 
            text="Cartes restantes: 0 | Cartes utilisées: 0 | Carte rouge à: 0", 
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        )
        self.deck_info_label.pack(pady=(0, 10))
        
        # Zone de mise
        bet_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
        bet_frame.pack(pady=20, padx=20, fill="x")
        
        bet_title = ctk.CTkLabel(
            bet_frame, 
            text="💵 Placer votre mise", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
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
            fg_color="#2D5D2D",  # Vert foncé
            hover_color="#1F4A1F",
            text_color="white"  # Écriture blanche sur vert
        )
        self.deal_button.pack(side="left", padx=5)
        
        # Zone d'informations du croupier
        dealer_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
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
            text_color="white",
            wraplength=700
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
        player_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
        player_frame.pack(pady=10, padx=20, fill="x")
        
        player_title = ctk.CTkLabel(
            player_frame, 
            text="👤 Vous", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        player_title.pack(pady=5)
        
        self.player_cards_label = ctk.CTkLabel(
            player_frame, 
            text="Cartes: []", 
            font=ctk.CTkFont(size=14),
            text_color="white",
            wraplength=700
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
            fg_color="#2D5D2D",  # Vert foncé
            hover_color="#1F4A1F",
            text_color="white"
        )
        self.hit_button.pack(side="left", padx=5)
        
        self.stand_button = ctk.CTkButton(
            buttons_frame, 
            text="Rester (Stand)",
            command=self._on_stand_clicked,
            state="disabled",
            width=100,
            fg_color="#2D5D2D",  # Vert foncé
            hover_color="#1F4A1F",
            text_color="white"
        )
        self.stand_button.pack(side="left", padx=5)
        
        self.double_button = ctk.CTkButton(
            buttons_frame, 
            text="Doubler",
            command=self._on_double_clicked,
            state="disabled",
            width=100,
            fg_color="#2D5D2D",  # Vert foncé
            hover_color="#1F4A1F",
            text_color="white"
        )
        self.double_button.pack(side="left", padx=5)
        
        self.insurance_button = ctk.CTkButton(
            buttons_frame, 
            text="Assurance",
            command=self._on_insurance_clicked,
            state="disabled",
            width=100,
            fg_color="#2D5D2D",  # Vert foncé
            hover_color="#1F4A1F",
            text_color="white"
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
    
    def _format_cards_display(self, cards):
        """
        Formate l'affichage des cartes de manière plus jolie
        """
        if not cards:
            return "Aucune carte"
        
        # Convertit les valeurs en noms de cartes
        card_names = []
        for card in cards:
            if card == 11:
                card_names.append("As")
            elif card == 10:
                card_names.append("10/V/D/R")
            else:
                card_names.append(str(card))
        
        return " | ".join(card_names)
    
    def update_display(self, game_state):
        """
        Met à jour l'affichage avec l'état actuel du jeu
        """
        # Mise à jour des cartes et valeurs du joueur
        player_cards = game_state['player_hand']
        player_value = game_state['player_value']
        self.player_cards_label.configure(text=f"Cartes: {self._format_cards_display(player_cards)}")
        self.player_value_label.configure(text=f"Valeur: {player_value}")
        
        # Mise à jour des cartes du croupier
        dealer_cards = game_state['dealer_hand']
        if game_state['round_over']:
            # Montrer toutes les cartes du croupier
            dealer_value = game_state['dealer_value']
            self.dealer_cards_label.configure(text=f"Cartes: {self._format_cards_display(dealer_cards)}")
            self.dealer_value_label.configure(text=f"Valeur: {dealer_value}")
        else:
            # Cacher la deuxième carte du croupier
            if len(dealer_cards) >= 2:
                visible_cards = [dealer_cards[0]]
                visible_display = self._format_cards_display(visible_cards) + " | ??"
                self.dealer_cards_label.configure(text=f"Cartes: {visible_display}")
                visible_value = dealer_cards[0] if dealer_cards[0] != 11 else '1/11'
                self.dealer_value_label.configure(text=f"Valeur: {visible_value} + ?")
            else:
                self.dealer_cards_label.configure(text=f"Cartes: {self._format_cards_display(dealer_cards)}")
                self.dealer_value_label.configure(text=f"Valeur: {game_state['dealer_value']}")
        
        # Mise à jour du portefeuille
        self.wallet_label.configure(text=f"💰 Portefeuille: {game_state['player_wallet']}€")
        
        # Mise à jour de la mise actuelle
        self.current_bet_label.configure(text=f"🎲 Mise actuelle: {game_state['current_bet']}€")
        
        # Mise à jour des informations du paquet - CORRIGÉ
        deck_remaining = game_state.get('deck_remaining', 0)
        cards_used = game_state.get('cards_used', 0)
        red_card_pos = game_state.get('red_card_position', 0)
        self.deck_info_label.configure(
            text=f"Cartes restantes: {deck_remaining} | Cartes utilisées: {cards_used} | Carte rouge à: {red_card_pos}"
        )
        
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