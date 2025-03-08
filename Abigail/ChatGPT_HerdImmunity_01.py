# https://chatgpt.com/share/67cc15cf-1d9c-8011-b3d5-dd95968a9a5b

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Herd Immunity Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)  # Immune
RED = (200, 0, 0)    # Infected
BLUE = (0, 0, 200)   # Susceptible

# Parameters
POPULATION = 200
INFECTION_RADIUS = 10
INFECTION_PROBABILITY = 0.05  # Chance of spreading when in range
VACCINATED_PERCENT = 0.7     # Starting vaccinated proportion (adjustable)

# Individual class
class Person:
    def __init__(self, x, y, status="susceptible"):
        self.x = x
        self.y = y
        self.status = status
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Boundary conditions
        if self.x < 0 or self.x > WIDTH:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > HEIGHT:
            self.angle = -self.angle

    def draw(self):
        color = BLUE if self.status == "susceptible" else GREEN if self.status == "immune" else RED
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 5)

# Initialize population
people = []
for _ in range(POPULATION):
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    if random.random() < VACCINATED_PERCENT:
        people.append(Person(x, y, status="immune"))
    else:
        people.append(Person(x, y))

# Infect one random person
random.choice(people).status = "infected"

def check_infection():
    for person in people:
        if person.status == "infected":
            for other in people:
                if other.status == "susceptible":
                    dist = math.hypot(person.x - other.x, person.y - other.y)
                    if dist < INFECTION_RADIUS and random.random() < INFECTION_PROBABILITY:
                        other.status = "infected"

# Main loop
running = True
clock = pygame.time.Clock()

days = 0
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for person in people:
        person.move()
        person.draw()

    check_infection()

    # Count statuses
    infected_count = sum(1 for p in people if p.status == "infected")
    immune_count = sum(1 for p in people if p.status == "immune")
    susceptible_count = POPULATION - infected_count - immune_count

    # Display stats
    font = pygame.font.SysFont(None, 30)
    stats = f"Day: {days} | Infected: {infected_count} | Immune: {immune_count} | Susceptible: {susceptible_count}"
    text = font.render(stats, True, BLACK)
    screen.blit(text, (10, 10))

    if infected_count == 0:
        result_text = f"Herd immunity achieved at {immune_count / POPULATION:.0%} vaccinated."
        result = font.render(result_text, True, GREEN)
        screen.blit(result, (10, 40))

    pygame.display.flip()
    clock.tick(30)
    days += 1

pygame.quit()
