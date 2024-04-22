import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# WIN.topleft = (500, 600)
# WIN.width = 300
# WIN.height = 50
pygame.display.set_caption("Symbol Selection")

# Load symbol images
SYM_PATH = 'graphics/0/symbols'
symbols = {
    'diamond': f"{SYM_PATH}/0_diamond.png",
    'floppy': f"{SYM_PATH}/0_floppy.png",
    'hourglass': f"{SYM_PATH}/0_hourglass.png",
    'hourglass2': f"{SYM_PATH}/0_seven.png",
    'telephone': f"{SYM_PATH}/0_telephone.png"
}

# Load symbol images
symbol_images = {name: pygame.image.load(path) for name, path in symbols.items()}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.SysFont(None, 30)


def display_selection_page():
    WIN.fill(WHITE)
    num_symbols = len(symbol_images)
    symbol_width = list(symbol_images.values())[0].get_width()
    total_width = symbol_width * num_symbols
    spacing = (WIDTH - total_width) // (num_symbols + 1)
    symbol_height = list(symbol_images.values())[0].get_height()

    # Draw symbols
    symbol_positions = {}
    for i, (symbol_name, symbol_image) in enumerate(symbol_images.items()):
        x = spacing * (i + 1) + symbol_width * i
        y = HEIGHT // 3 - symbol_height // 2
        WIN.blit(symbol_image, (x, y))

        # Store symbol positions
        symbol_positions[symbol_name] = (x, y, symbol_image)

        # Check for button click
        symbol_rect = pygame.Rect(x, y, symbol_image.get_width(), symbol_image.get_height())
        if symbol_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(WIN, BLACK, symbol_rect, 2)

        text = FONT.render(f"Select {symbol_name}", True, BLACK)
        text_rect = text.get_rect(center=(x + symbol_width // 2, y - 20))
        WIN.blit(text, text_rect)

    # Draw text box
    bet_input_rect = pygame.Rect(100, 100, 200, 100)
    bet_input_rect.topleft = (500, 500)  # Adjusted position
    bet_input_rect.width = 300
    bet_input_rect.height = 50
    pygame.draw.rect(WIN, BLACK, bet_input_rect, 2)
    bet_text = FONT.render("Enter bet amount:", True, BLACK)
    bet_text_rect = bet_text.get_rect(midtop=(WIDTH // 2, HEIGHT // 3 * 2 + 60))  # Adjusted position
    WIN.blit(bet_text, bet_text_rect)
    pygame.display.update()


def get_user_input():
    bet_amount = ""
    selected_symbol = None
    run = True

    while run:
        # Define symbol_positions dictionary
        symbol_positions = {}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for symbol_name, (symbol_x, symbol_y, symbol_image) in symbol_positions.items():
                    symbol_rect = pygame.Rect(symbol_x, symbol_y, symbol_image.get_width(), symbol_image.get_height())
                    if symbol_rect.collidepoint(mouse_pos):
                        selected_symbol = symbol_name
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_BACKSPACE:
                    bet_amount = bet_amount[:-1]
                else:
                    bet_amount += event.unicode

        WIN.fill(WHITE)
        display_selection_page()

        bet_text_surface = FONT.render(bet_amount, True, BLACK)
        bet_input_rect = pygame.Rect(100, 100, 200, 100)
        bet_input_rect.topleft = (500, 500)  # Adjusted position
        bet_input_rect.width = 300
        bet_input_rect.height = 50
        bet_text_rect = bet_text_surface.get_rect(center=bet_input_rect.center)
        WIN.blit(bet_text_surface, bet_text_rect)
        pygame.display.update()

    return selected_symbol, int(bet_amount)


symbol, bet = get_user_input()
