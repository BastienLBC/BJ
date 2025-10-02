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
        
        # Variable pour la mise actuelle en cours de construction
        self.current_bet_amount = 0
        
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
        
        # Zone de mise améliorée
        self.bet_frame = ctk.CTkFrame(self.root)
        self.bet_frame.pack(pady=10, padx=20, fill="x")
        
        bet_title = ctk.CTkLabel(
            self.bet_frame, 
            text="Placer une mise", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        bet_title.pack(pady=10)
        
        # Affichage de la mise en cours
        self.current_bet_display = ctk.CTkLabel(
            self.bet_frame, 
            text="Mise actuelle: 0€", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="yellow"
        )
        self.current_bet_display.pack(pady=5)
        
        # Entrée manuelle + slider
        input_frame = ctk.CTkFrame(self.bet_frame)
        input_frame.pack(pady=10)
        
        # Entrée de texte pour montant exact
        manual_frame = ctk.CTkFrame(input_frame)
        manual_frame.pack(pady=5)
        
        ctk.CTkLabel(
            manual_frame, 
            text="Montant exact:", 
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=5)
        
        self.bet_entry = ctk.CTkEntry(
            manual_frame, 
            placeholder_text="Ex: 25",
            width=100
        )
        self.bet_entry.pack(side="left", padx=5)
        
        # Bouton pour définir le montant exact
        ctk.CTkButton(
            manual_frame, 
            text="Définir",
            command=self._set_exact_amount,
            width=80
        ).pack(side="left", padx=5)
        
        # Slider pour montant variable (1 à 1000)
        slider_frame = ctk.CTkFrame(input_frame)
        slider_frame.pack(pady=10, fill="x", padx=10)
        
        ctk.CTkLabel(
            slider_frame, 
            text="Slider (1€ - 1000€):", 
            font=ctk.CTkFont(size=14)
        ).pack()
        
        self.bet_slider = ctk.CTkSlider(
            slider_frame,
            from_=1,
            to=1000,
            command=self._on_slider_change,
            width=300
        )
        self.bet_slider.pack(pady=5)
        self.bet_slider.set(10)  # Valeur par défaut
        
        # Boutons d'ajout rapide
        quick_add_frame = ctk.CTkFrame(self.bet_frame)
        quick_add_frame.pack(pady=10)
        
        ctk.CTkLabel(
            quick_add_frame, 
            text="Ajouter à la mise:", 
            font=ctk.CTkFont(size=14)
        ).pack()
        
        buttons_container = ctk.CTkFrame(quick_add_frame)
        buttons_container.pack(pady=5)
        
        quick_add_amounts = [1, 5, 10, 25, 50, 100]
        for amount in quick_add_amounts:
            btn = ctk.CTkButton(
                buttons_container,
                text=f"+{amount}€",
                command=lambda a=amount: self._add_to_bet(a),
                width=60
            )
            btn.pack(side="left", padx=2)
        
        # Boutons de contrôle de la mise
        bet_control_frame = ctk.CTkFrame(self.bet_frame)
        bet_control_frame.pack(pady=10)
        
        self.clear_bet_button = ctk.CTkButton(
            bet_control_frame, 
            text="Remettre à 0",
            command=self._clear_bet,
            width=100,
            fg_color="gray"
        )
        self.clear_bet_button.pack(side="left", padx=5)
        
        self.all_in_button = ctk.CTkButton(
            bet_control_frame, 
            text="All-in",
            command=self._all_in,
            width=100,
            fg_color="red"
        )
        self.all_in_button.pack(side="left", padx=5)
        
        self.deal_button = ctk.CTkButton(
            bet_control_frame, 
            text="Distribuer",
            command=self._on_bet_clicked,
            width=120,
            fg_color="green"
        )
        self.deal_button.pack(side="left", padx=5)
        
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
        
    def _set_exact_amount(self):
        """
        Définit le montant exact depuis l'entrée de texte
        """
        try:
            amount = float(self.bet_entry.get())
            if amount < 1:
                self.show_message("La mise minimum est de 1€!", "red")
                return
            self.current_bet_amount = int(amount)
            self._update_bet_display()
            self.bet_entry.delete(0, "end")
        except ValueError:
            self.show_message("Veuillez entrer un montant valide!", "red")
    
    def _on_slider_change(self, value):
        """
        Met à jour la mise avec la valeur du slider
        """
        self.current_bet_amount = int(value)
        self._update_bet_display()
    
    def _add_to_bet(self, amount):
        """
        Ajoute un montant à la mise actuelle
        """
        self.current_bet_amount += amount
        self._update_bet_display()
        # Met à jour le slider aussi
        if self.current_bet_amount <= 1000:
            self.bet_slider.set(self.current_bet_amount)
    
    def _clear_bet(self):
        """
        Remet la mise à zéro
        """
        self.current_bet_amount = 0
        self._update_bet_display()
        self.bet_slider.set(1)
    
    def _all_in(self):
        """
        Met tout l'argent disponible en mise
        """
        # Récupère le portefeuille actuel depuis le label
        wallet_text = self.wallet_label.cget("text")
        try:
            wallet_amount = int(wallet_text.split(":")[1].replace("€", "").strip())
            self.current_bet_amount = wallet_amount
            self._update_bet_display()
            if wallet_amount <= 1000:
                self.bet_slider.set(wallet_amount)
            else:
                self.bet_slider.set(1000)
        except:
            pass
    
    def _update_bet_display(self):
        """
        Met à jour l'affichage de la mise actuelle
        """
        self.current_bet_display.configure(text=f"Mise actuelle: {self.current_bet_amount}€")
    
    def _on_bet_clicked(self):
        """
        Gère le clic sur le bouton de mise
        """
        if self.current_bet_amount < 1:
            self.show_message("La mise minimum est de 1€!", "red")
            return
        
        if self.on_bet_callback:
            self.on_bet_callback(self.current_bet_amount)
    
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
        # Remettre la mise à 0 pour la prochaine manche
        self._clear_bet()
    
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
        
        # Désactiver les contrôles de mise pendant le jeu
        self.bet_slider.configure(state="disabled")
        self.clear_bet_button.configure(state="disabled")
        self.all_in_button.configure(state="disabled")
        
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
        
        # Réactiver les contrôles de mise
        self.bet_slider.configure(state="normal")
        self.clear_bet_button.configure(state="normal")
        self.all_in_button.configure(state="normal")
    
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
    
    def get_current_bet(self):
        """
        Retourne la mise actuelle (utile pour l'IA)
        """
        return self.current_bet_amount
    
    def set_bet_amount(self, amount):
        """
        Définit la mise (utile pour l'IA)
        """
        self.current_bet_amount = max(1, int(amount))
        self._update_bet_display()
        if self.current_bet_amount <= 1000:
            self.bet_slider.set(self.current_bet_amount)
    
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
