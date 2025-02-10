import pygame

# Settings for the mini-map
def init_minimap(screen_width, screen_height):
    MINIMAP_WIDTH = 150
    MINIMAP_HEIGHT = 100
    MINIMAP_MARGIN = 20
    MINIMAP_X = MINIMAP_MARGIN
    MINIMAP_Y = screen_height - MINIMAP_HEIGHT - MINIMAP_MARGIN
    return MINIMAP_WIDTH, MINIMAP_HEIGHT, MINIMAP_X, MINIMAP_Y

def draw_minimap(screen, orcs, soldiers, wizards, screen_width, screen_height, terrain_image):
    """Draws the mini-map with terrain.png background and a modern premium look."""
    
    MINIMAP_WIDTH, MINIMAP_HEIGHT, MINIMAP_X, MINIMAP_Y = init_minimap(screen_width, screen_height)

    # Mini-map background with shadow effect (border gradient)
    shadow_rect = pygame.Rect(MINIMAP_X + 5, MINIMAP_Y + 5, MINIMAP_WIDTH, MINIMAP_HEIGHT)
    pygame.draw.rect(screen, (0, 0, 0, 180), shadow_rect, border_radius=10)

    # Scaled terrain.png background for mini-map
    terrain_mini = pygame.transform.scale(terrain_image, (MINIMAP_WIDTH, MINIMAP_HEIGHT))
    screen.blit(terrain_mini, (MINIMAP_X, MINIMAP_Y))

    # Mini-map border for premium effect
    pygame.draw.rect(screen, (120, 120, 120), (MINIMAP_X, MINIMAP_Y, MINIMAP_WIDTH, MINIMAP_HEIGHT), 3, border_radius=12)

    # Mini-map title above the map with shadow
    font = pygame.font.SysFont("Segoe UI", 16, bold=True)
    title_text = font.render("Minimap", True, (255, 255, 255))
    shadow_text = font.render("Minimap", True, (0, 0, 0))
    
    title_rect = title_text.get_rect(center=(MINIMAP_X + MINIMAP_WIDTH // 2, MINIMAP_Y - 10))
    shadow_rect = shadow_text.get_rect(center=(MINIMAP_X + MINIMAP_WIDTH // 2 + 2, MINIMAP_Y - 8))
    
    screen.blit(shadow_text, shadow_rect.topleft)
    screen.blit(title_text, title_rect.topleft)

    # Scaling factors for unit positions
    scale_x = MINIMAP_WIDTH / screen_width
    scale_y = MINIMAP_HEIGHT / screen_height

    # Draw dots for each type of unit with shadow
    for orc in orcs:
        if orc.is_alive():
            orc_x = MINIMAP_X + int(orc.x * scale_x)
            orc_y = MINIMAP_Y + int(orc.y * scale_y)
            pygame.draw.circle(screen, (0, 0, 0), (orc_x + 1, orc_y + 1), 5)  # Black shadow
            pygame.draw.circle(screen, (34, 139, 34), (orc_x, orc_y), 4)      # Dark green for orcs

    for soldier in soldiers:
        if soldier.is_alive():
            soldier_x = MINIMAP_X + int(soldier.x * scale_x)
            soldier_y = MINIMAP_Y + int(soldier.y * scale_y)
            pygame.draw.circle(screen, (0, 0, 0), (soldier_x + 1, soldier_y + 1), 5)  # Black shadow
            pygame.draw.circle(screen, (169, 169, 169), (soldier_x, soldier_y), 4)    # Gray for soldiers

    for wizard in wizards:
        if wizard.is_alive():
            wizard_x = MINIMAP_X + int(wizard.x * scale_x)
            wizard_y = MINIMAP_Y + int(wizard.y * scale_y)
            pygame.draw.circle(screen, (0, 0, 0), (wizard_x + 1, wizard_y + 1), 5)  # Black shadow
            pygame.draw.circle(screen, (50, 50, 200), (wizard_x, wizard_y), 4)     # Blue for wizards
