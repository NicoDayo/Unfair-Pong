import pygame, sys, random
from titlescreen import title_screen

pygame.init()

WIDTH, HEIGHT = 800, 600
FONT = pygame.font.Font("./font/pixel.ttf", int(WIDTH / 20))
SMALL_FONT = pygame.font.Font("./font/pixel.ttf", int(WIDTH / 30))
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Unfair Pong")
CLOCK = pygame.time.Clock()

player_score, opponent_score = 0, 0
player = pygame.Rect(WIDTH - 110, HEIGHT / 2 - 50, 10, 100)
opponent = pygame.Rect(110, HEIGHT / 2 - 50, 10, 100)
ball_size = 20
ball = pygame.Rect(WIDTH / 2 - ball_size / 2, HEIGHT / 2 - ball_size / 2, ball_size, ball_size)
x_vel, y_vel = 1, 1
opponent_speed = random.randrange(10, 20)
hit_sound = pygame.mixer.Sound("./sounds/hit.mp3")

random_event_timer = 0
random_event_interval = 1200
random_event_countdown = 5
random_event_active = False
random_event_announcement = False
event_start_time = 0
reversed_controls = False
reversed_controls_timer = 0
event_description = ""
event_display_timer = 0

def trigger_random_event():
    global ball_size, ball, x_vel, y_vel
    event_type = random.choice([
        "ball_speed_increase",
        "ball_shrink",
        "opponent_size_increase",
        "player_shrink",
        "reverse_controls",
        "score_penalty",
    ])

    if event_type == "ball_speed_increase":
        x_vel += random.choice([-1, 1])
        y_vel += random.choice([-1, 1])
        x_vel = max(2, abs(x_vel)) * (1 if x_vel > 0 else -1)
        y_vel = max(2, abs(y_vel)) * (1 if y_vel > 0 else -1)
        return "Ball speed increased"
    elif event_type == "ball_shrink":
        ball_size = max(10, ball_size - 5)
        ball.width, ball.height = ball_size, ball_size
        return "Ball shrunk!"
    elif event_type == "opponent_size_increase":
        opponent.height = min(300, opponent.height + 20)
        return "Opponent paddle grew"
    elif event_type == "player_shrink":
        player.height = max(20, player.height - 20)
        return "Player paddle shrunk"
    elif event_type == "reverse_controls":
        global reversed_controls
        reversed_controls = True
        return "Controls reversed"
    elif event_type == "score_penalty":
        global player_score
        player_score = max(0, player_score - 1)
        return "Player lost a point!"

title_screen(SCREEN, FONT, CLOCK)

while True:
    keys_pressed = pygame.key.get_pressed()
    if reversed_controls:
        if keys_pressed[pygame.K_LEFT]:
            if player.bottom < HEIGHT:
                player.bottom += 2
        if keys_pressed[pygame.K_RIGHT]:
            if player.top > 0:
                player.top -= 2
    else:
        if keys_pressed[pygame.K_LEFT]:
            if player.top > 0:
                player.top -= 2
        if keys_pressed[pygame.K_RIGHT]:
            if player.bottom < HEIGHT:
                player.bottom += 2

    SCREEN.fill("Black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if ball.y >= HEIGHT:
        y_vel = -1

    if ball.y <= 0:
        y_vel = 1

    if ball.x <= 0:
        player_score += 1
        ball.center = [WIDTH / 2, HEIGHT / 2]
        x_vel, y_vel = random.choice([1, -1]), random.choice([1, -1])
        pygame.time.wait(2000)

    if ball.x >= WIDTH:
        opponent_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_vel, y_vel = random.choice([1, -1]), random.choice([1, -1])
        pygame.time.wait(2000)

    if ball.colliderect(player) or ball.colliderect(opponent):
        x_vel = -x_vel
        hit_sound.play()

    ball.x += x_vel * 2
    ball.y += y_vel * 2

    if opponent.y < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    player_score_text = FONT.render(str(player_score), True, "white")
    opponent_score_text = FONT.render(str(opponent_score), True, "white")

    pygame.draw.rect(SCREEN, "white", player)
    pygame.draw.rect(SCREEN, "white", opponent)
    pygame.draw.ellipse(SCREEN, "White", ball)

    SCREEN.blit(player_score_text, (WIDTH / 2 + 50, 50))
    SCREEN.blit(opponent_score_text, (WIDTH / 2 - 50, 50))

    random_event_timer += 1
    if random_event_timer > random_event_interval:
        if not random_event_announcement and not random_event_active:
            random_event_announcement = True
            event_start_time = pygame.time.get_ticks()

    if random_event_announcement:
        announcement_text = SMALL_FONT.render("Random event occurring", True, "red")
        SCREEN.blit(announcement_text, (WIDTH / 2 - 200, HEIGHT / 2 - 50))

        countdown_elapsed = (pygame.time.get_ticks() - event_start_time) // 1000
        countdown_text = SMALL_FONT.render(f"Starting in {max(0, random_event_countdown - countdown_elapsed)}", True, "white")
        SCREEN.blit(countdown_text, (WIDTH / 2 - 100, HEIGHT / 2))

        if countdown_elapsed >= random_event_countdown:
            random_event_announcement = False
            random_event_active = True
            event_description = trigger_random_event()
            event_display_timer = pygame.time.get_ticks()

    if random_event_active:
        event_text = SMALL_FONT.render(event_description, True, "yellow")
        SCREEN.blit(event_text, (WIDTH / 2 - 150, HEIGHT / 2 + 50))
        if pygame.time.get_ticks() - event_display_timer > 2000:
            random_event_active = False
            random_event_timer = 0

    if reversed_controls:
        reversed_controls_timer += 1
        if reversed_controls_timer > 300:
            reversed_controls = False
            reversed_controls_timer = 0

    pygame.display.update()
    CLOCK.tick(250)
