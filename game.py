import os
import pygame
import random

pygame.mixer.init()
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player properties
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 100
PLAYER_COLOR = (255, 0, 0)

# Ball properties
BALL_RADIUS = 20
BALL_COLOR = (0, 0, 255)

# Ground properties
GROUND_HEIGHT = 50

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Creepy-Uppy")

clock = pygame.time.Clock()

# Path to the folder containing the player animation frames
PLAYER_ANIMATION_PATH = "player"
player_frames = []
for i in range(1, 5):  # Assuming you have player_1.png to player_4.png
    frame_path = os.path.join(PLAYER_ANIMATION_PATH, f"player_{i}.png")
    frame = pygame.image.load(frame_path)
    player_frames.append(frame)

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.bounce_count = 0
        self.is_animating = False  # Add the is_animating attribute and initialize it to False
        self.animation_frame_index = 0
        self.animation_time = pygame.time.get_ticks()

    def start_animation(self):
        self.is_animating = True
        self.animation_frame_index = 0
        self.animation_time = pygame.time.get_ticks()

    def stop_animation(self):
        self.is_animating = False
        self.animation_frame_index = 0

    def draw(self):
        # If animating, switch frames at regular intervals
        if self.is_animating:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_time > 100:  # Adjust the interval as needed for animation speed
                self.animation_frame_index = (self.animation_frame_index + 1) % len(player_frames)
                self.animation_time = current_time

        # Draw the current frame of the animation
        frame = player_frames[self.animation_frame_index]
        screen.blit(frame, (self.x, self.y))

class Ball:
    def __init__(self, player):
        self.player = player
        self.reset()

    def reset(self):
        self.x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
        self.y = BALL_RADIUS
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = 5
        self.was_counted = False  # Track if the ball was counted for a bounce in the current frame

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce the ball when it hits the screen edges
        if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= SCREEN_WIDTH:
            self.speed_x *= -1

        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.speed_y *= -1

            # Increment the bounce count whenever the ball bounces off the ground
            if self.y + BALL_RADIUS >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.player.bounce_count += 1

    def draw(self):
        draw_fireball(self.x, self.y, BALL_RADIUS)

def draw_fireball(x, y, radius):
    # Create a flame-like pattern with circles of varying colors and sizes
    colors = [(255, 0, 0), (255, 165, 0), (255, 215, 0), (255, 255, 255)]
    for i in range(4):
        pygame.draw.circle(screen, colors[i], (int(x), int(y)), radius - i * 2)

def show_intro():
    intro_done = False
    intro_start_time = pygame.time.get_ticks()

    # Load the intro music (replace "intro_music.m4a" with your m4a audio file)
    pygame.mixer.music.load("player/intro_music.ogg")
    pygame.mixer.music.play()  # Start playing the intro music

    # Load the space background image
    space_background = pygame.image.load("player/space_background.jpg").convert()

    font = pygame.font.Font(None, 80)
    title_text = "CREPPY-UPPY"

    # Set the initial transparency of the intro text to 0 (completely transparent)
    title_alpha = 0

    while not intro_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                intro_done = True

        current_time = pygame.time.get_ticks()
        if current_time - intro_start_time >= 4000:  # Show the intro for 4 seconds
            intro_done = True

        # Blit the space background on the screen
        screen.blit(space_background, (0, 0))

        # Increase the transparency of the intro text over time to create the fade-in effect
        if title_alpha < 255:
            title_alpha += 5  # Adjust the increment value to control the speed of the fade-in effect

        # Render the intro text with the current transparency value
        title_text_surface = font.render(title_text, True, (255, 255, 255, title_alpha))
        title_text_rect = title_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(title_text_surface, title_text_rect)

        pygame.display.flip()
        clock.tick(60)

def game_over():
    font = pygame.font.Font(None, 80)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    font = pygame.font.Font(None, 36)
    play_again_text = font.render("Play Again", True, (255, 255, 255))
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    return

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(play_again_text, play_again_rect)
        pygame.display.flip()

def main():
    player = Player()
    ball = Ball(player)  # Pass the player object to the Ball constructor
    score = 0

    ball_miss_count = 0
    max_misses = 3

    # Create a font for displaying the score
    font = pygame.font.Font(None, 48)
    show_intro()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.start_animation()  # Start the player animation when spacebar is pressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.stop_animation()  # Stop the player animation when spacebar is released

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5

        ball.update()

        # Check collision with player
        if not ball.was_counted and player.x < ball.x < player.x + PLAYER_WIDTH and player.y < ball.y < player.y + PLAYER_HEIGHT:
            ball.speed_y *= -1
            ball.was_counted = True
            # Increment the score for each successful bounce
            score += 1

        # Reset the "was_counted" flag when the ball moves out of the player's area
        if ball.was_counted and (ball.y <= player.y or ball.x < player.x or ball.x > player.x + PLAYER_WIDTH):
            ball.was_counted = False

        # Check if the ball goes below the screen
        if ball.y - BALL_RADIUS > SCREEN_HEIGHT:
            ball_miss_count += 1
            if ball_miss_count >= max_misses:
                game_over()
                ball.reset()
                ball_miss_count = 0
                score = 0  # Reset the score when the game is over
            else:
                ball.reset()

        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (0, 255, 0), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        player.draw()
        ball.draw()

        player.draw()
        ball.draw()

        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(score_text, score_rect)

        # Display bounce count
        bounce_text = font.render(f"Missed Hits: {player.bounce_count}", True, (255, 255, 255))
        screen.blit(bounce_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
