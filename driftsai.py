import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Initial D Drift Simulation")
clock = pygame.time.Clock()

# -----------------------
# Car
# -----------------------
x = WIDTH / 2
y = HEIGHT / 2

vx = 0
vy = 0

angle = 0

running = True

while running:

    dt = clock.tick(60) / 16.67

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    throttle = 0
    steering = 0

    if keys[pygame.K_UP]:
        throttle = 0.25

    if keys[pygame.K_DOWN]:
        throttle = -0.18

    if keys[pygame.K_LEFT]:
        steering = -1

    if keys[pygame.K_RIGHT]:
        steering = 1

    handbrake = keys[pygame.K_SPACE]

    # -----------------------
    # Direction vectors
    # -----------------------
    forward_x = math.cos(angle)
    forward_y = math.sin(angle)

    right_x = -math.sin(angle)
    right_y = math.cos(angle)

    # Split velocity
    forward_speed = vx * forward_x + vy * forward_y
    side_speed = vx * right_x + vy * right_y

    # -----------------------
    # Engine
    # -----------------------
    forward_speed += throttle * dt

    # Forward drag
    forward_speed *= 0.99

    # Grip
    if handbrake:
        side_speed *= 0.995
        forward_speed *= 0.985
        turn_rate = 0.045
    else:
        side_speed *= 0.75
        turn_rate = 0.02

    # Steering
    if abs(forward_speed) > 0.1:
        angle += steering * forward_speed * turn_rate * dt

    # Rebuild velocity
    vx = forward_x * forward_speed + right_x * side_speed
    vy = forward_y * forward_speed + right_y * side_speed

    # Move
    x += vx * dt
    y += vy * dt

    # Wrap around screen
    if x < 0:
        x = WIDTH
    elif x > WIDTH:
        x = 0

    if y < 0:
        y = HEIGHT
    elif y > HEIGHT:
        y = 0

    # -----------------------
    # Draw
    # -----------------------
    screen.fill((50, 130, 50))
    pygame.draw.rect(screen, (70, 70, 70), (80, 80, 840, 540))

    car = pygame.Surface((60, 30), pygame.SRCALPHA)

    # Body
    pygame.draw.rect(car, (40, 120, 255), (8, 4, 44, 22), border_radius=5)

    # Roof
    pygame.draw.rect(car, (170, 220, 255), (18, 6, 24, 16), border_radius=3)

    # Wheels
    wheel = (20, 20, 20)
    pygame.draw.rect(car, wheel, (2, 2, 6, 8))
    pygame.draw.rect(car, wheel, (52, 2, 6, 8))
    pygame.draw.rect(car, wheel, (2, 20, 6, 8))
    pygame.draw.rect(car, wheel, (52, 20, 6, 8))

    # Headlights
    pygame.draw.circle(car, (255, 255, 150), (56, 8), 2)
    pygame.draw.circle(car, (255, 255, 150), (56, 22), 2)

    # Tail lights
    pygame.draw.circle(car, (255, 50, 50), (4, 8), 2)
    pygame.draw.circle(car, (255, 50, 50), (4, 22), 2)

    rotated = pygame.transform.rotate(car, -math.degrees(angle))
    rect = rotated.get_rect(center=(x, y))
    screen.blit(rotated, rect)

    font = pygame.font.SysFont(None, 80)

    if handbrake:
        text = font.render("DRIFTING", True, (255, 220, 0))
        screen.blit(text, (20, 20))

    pygame.display.flip()

pygame.quit()

