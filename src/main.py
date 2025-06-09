
'''
run the following commands

pip install pygame
pip install requests

'''
# Assets
#wallpaper: https://wallpapers.com/background/flappy-bird-background-gecj5m4a9yhhjp87/download
import pygame, requests
import pygame.image
import random
import io

class chr:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.color = (160,160,160)
        self.skin = pygame.transform.scale((pygame.image.load(io.BytesIO(requests.get('https://raw.githubusercontent.com/friendlyGroupGit/FlappyBird/refs/heads/main/bird.png').content))),(50,50))
    def render(self):
        #render hitbox
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
        screen.blit(self.skin, (self.x-25, self.y-25))
        
class bullet:
    def __init__(self):
        self.x = random.randint(1280,9000)
        self.y = random.randint(25, 695)
    def render(self, bullet_image):
        screen.blit(bullet_image, (self.x, self.y))
        
    def move(self):
        self.x -= 10
        
    def checkCollision(self, character):
        if self.x<= character.x < self.x + 85:
            if self.y- 25 <= character.y < self.y+55:
                return 'death'
class pipe:
    def __init__(self, x, gap_start, moving):
        self.x = x
        self.y = 0
        self.gap_start = gap_start
        if moving == True:
            self.gap_size = 200
        else:
            self.gap_size = 175
        self.moving = moving
        dir_num = random.randint(1,2)
        if dir_num == 1:
            self.direction = 'up'
        else:
            self.direction = 'down'
        self.scored = False
   
    def render(self, screen, color):
        if self.moving == True:
            if self.gap_start <= 130:
                self.direction = 'down'
            if self.gap_start >= 360:
                self.direction = 'up'
            if self.direction == 'up':
                self.gap_start -= 1
            if self.direction == 'down':
                self.gap_start += 1
        # main pipe parts
        top_pipe = pygame.Rect(self.x+2, 0, 96, self.gap_start-18)
        bottom_pipe = pygame.Rect(self.x+2, self.gap_start + self.gap_size + 20, 96, (1280-36-self.gap_start-self.gap_size))
        top_pipe_lip = pygame.Rect(self.x-18, self.gap_start-18, 136, 16)
        bottom_pipe_lip = pygame.Rect(self.x-18, self.gap_start + self.gap_size+2, 136, 16)
        # pipe border
        top_pipe_bd = pygame.Rect(self.x, 0, 100, self.gap_start-20)
        bottom_pipe_bd = pygame.Rect(self.x, self.gap_start + self.gap_size + 20, 100, (1280-40-self.gap_start-self.gap_size))
        top_pipe_lip_bd = pygame.Rect(self.x-20, self.gap_start-20, 140, 20)
        bottom_pipe_lip_bd = pygame.Rect(self.x-20, self.gap_start + self.gap_size, 140, 20)
        
        #draw out pipe
        border_color = (0,0,0)
        pygame.draw.rect(screen, border_color, top_pipe_bd)
        pygame.draw.rect(screen, color, top_pipe)
        pygame.draw.rect(screen, border_color, top_pipe_lip_bd)
        pygame.draw.rect(screen, color, top_pipe_lip)
        pygame.draw.rect(screen, border_color, bottom_pipe_bd)
        pygame.draw.rect(screen, color, bottom_pipe)
        pygame.draw.rect(screen, border_color, bottom_pipe_lip_bd)
        pygame.draw.rect(screen, color, bottom_pipe_lip)
        
       #bottom_pipe
    def move(self): # move the pipes
        self.x -= 2
        if self.y < -400:
            return True
        else:
            return False
        
    def checkCollision(self, character): # check player-pipe collisions for scoring and death
        if ((self.x - 25) < character.x < (self.x + 125)):          
            if self.gap_start + 25 < character.y < self.gap_start+self.gap_size - 25:
                if ((self.x + 50) < character.x < (self.x + 75)):   
                    character.color = (0,255,0)   
                    return 'score'       
            else:
                character.color = (255,0,0)     
                return 'death'
