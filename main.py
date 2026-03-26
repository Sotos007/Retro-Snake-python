import pygame
import sys
import random
import pygame.mixer
import logging

# Ρύθμιση Verbose Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Αρχικοποίηση του Pygame
pygame.init()
logging.info("Το Pygame αρχικοποιήθηκε επιτυχώς.")

# Διαστάσεις του παραθύρου
WIDTH, HEIGHT = 800, 600

# Χρώματα
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Δημιουργία του παραθύρου του παιχνιδιού
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Φιδάκι - Pro Edition")

# Προ-φόρτωση στατικών textures
try:
    border_texture = pygame.image.load("border.png").convert_alpha()
    border_texture = pygame.transform.scale(border_texture, (20, 20))
    grass_map_img = pygame.image.load("Map_bg.png").convert()
    logging.info("Τα βασικά textures φορτώθηκαν.")
except Exception as e:
    logging.error(f"Σφάλμα κατά τη φόρτωση των textures: {e}")

# Φόρτωση και αναπαραγωγή μουσικής
try:
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)
    logging.info("Η μουσική ξεκίνησε.")
except:
    logging.warning("Το αρχείο sound.mp3 δεν βρέθηκε.")

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([0, 1, 2, 3])
        self.game_over = False
        self.score = 0
        self.speed = 7.0
        self.fruits_eaten = 0
        self.new_high_score_flag = False
        self.paused = False
        self.game_over_sound_played = False
        
        # Pre-load snake assets
        self.head_img = pygame.image.load("head1.png").convert_alpha()
        self.body_img = pygame.image.load("body1.png").convert_alpha()
        self.eat_sound = pygame.mixer.Sound("eat.mp3")
        self.eat_sound.set_volume(0.2)
        logging.info("Το φίδι αρχικοποιήθηκε.")

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        if not self.game_over and not self.paused:
            cur = self.get_head_position()
            x, y = 0, 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and self.direction != 2:
                self.direction = 0
            elif keys[pygame.K_DOWN] and self.direction != 0:
                self.direction = 2
            elif keys[pygame.K_LEFT] and self.direction != 1:
                self.direction = 3
            elif keys[pygame.K_RIGHT] and self.direction != 3:
                self.direction = 1

            if self.direction == 0: y = -1
            elif self.direction == 1: x = 1
            elif self.direction == 2: y = 1
            elif self.direction == 3: x = -1

            new = (((cur[0] + (x * 20)) % WIDTH), (cur[1] + (y * 20)) % HEIGHT)

            # Έλεγχος σύγκρουσης
            if new[0] < 20 or new[0] >= WIDTH - 20 or new[1] < 20 or new[1] >= HEIGHT - 20:
                self.game_over = True
                logging.info(f"Game Over! Σύγκρουση με τοίχο στη θέση {new}")
            elif len(self.positions) > 2 and new in self.positions[2:]:
                self.game_over = True
                logging.info("Game Over! Σύγκρουση με το σώμα.")
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()

                if self.get_head_position() == fruit.position:
                    self.length += 1
                    self.score += 10
                    self.fruits_eaten += 1
                    self.eat_sound.play()
                    fruit.randomize_position()
                    logging.info(f"Φρούτο φαγώθηκε. Score: {self.score}")

                    if self.fruits_eaten % 3 == 0:
                        self.speed += 0.3
                        logging.info(f"Η ταχύτητα αυξήθηκε: {self.speed}")

                    if self.score > highscore and not self.new_high_score_flag:
                        self.new_high_score_flag = True
                        try:
                            new_highscore_sound = pygame.mixer.Sound("high.mp3")
                            new_highscore_sound.set_volume(0.35)
                            new_highscore_sound.play()
                            logging.info("Νέο High Score!")
                        except: pass

    def reset(self):
        self.__init__()
        logging.info("Το παιχνίδι έγινε reset.")

    def render(self, surface):
        surface.blit(grass_map_img, (0, 0))

        # Render σώμα και κεφάλι
        for i, p in enumerate(self.positions):
            if i == 0:
                rotated_head = pygame.transform.rotate(
                    pygame.transform.scale(self.head_img, (20, 27)), -90 * self.direction)
                surface.blit(rotated_head, p)
            else:
                rotated_body = pygame.transform.rotate(
                    pygame.transform.scale(self.body_img, (20, 26)), -90 * self.direction)
                surface.blit(rotated_body, p)

        # Borders
        for i in range(0, WIDTH, 20):
            surface.blit(border_texture, (i, 0))
            surface.blit(border_texture, (i, HEIGHT - 20))
        for i in range(0, HEIGHT, 20):
            surface.blit(border_texture, (0, i))
            surface.blit(border_texture, (WIDTH - 20, i))

