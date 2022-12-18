import pygame as pg
import sys
import os
import random
pg.init()

WIDTH, HEIGHT = 350,450
WIN = pg.display.set_mode((WIDTH,HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
x = pg.image.load(os.path.join("./assets/X.png"))
o = pg.image.load(os.path.join("./assets/o.png"))
gameOver=False
human=-1
ai=1
player=ai
font = pg.font.Font('freesansbold.ttf', 32)
coords = {(0,0):(10,10),(0,1):((WIDTH//3)+10,0),(0,2):(2*(WIDTH//3)+10,0),
        (1,0):(10,(WIDTH//3)+15),(1,1):((WIDTH//3)+10,(WIDTH//3)+15),(1,2):(2*(WIDTH//3)+10,(WIDTH//3)+15),
        (2,0):(10,2*(WIDTH//3)+15),(2,1):((WIDTH//3)+10,2*(WIDTH//3)+15),(2,2):(2*(WIDTH//3)+10,2*(WIDTH//3)+15)}

moves=0
played=[]
board=[[0,0,0],[0,0,0],[0,0,0]]
first_move = [[0,0],[0,2],[1,1],[2,0],[2,2]]
scores = {'X won':1,'O won':-1,'draw':0}
#x is 1
#o is -1
LINE1 = pg.Rect(WIDTH//3 - 5, 0, 10, WIDTH)
LINE2 = pg.Rect(2*(WIDTH//3) - 5, 0, 10, WIDTH)
LINE3 = pg.Rect(0,WIDTH//3+5,WIDTH,10)
LINE4 = pg.Rect(0,2*WIDTH//3+5,WIDTH,10)
LINE5 = pg.Rect(0,WIDTH,WIDTH,10)

def bestMove(board):
    Bestscore = -9999
    for i in range(3):
        for j in range(3):
            if board[i][j]==0:
                board[i][j]=ai
                score = minimax(board,False)
                board[i][j]=0
                if(score>Bestscore):
                    Bestscore=score
                    BestMove = [i,j]
    return BestMove              




def minimax(board,isMaximizing):
    #return 1
    ans = result(board)
    if ans:
        return scores[ans]
    if isMaximizing:
        bestScore=-9999
        for i in range(3):
            for j in range(3):
                if board[i][j]==0:
                    board[i][j]=ai
                    score = minimax(board,False)
                    board[i][j]=0
                    bestScore = max(score,bestScore)
        return bestScore
    if not(isMaximizing):
        bestScore=9999
        for i in range(3):
            for j in range(3):
                if board[i][j]==0:
                    board[i][j]=human
                    score = minimax(board,True)
                    board[i][j]=0
                    bestScore = min(score,bestScore)
        return bestScore
    
def draw_window():
    global gameOver
    WIN.fill(WHITE)
    pg.draw.rect(WIN,BLACK,LINE1)
    pg.draw.rect(WIN,BLACK,LINE2)
    pg.draw.rect(WIN,BLACK,LINE3)
    pg.draw.rect(WIN,BLACK,LINE4)
    pg.draw.rect(WIN,BLACK,LINE5)

    for i in range(3):
        for j in range(3):
            if board[i][j]==1:
                WIN.blit(x,coords[(i,j)])
            if board[i][j]==-1:
                WIN.blit(o,coords[(i,j)])
    res = result(board)
    if res:
        text = font.render(res, True, green, blue)
        textRect = text.get_rect()
        textRect.center = (WIDTH//2, HEIGHT-50)
        WIN.blit(text,textRect)
        gameOver=True
    pg.display.update()

def findSq(x,y):
    if x<WIDTH//3 and y<WIDTH//3:
        return (0,0)
    if x<WIDTH//3 and WIDTH//3<y<(2*WIDTH)//3:
        return (1,0)
    if x<WIDTH//3 and (2*WIDTH)//3<y<WIDTH:
        return (2,0)
    if WIDTH//3<x<(2*WIDTH)//3 and y<WIDTH//3:
        return (0,1)
    if WIDTH//3<x<(2*WIDTH)//3 and WIDTH//3<y<(2*WIDTH)//3:
        return (1,1)
    if WIDTH//3<x<(2*WIDTH)//3 and (2*WIDTH)//3<y<WIDTH:
        return (2,1)
    if (2*WIDTH)//3<x<WIDTH and y<WIDTH//3:
        return (0,2)
    if (2*WIDTH)//3<x<WIDTH and WIDTH//3<y<(2*WIDTH)//3:
        return (1,2)
    if (2*WIDTH)//3<x<WIDTH and (2*WIDTH)//3<y<WIDTH:
        return (2,2)

def draw(board):
    isdraw = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                isdraw=False
    return isdraw

def result(board):
    #horizontal 3s
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == 1:
            return 'X won'
        if board[i][0] == board[i][1] == board[i][2] == -1:
            return 'O won'

    #vertical 3s
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == 1:

            return 'X won'
        if board[0][i] == board[1][i] == board[2][i] == -1:

            return 'O won'
    
    #cross 3s
    if board[0][0] == board[1][1] == board[2][2] == 1:
        return 'X won'
    if board[0][0] == board[1][1] == board[2][2] == -1:
        return 'O won'
    if board[0][2] == board[1][1] == board[2][0] == 1:
        return 'X won'
    if board[0][2] == board[1][1] == board[2][0] == -1:
        return 'O won'
    
    if draw(board):
        return 'draw'

def isvalid(pos):
    global board
    (x,y)=findSq(pos[0],pos[1])
    if board[x][y]==0:
        return True
    return False 

def play_move(pos,player):
    global board,moves
    if player==ai:
        board[pos[0]][pos[1]]=1
        moves+=1
    elif player == human:
        (x,y)=findSq(pos[0],pos[1])
        board[x][y]=-1
        moves+=1



def main():
    global board,moves,played,gameOver,player
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run=False
                pg.quit()
                sys.exit()
            if draw(board):
                gameOver=True
            if player==ai and not(gameOver) and moves<10:
                if moves == 0:
                    play_move(first_move[random.randint(0,4)],player)
                    player=human
                else:
                    play_move(bestMove(board),player)
                    player=human
            if event.type == pg.MOUSEBUTTONDOWN and moves<10 and not(gameOver) and player==human:
                pos=pg.mouse.get_pos()
                if(pos[0]<WIDTH and pos[1]<WIDTH):
                    if isvalid(pos):
                        play_move(pos,player)
                        player=ai
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and gameOver:
                    board=[[0,0,0],[0,0,0],[0,0,0]]
                    moves=0
                    played=[]
                    player=ai
                    gameOver=False
            draw_window()
    main()

if __name__ == "__main__":
    main()