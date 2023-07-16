import pygame

# Initialize Pygame and create a game window
pygame.init()
clock = pygame.time.Clock()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# Game variables
game_running = True
game_speed = 120  # Desired frame rate of the game (frames per second)
player_speed = 5  # Player movement speed (pixels per frame)
player_x = 0
player_y = 100
# Game loop
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Update game logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Render the game
    window.fill((0, 0, 0))  # Clear the screen
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(player_x, player_y, 100, 100))  # Example player object

    pygame.display.flip()  # Update the display

    clock.tick(game_speed)  # Control the frame rate

# Quit the game
pygame.quit()