class button:
    def __init__(self, x, y, w, h, color, text, text_size, hidden):
        self.x  = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.text_size = text_size
        self.Rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.hidden = hidden
        self.hide_rect = False
        self.border = False

    def render(self, screen): # draws the button
        font = pygame.font.SysFont("Arial", self.text_size)
        if self.border:
            pygame.draw.rect(screen,(0), pygame.Rect(self.x-2,self.y-2,self.w+4,self.h+4))
        if self.hide_rect == False:
            pygame.draw.rect(screen,(self.color), self.Rect)
        text = font.render(self.text, True, (255,255,255))
        text_rect = text.get_rect(center=(self.x+(self.w/2), self.y+(self.h/2)))
        screen.blit(text, text_rect)

    def checkClick(self, event, db): # checks for button presses
        if db == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.Rect.collidepoint(mouse_pos):
                    return True
        return False
   
# image files

#load images/sounds from url
try:
    bg_rect_file = io.BytesIO(requests.get('https://raw.githubusercontent.com/friendlyGroupGit/FlappyBird/refs/heads/main/background.jpg').content)
    jump_soundfile = io.BytesIO(requests.get('https://raw.githubusercontent.com/friendlyGroupGit/FlappyBird/refs/heads/main/jump.mp3').content)
    score_soundfile = io.BytesIO(requests.get('https://raw.githubusercontent.com/friendlyGroupGit/FlappyBird/refs/heads/main/score.mp3').content)
    death_soundfile =io.BytesIO(requests.get('https://raw.githubusercontent.com/friendlyGroupGit/FlappyBird/refs/heads/main/death.mp3').content)
    bullet_image = bullet_image = pygame.transform.scale((pygame.image.load(io.BytesIO(requests.get('https://raw.githubusercontent.com/friendlyGroupGit/FlappyBird/refs/heads/main/bullet.png').content))),(60,30))
except:
    print('\nInternet Access is Required to play this game.\n')
    exit()

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# background image and infinite scroll
bg_img = pygame.transform.scale((pygame.image.load(bg_rect_file)), (1472, 828))
bg_rect_list = [0,1280,2560]

# soundeffects
jump_sfx = pygame.mixer.Sound(jump_soundfile)
score_sfx = pygame.mixer.Sound(score_soundfile)
death_sfx = pygame.mixer.Sound(death_soundfile)

#jump physics
gravity = 0.35
jump_height = 6
y_velocity = jump_height


#BUTTONS AND MENUS

#home
home_help_button = button(445, 450, 390, 100, (255, 178, 0), "How to Play", 64, False)
home_play_button = button(445, 300, 390, 100, (255, 178, 0), "Play Game", 64, False)
home_title = button(340, 40, 600, 200, (255, 178, 0), "Flappy Bird", 128, False)
home_menu = [home_title, home_play_button, home_help_button]

#help
help_body= button(140,30, 1000, 600, (255, 178, 0), '', 32, True)
help_title = button(180,30, 900, 100, (255, 178, 0), 'How to Play', 48, True)
help_body_1 = button(180,130, 900, 100, (255, 178, 0), 'Hit space or left click to make the bird jump.', 48, True)
help_body_2 = button(180 ,230, 900, 100, (255, 178, 0), 'Make the bird clear the pipes to score points.', 48, True)
help_body_3 = button(180 ,330, 900, 100, (255, 178, 0), 'Select from 3 gamemodes to make things interesting.', 48, True)
help_body_4 = button(180 ,430, 900, 100, (255, 178, 0), 'Score as many points as you can! Good Luck!', 48, True)
help_back_button = button(200, 60, 125, 75, (255, 200, 0), "< Back", 36, True)
help_menu = [help_body, help_title, help_body_1, help_body_2, help_body_3, help_body_4, help_back_button]

#gamemode
gamemode_regular_button = button(445, 300, 390, 100, (255, 178, 0), "Regular", 64, False)
gamemode_moving_button = button(445, 450, 390, 100, (255, 178, 0), "Moving Pipes", 64, False)
gamemode_bullets_mode_button = button(445, 600, 390, 100, (255, 178, 0), "Bullets", 64, False)
gamemode_title = button(200, 40, 880, 200, (255, 178, 0), "Select Gamemode", 128, False)
gamemode_back_button = button(305, 465, 125, 75, (255, 200, 0), "< Back", 36, True)
gamemode_menu = [gamemode_title, gamemode_regular_button, gamemode_moving_button, gamemode_bullets_mode_button, gamemode_back_button]

