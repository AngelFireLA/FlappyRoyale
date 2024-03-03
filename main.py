import csv
import random

import pygame


class Button:
    def __init__(self, text, x=0, y=0, color=(75, 174, 78),
                 highlight_color=(138, 192, 72), click_color=(255, 140, 0), text_color=(255, 255, 255),
                 font_size=50, size=1, corner=False):
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
        if not corner:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, 1, text_color)

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


import pygame

def place_text(x, y, text, size, color=None, border=False, corner=False):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    lines = text.split('\n')

    # Define border and inner color
    border_color = (0, 0, 0)  # Black color for border
    inner_color = color if color else (255, 255, 255)  # White color for inner text

    for i, line in enumerate(lines):
        # Render the text line
        line_surface = font.render(line, True, inner_color)

        # Determine position based on `corner` parameter
        if corner:
            # If `corner` is True, align text to the top-left corner based on `x` and `y`
            if corner == "opposite":
                line_rect = line_surface.get_rect(topright=(x, y + i * size))
            else:
                line_rect = line_surface.get_rect(topleft=(x, y + i * size))
        else:
            # If `corner` is False, center the text as usual
            line_rect = line_surface.get_rect(center=(x, y + i * size))

        if border:
            # Render text with border color for outline
            for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                border_line_surface = font.render(line, True, border_color)
                border_line_rect = border_line_surface.get_rect(topleft=(line_rect.x + dx, line_rect.y + dy))
                screen.blit(border_line_surface, border_line_rect)

        # Render the actual text
        screen.blit(line_surface, line_rect)



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
            #play assets/audio/wing.wav
            pygame.mixer.Sound("assets/audio/wing.wav").play()
        if pygame.mouse.get_pressed()[0] == 0:
            self.flapping = False
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]


class Pipe(pygame.sprite.Sprite):
    pipe_gap = 130
    scored = False

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/pipes/pipe-green.png')
        self.rect = self.image.get_rect()
        self.position = position
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(self.pipe_gap / 2)]

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


# default pygame setup + loop
pygame.init()
#init sound player
pygame.mixer.init()
scale_factor = 1.5
width, height = 304 * scale_factor, 457 * scale_factor
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird P2W")
clock = pygame.time.Clock()

background = pygame.image.load("assets/sprites/background/default.jpg")
# resize image to be multiplied by scale factor
background = pygame.transform.scale(background,
                                    (background.get_width() * scale_factor, background.get_height() * scale_factor))

quests_path = 'data/quests.csv'

# Define the header of your CSV file
header = ['id', 'type', 'value', 'gamemode', 'completed', 'text', 'progress']


