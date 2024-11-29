import pygame

def draw_stylized_button(
    window, x, y, width, height, text, font, top_color, bottom_color, border_color, hover=False
):
    """
    Draws a modern button with gradient, shadow, elegant text, and hover effects.
    :param window: The surface where we draw.
    :param x, y: Button coordinates.
    :param width, height: Button dimensions.
    :param text: Text displayed on the button.
    :param font: Font used for the text.
    :param top_color: Top color (gradient).
    :param bottom_color: Bottom color (gradient).
    :param border_color: Border color.
    :param hover: Indicates if the mouse is hovering over the button.
    """
    # Hover effect: slightly larger button
    if hover:
        x -= 2
        y -= 2
        width += 4
        height += 4

    # Shadow under the button
    shadow_rect = pygame.Rect(x + 4, y + 4, width, height)
    pygame.draw.rect(window, (50, 50, 50), shadow_rect, border_radius=12)

    # Background gradient
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(height):
        blend_ratio = i / height
        r = int(top_color[0] * (1 - blend_ratio) + bottom_color[0] * blend_ratio)
        g = int(top_color[1] * (1 - blend_ratio) + bottom_color[1] * blend_ratio)
        b = int(top_color[2] * (1 - blend_ratio) + bottom_color[2] * blend_ratio)
        pygame.draw.line(gradient_surface, (r, g, b), (0, i), (width, i))

    # Draw button
    pygame.draw.rect(window, border_color, (x - 2, y - 2, width + 4, height + 4), border_radius=15)  # Border
    window.blit(gradient_surface, (x, y))

    # Add glossy (shiny) effect
    glossy_rect = pygame.Rect(x, y, width, height // 2)
    glossy_surface = pygame.Surface((width, height // 2), pygame.SRCALPHA)
    glossy_surface.fill((255, 255, 255, 60))  # Translucent white
    pygame.draw.ellipse(glossy_surface, (255, 255, 255, 100), glossy_rect)
    window.blit(glossy_surface, (x, y))

    # Elegant text with shadow
    text_surface = font.render(text, True, (255, 255, 255))  # White text
    text_shadow = font.render(text, True, (0, 0, 0))  # Black text for shadow
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    shadow_rect = text_shadow.get_rect(center=(x + width // 2 + 2, y + height // 2 + 2))  # Offset shadow

    window.blit(text_shadow, shadow_rect.topleft)  # Shadow
    window.blit(text_surface, text_rect.topleft)  # Text
