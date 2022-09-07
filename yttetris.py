import pygame
import random
from pygame import mixer

pygame.font.init()
pygame.init()
mixer.music.load('Music.mp3')
 
# GLOBAL VARS
screen_width = 800
screen_height = 700
play_width = 300  
play_height = 600  
block_size = 30
Score=0
fall_speed=0
 
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height
 
# BLOCKS 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

background=pygame.image.load("tetris.jpg")
bg=pygame.transform.scale(background,(screen_width,screen_height))
image=pygame.image.load("landscape.jpg")
landscape=pygame.transform.scale(image,(screen_width,screen_height))

menu_background=pygame.image.load("menu.jpg")
meniu=pygame.transform.scale(menu_background,(screen_width,screen_height))

shapes = [Z, I, O, L, T]
shape_colors = [(0, 255, 85), (183,189,11), (253,11,11), (11,253,253), (11,253,181)]
# accesez formele cu un index de la 0 la 6

class Block:
    rows = 20  # y
    columns = 10  # x
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  
 
 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                grid[i][j]=locked_positions[(j,i)]
    return grid

def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines
 
 
def convert_shape(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions

def free_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True
 

def get_shape():
    global shapes, shape_colors
 
    return Block(5, 0, random.choice(shapes))
 
 
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('corbel', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
 
def draw_text(text,size,color,x,y,surface):
    font = pygame.font.SysFont('freestylescript', size, bold=True)
    label=font.render(text,1,color)
    surface.blit(label,[x,y])

 
def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
 
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    global Score

    Score+=inc*inc*10
 
 
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans',40)
    label = font.render('Next Shape', 1, (255,255,255))
 
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))
 
 
def draw_window(surface):

    surface.blit(landscape,(0,0))
    font = pygame.font.SysFont('castellar', 70,bold=True)
    label = font.render('TETRIS', 1, (255,128,0))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (0, 213, 255), (top_left_x, top_left_y, play_width, play_height), 5)
    #pygame.display.update()

    font2 = pygame.font.SysFont('castellar', 20,bold=True)
    sc=font2.render('Score: '+ str(Score),1,(255,255,255))
    surface.blit(sc, [600,70] )
 
def pause():
    paused = 1
    while paused:
        draw_text_middle("Game paused  (press SPACE to continue)",40,(255,255,255),win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = 0
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = 0
        pygame.display.update()

 
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

 
def main():
    global grid
    locked_positions = {}  
    grid = create_grid(locked_positions)
 
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
 
    while run:
        global fall_speed
 
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
 
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (free_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not free_space(current_piece, grid):
                        current_piece.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not free_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_RETURN:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not free_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not free_space(current_piece, grid):
                        current_piece.y -= 1   

                if event.key == pygame.K_SPACE:
                    pause()       
  
 
        shape_pos = convert_shape(current_piece)
 
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
 
        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            clear_rows(grid, locked_positions)
 
        draw_window(win)
        draw_next_shape(next_piece, win)
    
        pygame.display.update()
 
        if check_lost(locked_positions):
            run = False
 
    draw_text_middle("You Lost!", 150, (233,247,25), win)
    pygame.display.update()
    pygame.time.delay(2000)
    menu()

def menu():
    run = True
    state=1 


    while run:
    
        win.blit(meniu,[0,0])
        if state ==1:
            pygame.draw.rect(win,(23,57,89),pygame.Rect(345,400,120,50))
        elif state ==2:
            pygame.draw.rect(win,(23,57,89),pygame.Rect(317,500,180,50))
        elif state == 3:
            pygame.draw.rect(win,(23,57,89),pygame.Rect(346,600,120,50))

        draw_text("WELCOME!",80,(0,0,0),240,70,win)
        draw_text("Please select a game mode",60,(0,0,0),150,250,win)
        draw_text("EASY", 50,(0,0,0),350,400,win)
        draw_text("MEDIUM", 50,(0,0,0),320,500,win)
        draw_text("HARD", 50,(0,0,0),350,600,win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_DOWN:
                    state+=1
                    if state==4:
                        state=1
                if event.key ==pygame.K_UP: 
                        state-=1
                        if state ==0:
                            state=3
                if event.key ==pygame.K_RETURN:
                    global fall_speed
                    if state == 1:
                        fall_speed=0.27
                    elif state ==2:
                        fall_speed=0.20
                    elif state == 3:
                        fall_speed=0.13

                    start_game()
    pygame.quit()
 
 
def start_game():
    run = True

    while run:
        #win.fill((0,0,0))
        #Music
        mixer.music.play(-1)
        win.blit(bg,[0,0])
        draw_text_middle('Press any key to begin...', 70, (25, 166, 247), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
 
 
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
 
menu()  # start game