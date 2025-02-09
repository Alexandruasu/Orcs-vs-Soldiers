import pygame
import random
import pygame.gfxdraw


def draw_gradient(screen, colors):
    """
    Draw a vertical gradient on the background.
    """
    width, height = screen.get_size()
    for y in range(height):
        ratio = y / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))


def generate_stars(num_stars, screen_width, screen_height):
    """
    Generate a list of stars with random positions and colors.
    """
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        color = random.choice([(255, 0, 0), (255, 255, 0), (255, 165, 0), (139, 69, 19)])
        speed = random.randint(1, 3)
        stars.append({"x": x, "y": y, "color": color, "speed": speed})
    return stars


def move_stars(stars, screen_width, screen_height):
    """
    Move the stars and reset them when they leave the screen.
    """
    for star in stars:
        star["y"] += star["speed"]
        if star["y"] > screen_height:
            star["y"] = 0
            star["x"] = random.randint(0, screen_width)
            star["color"] = random.choice([(255, 0, 0), (255, 255, 0), (255, 165, 0), (139, 69, 19)])


def draw_stylized_button(screen, rect, text, font, colors, hover_colors, is_hovered):
    """
    Draw a stylized button with gradient and centered text.
    """
    top_color, bottom_color = hover_colors if is_hovered else colors

    for y in range(rect.height):
        ratio = y / rect.height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))

    pygame.gfxdraw.rectangle(screen, rect, (255, 255, 255))

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def selection_screen(screen):
    """
    Display the selection screen to choose the number of orcs, soldiers, and wizards.
    """
    width, height = screen.get_size()

    font = pygame.font.SysFont("Arial", 30)
    small_font = pygame.font.SysFont("Arial", 24)

    background_colors = [(0, 128, 0), (210, 105, 30)]
    text_color = (255, 255, 255)

    # Load character images
    orc_image = pygame.image.load("assets/Orc-Idle.png").convert_alpha()
    soldier_image = pygame.image.load("assets/Soldier-Idle.png").convert_alpha()
    wizard_image = pygame.image.load("assets/Wizard-Idle.png").convert_alpha()

    orc_image = pygame.transform.scale(orc_image, (120, 100))
    soldier_image = pygame.transform.scale(soldier_image, (100, 100))
    wizard_image = pygame.transform.scale(wizard_image, (100, 100))

    # Default counts for characters
    orc_count = 10
    soldier_count = 10
    wizard_count = 5

    # Generate background stars
    stars = generate_stars(100, width, height)

    # Variables for long-press behavior
    holding_button = None
    hold_start_time = 0
    initial_hold_delay = 300  # 0.3 seconds before auto-increment starts
    repeat_interval = 100     # Increment every 0.1 seconds after holding
    last_increment_time = 0   # Last time a count was incremented

    clock = pygame.time.Clock()  # Ensure constant frame rate

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check which button was clicked and set variables accordingly
                if orc_minus_rect.collidepoint(mouse_pos):
                    orc_count = max(1, orc_count - 1)  # Decrease instantly on short click
                    holding_button = 'orc_minus'
                    hold_start_time = pygame.time.get_ticks()
                elif orc_plus_rect.collidepoint(mouse_pos):
                    orc_count = min(50, orc_count + 1)  # Increase instantly on short click
                    holding_button = 'orc_plus'
                    hold_start_time = pygame.time.get_ticks()
                elif soldier_minus_rect.collidepoint(mouse_pos):
                    soldier_count = max(1, soldier_count - 1)
                    holding_button = 'soldier_minus'
                    hold_start_time = pygame.time.get_ticks()
                elif soldier_plus_rect.collidepoint(mouse_pos):
                    soldier_count = min(50, soldier_count + 1)
                    holding_button = 'soldier_plus'
                    hold_start_time = pygame.time.get_ticks()
                elif wizard_minus_rect.collidepoint(mouse_pos):
                    wizard_count = max(1, wizard_count - 1)
                    holding_button = 'wizard_minus'
                    hold_start_time = pygame.time.get_ticks()
                elif wizard_plus_rect.collidepoint(mouse_pos):
                    wizard_count = min(10, wizard_count + 1)
                    holding_button = 'wizard_plus'
                    hold_start_time = pygame.time.get_ticks()
                elif start_button_rect.collidepoint(mouse_pos):
                    return orc_count, soldier_count, wizard_count

            if event.type == pygame.MOUSEBUTTONUP:
                holding_button = None  # Stop auto-increment when mouse is released

        # Logic for smooth long-press increment
        if holding_button:
            current_time = pygame.time.get_ticks()

            # Start incrementing after the initial delay
            if current_time - hold_start_time > initial_hold_delay:
                if current_time - last_increment_time > repeat_interval:
                    if holding_button == 'orc_minus' and orc_count > 1:
                        orc_count -= 1
                    elif holding_button == 'orc_plus' and orc_count < 50:
                        orc_count += 1
                    elif holding_button == 'soldier_minus' and soldier_count > 1:
                        soldier_count -= 1
                    elif holding_button == 'soldier_plus' and soldier_count < 50:
                        soldier_count += 1
                    elif holding_button == 'wizard_minus' and wizard_count > 1:
                        wizard_count -= 1
                    elif holding_button == 'wizard_plus' and wizard_count < 10:
                        wizard_count += 1

                    last_increment_time = current_time  # Update last increment time

        # Draw the background gradient
        draw_gradient(screen, background_colors)

        # Move and draw background stars
        move_stars(stars, width, height)
        for star in stars:
            pygame.draw.circle(screen, star["color"], (star["x"], star["y"]), 2)

        # Display Orc count and image
        orc_text = font.render(f"Orcs: {orc_count}", True, text_color)
        orc_text_rect = orc_text.get_rect(center=(width // 4, height // 2 - 50))
        screen.blit(orc_image, (width // 4 - 50, height // 2 - 180))
        screen.blit(orc_text, orc_text_rect)

        # Orc buttons
        orc_minus_rect = pygame.Rect(width // 4 - 75, height // 2 + 20, 50, 30)
        orc_plus_rect = pygame.Rect(width // 4 + 25, height // 2 + 20, 50, 30)
        draw_stylized_button(screen, orc_minus_rect, "-", small_font, ((50, 150, 50), (30, 100, 30)),
                             ((100, 200, 100), (50, 150, 50)), orc_minus_rect.collidepoint(pygame.mouse.get_pos()))
        draw_stylized_button(screen, orc_plus_rect, "+", small_font, ((50, 150, 50), (30, 100, 30)),
                             ((100, 200, 100), (50, 150, 50)), orc_plus_rect.collidepoint(pygame.mouse.get_pos()))

        # Display Soldier count and image
        soldier_text = font.render(f"Soldiers: {soldier_count}", True, text_color)
        soldier_text_rect = soldier_text.get_rect(center=(3 * width // 4, height // 2 - 50))
        screen.blit(soldier_image, (3 * width // 4 - 50, height // 2 - 180))
        screen.blit(soldier_text, soldier_text_rect)

        # Soldier buttons
        soldier_minus_rect = pygame.Rect(3 * width // 4 - 75, height // 2 + 20, 50, 30)
        soldier_plus_rect = pygame.Rect(3 * width // 4 + 25, height // 2 + 20, 50, 30)
        draw_stylized_button(screen, soldier_minus_rect, "-", small_font, ((50, 150, 50), (30, 100, 30)),
                             ((100, 200, 100), (50, 150, 50)), soldier_minus_rect.collidepoint(pygame.mouse.get_pos()))
        draw_stylized_button(screen, soldier_plus_rect, "+", small_font, ((50, 150, 50), (30, 100, 30)),
                             ((100, 200, 100), (50, 150, 50)), soldier_plus_rect.collidepoint(pygame.mouse.get_pos()))

        # Display Wizard count and image
        wizard_text = font.render(f"Wizards: {wizard_count}", True, text_color)
        wizard_text_rect = wizard_text.get_rect(center=(width // 2, height // 2 + 100))
        screen.blit(wizard_image, (width // 2 - 50, height // 2))
        screen.blit(wizard_text, wizard_text_rect)

        # Wizard buttons
        wizard_minus_rect = pygame.Rect(width // 2 - 75, height // 2 + 160, 50, 30)
        wizard_plus_rect = pygame.Rect(width // 2 + 25, height // 2 + 160, 50, 30)
        draw_stylized_button(screen, wizard_minus_rect, "-", small_font, ((50, 150, 50), (30, 100, 30)),
                             ((100, 200, 100), (50, 150, 50)), wizard_minus_rect.collidepoint(pygame.mouse.get_pos()))
        draw_stylized_button(screen, wizard_plus_rect, "+", small_font, ((50, 150, 50), (30, 100, 30)),
                             ((100, 200, 100), (50, 150, 50)), wizard_plus_rect.collidepoint(pygame.mouse.get_pos()))

        # Start button to begin the game
        start_button_rect = pygame.Rect(width // 2 - 100, height - 100, 200, 50)
        draw_stylized_button(screen, start_button_rect, "START", font, ((210, 105, 30), (139, 69, 19)),
                             ((255, 140, 0), (160, 82, 45)), start_button_rect.collidepoint(pygame.mouse.get_pos()))

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Ensure a constant frame rate for smooth performance