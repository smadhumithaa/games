import pygame
import sys
import asyncio
from machine import Machine
from settings import *

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slot Machine")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

SYM_PATH = 'graphics/0/symbols'
symbols = {
    'diamond': {"image": f"{SYM_PATH}/0_diamond.png", "caption": "Diamond x6"},
    'floppy': {"image": f"{SYM_PATH}/0_floppy.png", "caption":"floppy x4"},
    'hourglass': {"image": f"{SYM_PATH}/0_hourglass.png", "caption":"hourglass x5"},
    'seven': {"image": f"{SYM_PATH}/0_seven.png", "caption":"seven x3"},
    'telephone': {"image": f"{SYM_PATH}/0_telephone.png", "caption":"telephone x2"}
}

# Load images
button_imgs = {name: pygame.image.load(data["image"]) for name, data in symbols.items()}
button_spacing = 20
button_width, button_height = button_imgs["diamond"].get_size()

# Calculate total width needed for all buttons and spacing
total_width = (button_width + button_spacing) * len(button_imgs) - button_spacing
start_x = (WIDTH - total_width) // 2

button_img_rects = {name: img.get_rect(topleft=(start_x + (button_width + button_spacing) * idx, (HEIGHT - button_height) // 2 - 150)) for idx, (name, img) in enumerate(button_imgs.items())}
button_clicked = {name: False for name in button_imgs}

# Load a font for captions
font = pygame.font.Font(None, 36)


# # Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()


# # Function to draw text on surface
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect = text_obj.get_rect(center=(x, y))  # Center the text horizontally and vertically
    surface.blit(text_obj, text_rect)


# Main game loop
async def main():
    global start_time
    start_time = pygame.time.get_ticks()
    slots = False
    click_name = ""
    bet_input = ''  # Initialize bet_input to an empty string
    bet_amount = None
    start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)  # Define start button rectangle

    running = True
    bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
    machine = None

    while running:
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - start_time) / 1000
        start_time = current_time  # Update start time for the next iteration

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not slots:  # Only handle events if slots are not active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        slots = True
                        screen3 = pygame.display.set_mode((1600, 1000))
                        machine = Machine(click_name, bet_amount)
                        print("Start Clicked!")
                    else:
                        for name, rect in button_img_rects.items():
                            if rect.collidepoint(mouse_pos):
                                click_name = name
                                print(f"Clicked {name}!")
                                print(f"Numerical value: {ord(name[-1]) - ord('0')}")
                                button_imgs[name].fill(GRAY, special_flags=pygame.BLEND_RGB_ADD)
                                button_clicked[name] = not button_clicked[name]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        bet_input = bet_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            bet_amount = int(bet_input)
                            print("Bet amount entered:", bet_amount)
                            bet_input = ''
                        except ValueError:
                            print("Please enter a valid integer for the bet amount.")
                            bet_input = ''
                    else:
                        bet_input += event.unicode

        if slots:
            # Rest of the game logic...

            screen3.blit(bg_image, (0, 0))
            machine.update(delta_time, click_name)
            pygame.display.update()

        else:
            screen.fill(BLACK)
            draw_text("Choose any one of the symbols", font, WHITE, screen, 200, 50)
            for name, img_rect in button_img_rects.items():
                screen.blit(button_imgs[name], img_rect)
                draw_text(symbols[name]["caption"], font, WHITE, screen, img_rect.centerx, img_rect.bottom + 10)  # Draw caption below button

                if button_clicked[name]:
                    pygame.draw.rect(screen, GRAY, img_rect, 3)  # Draw a highlight box around the button if clicked

            # Draw start button
            pygame.draw.rect(screen, WHITE, start_button_rect)
            draw_text("Start the Game", font, BLACK, screen, start_button_rect.centerx, start_button_rect.centery)

            first_image_name = next(iter(button_img_rects))
            first_image_rect = button_img_rects[first_image_name]
            draw_text("Selected symbol : "+click_name, font, WHITE, screen, first_image_rect.centerx, img_rect.bottom + 50)

            # Draw text input box for bet amount
            input_box_rect = pygame.Rect(start_x, img_rect.bottom + 80, 500, 32)
            pygame.draw.rect(screen, WHITE, input_box_rect, 2)
            input_text_surface = font.render("Enter bet amount: " + str(bet_input), True, WHITE)
            screen.blit(input_text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

            draw_text("Bet amount entered : " + str(bet_amount), font, WHITE, screen, first_image_rect.centerx, img_rect.bottom + 150)
            draw_text("Rupees 10 will be taken from your wallet for every reel", font, WHITE, screen, first_image_rect.centerx + 162, img_rect.bottom + 200)

            pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())