def main_menu():
    button1 = Button('Start', width / 2, height / 3, size=1)
    button2 = Button(text='FlappyPass', x=width / 2, y=height / 1.8, size=1, font_size=45)
    button3 = Button('Exit', width / 2, height / 1.3, size=1)

    buttons = [button1, button2, button3]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.handle_event(event):
                    game = start_game()
                    while game:
                        game = start_game()
                if button2.handle_event(event):
                    pass_royale()
                    pygame.display.set_mode((width, height))
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
    pipe_group = pygame.sprite.Group()

    flappy = Bird(100, height / 2)
    bird_group.add(flappy)
    start_time = None
    score = 0
    done = False
    game_over = False
    game_over_animation_done = False
    game_over_img = pygame.image.load('assets/sprites/gameover.png')
    game_over_img = pygame.transform.scale(game_over_img,
                                           (game_over_img.get_width() * scale_factor,
                                            game_over_img.get_height() * scale_factor))
    game_over_rect = game_over_img.get_rect(
        center=(width / 2, height + game_over_img.get_rect().height / 2.2))  # Start below screen

    pipe_frequency = 1000  # milliseconds
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    collisions = None
    game_over_start_time = None
    game_over_quest_update = False

    with open('data/quests.csv', 'r') as f:
        quests = {quest[0]:quest for quest in list(csv.reader(f))[1:]}
        for quest in quests:
            quests[quest] = {"type":quests[quest][1], "value":quests[quest][2], "gamemode":quests[quest][3], "completed":quests[quest][4], "text":quests[quest][5], "progress":quests[quest][6]}
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                return True
        # Draw the background images
        screen.blit(background, (ground_x1, 0))
        screen.blit(background, (ground_x2, 0))
        if not start_time:
            start_time = pygame.time.get_ticks()
        if not game_over:
            # Update the positions of the background images
            ground_x1 -= 3
            ground_x2 -= 3

        # Reset the positions to create the infinite scroll effect
        if ground_x1 <= -background.get_width():
            ground_x1 = background.get_width()
        if ground_x2 <= -background.get_width():
            ground_x2 = background.get_width()

        if not game_over:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(width, int(height / 2) + pipe_height, -1)
                top_pipe = Pipe(width, int(height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            for pipe in pipe_group:
                pipe.update()
                # Check if the bird has passed the pipe
                if flappy.rect.left > pipe.rect.right and not pipe.scored and pipe.position == 1:
                    score += 1
                    pipe.scored = True  # Mark this pipe as scored
                    pygame.mixer.Sound("assets/audio/point.wav").play()

            bird_group.update()
        pipe_group.draw(screen)
        bird_group.draw(screen)
        if not game_over:
            if bird_group.sprites()[0].rect.bottom >= 614:
                game_over = True
                game_over_start_time = pygame.time.get_ticks()
            collisions = pygame.sprite.groupcollide(bird_group, pipe_group, dokilla=False, dokillb=False)

        else:
            if not game_over_quest_update:
                quests["1"]["progress"] = int(quests["1"]["progress"])+score
                two_progress = quests["2"]["progress"]
                if score > int(two_progress):
                    quests["2"]["progress"] = score
                # Convert the updated quests dictionary back to a list of rows
                rows = [header]  # Start with the header row
                for quest_id, quest_details in quests.items():
                    row = [quest_id] + list(quest_details.values())
                    rows.append(row)

                # Write the rows back to the CSV file
                with open(quests_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(rows)
                game_over_quest_update = True
            if not game_over_animation_done:
                current_time = pygame.time.get_ticks()
                if game_over_rect.centery > height / 2.2:
                    game_over_rect.centery -= 5  # Speed of the game over image coming up
                else:
                    if current_time - game_over_start_time > 0:  # 3 seconds wait

                        game_over_animation_done = True
                        done = True  # Exit after animation

            screen.blit(game_over_img, game_over_rect)
        if not game_over and collisions:
            game_over = True
            game_over_start_time = pygame.time.get_ticks()
            pygame.mixer.Sound("assets/audio/hit.wav").play()
        place_text(width/2, 100, str(score), 50)
        pygame.display.flip()
        clock.tick(60)
    return False


def pass_royale():
    pygame.display.set_mode((912, height))
    code_box = pygame.image.load('assets/sprites/others/code_box.png')
    code_box_rect = code_box.get_rect()
    code_box_rect.x, code_box_rect.y = (25, 150)
    active_pass_button = Button('Activer', x=code_box.get_width() + 30 + 20, y=150, size=0.8, corner=True, color=(249, 220, 53), text_color=(0, 0, 0))
    input_text = ''
    input_active = False
    font = pygame.freetype.SysFont("Arial", 40)
    letter_spacing = 25
    with open('data/quests.csv', 'r') as f:
        reader = csv.reader(f)
        #quests are under format : id (int)	type(str)	value(int)	gamemode(str)	completed(bool)	text	progress(int)
        quests = list(reader)
        #as a dict where each id is a key, and then the value is a dict based on the format of a row
        quests = {quest[0]:quest for quest in quests[1:]}
        for quest in quests:
            quests[quest] = {"type":quests[quest][1], "value":quests[quest][2], "gamemode":quests[quest][3], "completed":quests[quest][4], "text":quests[quest][5], "progress":quests[quest][6]}
            if int(quests[quest]["value"]) != -1 and int(quests[quest]["value"]) <= int(quests[quest]["progress"]):
                quests[quest]["completed"] = "True"
            else:
                quests[quest]["completed"] = "False"
    rows = [header]  # Start with the header row
    for quest_id, quest_details in quests.items():
        row = [quest_id] + list(quest_details.values())
        rows.append(row)

    # Write the rows back to the CSV file
    with open(quests_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if code_box_rect.collidepoint(event.pos):
                    input_active = not input_active
                    print(input_active)
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        print(input_text)
                    elif len(input_text) < 4:
                        input_text += event.unicode.upper()  # Making input uppercase

        screen.blit(background, (0, 0))
        place_text(150, 50, "Flappy Pass", 40)

        screen.blit(code_box, code_box_rect)
        # Draw input box
        # Calcule la position de départ du texte
        text_x, text_y = code_box_rect.x + 15, code_box_rect.y + 15

        # Dessine chaque lettre individuellement avec un espacement
        for i, letter in enumerate(input_text):
            txt_surface, txt_rect = font.render(letter, (0, 0, 0))
            screen.blit(txt_surface, (text_x + i * (txt_rect.width + letter_spacing), text_y))
        active_pass_button.draw(screen)

        quest_area = pygame.Rect(450, 50, 450, 250)
        pygame.draw.rect(screen, (254, 152, 0), quest_area)
        place_text(460, 60, "Quêtes :", 25, corner=True)
        i = 0
        for quest in quests:
            place_text(460, 130+i*50, f"{quests[quest]['text'].replace('{}', quests[quest]['value'])}", 20, corner=True)
            if int(quests[quest]['value']) != -1 and int(quests[quest]['gamemode']) == 0:
                if quests[quest]['completed'] == "True":
                    place_text(875, 130 + i * 50, f"{quests[quest]['progress']}/{quests[quest]['value']}", 23,corner="opposite", color=(0, 255, 0))
                else:
                    place_text(875, 130 + i * 50, f"{quests[quest]['progress']}/{quests[quest]['value']}", 23,corner="opposite", color=(255, 0, 0))
            i += 1
        pygame.display.flip()

main_menu()
