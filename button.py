import pygame

class SpeedUpButton:
    def __init__(self, x, y, width, height, icon_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False  # Button state: active/inactive
        self.icon = pygame.image.load(icon_path).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (width - 10, height - 10))  # Resized icon
        self.font = pygame.font.SysFont("Arial", 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = not self.active  # Toggle button state

    def draw(self, screen):
        # Visual effect: color and pressed effect
        if self.active:
            button_color = (50, 50, 50)  # Darker color when active
            offset = 2  # Button appears pressed down
        else:
            button_color = (100, 100, 100)  # Normal color
            offset = 0

        # Draw a shadow under the button for a 3D effect
        shadow_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=8)

        # Draw the button with a pressed effect
        pygame.draw.rect(screen, button_color, 
                         (self.rect.x, self.rect.y + offset, self.rect.width, self.rect.height), 
                         border_radius=8)

        # Draw the icon in the center of the button
        icon_rect = self.icon.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
        screen.blit(self.icon, icon_rect)

    def is_active(self):
        return self.active
