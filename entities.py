import pygame
import math

class Character:
    def __init__(self, x, y, health, damage, walk_frames, attack_frames, death_frames, direction=1):
        self.x = x
        self.y = y
        self.health = health  # Initial health value
        self.damage = damage  # Damage dealt per attack
        self.walk_frames = walk_frames  # Animation frames for walking
        self.attack_frames = attack_frames  # Animation frames for attacking
        self.death_frames = death_frames  # Animation frames for death
        self.frames = walk_frames  # Default animation is walking
        self.current_frame = 0
        self.image = walk_frames[0]
        self.direction_x = direction  # Horizontal direction (1 for right, -1 for left)
        self.direction_y = 0  # Vertical direction (-1 for up, 1 for down)
        self.frame_delay = 5  # Delay between animation frames
        self.frame_counter = 0
        self.speed = 2  # Movement speed
        self.is_dead = False  # True if the character is dead
        self.death_timer = 0  # Timer for how long the death animation plays
        self.attack_cooldown = 120  # Cooldown period for attacks (2 seconds at 60 FPS)
        self.attack_timer = 0  # Timer to track when the character can attack next

    def take_damage(self, damage):
        """Reduce health and check for death."""
        if not self.is_dead:
            self.health -= damage
            if self.health <= 0:
                self.is_dead = True
                self.frames = self.death_frames  # Switch to death animation
                self.current_frame = 0  # Restart animation from first frame
                self.death_timer = len(self.death_frames) * self.frame_delay  # Play full death animation

    def attack(self, target):
        """Attack another character if within range and cooldown has passed."""
        # Check if the target is within attack range (50x50 pixels)
        if self.attack_timer == 0 and not self.is_dead and abs(self.x - target.x) < 50 and abs(self.y - target.y) < 50:
            self.frames = self.attack_frames  # Start attack animation
            target.take_damage(self.damage)  # Deal damage to the target
            self.attack_timer = self.attack_cooldown  # Reset attack cooldown

    def move_towards(self, target, screen_width, screen_height):
        """Move towards the target while staying within screen boundaries."""
        if not self.is_dead and not (abs(self.x - target.x) < 50 and abs(self.y - target.y) < 50):
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.hypot(dx, dy)

            if distance > 0:  # Prevent division by zero
                self.direction_x = 1 if dx > 0 else -1
                self.direction_y = 1 if dy > 0 else -1 if dy < 0 else 0
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)

            # Keep the character within screen bounds
            self.x = max(0, min(self.x, screen_width - 50))  # 50 is the character's width
            self.y = max(0, min(self.y, screen_height - 50))  # 50 is the character's height

    def update(self):
        """Update character's animation and logic."""
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.is_dead:
            # Run death animation if character is dead
            if self.death_timer > 0:
                self.death_timer -= 1
                self.frame_counter += 1
                if self.frame_counter >= self.frame_delay:
                    self.frame_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(self.death_frames)
                    self.image = self.death_frames[self.current_frame]
            return  # Stop further updates if dead

        # Switch back to walking animation if not attacking
        if self.attack_timer == 0 and self.frames != self.walk_frames:
            self.frames = self.walk_frames  # Set walking frames
            self.current_frame = 0  # Reset animation frame

        # Update animation frame (either walking or attacking)
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self, screen):
        """Draw the character and health bar on the screen."""
        if not self.is_dead or self.death_timer > 0:
            screen.blit(self.image, (self.x, self.y))
            # Draw health bar background
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, 50, 5))
            # Draw current health
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, 50 * (self.health / 100), 5))

    def is_alive(self):
        """Return True if the character is alive (health > 0) and not dead."""
        return self.health > 0 and not self.is_dead

