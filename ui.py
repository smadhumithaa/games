# from player import Player
# import pygame
# import random
# from settings import *
#
# # Other imports
# # Import settings if needed
#
# class UI:
#     def __init__(self, player):
#         self.player = player
#         self.display_surface = pygame.display.get_surface()
#         try:
#             # Change font loading to use pygame's built-in font
#             self.font = pygame.font.SysFont(None, UI_FONT_SIZE)
#             self.bet_font = pygame.font.SysFont(None, UI_FONT_SIZE)
#             self.win_font = pygame.font.SysFont(None, WIN_FONT_SIZE)
#         except:
#             print("Error loading font!")
#             quit()
#         self.win_text_angle = random.randint(-4, 4)
#
#     def display_info(self):
#         player_data = self.player.get_data()
#
#         # Balance and bet size
#         balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR)
#         x, y = 20, self.display_surface.get_size()[1] - 30
#         balance_rect = balance_surf.get_rect(bottomleft=(x, y))
#
#         bet_surf = self.bet_font.render("Wager: $" + player_data['bet_size'], True, TEXT_COLOR)
#         x = self.display_surface.get_size()[0] - 20
#         bet_rect = bet_surf.get_rect(bottomright=(x, y))
#
#         # Draw player data
#         pygame.draw.rect(self.display_surface, False, balance_rect)
#         pygame.draw.rect(self.display_surface, False, bet_rect)
#         self.display_surface.blit(balance_surf, balance_rect)
#         self.display_surface.blit(bet_surf, bet_rect)
#
#         # Print last win if applicable
#         if self.player.last_payout:
#             last_payout = player_data['last_payout']
#             win_surf = self.win_font.render("WIN! $" + last_payout, True, TEXT_COLOR)
#             x1 = 800
#             y1 = self.display_surface.get_size()[1] - 60
#             win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
#             win_rect = win_surf.get_rect(center=(x1, y1))
#             self.display_surface.blit(win_surf, win_rect)
#
#     def update(self):
#         pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
#         self.display_info()
#
#

from player import Player
import pygame
import random
from settings import *

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        try:
            # Change font loading to use pygame's built-in font
            self.font = pygame.font.SysFont(None, UI_FONT_SIZE)
            self.bet_font = pygame.font.SysFont(None, UI_FONT_SIZE)
            self.symbol_font = pygame.font.SysFont(None, UI_FONT_SIZE)  # New font for symbol
            self.win_font = pygame.font.SysFont(None, WIN_FONT_SIZE)
        except:
            print("Error loading font!")
            quit()
        self.win_text_angle = random.randint(-4, 4)

    def display_info(self):
        player_data = self.player.get_data()

        # Balance and bet size
        balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR)
        x, y = 20, self.display_surface.get_size()[1] - 30
        balance_rect = balance_surf.get_rect(bottomleft=(x, y))

        bet_surf = self.bet_font.render("Wager: $" + player_data['bet_size'], True, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        bet_rect = bet_surf.get_rect(bottomright=(x, y))

        # Bet amount and symbol
        bet_amount_surf = self.bet_font.render("Bet Amount: $" + str(self.player.bet_amount), True, TEXT_COLOR)
        symbol_surf = self.symbol_font.render("Selected Symbol: " + self.player.selected_symbol, True, TEXT_COLOR)
        bet_amount_rect = bet_amount_surf.get_rect(topleft=(500, self.display_surface.get_size()[1] - 55))  # Adjust position as needed
        symbol_rect = symbol_surf.get_rect(topleft=(800, self.display_surface.get_size()[1] - 55))  # Adjust position as needed

        # Draw player data
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        pygame.draw.rect(self.display_surface, False, bet_amount_rect)  # Draw bet amount rect
        pygame.draw.rect(self.display_surface, False, symbol_rect)  # Draw symbol rect
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)
        self.display_surface.blit(bet_amount_surf, bet_amount_rect)  # Display bet amount
        self.display_surface.blit(symbol_surf, symbol_rect)  # Display symbol

        # Print last win if applicable
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! $" + last_payout, True, TEXT_COLOR)
            x1 = 800
            y1 = self.display_surface.get_size()[1] - 200
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center=(x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()

