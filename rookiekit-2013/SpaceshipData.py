import time
import pygame
import random
from background import Background
from spaceship import Spaceship
from baddie import Baddie
# multiple baddies
# you are dead menu
# pelican mode
# collision detection for player
# health points

white = 255,255,255

class SpaceshipData:

    def __init__(self,width,height,frame_rate):



        # Game Sounds 
        pygame.mixer.init()
        self.player_killed = pygame.mixer.Sound("spartan_die.wav")
        self.player_killed.set_volume(.55)

        self.baddie_killed = pygame.mixer.Sound("grunt_death.wav")
        self.baddie_killed.set_volume(1.)

        self.baddie2_killed = pygame.mixer.Sound("elite_killed.wav")
        self.baddie2_killed.set_volume(.5)

        self.bullet_sound = pygame.mixer.Sound("assault_rifle.wav")
        self.bullet_sound.set_volume(1.)

        self.pelican_shoot = pygame.mixer.Sound("chain_gun.wav")
        self.pelican_shoot.set_volume(.75)

        self.battle_theme = pygame.mixer.music.load("battle_theme2.wav")


        pygame.mixer.music.play()

        # Game Images

        self.bg = Background("blood_gulch800x500.png", width)

        self.baddie_img  = pygame.image.load("grunt_100x68.png")
        self.baddie2_img = pygame.image.load("blue_elite80x109.png")
        self.player_img  = pygame.image.load("master_chief70x79.png")
        self.player_img2 = pygame.image.load("goku_90x105.png")

        self.font = pygame.font.SysFont("Times New Roman",36)
        self.font2 = pygame.font.SysFont("Courier New",20)
        self.frame_rate = frame_rate
        self.text_color = (255,0,0)
        self.width  = width
        self.height = height
        self.upper_limit = self.width/3
        self.spaceship_width  = 50   #to compensate for the size of his body
        self.spaceship_height = 79   #he is not a rectangle
        self.spaceship = Spaceship(self.spaceship_width, self.spaceship_height,
                                   0, (self.height / 2) - 10, (255,255,255),
                                   self.player_img, self.player_killed)
        self.spaceship.setName('Chief')
        print self.spaceship.getName()
        self.spaceship_speed = 10
        self.spaceship.setHitPoints(3)

        self.bullets = []
        self.bullet_width = 10
        self.bullet_height = 5
        self.bullet_color = (255,255,255)

        ### Delay baddies for 37 seconds ###
        #time.sleep(17)

        self.baddies = []
        self.baddie_width = 100
        self.baddie_height = 68

		#self.baddies2 = []
        self.baddie2_width = 35
        self.baddie2_height = 109
    
       #    Code to change the game to DBZ themes  
       # 
        #if self.kills > 25:
          #  self.bg.setImage("cell_games.png")
       #     self.bullet_sound       = pygame.mixer.Sound("ki_blast.wav")
       #     self.bullet_img         = pygame.mixer.Sound("ki_blast.png")
       #     self.baddie_killed      = pygame.mixer.Sound("Cell.wav")
           # self.baddie_img         = pygame.image.load("Cell.png")
       #     self.player_img         = pygame.image.load("Goku.png")
       #     self.dbz_theme          = pygame.mixer.music.load("DBZ_theme.wav")
       #     self.player_hit_points  = 5
       #     self.baddie_hit_points  = 25



           #     Use code for boss to shoot at random times #
           #  
           # def boss_shoot():
           #     time.sleep(random.choice([0, 1, 2])

        # Number of Player Health
        self.health = self.spaceship.getHitPoints()

        # Kill Points
        self.kills = 0

        # Display the health
        self.health_color = (255,255,255)
        self.health_x     = self.width/2
        self.health_y     = self.height - 30

        # Display the Score
        self.score_color = (0,150,0)
        self.score_x     = 20
        self.score_y     = 50



        return

    def evolve(self, keys, newkeys, buttons, newbuttons, mouse_position):
        
        self.bg.update()    # Update Background
        if pygame.K_w in keys:
            self.spaceship.setHitPoints(10)
            self.spaceship.setWidth(225)
            self.spaceship.setHeight(75)
            self.spaceship.setImage('pelican_250x99.png')
            self.spaceship.setName('Pelican')
            self.spaceship_speed       = 15
            self.health = self.spaceship.getHitPoints()
            self.bullet_sound = self.pelican_shoot
            self.bg.setSpeed(-20)


        if pygame.K_LEFT in keys:
            self.spaceship.moveLeft(self.spaceship_speed)
        if pygame.K_RIGHT in keys:
            self.spaceship.moveRight(self.spaceship_speed,self.upper_limit)
        if pygame.K_UP in keys:
            self.spaceship.moveUp(self.spaceship_speed)
        if pygame.K_DOWN in keys:
            self.spaceship.moveDown(self.spaceship_speed,self.height)

        if self.spaceship.getAlive() == True:   # If space ship is alive, then
                                                # it can fire.
            if pygame.K_SPACE in newkeys:
                self.bullet_sound.play()
                self.bullets.append(self.spaceship.fire(self.bullet_width,
                                                        self.bullet_height,
                                                        self.bullet_color))

        if pygame.K_q in newkeys:
            print "PRESSED Q"
            pygame.quit()
            return

        if pygame.K_r in keys:
            print "GAME RESTARTED"
            self.__init__(1024, 768, 30)
            return



        if random.randint(1, self.frame_rate/2) == 1:
            self.addBaddie()                                ## Spawn Baddie
        elif random.randint(1, self.frame_rate+10) == 2:     ## Spawn Baddie2
            self.addStrongBaddie()

        for bullet in self.bullets:
            bullet.moveBullet()
            bullet.checkBackWall(self.width)
                
        for baddie in self.baddies:
            baddie.tick(0,0,self.height)

        ## Checks if the baddie was hit.
        ## Adds to the kill count each time a baddie dies.

        for bullet in self.bullets:
            if not bullet.alive:
                continue
            for baddie in self.baddies:
                if not baddie.alive:
                    continue
                x,y,w,h = baddie.getDimensions()
                bullet.checkHitBaddie(x,y,w,h)
                if bullet.getHit():
                    print "Baddie hit"
                    bullet.setAlive(False)
                    if self.spaceship.getName() == 'Pelican':
                        baddie.decreaseHitPoints(10)
                    else:
                        baddie.decreaseHitPoints(1)
                    bullet.hit = False
                    if baddie.getAlive() == False:
                        if baddie.getName() == 'Elite':
			    self.baddie2_killed.play()
			    print baddie.getName()
			elif baddie.getName() == 'Grunt':
			    self.baddie_killed.play()
			    print baddie.getName()
			self.kills += 1
			print "BADDIE KILLED"

        # Checks if player was hit
        # If he dies, a pause menu is shown to the user

        for baddie in self.baddies:
            if not baddie.alive:
                continue
            if self.spaceship.getAlive:
                if not self.spaceship.alive:
                    continue
                x,y,w,h = self.spaceship.getDimensions()
                baddie.checkHitPlayer(x,y,w,h)
                if baddie.getHit():
                    print "PLAYER HIT"
                    baddie.setAlive(False)
                    self.spaceship.decreaseHitPoints(1)
                    self.health = self.health - 1
                    baddie.hit = False

                    if self.spaceship.getName() == 'Pelican':
                        print "Player Hit Points: %s" % (self.spaceship.getHitPoints())
                        if self.spaceship.getHitPoints() == 1:  # When Pelican dies

                        # Set everything back to Master Chief #
                        # "Spawn him"
                            print "You are almost dead."
                            self.spaceship.setHitPoints(3)
                            self.spaceship.setWidth(50)
                            self.spaceship.setHeight(75)
                            self.spaceship.setImage('master_chief70x79.png')
                            self.spaceship.setName('Chief')
                            self.spaceship_speed       = 5
                            self.bullet_sound = pygame.mixer.Sound('assault_rifle.wav')
                            self.bg.setSpeed(-1)
                            self.health = self.spaceship.getHitPoints()

                    if self.spaceship.getAlive() == False:
                        print "PLAYER KILLED"
                        self.player_killed.play()


        live_bullets = []
        live_baddies = []

        for bullet in self.bullets:
            if bullet.alive:
                live_bullets.append(bullet)
        for baddie in self.baddies:
            if baddie.alive:
                live_baddies.append(baddie)
            #elif baddie.getAlive() == False:  #Every time a baddie dies
      
        self.bullets = live_bullets
        self.baddies = live_baddies
            
        return

    def addStrongBaddie(self):
        self.new_baddie2 = Baddie( self.baddie2_width, self.baddie2_height,
                             self.width, random.randint(0,
                            (self.height - self.baddie2_height)),
                             self.baddie2_img, self.baddie2_killed )
							 
	self.new_baddie2.setName('Elite')
        self.new_baddie2.setHitPoints(3)
        self.baddies.append( self.new_baddie2 )

        return

    def addBaddie(self):
        self.new_baddie = Baddie( self.baddie_width, self.baddie_height,
                             self.width, random.randint(0,
                            (self.height-self.baddie_height)),
                             self.baddie_img, self.baddie_killed )
	self.new_baddie.setName('Grunt')
        self.new_baddie.setHitPoints(2)
        self.baddies.append( self.new_baddie )

        return

    def draw(self,surface):
        rect = pygame.Rect(0,0,self.width,self.height)
        surface.fill((0,0,0),rect )

        self.bg.paint(surface)  #Paint the Background to the screen

        if self.spaceship.alive:
            self.spaceship.draw(surface)
        else:
            dead_str = "#you are dead."
            restart_str = "# r for restart, q for quit."
            self.drawTextRight(surface, dead_str, white,
                               (self.width/2)+75, self.height/2, self.font2)

            self.drawTextRight(surface, restart_str, white,
                               (self.width/2)+150, self.height-150, self.font2)

        for bullet in self.bullets:
            bullet.draw(surface)

        for baddie in self.baddies:
            baddie.draw(surface)

        score_str = "#score: %s" % (str(self.kills))
        self.drawTextLeft(surface, score_str, self.score_color, self.score_x,
                          self.score_y, self.font)

        health_str = "#health: %s" % str(self.health)
        self.drawTextRight(surface, health_str, self.health_color, self.health_x,
                           self.health_y, self.font)

        pelican_str = "#press 'W' for upgraded Spaceship!"
        self.drawTextRight(surface, pelican_str, (255,255,255), self.health_x+150,
                           self.health_y-50, self.font2)

        return

    
    def drawTextLeft(self, surface, text, color, x, y, font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomleft = (x, y)
        surface.blit(textobj, textrect)
        return

    def drawTextRight(self, surface, text, color, x, y, font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomright = (x, y)
        surface.blit(textobj, textrect)
        return
