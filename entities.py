import pygame
import math

class Character:
    def __init__(self, x, y, health, damage, walk_frames, attack_frames, death_frames, direction=1):
        self.x = x
        self.y = y
        self.health = health  # Initial health (100)
        self.damage = damage  # Damage per attack (10)
        self.walk_frames = walk_frames
        self.attack_frames = attack_frames
        self.death_frames = death_frames
        self.frames = walk_frames  # Default to walking frames
        self.current_frame = 0
        self.image = walk_frames[0]
        self.direction_x = direction  # 1 = moving right, -1 = moving left
        self.direction_y = 0  # Vertical movement: -1 = up, 1 = down
        self.frame_delay = 5  # Delay for animation
        self.frame_counter = 0
        self.speed = 2  # Speed of movement
        self.is_dead = False  # True if character is dead
        self.death_timer = 0  # Time to keep the death animation
        self.attack_cooldown = 120  # Cooldown timer (2 seconds at 60 FPS)
        self.attack_timer = 0  # Timer to track when the character can attack next

    def take_damage(self, damage):
        """Reduce health and check for death."""
        if not self.is_dead:
            self.health -= damage
            if self.health <= 0:
                self.is_dead = True
                self.frames = self.death_frames  # Switch to death animation
                self.current_frame = 0  # Restart animation
                self.death_timer = len(self.death_frames) * self.frame_delay  # Play death animation fully

    def attack(self, target):
        """Attack another character once every cooldown period."""
        if self.attack_timer == 0 and not self.is_dead and abs(self.x - target.x) < 50 and abs(self.y - target.y) < 50:
            self.frames = self.attack_frames  # Switch to attack animation
            target.take_damage(self.damage)  # Apply damage to target
            self.attack_timer = self.attack_cooldown  # Reset the attack timer

    def move_towards(self, target, screen_width, screen_height):
        """Move towards the target while staying within screen bounds."""
        if not self.is_dead and not (abs(self.x - target.x) < 50 and abs(self.y - target.y) < 50):
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.hypot(dx, dy)

            if distance > 0:  # Avoid division by zero
                self.direction_x = 1 if dx > 0 else -1
                self.direction_y = 1 if dy > 0 else -1 if dy < 0 else 0
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)

            # Keep character within screen bounds
            self.x = max(0, min(self.x, screen_width - 50))  # 50 is the width of the character
            self.y = max(0, min(self.y, screen_height - 50))  # 50 is the height of the character

    def update(self):
        """Update character animation and logic."""
        # Reduce attack timer if above 0
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.is_dead:
            # If the character is dead, we play the death animation
            if self.death_timer > 0:
                self.death_timer -= 1  # Countdown pentru timpul de animație
                self.frame_counter += 1
                if self.frame_counter >= self.frame_delay:
                    self.frame_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(self.death_frames)
                    self.image = self.death_frames[self.current_frame]
            return  # Stop further updates if dead

        # Update animation frame
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:  # Only update frame after delay
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

            # Flip image if facing left or permanently flipped
            # f self.direction_x == -1:
            #    self.image = pygame.transform.flip(self.image, True, False)


    def draw(self, screen):
        """Draw character on the screen."""
        if not self.is_dead or self.death_timer > 0:
            screen.blit(self.image, (self.x, self.y))
            # Draw health bar
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, 50, 5))  # Background bar
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, 50 * (self.health / 100), 5))  # Health bar
            
    def is_alive(self):
        """Return True if the character is alive (health > 0) and not in death state."""
        return self.health > 0 and not self.is_dead