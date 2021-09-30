import pygame
import random
import os

pygame.mixer.init()

pygame.init()

#define colors R G B VALUES
white = (255,255,255)
red = (255,0,0)
green = (0 ,255,0)
black = (0,0,0)

screen_width = 1000
screen_height = 600

clock = pygame.time.Clock() #creates a clock

gamewindow = pygame.display.set_mode((screen_width,screen_height))

#background image
bg = pygame.image.load('snakes.png')
# trandform takes two input first the loaded image and second the screen display of the game 
#conert_alpha help to ignore the effects of image blitting on the game speed
bg = pygame.transform.scale(bg , (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("SNAKES")
pygame.display.update()

font = pygame.font.SysFont(None,45) #stores the type of font for late use
def text_score(text , color , x , y):
    screen_text = font.render(text , True , color)
    gamewindow.blit(screen_text , [x,y])   #update the text on the screen

def plot_snake(window , color , snake_ls , size):
    for x,y in snake_ls: #takesthe input x and y from the list
        pygame.draw.rect(window , color , [x, y, size, size])
    
def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.fill(black)
        text_score("welcome", red , 400,200)
        text_score("PRESS SPACEBAR TO PLAY", red , 300,250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Nine Lives.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        
        pygame.display.update()
        clock.tick(60)

def gameloop():
    
    #game specific variable
    exit_game = False
    game_over = False
    snake_x = 45
    velocity_x = 0
    velocity_y = 0
    velocity = 5
    snake_y = 50
    size = 15
    food_x = random.randint(20,screen_width/2) #generates a random no. between 0 and screen and set it as its coordinate 
    food_y = random.randint(20,screen_height/2)
    score = 0
    fps = 60
    snake_ls = []
    snake_length = 1
    
    #creting non existent score file
    if (not os.path.exists("score.txt")):
        with open("score.txt","w") as f:
            f.write("0")
            
    with open("score.txt","r") as f:
        hiscore = f.read()
    
    while not exit_game:
        if game_over:
            with open("score.txt","w") as f:
                f.write(str(hiscore))
            gamewindow.fill(black)
            text_score("GAME OVER \n PRESS CONTINUE TO PLAY",green , 200 , 300)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
            
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = velocity
                        velocity_y = 0
                        
                    if event.key == pygame.K_LEFT:
                        velocity_x = -velocity
                        velocity_y = 0
                        
                    if event.key == pygame.K_UP:
                        velocity_y = -velocity
                        velocity_x = 0#- moves the object uppward
                        
                    if event.key == pygame.K_DOWN:
                        velocity_y = velocity
                        velocity_x = 0#+ moves the object downward
                        
                    if event.key == pygame.K_q:
                            score += 10
                        
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score = score + 10
                food_x = random.randint(20,screen_width/2)
                food_y = random.randint(20,screen_height/2)
                snake_length += 5#coordinate
                
                
            if score > int(hiscore):
                hiscore = score
                
            gamewindow.fill(white)
            gamewindow.blit(bg, (0,0))
            text_score("Score : " + str(score) + "  Hiscore : " + str(hiscore) , green  , 5 , 5)
            
            #creates  a list with the coordinates of the head of the sc\nake 
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_ls.append(head)
            
            if len(snake_ls)> snake_length:
                del snake_ls[0]
            
            if head in snake_ls[:-1]:
                game_over =True
                pygame.mixer.music.load('Alien Beam.mp3')
                pygame.mixer.music.play()
            
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('Alien Beam.mp3')
                pygame.mixer.music.play()
            
            plot_snake(gamewindow,white, snake_ls, size)
            
            #creates a rectangle and takes input :----> display , colour, and a list containing object coordinate and size
            pygame.draw.rect(gamewindow , red , [food_x , food_y , size, size])
        pygame.display.update()
        clock.tick(fps) #give us the required fps
        
        
    pygame.quit()
    quit()


welcome()