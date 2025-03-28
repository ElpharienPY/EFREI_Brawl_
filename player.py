import pygame
class Player():

    def __init__(self,player, x, y, flip, data, sprite_sheet, animation_steps,sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip=flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:afk/#1:courir/#2:sauter/#3:attaque1/#4:attaque2/#5:coup/#6:mort
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect=pygame.Rect(x,y,80,180)
        self.vel_y=0
        self.running=False
        self.jump = False
        self.attack_type=0
        self.attacking=False
        self.attacking_cooldown=0
        self.attack_sound=sound
        self.hit=False
        self.health=100
        self.alive=True

    def load_images(self, sprite_sheet, animation_steps):
        #extraire images
        animation_list=[]
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x*self.size,y*self.size,self.size,self.size)
                zoom=pygame.transform.scale(temp_img,(self.size*self.image_scale,self.size*self.image_scale))
                temp_img_list.append(zoom)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target,round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running=False
        self.attack_type=0

        #Touche clavier
        key = pygame.key.get_pressed()

        #rien faire s'il n'attaque pas
        if self.attacking == False and self.alive == True and round_over == False:
            # check player 1 controls
            if self.player == 1:
                # movement
                if key[pygame.K_q]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_z] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pygame.K_e] or key[pygame.K_r]:
                    self.attack(surface,target)
                    # determine which attack type was used
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_r]:
                        self.attack_type = 2

                # check player 2 controls
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface,target)
                    # determine which attack type was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2


        #Gravité
        self.vel_y += GRAVITY
        dy += self.vel_y

        #Ne pas sortir de l'écran
        if self.rect.left + dx < 0:
            dx = -self.rect.x
        if self.rect.right + dy > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 55:
            self.vel_y = 0
            self.jump = False
            dy= screen_height - 55 - self.rect.bottom

        #face to face
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #appliqué afk
        if self.attacking_cooldown > 0:
            self.attacking_cooldown -= 1

        #position joueur
        self.rect.x += dx
        self.rect.y += dy

    #animation
    def update(self):
        #quelle action demandée
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)#death
        elif self.hit == True:
            self.update_action(5)#hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)#attaque1
            elif self.attack_type == 2:
                self.update_action(4)#attaque2
        elif self.jump == True:
            self.update_action(2)#saut
        elif self.running==True:
            self.update_action(1)#courir
        else :
            self.update_action(0)#afk

        animation_cooldown = 60
        self.image = self.animation_list[self.action][self.frame_index]
        #temps entre chaque frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #fin animation
        if self.frame_index >= len(self.animation_list[self.action]):
            #joueur mort ?
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                #attaque exécutée ?
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attacking_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attacking_cooldown = 20

    def attack(self, surface, target):
        if self.attacking_cooldown == 0:
            #execute attaque
            self.attacking = True
            self.attack_sound.play()
            attacking_rect= pygame.Rect(self.rect.centerx - (3*self.rect.width*self.flip), self.rect.y, 3*self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface,(0,255,0), attacking_rect)

    def update_action(self, new_action):
        #nouvelle action différente de la précédente
        if new_action != self.action:
            self.action = new_action
            #mettre à jour paramètres animation
            self.frame_index =0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255,0,0), self.rect)
        surface.blit(img, (self.rect.x-(self.offset[0]*self.image_scale), self.rect.y-(self.offset[1]*self.image_scale)))

