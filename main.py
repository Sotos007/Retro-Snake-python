import pygame
import sys
import random
import pygame.mixer

# Αρχικοποίηση του Pygame
pygame.init()

head_texture = None

# Διαστάσεις του παραθύρου
WIDTH, HEIGHT = 800, 600

# Χρώματα
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Εικόνα για το χάρτη του παιχνιδιού
grass_map = "Map_bg.png"

# Φόρτωση της εικόνας για τα borders
border_texture = pygame.image.load("border.png")
border_texture = pygame.transform.scale(border_texture, (20, 20))

# Δημιουργία του παραθύρου του παιχνιδιού
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Φιδάκι")

# Φόρτωση και αναπαραγωγή μουσικής
pygame.mixer.music.load("sound.mp3")
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1)


class Snake:  # Κλάση για το φίδι
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
        self.head_texture = None
        self.head_texture = pygame.image.load("head1.png")
        self.head_texture = pygame.transform.scale(self.head_texture, (20, 27))
        self.head_texture = pygame.transform.rotate(self.head_texture, -90 * self.direction)

    def get_head_position(self):
        return self.positions[0]

    # Φόρτωση ήχου για όταν το φίδι τρώει ένα φρούτο
    eat_sound = pygame.mixer.Sound("eat.mp3")
    eat_sound.set_volume(0.2)

    def update(self):
        # Ενημέρωση θέσης φιδιού αν δεν είναι παιχνίδι τελειωμένο ή paused
        if not self.game_over and not self.paused:
            cur = self.get_head_position()
            x, y = 0, 0
            keys = pygame.key.get_pressed()
            prev_direction = self.direction

            # Ανίχνευση πλήκτρων για την κίνηση φιδιού
            if keys[pygame.K_UP] and self.direction != 2:
                self.direction = 0
            elif keys[pygame.K_DOWN] and self.direction != 0:
                self.direction = 2
            elif keys[pygame.K_LEFT] and self.direction != 1:
                self.direction = 3
            elif keys[pygame.K_RIGHT] and self.direction != 3:
                self.direction = 1

            if self.direction == 0:
                y = -1
            elif self.direction == 1:
                x = 1
            elif self.direction == 2:
                y = 1
            elif self.direction == 3:
                x = -1

            new = (((cur[0] + (x * 20)) % WIDTH), (cur[1] + (y * 20)) % HEIGHT)

            # Έλεγχος σύγκρουσης του φιδιού με τον εαυτό ή τους τοίχους
            if new[0] < 20 or new[0] >= WIDTH - 20 or new[1] < 20 or new[1] >= HEIGHT - 20:
                self.game_over = True
            else:
                if len(self.positions) > 2 and new in self.positions[2:]:
                    self.game_over = True
                else:
                    self.positions.insert(0, new)
                    if len(self.positions) > self.length:
                        self.positions.pop()

                    if self.get_head_position() == fruit.position:
                        # Αν έχει φάει φρούτο, αύξηση του σκορ
                        self.length += 1
                        self.score += 10
                        fruit.randomize_position()
                        self.fruits_eaten += 1

                        # Αύξηση τησ δυσκολίας του παιχνιδιού
                        if self.fruits_eaten % 3 == 0:
                            # Αύξηση ταχύτητας κάθε 3 φρούτα
                            self.speed += 0.3

                        if self.score > highscore and not self.new_high_score_flag:
                            # Έλεγχος αν έχει φτάσει υψηλότερο σκορ από το highscore
                            self.new_high_score_flag = True
                            # Αναπαραγωγή μουσικής
                            new_highscore_sound = pygame.mixer.Sound("high.mp3")
                            new_highscore_sound.set_volume(0.35)
                            new_highscore_sound.play()

                        Snake.eat_sound.play()

                        self.game_over_sound_played = False

            # Περιστροφή του κεφαλιού του φιδιού ανάλογα με την κατεύθυνση του
            if self.direction != prev_direction or self.head_texture is None:
                self.head_texture = pygame.image.load("head1.png")
                self.head_texture = pygame.transform.scale(self.head_texture, (20, 27))
                self.head_texture = pygame.transform.rotate(self.head_texture, -90 * self.direction)

    def reset(self):
        # Επαναφορά όλων των παραμέτρων φιδιού σε αρχική κατάσταση
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

    def render(self, surface):
        # Απεικόνιση για το χάρτη του παιχνιδιού
        grass_image = pygame.image.load(grass_map)
        surface.blit(grass_image, (0, 0))

        # Φόρτωση εικόνας για το σώμα του φιδιού
        snake_body_texture = pygame.image.load("body1.png")
        snake_body_texture = pygame.transform.scale(snake_body_texture, (20, 26))
        # Περιστροφή της εικόνας του σώματος ανάλογα με την κατεύθυνση
        rotated_texture = pygame.transform.rotate(snake_body_texture, -90 * self.direction)

        for i, p in enumerate(self.positions):
            if i == 0 and self.head_texture is not None:
                # Απεικόνιση του head_texture στη θέση του κεφαλιού
                surface.blit(self.head_texture, (p[0], p[1]))
            else:
                surface.blit(rotated_texture, (p[0], p[1]))

        # Δημιουργία των τοιχωμάτων του παιχνιδιού
        for i in range(0, WIDTH, 10):
            screen.blit(border_texture, (i, 0))  # Πάνω περιθώριο
            screen.blit(border_texture, (i, HEIGHT - 20))  # Κάτω περιθώριο

        for i in range(0, HEIGHT, 10):
            screen.blit(border_texture, (0, i))  # Αριστερό περιθώριο
            screen.blit(border_texture, (WIDTH - 20, i))  # Δεξί περιθώριο


