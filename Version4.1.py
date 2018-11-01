
#1.
#Atherosclerosis Blasters
#Version 4.1*
#Fully Documented Version
#File Created 28/07/2015
#Created by Liam Noonan, co-authored by Jonathan Noonan


#*screen compatibility improvements, added good characters, using new images.
#--------------------------------------------------------




#Core
#2 Imports
import sys
from pygame import *
import pygame
import random
import os
#initialise
init()
pygame.init()





#----------------------------------------------------------------------------------------------------------------------------------------------------




#3
#Define Classes, Functions and Global Variables

#Create universal class for sprites
class Sprite:
        def __init__(self, xpos, ypos, filename):
                self.x = xpos
                self.y = ypos
                self.bitmap = image.load(filename).convert()
                self.bitmap.set_colorkey((255,255,255))
                self.filename = filename
        def set_position(self, xpos, ypos):
                self.x = xpos
                self.y = ypos
        def Change(self):
                SyringeColours = ['data/BlueSyringe.png','data/PinkSyringe.png','data/PurpleSyringe.png','data/GreenSyringe.png','data/OrangeSyringe.png']
                self.filename = random.choice(SyringeColours)
                self.bitmap = image.load(self.filename).convert()
                self.bitmap.set_colorkey((255,255,255))
        def render(self):
                screen.blit(self.bitmap, (self.x, self.y))




class Monsters:
        x = 0
        y = 0
        def __init__(self, filename, character, Hit):
                self.bitmap = image.load(filename).convert()
                self.bitmap.set_colorkey((255,255,255))
                self.filename = filename
                self.x = Monsters.x + random.randint(120,750)
                self.y = Monsters.y + random.randint(100,300)
                self.xspeed = random.randint(25,45) / 20
                self.yspeed = random.randint(21,30) / 20
                self.character = character
                self.Hit = Hit
        def Moving(self,xspeed,yspeed):

                if self.x > 800:
                        self.xspeed *= -1
                if self.x < 30:
                        self.xspeed *= -1
                if self.y > 500:
                        self.yspeed *= -1
                if self.y < 100:
                        self.yspeed *= -1        
                        
                self.x = self.x + self.xspeed 
                self.y = self.y + self.yspeed              
        def Expose(self):
                self.bitmap = image.load('data/' + self.character + '.png').convert()
                self.bitmap.set_colorkey((255,255,255))                
        def render(self):
                screen.blit(self.bitmap, (self.x, self.y))



                                
def Bombs(BombList):
        for count in range(len(BombList)):
                try:
                        
                        if BombList[count] .y > -100:

                                BombList[count].y -= 6

                        else:
                                del BombList[count]
                except IndexError:
                        pass
                
        

def HitDetection(BombList,TestEnemy):
        global Score
        try:
                
                for count in range(len(BombList)):
                        for counter in range(len(TestEnemy)):
                                if Intersect(BombList[count].x,BombList[count].y,TestEnemy[counter].x,TestEnemy[counter].y):
                                        if TestEnemy[counter].character[3:] == BombList[count].filename[5:-8]:
                                                if TestEnemy[counter].Hit == False:
                                                        TestEnemy[counter].Expose()
                                                        TestEnemy[counter].Hit = True
                                                        del BombList[count]
                                                        Score += 10
                                                        return
                                                
                                                
                                                if TestEnemy[counter].Hit == True:
                                                        
                                                        del TestEnemy[counter]
                                                        #MultiKill not currently in use -overpowered?
                                                        #for Multikill in range (len(TestEnemy)):
                                                                #if TestEnemy[counter].character == TestEnemy[Multikill].character and TestEnemy[Multikill].Hit == True and TestEnemy[counter].Hit == True:
                                                                        #del TestEnemy[Multikill]
                                                                        #del TestEnemy[counter]
                                                                        #del BombList[count]
                                                                        #Score += 10
                                                        del BombList[count]
                                                        Score += 10
                                        elif TestEnemy[counter].character == "BadGood":
                                                if TestEnemy[counter].Hit == True:
                                                        Score -= 30
                                                        #print('HIT')
                                                        del TestEnemy[counter]
                                                        del BombList[count]
                                                else:
                                                                TestEnemy[counter].Expose()
                                                                TestEnemy[counter].Hit = True
                                                                del BombList[count]
                                                                return
                                                        
                                                
                                                                          
        except IndexError:
                pass




                                        
        
