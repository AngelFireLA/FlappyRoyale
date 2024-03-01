import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.counter = 0
        self.images = []
        for i in range(0, 3):
            self.images.append(pygame.image.load(f"assets/sprites/birds/yellowbird-{i}.png"))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 0.1
        self.velocity = 0
        self.flapping = False

    def update(self):
        velocity_down = 0.375
        velocity_up = -7.5
        self.velocity += velocity_down
        if (self.rect.bottom < 630 or self.velocity < 0) and (self.velocity > 0 or self.rect.top > 0):
            self.rect.y += self.velocity


        if pygame.mouse.get_pressed()[0] == 1 and not self.flapping:
            self.velocity = velocity_up
            self.flapping = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.flapping = False
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]


class Button:
    def __init__(self, text, x=0, y=0, color=(75, 174, 78),
                 highlight_color=(138, 192, 72), click_color=(255, 140, 0),
                 font_size=50, size=1):
        self.text = text
        self.x = x
        self.y = y

        self.font_size = font_size

        self.normal_color = color
        self.highlight_color = highlight_color
        self.click_color = click_color

        self.image_normal = pygame.Surface((200 * size, 100 * size))
        self.image_normal.fill(color)

        self.image_highlighted = pygame.Surface((200 * size, 100 * size))
        self.image_highlighted.fill(highlight_color)

        self.image_clicked = pygame.Surface((200 * size, 100 * size))
        self.image_clicked.fill(click_color)

        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, 1, color_dict["white"])

        W = self.text_surface.get_width()
        H = self.text_surface.get_height()
        self.image_normal.blit(self.text_surface, ((200 * size - W) // 2, (100 * size - H) // 2))
        self.image_highlighted.blit(self.text_surface, ((200 * size - W) // 2, (100 * size - H) // 2))
        self.image_clicked.blit(self.text_surface, ((200 * size - W) // 2, (100 * size - H) // 2))

        self.click_start = 0
        self.click_duration = 200

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if event.button == 1:
                self.image = self.image_clicked
                self.click_start = pygame.time.get_ticks()
                return True
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            if pygame.time.get_ticks() - self.click_start > self.click_duration:
                self.image = self.image_highlighted
        return False

    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.image != self.image_clicked or (
                    self.image == self.image_clicked and pygame.time.get_ticks() - self.click_start > self.click_duration):
                self.image = self.image_highlighted
        else:
            self.image = self.image_normal

        bordered_image = self.image.copy()

        image_rect = bordered_image.get_rect()

        pygame.draw.rect(bordered_image, (0, 0, 0), image_rect, 2)

        surface.blit(bordered_image, self.rect)


color_dict = {"black": [0, 0, 0], "red": [255, 0, 0], "green": [0, 255, 0], "blue": [0, 0, 255],
              "yellow": [255, 255, 0], "magenta": [255, 0, 255], "cyan": [0, 255, 255], "white": [255, 255, 255],
              "gray": [128, 128, 128], "light gray": [192, 192, 192], "dark gray": [64, 64, 64],
              "light red": [255, 64, 64], "light green": [64, 255, 64]}


def place_text(x, y, text, size, color=None, border=False):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    lines = text.split('\n')

    # Define border and inner color
    border_color = (0, 0, 0)  # Black color for border
    inner_color = color if color else (255, 255, 255)  # White color for inner text

    for i, line in enumerate(lines):
        if border:
            # Render text with border color for outline
            for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                line_surface = font.render(line, True, border_color)
                line_rect = line_surface.get_rect(center=(x + dx, y + i * size + dy))
                screen.blit(line_surface, line_rect)

        # Render the actual text in designated color or default color
        line_surface = font.render(line, True, inner_color)
        line_rect = line_surface.get_rect(center=(x, y + i * size))
        screen.blit(line_surface, line_rect)


# default pygame setup + loop
pygame.init()
scale_factor = 1.5
width, height = 304*scale_factor, 457*scale_factor
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird P2W")
clock = pygame.time.Clock()

background = pygame.image.load("assets/sprites/background/default.jpg")
# resize image to be multiplied by scale factor
background = pygame.transform.scale(background,
                                    (background.get_width() * scale_factor, background.get_height() * scale_factor))


def main_menu():
    button1 = Button('Start', width / 2, height / 3, size=1)
    button2 = Button('Settings', width / 2, height / 1.8, size=1)
    button3 = Button('Exit', width / 2, height / 1.3, size=1)

    buttons = [button1, button2, button3]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.handle_event(event):
                    start_game()
                elif button3.handle_event(event):
                    pygame.quit()
                    exit()

        screen.blit(background, (0, 0))

        for button in buttons:
            button.draw(screen)
        place_text(width / 2, height / 7, "Flappy Royale", 50, color_dict["white"], border=True)
        pygame.display.flip()


def start_game():
    ground_x1 = 0
    ground_x2 = background.get_width()

    bird_group = pygame.sprite.Group()
    flappy = Bird(100, height/2)
    bird_group.add(flappy)
    start_time = None
    score = 0
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            start_time = pygame.time.get_ticks()
        # Update the positions of the background images
        ground_x1 -= 3
        ground_x2 -= 3

        # Reset the positions to create the infinite scroll effect
        if ground_x1 <= -background.get_width():
            ground_x1 = background.get_width()
        if ground_x2 <= -background.get_width():
            ground_x2 = background.get_width()

        # Draw the background images
        screen.blit(background, (ground_x1, 0))
        screen.blit(background, (ground_x2, 0))
        # if pygame.time.get_ticks() - start_time >= 1000:
        #     start_time = None
        #     score+=1
        bird_group.update()
        bird_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)


main_menu()
