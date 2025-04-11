import pygame

class Player():

    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:afk/#1:courir/#2:sauter/#3:attaque1/#4:attaque2/#5:coup/#6:mort
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attack_type = 0
        self.attacking = False
        self.attacking_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.energy = 0  # Jauge d'énergie de 0 à 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                zoom = pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))
                temp_img_list.append(zoom)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()

        if self.attacking == False and self.alive == True and round_over == False:
            if self.player == 1:
                if key[pygame.K_q]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_z] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_e] or key[pygame.K_r]:
                    self.attack(surface, target)
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_r]:
                        self.attack_type = 2

            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.x
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 55:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 55 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attacking_cooldown > 0:
            self.attacking_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 60
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attacking_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attacking_cooldown = 20

    def attack(self, surface, target):
        if self.attacking_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(
                self.rect.centerx - (3 * self.rect.width * self.flip), self.rect.y, 3 * self.rect.width, self.rect.height
            )
            if attacking_rect.colliderect(target.rect):
                target.health -= 5
                target.hit = True
                target.energy = min(target.energy + 5, 100)  # Moins d'énergie en subissant
                self.energy = min(self.energy + 20, 100)  # Plus d'énergie en attaquant
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def get_projectile_origin(self):
        """Retourne un point ajusté (torse/poitrine) pour faire partir les projectiles."""
        origin_x = self.rect.centerx
        origin_y = self.rect.top + self.rect.height // 3
        return origin_x, origin_y