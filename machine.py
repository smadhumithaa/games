from player import Player
from reel import *
from settings import *
from ui import UI
from wins import *
import pygame

class Machine:
    def __init__(self, selected_symbol, bet_amount):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False
        self.selected_symbol = selected_symbol
        self.bet_amount=bet_amount
        self.flag = False
        self.win_data = True
        # Results
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels()
        self.currPlayer = Player(self.selected_symbol, self.bet_amount)
        self.ui = UI(self.currPlayer)


    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                # Play the win sound
                # self.play_win_sound(self.win_data)
                self.pay_player(self.win_data, self.currPlayer, self.selected_symbol, self.bet_amount)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

    def input(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            # Checks for space key, ability to toggle spin, and balance to cover bet size
            if self.flag:
                return
            if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
                self.toggle_spinning()
                self.spin_time = pygame.time.get_ticks()
                self.currPlayer.place_bet()
                self.machine_balance += self.currPlayer.bet_size
                self.currPlayer.last_payout = None
                self.flag = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.toggle_spinning()
                self.spin_time = pygame.time.get_ticks()
                self.currPlayer.place_bet()
                self.machine_balance += self.currPlayer.bet_size
                self.currPlayer.last_payout = None
                self.flag = True
            elif event.type == pygame.FINGERDOWN:
                self.toggle_spinning()
                self.spin_time = pygame.time.get_ticks()
                self.currPlayer.place_bet()
                self.machine_balance += self.currPlayer.bet_size
                self.currPlayer.last_payout = None
                self.flag = True

            
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft
            
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft)) # Need to create reel class
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                # self.spin_sound.play()
                self.win_animation_ongoing = False

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    # def check_wins(self, result):
    #     hits = {}
    #     horizontal = flip_horizontal(result)
    #     for row in horizontal:
    #         for sym in row:
    #             if row.count(sym) > 2: # Potential win
    #                 possible_win = [idx for idx, val in enumerate(row) if sym == val]
    #
    #                 # Check possible_win for a subsequence longer than 2 and add to hits
    #                 if len(longest_seq(possible_win)) > 2:
    #                     hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
    #     if hits:
    #         self.can_animate = True
    #         return hits
    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row_idx, row in enumerate(horizontal):
            for col_idx, sym in enumerate(row):
                if sym == self.selected_symbol:  # Check if the symbol matches the selected symbol
                    start_idx = col_idx
                    end_idx = start_idx
                    # Find the end index of the aligned symbols
                    while end_idx + 1 < len(row) and row[end_idx + 1] == self.selected_symbol:
                        end_idx += 1
                    # Check if there are 3 or more aligned symbols
                    if end_idx - start_idx >= 2:
                        hits[row_idx + 1] = [sym, row[start_idx:end_idx + 1]]  # Add the winning combination to hits
        if hits:
            self.can_animate = True
            self.win_data = False
            return hits

    # def pay_player(self, win_data, curr_player, selected_symbol, bet_amount):
    #     multiplier = 0
    #     spin_payout = 0
    #     for v in win_data.values():
    #         multiplier += len(v[1])
    #     spin_payout = (multiplier * curr_player.bet_size)
    #     curr_player.balance += spin_payout
    #     self.machine_balance -= spin_payout
    #     curr_player.last_payout = spin_payout
    #     curr_player.total_won += spin_payout

    def pay_player(self, win_data, curr_player, selected_symbol, bet_amount):
        multiplier = 1
        spin_payout = 0

        # Calculate the multiplier based on the winning combinations

        # Check if the winning symbol matches the selected symbol
        if selected_symbol == '0_telephone':
            multiplier *= 2
        elif selected_symbol == '0_seven':
            multiplier *= 3
        elif selected_symbol == '0_diamond':
            multiplier *= 6
        elif selected_symbol == '0_floppy':
            multiplier *= 4
        elif selected_symbol == '0_hourglass':
            multiplier *= 5

        # Calculate the spin payout based on the multiplier and bet amount
        spin_payout = multiplier * bet_amount

        # Add the spin payout to the player's balance
        curr_player.balance += spin_payout

        # Deduct the spin payout from the machine balance
        self.machine_balance -= spin_payout

        # Update player's last payout and total won
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout


    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True


    def update(self, delta_time, selected_symol):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()

        # if self.win_data:
        #     self.display_try_again()

    def display_try_again(self):
        try_again_font = pygame.font.SysFont(None, 30)
        try_again_surf = try_again_font.render("Try again", True, (255, 0, 0))
        try_again_rect = try_again_surf.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        self.display_surface.blit(try_again_surf, try_again_rect)
