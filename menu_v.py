import pygame , cv2 , random , os
pygame.init()

screen_size = WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
#Screen2 = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32)


autodetect_screen_info = pygame.display.Info()
detected_width = autodetect_screen_info.current_w
detected_height = autodetect_screen_info.current_h




if detected_width <= detected_height:
	Screen = pygame.display.set_mode(screen_size, pygame.NOFRAME)
else:
	Screen = pygame.display.set_mode(screen_size, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

game_paused=False
game_paused2=False
title2_font = pygame.font.Font("fonts/VanDoesburg.ttf", 28)
title3_font = pygame.font.Font("fonts/TitilliumWeb-SemiBold.ttf", 38)
title4_font = pygame.font.Font("fonts/TitilliumWeb-SemiBold.ttf", 28)
solve_rect=pygame.draw.rect(Screen, (0, 0, 255), pygame.Rect(28,250, 140, 70), 7, 15)
check_rect=pygame.draw.rect(Screen, (0, 0, 255), pygame.Rect(28,330, 140, 70), 7, 15)
_1=pygame.image.load("Capture.png")
_1=pygame.transform.scale(_1,(200,200))
_2=pygame.image.load("Capture1.png")
_2=pygame.transform.scale(_2,(200,200))
_3=pygame.image.load("Capture2.png")
_3=pygame.transform.scale(_3,(200,200))
_4=pygame.image.load("Capture3.png")
_4=pygame.transform.scale(_4,(200,200))
_5=pygame.image.load("Capture4.png")
_5=pygame.transform.scale(_5,(200,200))
_6=pygame.image.load("Capture5.png")
_6=pygame.transform.scale(_6,(200,200))
_7=pygame.image.load("Capture6.png")
_7=pygame.transform.scale(_7,(200,200))
_8=pygame.image.load("Capture7.png")
_8=pygame.transform.scale(_8,(200,200))

instruction_exit = title4_font.render("PRESS ESC TO QUIT",True,(255,0,0))



class Tile(pygame.sprite.Sprite):
    def __init__(self, filename , x, y):
        super().__init__()     #calling the parent class (sprite) constructor

        self.name= filename.split('.')[0]       # TO SPLT THE EXTENSION WITH FILENAME
        self.orignal_image= pygame.image.load("images/aliens/"+ filename)
        self.back_image= pygame.image.load("images/aliens/"+ filename)
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image=self.back_image
        self.rect= self.image.get_rect(topleft=(x,y))
        self.shown =False    #face of card down
        
        
    def update(self):     #to check  shown is true or false
        self.image=self.orignal_image if self.shown else self.back_image    
    def show(self):  # function to flip front
        self.shown= True
    def hide(self):   # function to flip baack
        self.shown = False



class Game():
   

    

    def __init__(self):
        self.level = 1
        self.level_complete = False
        self.turns=0
        # initialize cards
  
        self.all_aliens = [f for f in os.listdir("images/aliens") if os.path.join("images/aliens", f)]
        
        self.img_width,self.img_height= (128,128)
        self.padding= 20
        self.margin_top = 80
        self.cols=4
        self.rows=2
        self.width=1280

        self.tiles_group= pygame.sprite.Group()

        #flipping and timing
        self.flipped=[]
        self.frame_count =0
        self.block_game = False
       

        # GENERATE LEVEL 1
        self.generate_level(self.level)
        
        #initialize video
        
        self.is_video_playing = True
        self.play= pygame.image.load('images/play (2).png').convert_alpha()
        self.stop=pygame.image.load('images/stop (2).png').convert_alpha()
        self.video_toggle= self.play
        self.video_toggle_rect= self.video_toggle.get_rect(topright=(WINDOW_WIDTH-58,14))
        self.get_video()
        #INITIALIZE MUSIC
        self.is_music_playing = True
        self.sound_on = pygame.image.load('images/speaker.png').convert_alpha()
        self.sound_off = pygame.image.load('images/mute.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH-15,14))
        #load music
        pygame.mixer.music.load('bg_music/music.mp3')
        pygame.mixer.music.set_volume(.3)   # we can set volume btw .1 to 1
        pygame.mixer.music.play()
       
    
    def update(self, event_list):
        
        self.draw()
        if self.is_video_playing:
            self.success, self.img = self.cap.read()
        self.user_input()
       
        self.check_level_complete(event_list)
        # passing draw
    
    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type==pygame.MOUSEBUTTONDOWN and event.button== 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):

                            self.turns+=1
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped)==2:
                                if self.flipped[0]!= self.flipped[1]:
                                    self.block_game= True
                                    
                                    
                                else:
                                    self.flipped=[]
                                    self.turns-=1  # list emptied
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete= True
                                        else:
                                            self.level_complete= False
                                            break

        else:
            self.frame_count+=1
            if self.frame_count==FPS:
                self.frame_count=0
                self.block_game= False
                

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped=[]        
    def generate_level(self, level):
       
        self.aliens= self.select_random_aliens(self.level)
        self.level_complete= False
        self.rows= self.level + 1
        self.cols = 4
        self.generate_tileset(self.aliens)
       

    def generate_tileset(self, aliens): # at level 4 and 5 it will swap
        self.cols = self.rows= self.cols if self.cols>= self.rows else self.rows

        TILES_WIDTH =(self.img_width + self.cols+ self.padding) *3
        LEFT_MARGIN = RIGHT_MARGIN= (self.width - TILES_WIDTH)//2
        self.tiles_group.empty()
        for i in range(len(aliens)):
            
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i %self.cols))
            y = 2*self.margin_top + (i // self.rows *(self.img_height + self.padding))
            tile = Tile(aliens[i], x, y)     #object o class Tile
            self.tiles_group.add(tile)       

    def select_random_aliens(self , level):
        
                  aliens= random.sample(self.all_aliens,(self.level + self.level +2))
                  aliens_copy= aliens.copy() #duplicate
                  aliens.extend(aliens_copy)
                  random.shuffle(aliens)
                  return aliens


    def user_input(self):
        
        for event in event_list:
            if event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
                 
                 
                 if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()): # when click on sound icon
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle= self.sound_on
                        pygame.mixer.music.unpause()
                 if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_video_playing:
                        self.is_video_playing= False
                        self.video_toggle=self.stop
                    else:
                        self.is_video_playing=True
                        self.video_toggle=self.play
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and self.level_complete:
                    self.level+= 1
                    if self.level>=6:
                        self.level=1 
                    self.generate_level(self.level)
            
            
           
    def draw(self):
        Screen.fill(BLACK)
        
        #fonts
        title_font = pygame.font.Font("fonts/BungeeShade-Regular.ttf", 52)
        content_font = pygame.font.Font("fonts/TitilliumWeb-SemiBold.ttf", 28)

        #text
        title_text= title_font.render('_MEMORY GAME_', True , WHITE)
        title_rect= title_text.get_rect(midtop = (WINDOW_WIDTH//2,10))
        
        level_text=content_font.render('Level '+str(self.level), True, (255,215,0))
        level_rect=level_text.get_rect(midtop = (WINDOW_WIDTH//2,70))

        info_text=content_font.render('FIND SIMILAR OF EACH',True, (255,165,0))
        info_rect=info_text.get_rect(midtop = (WINDOW_WIDTH//2,100))
        
        turns_text=content_font.render('Card-turns: '+str(self.turns),True, (0,255,0))
        turns_rect=turns_text.get_rect(midbottom = (100,150))
        
        
        def menu_bar(self):
             Screen.blit(instruction_exit,(40,670))
             check_rect=pygame.draw.rect(Screen, (255, 215, 0), pygame.Rect(28,250, 140, 70), 7, 15)
             solve_rect=pygame.draw.rect(Screen, (255, 215,0), pygame.Rect(28,330, 140, 70), 7, 15)
             demo = title2_font.render("Demo", True, (255, 255, 255))
             Screen.blit(demo, (47, 268))

             Ruless = title2_font.render("Rules", True, (255, 255, 255))
             Screen.blit(Ruless, (40, 348))
             if game_paused==True:
                  pygame.draw.rect(Screen,(192,192,192), pygame.Rect(225, 75, 830, 600))
                  pygame.draw.rect(Screen,(255,255,255), pygame.Rect(225, 75, 830, 600),8,15)     
                  Rules=title2_font.render(("Rules"),True,(0,0,255))
                  Screen.blit(Rules,(550,100))
                  Rulesa=title3_font.render("* The rules for memory game are simple.",True,(160,32,240))
                  Rulesb=title3_font.render("* A group of several cards are given.",True,(160,32,240))
                  Rulesc=title3_font.render("* Player needs to flip one card at a time.",True,(160,32,240))
                  Rulesd=title3_font.render("* After flipping the first card, flip the  ",True,(160,32,240))
                  Rulese=title3_font.render("  second; if both the cards are same, number ",True,(160,32,240))
                  Rulesf=title3_font.render (" of turns will be null, otherwise each",True,(160,32,240))
                  Rulesg=title3_font.render(" flip of unequal pairs your score will be",True,(160,32,240))
                  Rulesh=title3_font.render(" exceed by two. After completion of present level,",True,(160,32,240))
                  Rulesi=title3_font.render(" a new level will generate with more cards.",True,(160,32,240))
                  Screen.blit(Rulesa,(240,165))
                  Screen.blit(Rulesb,(240,210))
                  Screen.blit(Rulesc,(240,255))
                  Screen.blit(Rulesd,(240,290))
                  Screen.blit(Rulese, (240,335))
                  Screen.blit(Rulesf, (240, 380))
                  Screen.blit(Rulesg,(240,425))
                  Screen.blit(Rulesh,(240,460))
                  Screen.blit(Rulesi,(240,500))
                  global elipse_rect 
                  elipse_rect=pygame.draw.ellipse(Screen,(255, 0, 0),(524,588,140,65),3)
                  Back=title2_font.render("Back",True,(0,0,255))
                  Screen.blit(Back,(550,600))
                  
               
        def demo(self):
            if game_paused2==True:

                pygame.draw.rect(Screen,(254,200,200), pygame.Rect(205, 75, 950, 600))
                Screen.blit(_1,(230,125))
                Screen.blit(_2,(450,125))
                Screen.blit(_3,(680,125))
                Screen.blit(_4,(910,125))
                Screen.blit(_5,(230,400))
                Screen.blit(_6,(450,400))
                Screen.blit(_7,(680,400))
                Screen.blit(_8,(910,400))
                pygame.draw.rect(Screen,(0,0,254), pygame.Rect(205, 75, 950, 600),8,15)
                global elipse2_rect
                elipse2_rect=pygame.draw.ellipse(Screen,(92, 254, 95),(570,600,145,65),4)
                Back=title2_font.render("Back",True,(254,0,0))
                Screen.blit(Back,(590,600))

                       
                               
        if self.is_video_playing:
             if self.success:      # self success is true
                 Screen.blit(pygame.image.frombuffer(self.img.tobytes(),self.shape,'BGR'),(0,0))
             else:       # loop to continue video
                self.get_video()
        else :
             Screen.blit(pygame.image.frombuffer(self.img.tobytes(),self.shape,'BGR'),(0,0))
        if not self.level == 5:
            next_text = content_font.render('level complete. press space for next level', True, WHITE)
        else:
            next_text = content_font.render('congrats. you won.press space to play again', True, WHITE)
        next_rect = next_text.get_rect(midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT-40))
        
           
        
        Screen.blit(title_text, title_rect)
        Screen.blit(title_text,title_rect)
        Screen.blit(level_text, level_rect)
        Screen.blit(info_text,info_rect)
        Screen.blit(turns_text,turns_rect)
        pygame.draw.rect(Screen, WHITE,(WINDOW_WIDTH-90,0,100,50))
        
        Screen.blit(self.video_toggle,self.video_toggle_rect)
        Screen.blit(self.music_toggle,self.music_toggle_rect)
       

        # call tileset
        # call menu bar and demo
        self.tiles_group.draw(Screen)
        menu_bar(Screen)
        demo(Screen)
        self.tiles_group.update()
        

        if self.level_complete:
            Screen.blit(next_text,next_rect)
    def get_video(self):
        self.cap=cv2.VideoCapture('bgv2.mp4')
        self.success,self.img= self.cap.read()  
        self.shape=self.img.shape[1::-1]  
       
       
       

       
        
#TO SHOW THE PROGRAM ,10 PIXEL FROM TOP AND CENTRE FROM HORIZONTAL axis

WHITE = (255 ,255,255)
RED = (255 , 0, 0)
BLACK =(0 , 0 , 0)

FPS= 10
Clock = pygame.time.Clock()




game=Game()  

running = True

while running:
    
        
        
    event_list = pygame.event.get() 
    for event in event_list:
        if event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos=pygame.mouse.get_pos()
                 w,t=pos
                 if check_rect.collidepoint(w,t):
                   
                   game_paused=True
                 elif game_paused==True:
                     if elipse_rect.collidepoint(w,t):
                         game_paused=False
                 elif solve_rect.collidepoint(w,t):
                     game_paused2=True
                 elif game_paused2==True:
                      if elipse2_rect.collidepoint(w,t):
                           game_paused2=False
                      
        if event.type == pygame.QUIT:
            running= False
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                  running = False
    
    game.update(event_list)
    # calling update method from game object
    pygame.draw.rect(Screen, (0,0,255), (0,0,WINDOW_WIDTH,WINDOW_HEIGHT), 5)
    pygame.display.update()
    Clock.tick(FPS)
pygame.quit()