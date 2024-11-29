import pygame
import time
from stylized_button import draw_stylized_button  # Import the button function

def start_screen(screen):
    """
    Displays the start screen with a static image and a stylized button 
    that appears after 5 seconds.
    :param screen: Main pygame surface.
    """
    # Configuration
    width, height = screen.get_size()
    start_image = pygame.image.load("assets/start.png").convert()
    start_image = pygame.transform.scale(start_image, (width, height))
    button_font = pygame.font.SysFont("Arial", 40)

    # Start time
    start_time = time.time()
    button_visible = False

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_visible:
                # Detect button click
                mouse_pos = pygame.mouse.get_pos()
                button_x, button_y = width // 2 - 100, height // 2
                button_width, button_height = 200, 80
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    return  # Start the game

        # Draw background
        screen.blit(start_image, (0, 0))

        # After 1 second, display the button
        if time.time() - start_time > 1:
            button_visible = True
            # Draw the START button
            button_x, button_y = width // 2 - 100, height // 2
            button_width, button_height = 200, 80
            draw_stylized_button(
                screen,
                button_x,
                button_y,
                button_width,
                button_height,
                "START",
                button_font,
                (255, 165, 0),  # Orange (gradient top)
                (139, 69, 19),  # Brown (gradient bottom)
                (255, 140, 0)  # Orange border
            )

        # Detect hover for the button
        mouse_pos = pygame.mouse.get_pos()
        if button_visible and button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
            draw_stylized_button(
                screen,
                button_x,
                button_y,
                button_width,
                button_height,
                "START",
                button_font,
                (255, 200, 100),  # Hover effect (light orange)
                (205, 92, 92),  # Reddish brown
                (255, 255, 0)  # Yellow border
            )

        # Update the screen
        pygame.display.flip()