class Fruit:  # Κλάση για τη δημιουργία των φρούτων
    def __init__(self):
        self.texture = None
        self.position = (0, 0)
        self.size = (20, 20)
        self.textures = [
            pygame.image.load("apple.png"),
            pygame.image.load("orange.png"),
            pygame.image.load("cherry.png")
        ]
        self.randomize_position()

    def randomize_position(self):
        while True:
            self.position = (
                random.randint(1, (WIDTH // 20) - 2) * 20,
                random.randint(1, (HEIGHT // 20) - 2) * 20
            )
            if self.position not in snake.positions:
                break

        # Επιλογή τυχαία εικόνας από τη λίστα εικόνων
        self.texture = random.choice(self.textures)

    def render(self, surface):
        surface.blit(pygame.transform.scale(self.texture, self.size), (self.position[0], self.position[1]))


class MainMenu:  # Κλάση για το αρχικό μενού του παιχνιδιού
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.title = self.font.render("Καλώς ήρθες στο Φιδάκι!", True, BLACK)
        self.subtitle = self.font.render("Πάτησε SPACE για να ξεκινήσεις", True, BLACK)
        self.title_rect = self.title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.subtitle_rect = self.subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    def render(self, surface):
        # Εμφάνιση τίτλου και υποτίτλου κυρίως μενού
        surface.blit(self.title, self.title_rect)
        surface.blit(self.subtitle, self.subtitle_rect)


class Background:  # Κλάση για τη δημιουργία του φόντου
    def __init__(self):
        self.image = pygame.image.load("Main_Menu.png")
        self.game_over_image = pygame.image.load("Game_Over.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (-100, 0)
        self.game_over_rect = self.game_over_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.show_game_over = False

    def render(self, surface):
        # Εμφάνιση της εικόνας για το τέλος του παιχνιδιού
        if not self.show_game_over:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.game_over_image, self.game_over_rect)


def load_highscore():
    try:
        # Διάβασμα του υψηλότερου σκορ από το αρχείο
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        # Επιστροφή 0 αν το αρχείο δεν υπάρχει
        return 0


def save_highscore(score):
    # Αποθήκευση του υψηλότερου σκορ στο αρχείο
    with open("highscore.txt", "w") as file:
        file.write(str(score))


# Φόρτωση και αναπαραγωγή μουσικής
game_over_sound = pygame.mixer.Sound("game_over.mp3")
game_over_sound.set_volume(0.5)

main_menu = MainMenu()
snake = Snake()
fruit = Fruit()
background = Background()
clock = pygame.time.Clock()
highscore = load_highscore()
show_highscore_message = False
in_main_menu = True

while True:
    # Φόρτωση εικόνας pause
    pause_image = pygame.image.load("pause.png")
    pause_image = pygame.transform.scale(pause_image, (100, 100))
    pause_rect = pause_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    # Φόρτωση εικόνας play
    play_image = pygame.image.load("play.png")
    play_image = pygame.transform.scale(play_image, (65, 65))
    play_rect = play_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if in_main_menu and event.key == pygame.K_SPACE:
                # Έναρξη του παιχνιδιού με το πάτημα του SPACE στο κύριο μενού
                in_main_menu = False
                snake.reset()
            elif not in_main_menu and snake.game_over:
                if event.key == pygame.K_SPACE:
                    # Επανεκκίνηση του παιχνιδιού με το πάτημα του SPACE μετά τον θάνατο
                    snake.reset()
                    show_highscore_message = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif not in_main_menu and event.key == pygame.K_RETURN:
                if not snake.paused:
                    # Εμφάνιση εικόνας pause όταν το game μπαίνει σε παύση
                    screen.blit(pause_image, pause_rect)
                    pygame.display.flip()
                    # Παύση του παιχνιδιού
                    snake.paused = True
                    pygame.time.delay(400)
                else:
                    # Εμφάνιση εικόνας play όταν το game συνεχίζεται από παύση
                    screen.blit(play_image, play_rect)
                    pygame.display.flip()
                    # Συνέχιση του παιχνιδιού
                    snake.paused = False
                    pygame.time.delay(300)

    if in_main_menu:
        # Εμφάνιση κύριου μενού
        screen.fill(WHITE)
        background.render(screen)
        main_menu.render(screen)
        font = pygame.font.Font(None, 36)
        highscore_text = font.render(f"High Score: {highscore}", True, BLACK)
        highscore_rect = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(highscore_text, highscore_rect)
    else:
        if not snake.paused:
            # Ενημέρωση κατάστασης φιδιού
            snake.update()

        if snake.game_over:
            if not snake.game_over_sound_played:
                # Αναπαραγωγή ήχου για το τέλος του παιχνιδιού
                game_over_sound.play()
                snake.game_over_sound_played = True

            # Εμφάνιση οθόνης τέλους παιχνιδιού
            screen.fill(WHITE)
            background.show_game_over = True
            background.render(screen)

            font = pygame.font.Font(None, 36)
            restart_text = font.render(f"Πάτησε SPACE για να ξανά παίξεις ή ESC για έξοδο. Score: {snake.score}", True,
                                       WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 220))
            screen.blit(restart_text, restart_rect)

            if snake.score > highscore:
                # Αν έχει πετύχει υψηλότερο σκορ, αποθήκευση
                highscore = snake.score
                save_highscore(highscore)
                show_highscore_message = True
        else:
            # Εμφάνιση φιδιού και φρούτου κατά τη διάρκεια του παιχνιδιού
            snake.render(screen)
            fruit.render(screen)
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {snake.score}", True, BLACK)
            score_rect = score_text.get_rect(topleft=(20, 20))
            screen.blit(score_text, score_rect)

    # Εμφάνιση κατάλληλου μηνύματος εαν ο παίχτης επιτύχει νεο high score
    if show_highscore_message:
        highscore_message = font.render("Συγχαρητήρια! Πετύχατε νέο high score!", True, WHITE)
        highscore_rect = highscore_message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 175))
        screen.blit(highscore_message, highscore_rect)

    pygame.display.update()
    clock.tick(snake.speed)