#Define Intersect Function
def Intersect(s1_x, s1_y, s2_x, s2_y):
	if (s1_x > s2_x - 32) and (s1_x < s2_x + 32) and (s1_y > s2_y - 32) and (s1_y < s2_y + 32):
		return 1
	else:
		return 0

	
#Define message to screen function (specifically, score indicator)
def MessageToScreen(msg,colour,x,y,size):
        if size == "small":
                Text = font.render(msg,True,colour)
        if size == "big":
                Text = bigfont.render(msg,True,colour)
        screen.blit(Text, (x,y))

        
def Render(Score,Timer,player,TestEnemy,BombList):

        screen.fill(Black)
        #block image transfer background to screen   
        screen.blit(backdrop, (0, 0))
        #display score                            
        MessageToScreen("Score: " + (str(Score)), White, 380, 660, "small")
        #print time elapsed to screen (Bottom Right)                   
        MessageToScreen(str(Timer[0]) + "  :  " + str(Timer[1]) , White, 750, 660, "small")
        #render player
        player.render()
        #render Enemies and call Moving function to update their positions
        for count in range(len(TestEnemy)):
                TestEnemy[count].Moving(0,0)
                TestEnemy[count].render()
        #render bombs
        for count in range(len(BombList)):
                BombList[count].render()
        #update frame
        display.update()
        #time delay, basically housekeeping. Without these game would run as fast as PC could handle the commands so is excessively intensive
        time.delay(5)

        
#Define Text for Screens
def Controls(Score):
        
        
        Menu = True        
        while Menu == True:
                
                for ourevent in event.get():
                        if ourevent.type == QUIT:
                                os._exit(1)
                        if ourevent.type == KEYDOWN:
                                if ourevent.key == K_ESCAPE or ourevent.key == K_q:
                                        os._exit(1)
                                if ourevent.key == K_p:
                                        return "Run"
                        else:
                                screen.fill(Black)
                                screen.blit(Screen1, (0, 0))
                                display.update()
                                
        


#----------------------------------------------------------------------------------------------------------------------------------------------------

#declare global variables
      
#create background - ,pygame.FULLSCREEN
screen = pygame.display.set_mode((900,700))
#assign background image to variable for later use
backdrop = image.load('data/BackGroundV2.bmp').convert()
Screen1 = image.load('data/Screen1.bmp').convert()
Screen2 = image.load('data/Screen2.bmp').convert()
#defined colours for text:
White = (255,255,255)
Black = (0, 0, 0)
#define font(s)
font = pygame.font.SysFont("arial",25)
bigfont = pygame.font.SysFont("arial",50)

#set mouse cursor to invisible
pygame.mouse.set_visible(False)
#sets how long before next key event (1 ms)
key.set_repeat(5, 5)

#display caption
display.set_caption('Atherosclerosis Blasters!')

#create game clock
clock = pygame.time.Clock()
#creates timer (triggers event every 1000ms)
ClockCount = pygame.USEREVENT+2
Milliseconds = 1000
ClockTimer = pygame.time.set_timer(ClockCount, Milliseconds)

#create array for clock values [minutes,seconds]
Timer = [1,30]

#set clock event to change syringe (and bomb) colour every five seconds or so (milliseconds are weirdly innacurate due to clock tick rate (hence 6000 instead of 5000)
PlayerChange = pygame.USEREVENT+1
ChangeTime = 6000
PlayerTimer = pygame.time.set_timer(PlayerChange, ChangeTime)
 
#define list of available syringe colours (these are spliced and concatenated to load bomb colours to match)
SyringeColours = ['data/BlueSyringe.png','data/PinkSyringe.png','data/PurpleSyringe.png','data/GreenSyringe.png','data/OrangeSyringe.png']
#set player speed
PlayerSpeed = 5.7
#create player sprite
player = Sprite(390, 520, random.choice(SyringeColours))
#declare array for bombs (deleted in Bombs() function when their y value is beyond the screen boundary 
BombList = []

