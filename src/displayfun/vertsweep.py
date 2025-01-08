import pygame
import sys

# Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480  # Adjust to your screen resolution
LINE_COLOR = (0, 255, 255)  # Cyan color
SCROLL_SPEED = 2  # Pixels per frame
GLOW_INTENSITY = 5  # Number of layers for the glow effect
GLOW_SPREAD = 20  # Pixel spread of the glow

def draw_glowing_line(surface, y_position):
    """Draws a horizontal line with a diffuse glow effect."""
    for i in range(GLOW_INTENSITY):
        alpha = 255 - (i * (255 // GLOW_INTENSITY))
        glow_color = (*LINE_COLOR, alpha)
        thickness = GLOW_SPREAD - (i * (GLOW_SPREAD // GLOW_INTENSITY))

        # Create a translucent surface for the glow layer
        glow_surface = pygame.Surface((SCREEN_WIDTH, thickness), pygame.SRCALPHA)
        pygame.draw.line(glow_surface, glow_color, (0, thickness // 2), (SCREEN_WIDTH, thickness // 2), thickness)

        # Blit the glow surface onto the main surface
        surface.blit(glow_surface, (0, y_position - (thickness // 2)))

    # Draw the main solid line
    pygame.draw.line(surface, LINE_COLOR, (0, y_position), (SCREEN_WIDTH, y_position), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    y_position = 0
    direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill((0, 0, 0))

        # Calculate new position
        y_position += SCROLL_SPEED * direction
        if y_position <= 0 or y_position >= SCREEN_HEIGHT:
            direction *= -1

        # Draw the glowing line
        draw_glowing_line(screen, y_position)

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 frames per second

if __name__ == "__main__":
    main()
