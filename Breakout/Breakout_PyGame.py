import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 8

# Ball settings
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 1 #random.choice([-4, 4])
ball_speed_y = 2 #-4

# Brick settings
BRICK_ROWS = 8 
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30
bricks = []

# Create Rectangles for bricks
brick_colors = [RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, ORANGE, PINK]
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * BRICK_WIDTH,
                            row * BRICK_HEIGHT + 50,
                            BRICK_WIDTH - 2,
                            BRICK_HEIGHT - 2)
        bricks.append(brick)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # paddle.x = ball.x  # Move paddle to follow ball
    paddle.x = ball.x

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            break

    # Game over if ball falls below paddle
    if ball.bottom >= HEIGHT:
        running = False

    # Draw paddle
    pygame.draw.rect(screen, BLUE, paddle)

    # Draw ball
    # pygame.draw.ellipse(screen, RED, ball)
    pygame.draw.rect(screen, RED, ball)

    # Draw bricks
    brick_row = 0
    for brick in bricks:
        # brick_row  = brick_row // BRICK_ROWS
        # pygame.draw.rect(screen, brick_colors[brick_row], brick)
        pygame.draw.rect(screen, YELLOW, brick)

    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