#gameover
gameover_body = button(140, 30, 1000, 600, (255, 178, 0), '', 32, True)
gameover_title = button(180, 50, 900, 100, (255, 178, 0), 'Gameover!', 96, True)
gameover_score = button(180, 150, 900, 100, (255, 178, 0), '', 64 , True)
gameover_play_button = button(445, 250, 390, 100, (255, 178, 0), "Play Again", 48, False)
gameover_gamemode_button = button(445, 375, 390, 100, (255, 178, 0), "Change Gamemode", 48, False)
gameover_home_button = button(445, 500, 390, 100, (255, 178, 0), "Return Home", 48, False)

gameover_menu = [gameover_body, gameover_title, gameover_score, gameover_play_button,gameover_gamemode_button, gameover_home_button]

#add a border to gameover menu buttons
for i in range(3,6):
    gameover_menu[i].border = True

#menu functions
def renderMenu(ui, screen): # show and hide the different menus
    for item in ui:
        item.render(screen)

def resetGame(moving_mode, bullets_mode, menu, refillPipes): # resets the game after a game over
    pipes = []
    bullets = []
    if refillPipes:
        for i in range(0,6):
            gapstart = random.randint(80, 500)
            pipes.append(pipe(((i*400)+600), gapstart, moving_mode))
    if bullets_mode:
        for i in range(30):
            bullets.append(bullet())
   
    return(False, False, 360, pipes, bullets, menu, False, False)

def initializeGame(moving, bullets): # sets up game when a gamemode button is pressed
    bullets_list = []
    pipe_list = []
    for i in range(6):
        gapstart = random.randint(80, 500)
        pipes_list.append(pipe(((i*400)+600), gapstart, moving))
    if bullets:
        for i in range(30):
            bullets_list.append(bullet())
    return (moving, bullets, pipes_list, bullets_list, 'game', False)


# initialize character
character = chr(300, 360)
score = 0
display_score = 0

#game events/settings
game_start = False
gameover_bool = False
current_menu = 'home'
moving_pipes_mode = False
bullets_mode = False
pipes_list = []
bullets_list = []

gameover_menu_delay = 0

#ui debounce
db = True

