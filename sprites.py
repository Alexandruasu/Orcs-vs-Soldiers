import pygame

def load_sprite(file_path, frame_width, frame_height):
    """Load a sprite sheet and divide it into frames."""
    sprite_sheet = pygame.image.load(file_path).convert_alpha()
    frames = []
    for i in range(sprite_sheet.get_width() // frame_width):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames
