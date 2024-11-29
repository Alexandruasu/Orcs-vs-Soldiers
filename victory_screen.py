import pygame

def display_victory_screen(screen, winner, width, height):
    """
    Displays the victory screen with the corresponding image and modernized text.
    """
    if winner == "Orcs":
        image_path = "assets/Orcs_Win.png"
        victory_message = "ORCS WIN!"
    else:
        image_path = "assets/Soldiers_Win.png"
        victory_message = "SOLDIERS WIN!"

    # Load the corresponding image
    victory_image = pygame.image.load(image_path).convert_alpha()
    victory_image = pygame.transform.scale(victory_image, (width, height))

    # Use a modern font available in the system
    font = pygame.font.SysFont("Segoe UI", 60)  # You can also try "Calibri", "Arial", etc.

    # Victory text
    text_surface = font.render(victory_message, True, (255, 255, 255))  # White text
    shadow_surface = font.render(victory_message, True, (0, 0, 0))  # Black shadow

    # Text position
    text_rect = text_surface.get_rect(center=(width // 2, height // 4))
    shadow_rect = shadow_surface.get_rect(center=(width // 2 + 2, height // 4 + 2))  # Offset for shadow

    # Draw the background and text with shadow
    screen.blit(victory_image, (0, 0))  # Background
    screen.blit(shadow_surface, shadow_rect.topleft)  # Shadow
    screen.blit(text_surface, text_rect.topleft)  # Main text

    # Update the screen
    pygame.display.flip()
    pygame.time.wait(3000)  # Keep the screen for 3 seconds