while running:
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons_pressed = pygame.mouse.get_pressed() 
   #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.MOUSEBUTTONUP:
            db = True   
            
        #handle ui interactions for the home page
        if current_menu == 'home':
            if home_menu[1].checkClick(event, db) == True:
                current_menu = 'gamemode'
                db = False
            if home_menu[2].checkClick(event, db) == True:
                current_menu = 'help'
                db = False
                
        if current_menu == 'help':
            if help_menu[6].checkClick(event, db) == True:
                current_menu = 'home'
                db = False
                
        if current_menu == 'gamemode': # handle gamemode selector
            if gamemode_menu[1].checkClick(event, db) == True:
                game_options = initializeGame(False, False)
                moving_pipes_mode, bullets_mode, pipes_list, bullets_list, current_menu, db = game_options
                
            if gamemode_menu[2].checkClick(event, db) == True:
                game_options = initializeGame(True, False)
                moving_pipes_mode, bullets_mode, pipes_list, bullets_list, current_menu, db = game_options
                
            if gamemode_menu[3].checkClick(event, db) == True:
                game_options = initializeGame(False, True)
                moving_pipes_mode, bullets_mode, pipes_list, bullets_list, current_menu, db = game_options
                
            if gamemode_menu[4].checkClick(event, db) == True:
                current_menu = 'home'
                db = False
                
        #handle inputs for the game    
        if current_menu == 'game':
            #handle player jumping
            if db == True:
                if gameover_bool == False:
                    if game_start == True:
                        if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE)) or event.type == pygame.MOUSEBUTTONDOWN:
                            y_velocity = jump_height
                            jump_sfx.play()
                            
                    if game_start == False:
                        if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE)) or event.type == pygame.MOUSEBUTTONDOWN:
                            y_velocity = jump_height
                            jump_sfx.play()
                            game_start = True
                            
                    #handle game over menu
                if gameover_bool == True:
                    if ((pygame.time.get_ticks()) - gameover_menu_delay) > 750:
                        if gameover_menu[3].checkClick(event, db) == True:
                            new_game = resetGame(moving_pipes_mode, bullets_mode,'game', True)
                            game_start, gameover_bool, character.y, pipes_list, bullets_list,current_menu, gameover_bool, db = new_game
                            
                        if gameover_menu[4].checkClick(event, db) == True:
                            new_game = resetGame(moving_pipes_mode, bullets_mode,'gamemode', False)
                            game_start, gameover_bool, character.y, pipes_list, bullets_list,current_menu, gameover_bool, db = new_game
                        
                        if gameover_menu[5].checkClick(event, db) == True:
                            new_game = resetGame(moving_pipes_mode, bullets_mode,'home', False)
                            game_start, gameover_bool, character.y, pipes_list, bullets_list,current_menu, gameover_bool, db = new_game
        
        #handle ui interactions for the gamemode selector page
        
    #check for current menu
    if current_menu == 'home':
        screen.blit(bg_img,(0, 0))
        renderMenu(home_menu, screen)
    if current_menu == 'gamemode':
        screen.blit(bg_img,(0, 0))
        renderMenu(gamemode_menu, screen)                
    if current_menu == 'help':
        screen.blit(bg_img,(0, 0))
        renderMenu(help_menu, screen)

    #main gameplay
    if current_menu == 'game':
        
        #draw background
        for i in range(0,len(bg_rect_list)):
            screen.blit(bg_img,(bg_rect_list[i], 0))

        #move the background and move pipes once the game starts
        if game_start == True and gameover_bool == False:
            for i in range(0,len(bg_rect_list)):
                bg_rect_list[i] -= 2
            for i in range(0,len(bg_rect_list)):
                if bg_rect_list[i] < -1280:
                    bg_rect_list[i] = 1280
            for pipeItem in pipes_list:
                pipeItem.move()
            character.y -= y_velocity
            y_velocity -= gravity  
        character.render() #draw the bird
        
        #pipe moving and generation     
        for pipeItem in pipes_list:
            pipeItem.render(screen, (0,255,0))
            pipeItem.checkCollision(character)
            if pipeItem.x < -600:
                pipes_list.remove(pipeItem)
                gapstart = random.randint(80, 500)
                pipes_list.append(pipe(1800, gapstart, moving_pipes_mode))
            collision = pipeItem.checkCollision(character)
            
            #handle pipe collisions
            if collision == 'score':
                if pipeItem.scored == False:
                    pipeItem.scored = True
                    score +=1
                    score_sfx.play()
            if collision == 'death':
                if game_start == True:
                    death_sfx.play()
                    display_score = score
                    score = 0
                    game_start = False
                    gameover_menu_delay = pygame.time.get_ticks()
                gameover_bool = True
        
        #handle bullet rendering and collisions        
        if bullets_mode == True:
            for bullet_item in bullets_list:
                if game_start:
                    bullet_item.move()
                bullet_item.render(bullet_image)
                if bullet_item.x < -200:
                    bullets_list.remove(bullet_item)
                    bullets_list.append(bullet())
                #handle bullet collisions
                collision = bullet_item.checkCollision(character)
                if collision == 'death':
                    if game_start == True:
                        death_sfx.play()
                        game_start = False
                        display_score = score
                        score = 0
                        gameover_menu_delay = pygame.time.get_ticks()
                    gameover_bool = True
        #game start message
        if game_start == False and gameover_bool == False:
            start_text = pygame.font.SysFont("Arial",24).render("Press [SPACE] or click [MOUSE] to start game!", True, (255,255,255))
            screen.blit(start_text, (120,200))     
        #display score
        score_display = button(540, 60, 200, 75, (0,0,0), str(score), 64, False)
        score_display.hide_rect = True 
        score_display.render(screen)
                
        #handle floor-player collisions
        if character.y > 655:
            if game_start == True:
                game_start = False
                gameover_bool = True
                gameover_menu_delay = pygame.time.get_ticks()
            
        # handle gameovers   
        if gameover_bool == True:
            if character.y < 655:
                character.y -= y_velocity
                y_velocity -= gravity*3
            else:
                character.y = 655
            if ((pygame.time.get_ticks()) - gameover_menu_delay) > 750:
                gameover_menu[2].text = ("Score: " + str(display_score))
                #add a translucent shadow
                shadow = pygame.Surface((1280,720))
                shadow.set_alpha(128)
                shadow.fill((0,0,0))
                screen.blit(shadow, (0,0))
                renderMenu(gameover_menu, screen) #render gameover menu
   
    pygame.display.flip()
    clock.tick(60) 
