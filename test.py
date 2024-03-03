import pygame
import pygame.freetype

def main():
    pygame.init()

    # Screen dimensions
    width, height = 992, 573
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy Pass")

    # Colors
    BLACK = pygame.Color('#000001')
    YELLOW = pygame.Color('#F9DC35')
    WHITE = pygame.Color('#FFFFFE')
    ORANGE = pygame.Color('#FE9800')
    LIGHT_GREEN = pygame.Color('#8AC048')
    GREEN = pygame.Color('#4BAE4E')
    DARK_GREEN = pygame.Color('#528A2C')
    SKY_BLUE = pygame.Color('#87CEEB')  # Assuming a sky blue for the background

    # Background
    screen.fill(SKY_BLUE)

    # Font setup
    font = pygame.freetype.SysFont("Arial", 24)

    # Input box setup
    input_box = pygame.Rect(50, 50, 140, 40)
    input_text = ''
    input_active = False

    # Button setup
    activate_button = pygame.Rect(200, 50, 100, 40)
    quest_buttons = [pygame.Rect(750, 100 + i*60, 80, 40) for i in range(3)]

    # Main loop flag
    running = True

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    input_active = False

                # Check if quest play buttons are pressed
                for button in quest_buttons:
                    if button.collidepoint(event.pos):
                        print("Quest button pressed!")
                        # Placeholder for actual quest button functionality

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < 4:
                        input_text += event.unicode.upper()  # Making input uppercase

        screen.fill(SKY_BLUE)  # Refresh background

        # Draw input box
        txt_surface, _ = font.render(input_text, WHITE)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        # Draw activate button
        pygame.draw.rect(screen, YELLOW, activate_button)
        font.render_to(screen, (activate_button.x + 10, activate_button.y + 10), "Activer", BLACK)

        # Draw quest section
        quest_area = pygame.Rect(700, 50, 250, 250)
        pygame.draw.rect(screen, YELLOW, quest_area)
        for i, button in enumerate(quest_buttons):
            pygame.draw.rect(screen, ORANGE, button)
            font.render_to(screen, (button.x + 10, button.y + 10), "Jouer", WHITE)
            font.render_to(screen, (710, 110 + i*60), f"Quête {i+1}: truc", BLACK)

        # Draw battle pass tiers
        for i in range(5):  # Draw example 5 boxes per section
            pygame.draw.rect(screen, LIGHT_GREEN, [50 + (i*100), 350, 80, 40])
            pygame.draw.rect(screen, GREEN, [50 + (i*100), 400, 80, 40])
        font.render_to(screen, (50, 320), "Gratuit", BLACK)
        font.render_to(screen, (50, 370), "Premium", BLACK)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
