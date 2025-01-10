import pygame
import sys

# Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480  # Adjust to your screen resolution
LINE_COLOR = (0, 255, 255)  # Cyan color
LINE_THICKNESS = 5
GLOW_HEIGHT = 100  # Total height of the glow effect
SCROLL_SPEED = 2  # Pixels per frame

def create_glow_surface(line_width, glow_height, color):
    """
    Creates a surface with a vertical gradient to simulate glow.
    """
    glow_surface = pygame.Surface((line_width, glow_height), pygame.SRCALPHA)
    for y in range(glow_height):
        # Calculate alpha based on distance from the center
        distance = abs(y - glow_height // 2)
        alpha = max(0, 255 - (distance * (255 // (glow_height // 2))))
        glow_color = (*color, alpha)
        pygame.draw.line(glow_surface, glow_color, (0, y), (line_width, y))
    return glow_surface

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Cinematic Glowing Line")
    clock = pygame.time.Clock()
    y_position = 0
    direction = 1

    # Create the main line surface
    line_surface = pygame.Surface((SCREEN_WIDTH, LINE_THICKNESS), pygame.SRCALPHA)
    pygame.draw.line(line_surface, LINE_COLOR, (0, 0), (SCREEN_WIDTH, 0), LINE_THICKNESS)

    # Create the glow surface
    glow_surface = create_glow_surface(SCREEN_WIDTH, GLOW_HEIGHT, LINE_COLOR)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Exit on ESC key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill((0, 0, 0))

        # Update the line position
        y_position += SCROLL_SPEED * direction
        if y_position <= 0 or y_position >= SCREEN_HEIGHT - LINE_THICKNESS:
            direction *= -1

        # Calculate the top position for the glow
        glow_top = y_position - (GLOW_HEIGHT // 2) + (LINE_THICKNESS // 2)

        # Blit the glow surface with additive blending
        screen.blit(glow_surface, (0, glow_top), special_flags=pygame.BLEND_ADD)

        # Blit the main line
        screen.blit(line_surface, (0, y_position))

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 frames per second

if __name__ == "__main__":
    main()
