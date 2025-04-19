import pygame

class Player:

    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, control_mode="clavier", joystick_id=None):
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
        self.can_double_jump = True
        self.attack_type = 0
        self.attacking = False
        self.attacking_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.energy = 0  # Jauge d'énergie de 0 à 100
        self.alive = True
        self.can_double_jump = True
        self.hit_counter = 0

        # Contrôle : manette ou clavier
        self.control_mode = control_mode
        self.joystick = None
        if control_mode == "manette" and joystick_id is not None:
            if pygame.joystick.get_count() > joystick_id:
                self.joystick = pygame.joystick.Joystick(joystick_id)
                self.joystick.init()
                print(f"🕹️ Manette {joystick_id} assignée au joueur {self.player}")
            else:
                print(f"⚠️ Manette {joystick_id} non détectée pour joueur {self.player}")
        else:
            print(f"⌨️ Joueur {self.player} utilise le clavier")

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

    """def move(self, screen_width, screen_height, surface, target, round_over):
        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()

        if self.attacking == False and self.alive == True and round_over == False:
            if self.player == 1:
                if key[pygame.K_q]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_d]:
                    dx = speed
                    self.running = True
                if key[pygame.K_z] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                    self.can_double_jump = True

                elif key[pygame.K_2] and self.jump and self.can_double_jump:
                    self.vel_y = -25
                    self.can_double_jump = False
                    #print("Double saut J1 !")

                if key[pygame.K_e] or key[pygame.K_r]:
                    self.attack(surface, target)
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_r]:
                        self.attack_type = 2

            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.running = True
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                    self.can_double_jump = True

                elif key[pygame.K_RSHIFT] and self.jump and self.can_double_jump:
                    self.vel_y = -30
                    self.can_double_jump = False
                    #print("Double saut J2 !")

                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        self.vel_y += gravity
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.x
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 55:
            self.vel_y = 0
            self.jump = False
            self.can_double_jump = True
            dy = screen_height - 55 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attacking_cooldown > 0:
            self.attacking_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy"""

    def move(self, screen_width, screen_height, surface, target, round_over):
        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        if not self.attacking and self.alive and not round_over:
            if self.control_mode == "clavier":
                key = pygame.key.get_pressed()

                if self.player == 1:
                    if key[pygame.K_q]:
                        dx = -speed
                        self.running = True
                    if key[pygame.K_d]:
                        dx = speed
                        self.running = True
                    if key[pygame.K_z] and not self.jump:
                        self.vel_y = -30
                        self.jump = True
                    if key[pygame.K_2] and self.jump and self.can_double_jump:
                        self.vel_y = -30
                        self.can_double_jump = False
                    if key[pygame.K_e]:
                        self.attack(surface, target, 1)
                    elif key[pygame.K_e]:
                        self.attack(surface, target, 2)



                if self.player == 2:
                    if key[pygame.K_LEFT]:
                        dx = -speed
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx = speed
                        self.running = True
                    if key[pygame.K_UP] and not self.jump:
                        self.vel_y = -30
                        self.jump = True
                        self.can_double_jump = True  # si activé
                    # DOUBLE SAUT (ex: touche SHIFT droit)
                    if key[pygame.K_RSHIFT] and self.jump and self.can_double_jump:
                        self.vel_y = -30
                        self.can_double_jump = False
                    if key[pygame.K_KP1]:
                        self.attack(surface, target, 1)
                    elif key[pygame.K_KP2]:
                        self.attack(surface, target, 2)

            elif self.control_mode == "manette" and self.joystick:
                axis_x = self.joystick.get_axis(0)
                if axis_x < -0.5:
                    dx = -speed
                    self.running = True
                elif axis_x > 0.5:
                    dx = speed
                    self.running = True

                # Saut principal avec bouton X
                if self.joystick.get_button(0) and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                    self.can_double_jump = True

                # Double saut avec bouton 12 (flèche haut de la croix)
                if self.jump and self.can_double_jump and self.joystick.get_button(11):
                    self.vel_y = -30
                    self.can_double_jump = False
                    print(f"Double saut joueur {self.player} avec bouton 12 (croix directionnelle)")

                if self.joystick.get_button(1):  # Carré
                    self.attack(surface, target, 1)
                elif self.joystick.get_button(2):  # Triangle
                    self.attack(surface, target, 2)

        self.vel_y += gravity
        dy += self.vel_y

        if self.rect.bottom + dy > screen_height - 55:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 55 - self.rect.bottom

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

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
        elif self.hit:
            self.update_action(5)
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 60
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
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

    """def attack(self, surface, target):
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
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)"""

    def attack(self, surface, target, attack_type):
        if self.attacking_cooldown == 0:
            self.attacking = True
            self.attack_type = attack_type
            self.attack_sound.play()

            attacking_rect = pygame.Rect(
                self.rect.centerx - (3 * self.rect.width * self.flip),
                self.rect.y,
                3 * self.rect.width,
                self.rect.height
            )

            if attacking_rect.colliderect(target.rect):
                target.health -= 5
                target.hit = True
                target.energy = min(target.energy + 10, 100)
                target.hit_counter += 1
                if target.hit_counter >= 3:
                    target.energy = min(target.energy + 20, 100)
                    target.hit_counter = 0

                self.energy = min(self.energy + 20, 100)
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect) #Fait apparaitre la hitbox

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def get_projectile_origin(self):
        """Retourne la vraie position visuelle (milieu du torse) du sprite à l'écran."""
        draw_x = self.rect.x - (self.offset[0] * self.image_scale)
        draw_y = self.rect.y - (self.offset[1] * self.image_scale)

        sprite_width = self.size * self.image_scale
        sprite_height = self.size * self.image_scale

        origin_x = draw_x + sprite_width // 2
        origin_y = draw_y + sprite_height // 2.4  # torse

        return origin_x, origin_y