#declare array for enemies
TestEnemy = []
MonsterColours = ['BadBlue','BadGreen','BadPurple','BadOrange','BadPink','BadGood']


#Define score variable, global for multi-func access        
Score = 0
SpamCount = 0
BombList.append(Sprite((player.x - 10), player.y, ('data/' + player.filename[5:-11] + 'Bomb.png')))
#set running to false by default, until player presses P for play.
Running = False

#----------------------------------------------------------------------------------------------------------------------------------------------------

def Runtime(Score, Timer, BombList):

        global SpamCount
        
        #block image transfer background to screen   
        screen.blit(backdrop, (0, 0))

        #get user events, ie player inputes
        for userevent in event.get():
                if userevent.type == QUIT:
                                os._exit(1)
                                
                if userevent.type == KEYDOWN:
                        if userevent.key == K_ESCAPE or userevent.key == K_q:
                                os._exit(1)
                        if userevent.key == K_n:
                                return "Back"
                        
                        if userevent.key == K_RIGHT and player.x < 850:
                                player.x += PlayerSpeed        
                        if userevent.key == K_LEFT and player.x > -25:
                                player.x -= PlayerSpeed
                                
                if userevent.type == KEYUP:
                        if userevent.key == K_b:
                                player.Change()
                        if userevent.key == K_SPACE and len(BombList) < 3:
                                BombList.append(Sprite((player.x - 10), player.y, ('data/' + player.filename[5:-11] + 'Bomb.png')))
                                SpamCount += 1

                                

                                
                                

                #call player change function every five-ish seconds
                if userevent.type == PlayerChange:
                        player.Change()
                        Chance = random.randint(1,5)
                        if Chance == 2 or Chance ==5 or Chance ==3:
                                TestEnemy.append(Monsters(('data/BadGrey.png'),random.choice(MonsterColours),False))
                                

                
                #Check for clock event and increment time
                if userevent.type == ClockCount:
                        Timer[1] -= 1
                        if Timer[1] < 1:
                                Timer[0] -= 1
                                Timer[1] = 59
                        if Timer[1] > 59:
                                Timer[0] += 1
                                Timer[1] = Timer[1] - 59

        if SpamCount >= 4:
                player.Change()
                SpamCount = 0

        #if time is up, return to menu screen
        if Timer[0] == 0 and Timer[1] == 1:
                return "Back"

        #keeps four monsters on screen at all times
        if len(TestEnemy) < 4:
                TestEnemy.append(Monsters(('data/BadGrey.png'),random.choice(MonsterColours),False))
        if len(TestEnemy) > 5:
               del TestEnemy[-1]

        #call HitDetection Function        
        HitDetection(BombList,TestEnemy)
        #call Bombs Function to keep Bombs moving once fired and delete once out of range
        Bombs(BombList)
        #call Render Function
        Render(Score,Timer,player,TestEnemy,BombList)


#----------------------------------------------------------------------------------------------------------------------------------------------------



#                   !!!!!! Start of Runtime !!!!!



#Define MasterLoop
MasterLoop = True
#Start loop to keep game running indefinitely.
while MasterLoop == True:
        

        while Running == False:

                #if player presses P to start game
                if Controls(Score) == "Run":
                        #set timer and score accordingly, delete all exisitng monsters
                        screen.fill(Black)
                        screen.blit(Screen2, (0, 0))
                        display.update()
                        time.delay(5000)
                        del TestEnemy[:]
                        Timer = [1,30]
                        Score = 0
                        #spawn four enemies at start of game
                        for count in range(4):
                                TestEnemy.append(Monsters(('data/BadGrey.png'),random.choice(MonsterColours),False))
                                #print(TestEnemy[count].character)
                        #set Running as True to start Runtime loop
                        Running = True
                        break

        
        #if runtime function returns Back (player presses N for New game or Timer hits zero        
        if Runtime(Score, Timer, BombList) == "Back":
                #set running to false
                Running = False
                        
    
        
               

sys.exit       


        



        

      
        
        


        
