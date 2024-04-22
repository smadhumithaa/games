from machine import Machine
from settings import *
import ctypes, pygame, sys
import asyncio
# Maintain resolution regardless of Windows scaling settings
# ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self, bet_amount, selected_symbol):

        # General setup
        # pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # pygame.display.set_caption('Slot Machine Demo')
        # self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        # self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()

        self.delta_time = 0
        # Additional attributes to store bet_amount and selected_symbol
        self.bet_amount = bet_amount
        self.selected_symbol = selected_symbol
        self.machine = Machine(selected_symbol, bet_amount)
        # self.ui_font = pygame.font.SysFont(None, UI_FONT_SIZE)
        # self.bet_text_surface = self.ui_font.render(f'Bet Amount: {self.bet_amount}', True, pygame.Color(TEXT_COLOR))
        # self.symbol_text_surface = self.ui_font.render(f'Selected Symbol: {self.selected_symbol}', True, pygame.Color(TEXT_COLOR))
        # # Calculate positions for text surfaces
        # self.bet_text_rect = self.bet_text_surface.get_rect(center=(WIDTH // 4, HEIGHT - 50))
        # self.symbol_text_rect = self.symbol_text_surface.get_rect(center=(WIDTH * 3 // 4, HEIGHT - 50))

        # Sound
        # main_sound = pygame.mixer.Sound('audio/track.mp3')
        # main_sound.play(loops = -1)
        # self.spin_allowed = True

    def run1(self):

        self.start_time = pygame.time.get_ticks()

        # Call the calculate_winning_probability method
        # probability = self.machine.calculate_winning_probability()
        # print("Probability of winning:", probability)


        while True:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Time variables

            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            # self.screen.blit(self.bet_text_surface, self.bet_text_rect)
            # self.screen.blit(self.symbol_text_surface, self.symbol_text_rect)
            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(self.delta_time, self.selected_symbol)

            # self.screen.blit(self.grid_image, (0, 0))
            self.clock.tick(FPS)


