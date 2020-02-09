import random #for generating randon number
import sys #we will use sys.exit() to exit the game
import pygame
from pygame.locals import * #basic Pygame import


#global variabls for games
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "gallery/sprites/bird.png"
BACKGROUND = "gallery/sprites/background.png"
PIPE = "gallery/sprites/pipe.png"


def welcomeScreen():

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES["message"].get_height())/2)
    messagey = int(SCREENHEIGHT *0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if return click on close button
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if user press up or space key
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key== K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES["background"], (0,0))
                SCREEN.blit(GAME_SPRITES["player"], (playerx,playery))
                SCREEN.blit(GAME_SPRITES["message"], (messagex,messagey))
                SCREEN.blit(GAME_SPRITES["base"], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    #create 2 pipes for litting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my list of upper pipes
    upperPipes = [
        {"x":SCREENWIDTH+200, "y":newPipe1[0]["y"]},
        {"x":SCREENWIDTH+200+(SCREENWIDTH/2), "y":newPipe2[0]["y"]}
    ]
    #Lower Pipes
    lowerPipes = [
        {"x": SCREENWIDTH + 200, "y": newPipe1[1]["y"]},
        {"x": SCREENWIDTH + 200 + (SCREENWIDTH / 2), "y": newPipe2[1]["y"]}
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 #Velocity while flapping
    playerFlapped = False #only true when player is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type ==KEYDOWN and(event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS["wing"].play()

        crashTest = iscollide(playerx, playery, upperPipes, lowerPipes) #return true if player is crashed
        if crashTest:
            return

        #check for score
        playerMidPos = playerx +GAME_SPRITES["player"].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe["x"] + GAME_SPRITES["pipe"][0].get_width()/2
            if pipeMidPos <= playerMidPos <= pipeMidPos+4:
                score += 1
                print(f"Score: {score}")
                GAME_SOUNDS["point"].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES["player"].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)



        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe["x"] += pipeVelX
            lowerPipe["x"] += pipeVelX


        #add a new pipe when first pipe is about cross out of screen
        if  0 < upperPipes[0]["x"] <5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        #if pipe out of screen remove it
        if upperPipes[0]["x"] < -GAME_SPRITES["pipe"][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit the sprites
        SCREEN.blit(GAME_SPRITES["background"], (0,0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES["pipe"][0], (upperPipe["x"],upperPipe["y"]))
            SCREEN.blit(GAME_SPRITES["pipe"][1], (lowerPipe["x"],lowerPipe["y"]))

        SCREEN.blit(GAME_SPRITES["base"], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES["player"], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0 #width score will take to blith
        for digit in myDigits:
            width = GAME_SPRITES["numbers"][digit].get_width()

        xoffset = (SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES["numbers"][digit], (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES["numbers"][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def iscollide(playerx, playery, upperPipes, lowerPipes):
    if playery >= GROUNDY - GAME_SPRITES["player"].get_height() or playery < 0:
        GAME_SOUNDS["hit"].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES["pipe"][0].get_height()
        if(playery < pipeHeight + pipe["y"] and abs(playerx - pipe["x"]) < GAME_SPRITES["pipe"][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES["player"].get_height() > pipe["y"]) and abs(playerx - pipe["x"]) < GAME_SPRITES["pipe"][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False



def getRandomPipe():
    """
    Generate 2 pipe (top an bottom)
    """
    pipeHeight = GAME_SPRITES  ["pipe"][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT- GAME_SPRITES["base"].get_height()-1.2*offset))
    pipex = SCREENWIDTH +10
    y1 = pipeHeight-y2+offset
    pipe = [
        {"x": pipex, "y": -y1},
        {"x": pipex, "y": y2}
    ]
    return pipe


if __name__ == '__main__':
    #This is the main point from where game will start
    pygame.init() #initialize pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird (RAJAT HADA)")
    GAME_SPRITES["numbers"] = (
        pygame.image.load("gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("gallery/sprites/1.png").convert_alpha(),
        pygame.image.load("gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("gallery/sprites/7.png").convert_alpha(),
        pygame.image.load("gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("gallery/sprites/9.png").convert_alpha()
    )

    GAME_SPRITES["message"] = pygame.image.load("gallery/sprites/message.png").convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load("gallery/sprites/base.png").convert_alpha()
    GAME_SPRITES["pipe"] = (
        pygame.transform.rotate(pygame.image.load("gallery/sprites/pipe.png").convert_alpha(), 180),
        pygame.image.load("gallery/sprites/pipe.png").convert_alpha()
    )

    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES["player"] = pygame.image.load(PLAYER).convert_alpha()


    #game sounds
    GAME_SOUNDS["die"] = pygame.mixer.Sound("gallery/audio/die.wav")
    GAME_SOUNDS["hit"] = pygame.mixer.Sound("gallery/audio/hit.wav")
    GAME_SOUNDS["point"] = pygame.mixer.Sound("gallery/audio/point.wav")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("gallery/audio/swoosh.wav")
    GAME_SOUNDS["wing"] = pygame.mixer.Sound("gallery/audio/wing.wav")


    while True:
        welcomeScreen() #shows welcomscreen untill pressing any button
        mainGame() #Main game function