class Fruit:
    def __init__(self):
        self.size = (20, 20)
        try:
            self.textures = [
                pygame.image.load("apple.png").convert_alpha(),
                pygame.image.load("orange.png").convert_alpha(),
                pygame.image.load("cherry.png").convert_alpha()
            ]
        except:
            logging.error("Δεν βρέθηκαν οι εικόνες των φρούτων.")
            self.textures = []
        self.randomize_position()

    def randomize_position(self):
        while True:
            self.position = (
                random.randint(1, (WIDTH // 20) - 2) * 20,
                random.randint(1, (HEIGHT // 20) - 2) * 20
            )
            if self.position not in snake.positions:
                break
        self.current_texture = random.choice(self.textures) if self.textures else None

    def render(self, surface):
        if self.current_texture:
            surface.blit(pygame.transform.scale(self.current_texture, self.size), self.position)

class Background:
    def __init__(self):
        try:
            self.image = pygame.image.load("Main_Menu.png").convert()
            self.game_over_image = pygame.image.load("Game_Over.png").convert()
        except:
            logging.warning("Background images missing.")
        self.rect = self.image.get_rect(topleft=(-100, 0))
        self.game_over_rect = self.game_over_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.show_game_over = False

    def render(self, surface):
        if not self.show_game_over:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.game_over_image, self.game_over_rect)

def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))
    logging.info(f"Το highscore {score} αποθηκεύτηκε.")

# Αρχικοποίηση αντικειμένων
game_over_sound = None
try:
    game_over_sound = pygame.mixer.Sound("game_over.mp3")
    game_over_sound.set_volume(0.5)
except: pass

snake = Snake()
fruit = Fruit()
background = Background()
clock = pygame.time.Clock()
highscore = load_highscore()
in_main_menu = True
show_highscore_message = False

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if in_main_menu and event.key == pygame.K_SPACE:
                in_main_menu = False
                snake.reset()
            elif not in_main_menu and snake.game_over:
                if event.key == pygame.K_SPACE:
                    snake.reset()
                    background.show_game_over = False
                    show_highscore_message = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif not in_main_menu and event.key == pygame.K_RETURN:
                snake.paused = not snake.paused
                logging.info(f"Pause toggled: {snake.paused}")

    if in_main_menu:
        screen.fill(WHITE)
        background.render(screen)
        font = pygame.font.Font(None, 36)
        title = font.render("Καλώς ήρθες στο Φιδάκι!", True, BLACK)
        subtitle = font.render("Πάτησε SPACE για να ξεκινήσεις", True, BLACK)
        hs_text = font.render(f"High Score: {highscore}", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        screen.blit(subtitle, (WIDTH // 2 - 180, HEIGHT // 2 + 20))
        screen.blit(hs_text, (WIDTH // 2 - 80, HEIGHT // 2 + 100))
    else:
        if not snake.paused:
            snake.update()

        if snake.game_over:
            if not snake.game_over_sound_played:
                if game_over_sound: game_over_sound.play()
                snake.game_over_sound_played = True
            
            background.show_game_over = True
            background.render(screen)
            
            font = pygame.font.Font(None, 30)
            restart_text = font.render(f"SPACE για Επανεκκίνηση | Score: {snake.score}", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 200))

            if snake.score > highscore:
                highscore = snake.score
                save_highscore(highscore)
                show_highscore_message = True
            
            if show_highscore_message:
                msg = font.render("ΝΕΟ HIGH SCORE!", True, WHITE)
                screen.blit(msg, (WIDTH // 2 - 100, HEIGHT // 2 + 150))
        else:
            snake.render(screen)
            fruit.render(screen)
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {snake.score}", True, BLACK)
            screen.blit(score_text, (30, 30))
            if snake.paused:
                pause_label = font.render("PAUSED", True, BLACK)
                screen.blit(pause_label, (WIDTH // 2 - 40, HEIGHT // 2))

    pygame.display.update()
    clock.tick(snake.speed)
