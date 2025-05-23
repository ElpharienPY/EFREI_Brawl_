import pygame

class Projectile:
    def __init__(self, x, y, direction, frames, speed, damage, owner, player_name, hit_sound, trigger_shake):
        self.frames = frames  # List of Pygame frames
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_rate = 4  # Number of ticks per frame

        self.image = self.frames[self.frame_index]
        # Create a hitbox smaller than the visible sprite
        full_rect = self.frames[0].get_rect()
        hitbox_scale = 0.4  # Reduce the hitbox size to 40% of the image

        reduced_width = int(full_rect.width * hitbox_scale)
        reduced_height = int(full_rect.height * hitbox_scale)

        self.rect = pygame.Rect(0, 0, reduced_width, reduced_height)
        self.rect.center = (x, y)

        self.direction = direction  # -1 = left, 1 = right
        self.speed = speed
        self.damage = damage
        self.owner = owner  # Reference to the player who launched the projectile
        self.player_name = player_name
        self.hit_sound = hit_sound
        self.active = True
        self.trigger_shake = trigger_shake

    def move(self):
        self.rect.x += self.speed * self.direction

        # Deactivate the projectile if it goes off-screen
        if self.rect.right < 0 or self.rect.left >= 1280:
            self.active = False

    def animate(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_rate:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.frame_timer = 0

    def update(self):
        self.move()
        self.animate()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_collision(self, target):
        if self.rect.colliderect(target.rect) and self.active:
            self.hit_sound.play()
            target.health -= self.damage
            target.hit = True
            target.energy = min(target.energy + 5, 100)
            self.active = False

            self.trigger_shake(30)




