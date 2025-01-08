import pygame
import sys
import math

# Configuration
FPS = 60
LINE_COLOR = (0, 255, 255)  # Cyan
LINE_THICKNESS = 10
GLOW_INTENSITY = 100
SCROLL_SPEED = 200  # Pixels per second

def main():
    pygame.init()

    # Get screen dimensions
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    # Create fullscreen display
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Glowing Line Animation")

    clock = pygame.time.Clock()

    # Line position variables
    line_y = screen_height // 2
    direction = 1  # 1 for down, -1 for up

    # Animation loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw the glowing line effect
        for glow_offset in range(1, GLOW_INTENSITY // 10 + 1):
            glow_alpha = max(0, 255 - glow_offset * 10)
            pygame.draw.line(
                screen,
                (LINE_COLOR[0], LINE_COLOR[1], LINE_COLOR[2], glow_alpha),
                (0, line_y),
                (screen_width, line_y),
                LINE_THICKNESS + glow_offset * 2,
            )

        # Draw the main line
        pygame.draw.line(screen, LINE_COLOR, (0, line_y), (screen_width, line_y), LINE_THICKNESS)

        # Update line position
        line_y += direction * SCROLL_SPEED * clock.get_time() / 1000
        if line_y <= 0 or line_y >= screen_height:
            direction *= -1

        # Refresh display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
