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
        color = random.choice([(255, 0, 0), (255, 255, 0), (255, 165, 0), (139, 69, 19)])  # Red, Yellow, Orange, SaddleBrown
        speed = random.randint(1, 3)
        stars.append({"x": x, "y": y, "color": color, "speed": speed})
    return stars


def move_stars(stars, screen_width, screen_height):
    """
    It moves the stars and resets them when they leave the screen.
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
    Brings up a selection screen to choose the number of orcs and soldiers.
    """
    width, height = screen.get_size()

    font = pygame.font.SysFont("Arial", 30)
    small_font = pygame.font.SysFont("Arial", 24)

    background_colors = [(0, 128, 0), (210, 105, 30)] 
    text_color = (255, 255, 255)

    orc_image = pygame.image.load("assets/Orc-Idle.png").convert_alpha()
    soldier_image = pygame.image.load("assets/Soldier-Idle.png").convert_alpha()

    orc_image = pygame.transform.scale(orc_image, (120, 100))
    soldier_image = pygame.transform.scale(soldier_image, (100, 100))

    orc_count = 10
    soldier_count = 10

    stars = generate_stars(100, width, height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Increase/decrease orcs
                if orc_minus_rect.collidepoint(mouse_pos) and orc_count > 1:
                    orc_count -= 1
                if orc_plus_rect.collidepoint(mouse_pos) and orc_count < 50:
                    orc_count += 1

                # Increase/decrease soldiers
                if soldier_minus_rect.collidepoint(mouse_pos) and soldier_count > 1:
                    soldier_count -= 1
                if soldier_plus_rect.collidepoint(mouse_pos) and soldier_count < 50:
                    soldier_count += 1

                # Start Button
                if start_button_rect.collidepoint(mouse_pos):
                    return orc_count, soldier_count

        draw_gradient(screen, background_colors)

        move_stars(stars, width, height)

        for star in stars:
            pygame.draw.circle(screen, star["color"], (star["x"], star["y"]), 2)

        orc_text = font.render(f"Orcs: {orc_count}", True, text_color)
        soldier_text = font.render(f"Soldiers: {soldier_count}", True, text_color)

        orc_text_rect = orc_text.get_rect(center=(width // 4, height // 2 - 50))
        soldier_text_rect = soldier_text.get_rect(center=(3 * width // 4, height // 2 - 50))

        screen.blit(orc_image, (width // 4 - 50, height // 2 - 180))
        screen.blit(orc_text, orc_text_rect)
        screen.blit(soldier_image, (3 * width // 4 - 50, height // 2 - 180))
        screen.blit(soldier_text, soldier_text_rect)

        # orc button
        orc_minus_rect = pygame.Rect(width // 4 - 75, height // 2 + 20, 50, 30)
        orc_plus_rect = pygame.Rect(width // 4 + 25, height // 2 + 20, 50, 30)
        draw_stylized_button(
            screen, orc_minus_rect, "-", small_font,
            ((50, 150, 50), (30, 100, 30)), ((100, 200, 100), (50, 150, 50)),
            orc_minus_rect.collidepoint(pygame.mouse.get_pos())
        )
        draw_stylized_button(
            screen, orc_plus_rect, "+", small_font,
            ((50, 150, 50), (30, 100, 30)), ((100, 200, 100), (50, 150, 50)),
            orc_plus_rect.collidepoint(pygame.mouse.get_pos())
        )

        # soldier button
        soldier_minus_rect = pygame.Rect(3 * width // 4 - 75, height // 2 + 20, 50, 30)
        soldier_plus_rect = pygame.Rect(3 * width // 4 + 25, height // 2 + 20, 50, 30)
        draw_stylized_button(
            screen, soldier_minus_rect, "-", small_font,
            ((50, 150, 50), (30, 100, 30)), ((100, 200, 100), (50, 150, 50)),
            soldier_minus_rect.collidepoint(pygame.mouse.get_pos())
        )
        draw_stylized_button(
            screen, soldier_plus_rect, "+", small_font,
            ((50, 150, 50), (30, 100, 30)), ((100, 200, 100), (50, 150, 50)),
            soldier_plus_rect.collidepoint(pygame.mouse.get_pos())
        )

        # Start button
        start_button_rect = pygame.Rect(width // 2 - 100, height - 100, 200, 50)
        draw_stylized_button(
            screen, start_button_rect, "START", font,
              ((210, 105, 30), (139, 69, 19)), ((255, 140, 0), (160, 82, 45)),
            start_button_rect.collidepoint(pygame.mouse.get_pos())
        )

        pygame.display.flip()
