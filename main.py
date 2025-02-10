import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from sprites import load_sprite
from entities import Character, Wizard
from battle import battle
from start_screen import start_screen
from victory_screen import display_victory_screen
from selection_screen import selection_screen
from button import SpeedUpButton
from minimap import draw_minimap
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Orcs vs Soldiers")
clock = pygame.time.Clock()

# Load resources
background = pygame.image.load("assets/terrain.png").convert()
orc_walk_frames = load_sprite("assets/Orc-Walk.png", 100, 100)
orc_attack_frames = load_sprite("assets/Orc-Attack01.png", 100, 100)
orc_death_frames = load_sprite("assets/Orc-Death.png", 100, 100)
soldier_walk_frames = load_sprite("assets/Soldier-Walk.png", 100, 100)
soldier_attack_frames = load_sprite("assets/Soldier-Attack01.png", 100, 100)
soldier_death_frames = load_sprite("assets/Soldier-Death.png", 100, 100)
wizard_idle_frames = load_sprite("assets/Wizard-Idle.png", 100, 100)
wizard_walk_frames = load_sprite("assets/Wizard-Walk.png", 100, 100)
wizard_attack_frames = load_sprite("assets/Wizard-Attack01.png", 100, 100)
wizard_effect_frames = load_sprite("assets/Wizard-Attack01_Effect.png", 100, 100)
wizard_death_frames = load_sprite("assets/Wizard-DEATH.png", 100, 100)

# Start screen
start_screen(screen)

# Selection screen
orc_count, soldier_count, wizard_count = selection_screen(screen)

# Create characters
orcs = [Character(100, random.randint(50, SCREEN_HEIGHT - 150), 100, 25,
                  orc_walk_frames, orc_attack_frames, orc_death_frames)
        for _ in range(orc_count)]
soldiers = [Character(600, random.randint(50, SCREEN_HEIGHT - 150), 100, 25,
                      soldier_walk_frames, soldier_attack_frames, soldier_death_frames)
            for _ in range(soldier_count)]
wizards = [Wizard(700, random.randint(50, SCREEN_HEIGHT - 150), 100, 30,
                  wizard_walk_frames, wizard_attack_frames, wizard_effect_frames, wizard_idle_frames, wizard_death_frames)
           for _ in range(wizard_count)]

# Initialize Speed Up button
speed_button = SpeedUpButton(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80, 60, 60, "assets/speed_up_button.png")

# Normal and fast FPS
normal_fps = FPS
fast_fps = 60

# Initialize modern font and colors
font = pygame.font.SysFont("Segoe UI", 20, bold=True)
orc_color = (200, 50, 50)       # Red for orcs
soldier_color = (50, 150, 50)   # Green for soldiers
wizard_color = (50, 50, 200)    # Blue for wizards

# Function to draw text with shadow
def draw_text_with_shadow(screen, text, font, color, shadow_color, position):
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)
    x, y = position
    screen.blit(shadow_surface, (x + 2, y + 2))  # Shadow offset
    screen.blit(text_surface, (x, y))            # Main text

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle events for the Speed Up button
        speed_button.handle_event(event)

    # Check victory conditions
    if all(orc.is_dead for orc in orcs):
        display_victory_screen(screen, "Soldiers", SCREEN_WIDTH, SCREEN_HEIGHT)
        running = False
    elif all(soldier.is_dead for soldier in soldiers) and all(wizard.is_dead for wizard in wizards):
        display_victory_screen(screen, "Orcs", SCREEN_WIDTH, SCREEN_HEIGHT)
        running = False

    # Battle logic
    battle(orcs, soldiers, wizards, screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Update characters
    for orc in orcs:
        orc.update()
    for soldier in soldiers:
        soldier.update()
    for wizard in wizards:
        wizard.update()

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw the wizard projectiles
    for wizard in wizards:
        wizard.update_projectiles(screen)

    # Draw the characters
    for orc in orcs:
        orc.draw(screen)
    for soldier in soldiers:
        soldier.draw(screen)
    for wizard in wizards:
        wizard.draw(screen)

    # Calculate the number of alive troops
    alive_orcs = sum(1 for orc in orcs if orc.is_alive())
    alive_soldiers = sum(1 for soldier in soldiers if soldier.is_alive())
    alive_wizards = sum(1 for wizard in wizards if wizard.is_alive())

    # Orcs (top left)
    draw_text_with_shadow(screen, f"Orcs: {alive_orcs}", font, orc_color, (0, 0, 0), (20, 20))

    # Soldiers and Wizards (top right, aligned on the same line)
    soldier_text = f"Soldiers: {alive_soldiers}"
    wizard_text = f"Wizards: {alive_wizards}"

    total_width = font.size(soldier_text)[0] + font.size(wizard_text)[0] + 20
    start_x = SCREEN_WIDTH - total_width - 20

    draw_text_with_shadow(screen, soldier_text, font, soldier_color, (0, 0, 0), (start_x, 20))
    draw_text_with_shadow(screen, wizard_text, font, wizard_color, (0, 0, 0), (start_x + font.size(soldier_text)[0] + 20, 20))

    # Draw mini-map with terrain in the bottom left corner
    draw_minimap(screen, orcs, soldiers, wizards, SCREEN_WIDTH, SCREEN_HEIGHT, background)

    # Draw Speed Up button
    speed_button.draw(screen)

    # Update the screen
    pygame.display.flip()

    # Set game speed based on button state
    if speed_button.is_active():
        clock.tick(fast_fps)  # Fast speed
    else:
        clock.tick(normal_fps)  # Normal speed

# Quit pygame
pygame.quit()