class Wizard(Character):
    def __init__(self, x, y, health, damage, walk_frames, attack_frames, effect_frames, idle_frames):
        super().__init__(x, y, health, damage, walk_frames, attack_frames, idle_frames)
        self.effect_frames = effect_frames  # Frames for spell effects
        self.projectiles = []  # List to store active projectiles

    def attack(self, target):
        """Wizard casts a spell at the target."""
        if self.attack_timer == 0 and not self.is_dead:
            self.frames = self.attack_frames  # Switch to attack animation
            self.attack_timer = self.attack_cooldown  # Reset cooldown

            # Calculate the direction to the target
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.hypot(dx, dy)

            direction_x = dx / distance
            direction_y = dy / distance

            offset_distance = 10  # Distance to spawn projectile in front of the wizard

            # Position the projectile right in front of the wizard
            projectile_data = {
                "x": self.x + direction_x * offset_distance,
                "y": self.y + direction_y * offset_distance,
                "target": target,
                "frame_index": 0,
                "hit": False
            }

            self.projectiles.append(projectile_data)

    def update_projectiles(self, screen):
        """Update and draw projectiles."""
        for projectile in self.projectiles[:]:

            target = projectile["target"]
            dx = target.x - projectile["x"]
            dy = target.y - projectile["y"]
            distance = math.hypot(dx, dy)

            # Initialize update time if it doesn't exist
            if "last_update_time" not in projectile:
                projectile["last_update_time"] = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()

            create_delay = 150  # Delay for fire creation phase
            flight_delay = 50  # Delay during projectile flight
            explosion_delay = 80  # Delay during explosion phase

            # Phase 3: Explosion (frames 8-9)
            if projectile["hit"]:
                if current_time - projectile["last_update_time"] > explosion_delay:
                    if projectile["frame_index"] < 10:
                        current_frame = min(projectile["frame_index"], 9)

                        # Display explosion at normal size (100x100)
                        explosion_image = pygame.transform.scale(self.effect_frames[current_frame], (100, 100))
                        screen.blit(explosion_image, (projectile["x"], projectile["y"]))

                        projectile["frame_index"] += 1
                        projectile["last_update_time"] = current_time
                    else:
                        self.projectiles.remove(projectile)  # Remove projectile after explosion
                else:
                    # Continue displaying the same frame until delay time passes
                    current_frame = min(projectile["frame_index"], 9)
                    explosion_image = pygame.transform.scale(self.effect_frames[current_frame], (100, 100))
                    screen.blit(explosion_image, (projectile["x"], projectile["y"]))
                continue  # Move to the next projectile

            # Phase 1: Fire creation (frames 0-3)
            if projectile["frame_index"] < 4:
                if current_time - projectile["last_update_time"] > create_delay:
                    screen.blit(self.effect_frames[projectile["frame_index"]], (projectile["x"], projectile["y"]))
                    projectile["frame_index"] += 1
                    projectile["last_update_time"] = current_time
                else:
                    screen.blit(self.effect_frames[projectile["frame_index"]], (projectile["x"], projectile["y"]))
                continue  # Wait to finish the creation phase

            # Phase 2: Fire flight (frames 4-7) - scaled smaller (80x80) without changing speed
            if distance > 5:
                projectile["x"] += (dx / distance) * 3
                projectile["y"] += (dy / distance) * 3

                if current_time - projectile["last_update_time"] > flight_delay:
                    loop_frame = 4 + ((projectile["frame_index"] - 4) % 4)

                    # Scale projectile down to 80x80 pixels during flight
                    smaller_projectile = pygame.transform.scale(self.effect_frames[loop_frame], (80, 80))
                    screen.blit(smaller_projectile, (projectile["x"], projectile["y"]))

                    projectile["frame_index"] += 1
                    projectile["last_update_time"] = current_time
                else:
                    loop_frame = 4 + ((projectile["frame_index"] - 4) % 4)
                    smaller_projectile = pygame.transform.scale(self.effect_frames[loop_frame], (80, 80))
                    screen.blit(smaller_projectile, (projectile["x"], projectile["y"]))
            else:
                # Trigger explosion when the projectile hits the target
                projectile["hit"] = True
                projectile["frame_index"] = 8  # Start explosion from frame 8
                target.take_damage(self.damage)
