import pygame
import random

pygame.init()
pygame.font.init()

BLOCK_SIZE = 40
VERTICAL_BLOCKS = 16
HORIZONTAL_BLOCKS = 10
HEIGHT = (VERTICAL_BLOCKS + 1) * BLOCK_SIZE
WIDTH = (HORIZONTAL_BLOCKS + 2) * BLOCK_SIZE + 200
BOARD_WIDTH = BLOCK_SIZE * HORIZONTAL_BLOCKS
BOARD_HEIGHT = BLOCK_SIZE * VERTICAL_BLOCKS
WALL_COLOR = ((169,169,169))

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")
major_font = pygame.font.SysFont("Comic Sans MS", 100)
major_info_font = pygame.font.SysFont("Comic Sans MS", 60)
instruction_font = pygame.font.SysFont("Comic Sans MS", 40)
medium_font = pygame.font.SysFont("Comic Sans MS", 30)
subnote_font = pygame.font.SysFont("Clear Sans", 17)

lines = 0
high_score = 0
frequency = 20

#Information About Blocks:
#0: | (I)       #1: ▇ (O)      #2: ▙ (L)       #3: ▟ (J)
#4: ▚ (S)       #5: ▞ (Z)      #6: ⊥  (T)
block_positions =   [
                    [ [[0,0],[0,1],[0,-1],[0,-2]], [[0,0],[1,0],[-1,0],[-2,0]] ],
                    
                    [ [[0,0],[-1,0],[-1,-1],[0,-1]] ],

                    [ [[0,1],[-1,1],[-1,0],[-1,-1]], [[-1,0],[-1,-1],[0,-1],[1,-1]],
                      [[0,0],[-1,-1],[0,-1],[0,1]], [[0,0],[1,-1],[-1,0],[1,0]] ],

                    [ [[0,0],[0,1],[0,-1],[-1,1]], [[0,0],[-1,0],[1,0],[-1,-1]],
                      [[0,-1],[-1,-1],[-1,0],[-1,1]],  [[0,-1],[1,0],[-1,-1],[1,-1]]],
                    
                    [ [[0,0],[0,1],[-1,0],[-1,-1]], [[0,0],[0,-1],[1,-1],[-1,0]] ],

                    [ [[0,0],[0,-1],[-1,0],[-1,1]], [[0,0],[1,0],[0,-1],[-1,-1]] ],

                    [ [[0,0],[0,-1],[-1,0],[1,0]],  [[0,0],[0,-1],[0,1],[1,0]],
                      [[0,0],[-1,0],[1,0],[0,1]],   [[0,0],[-1,0],[0,-1],[0,1]] ],
                    ]

block_depths = [ [2,1], [1], [1,2,2,1], [1,1,2,2], [2,1], [2,1], [1,2,2,2]]

block_colors = [ [0,255,255], [255,255,0], [255,165,0], [0,0,255], [0,255,0], [255,0,0], [128,0,128], [255,255,255], [169,169,169]]

taken_squares = set()

board = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],]
        
temporary_occupied = []

class Wall:
    def __init__(self,start_x,start_y,vertical):
        self.start_x = start_x
        self.start_y = start_y
        self.vertical = vertical
        self.horizontal = not vertical
        if vertical:
            self.end_x = start_x
            self.end_y = self.start_y + BOARD_HEIGHT + BLOCK_SIZE
            self.repetitions = VERTICAL_BLOCKS + 2
        else:
            self.end_x = start_x + BOARD_WIDTH + BLOCK_SIZE
            self.end_y = self.start_y
            self.repetitions = HORIZONTAL_BLOCKS + 2
        self.color = WALL_COLOR
        self.size = BLOCK_SIZE-2
    
    def draw_on(self,surface):
        if self.vertical:
            x = self.start_x
            y = self.start_y
            for square in range(self.repetitions):
                pygame.draw.rect(surface, self.color, (x,y,self.size,self.size))
                y += BLOCK_SIZE
        else:
            x = self.start_x
            y = self.start_y
            for square in range(self.repetitions):
                pygame.draw.rect(surface, self.color, (x,y,self.size,self.size))
                x += BLOCK_SIZE

class Block:
    def __init__(self,type,frequency):
        self.x = 5
        self.y = 2
        self.rotation = 0
        self.type = type
        self.positions = []
        self.frequency = frequency
        for i in block_positions[self.type][self.rotation]:
            self.positions.append([self.x+i[0],self.y+i[1]])
        self.left = False
        self.right = False
    
    def move_down(self):
        if timer % self.frequency == 0:
            self.y = self.y + 1
    
    def place_on(self,board):
        for i in self.positions:
            x = i[0]
            y = i[1]
            board[y][x] = self.type
    
    def remove_from(self,board):
        for i in self.positions:
            x = i[0]
            y = i[1]
            board[y][x] = -1
    
    def move_right(self,board):
        valid = True
        for i in self.positions:
            x = i[0] + 1
            y = i[1]
            if x >= HORIZONTAL_BLOCKS or board[y][x] != -1:
                valid = False
                break
        if valid:
            self.x += 1
    
    def move_left(self,board):
        valid = True
        for i in self.positions:
            x = i[0] - 1
            y = i[1]
            if x < 0 or board[y][x] != -1:
                valid = False
                break
        if valid:
            self.x -= 1

    def rotate(self,board):
        valid = True
        number = len(block_depths[self.type])
        for i in block_positions[self.type][(self.rotation+1)%number]:
            x = self.x + i[0]
            y = self.y + i[1]
            if x < 0 or x >= HORIZONTAL_BLOCKS:
                valid = False
                break
            if y < 2 or y >= VERTICAL_BLOCKS+2:
                valid = False
                break
            if board[y][x] != -1:
                valid = False
                break
        if valid:
            self.rotation = (self.rotation + 1) % number
    
    def check_if_can_move_down(self,board):
        for i in self.positions:
            x = i[0]
            y = i[1]+1
            if y >= VERTICAL_BLOCKS+2 or board[y][x] != -1:
                return False
        return True

    def am_i_dead(self,board):
        for i in self.positions:
            x = i[0]
            y = i[1]
            if board[y][x] != -1:
                return 2
        for i in self.positions:
            x = i[0]
            y = i[1]
            if y < 2:
                return 1
        return 0
    
    def calculate_positions(self):
        self.positions = []
        for i in block_positions[self.type][self.rotation]:
            self.positions.append([self.x+i[0],self.y+i[1]])
    
    def drop(self,board):
        while self.check_if_can_move_down(board):
            self.y += 1
            self.calculate_positions()
    
    def handle_events(self,event,board,frequency):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
                self.left_start = 1
                self.move_left(board)
            elif event.key == pygame.K_RIGHT:
                self.right = True
                self.right_start = 1
                self.move_right(board)
            elif event.key == pygame.K_DOWN and frequency >= 2:
                self.frequency = 2
            elif event.key == pygame.K_r:
                self.rotate(board)
            elif event.key == pygame.K_UP:
                self.drop(board)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.frequency = frequency
            elif event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False
            
    def combined_movement(self,board,placed,dead,temporary_occupied):
        if self.right:
            if self.right_start % 8 == 0:
                self.move_right(board)
            self.right_start += 1
        if self.left:
            if self.left_start % 8 == 0:
                self.move_left(board)
            self.left_start += 1
        if self.check_if_can_move_down(board):
            self.move_down()
            placed = False
        else:
            placed = True
        self.calculate_positions()
        if placed and self.am_i_dead(board) == 2:
            dead = True   
        elif placed and self.am_i_dead(board) == 1:
            self.place_on(board)
            temporary_occupied = self.positions
            dead = True
        else:
            self.place_on(board)
            temporary_occupied = self.positions
        return placed,dead

walls = [Wall(0,0,True),
        Wall(0,BOARD_HEIGHT,False),
        Wall(BOARD_WIDTH+BLOCK_SIZE,0,True)]

def check_row(board,lines):
    full_rows = []
    for i in range(len(board)):
        full_row = True
        for j in range(len(board[i])):
            if board[i][j] == -1 or [j,i] in temporary_occupied:
                full_row = False
                break
        if full_row:
            lines += 1
            full_rows.append(i)
            for j in range(len(board[i])):
                board[i][j] = 7
    return full_rows,lines

def display_board(board,surface):
    for i in range(2,len(board)):
        for j in range(len(board[i])):
            if board[i][j] != -1:
                color = block_colors[board[i][j]]
                x = BLOCK_SIZE * (j+1)
                y = BLOCK_SIZE * (i-2)
                size = BLOCK_SIZE - 2
                pygame.draw.rect(surface, color, (x,y,size,size))

def display_next_block(next_type,surface):
    size = BLOCK_SIZE
    next_positions = []
    for i in block_positions[next_type][0]:
            x = (i[0] + 14) * size
            y = (i[1] + 3) * size
            draw = size - 2
            pygame.draw.rect(surface, block_colors[next_type], (x,y,draw,draw))

def pause_message(surface):
    paused = major_font.render("PAUSED", 1, (255,255,255))
    screen.blit(paused, (100,250 ))
    
def display_instructions(surface):
    instructions = subnote_font.render("INSTRUCTIONS:",1,(255,255,255))
    left_right = subnote_font.render("Arrows to move left and right",1,(255,255,255))
    speed_up =  subnote_font.render("Down arrow to move down quicker",1,(255,255,255))
    drop = subnote_font.render("Up arrow to drop block",1,(255,255,255))
    r = subnote_font.render("R to rotate",1,(255,255,255))
    spacebar = subnote_font.render("Spacebar to restart game",1,(255,255,255))
    pause = subnote_font.render("P to pause",1,(255,255,255))
    surface.blit(instructions,(490,440))
    surface.blit(left_right,(490,470))
    surface.blit(speed_up,(490,500))
    surface.blit(drop,(490,530))
    surface.blit(r,(490,560))
    surface.blit(spacebar,(490,590))
    surface.blit(pause,(490,620))

def display_game_state(surface,lines,frequency,high_score):
    lines = "Lines: "+str(lines)
    level = "Level: " + str(21-frequency)
    high_score = "High Score: " + str(high_score)
    lines = medium_font.render(lines,1,(255,255,255))
    level = medium_font.render(level,1,(255,255,255))
    high_score = medium_font.render(high_score,1,(255,255,255))
    surface.blit(lines,(490,250))
    surface.blit(level,(490,300))
    surface.blit(high_score,(490,350))


screen.fill((0,0,0))
for wall in walls:
    wall.draw_on(screen)
restart_message = instruction_font.render("Press the spacebar to start",1,(255,255,255))
screen.blit(restart_message,(60,350))
display_instructions(screen)
pygame.display.update()

reborn = False
dead = True

while True:
    clock.tick(40)
    events = pygame.event.get()

    if reborn:
        placed = False
        paused = False
        timer = 0
        frequency = 20
        next_type = random.randint(0,6)
        current = Block(next_type,frequency)
        dead = False
        reborn = False
        lines = 0
        board = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],]
    
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dead = True
                reborn = True
                if lines > high_score:
                    high_score = lines
            elif event.key == pygame.K_p:
                if not paused and not reborn:
                    paused = True
                    pause_message(screen)
                    pygame.display.update()
                elif paused and not reborn:
                    paused = False
            elif not dead:
                current.handle_events(event,board,frequency)
        elif not dead:
            current.handle_events(event,board,frequency)
    
    if not dead and not paused:
        placed,dead = current.combined_movement(board,placed,dead,temporary_occupied)
        if not dead:
            if placed:
                full_rows,lines = check_row(board,lines)
                current = Block(next_type,frequency)
                next_type = random.randint(0,6)

            screen.fill((0,0,0))

            for wall in walls:
                wall.draw_on(screen)

            display_instructions(screen)
            display_next_block(next_type,screen)
            display_board(board,screen)
            display_game_state(screen,lines,frequency,high_score)
            pygame.display.update()

            if placed:
                for i in full_rows:
                    board.pop(i)
                    board.insert(0,[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])

            current.remove_from(board)

            frequency = 20 - lines//2

            if frequency == 0:
                high_score = lines
                won = major_font.render("YOU WON", 1, (255,255,255))
                screen.blit(won, (80,250 ))

            if lines > high_score:
                high_score = lines
            timer = (timer + 1) % current.frequency

        elif dead:
            screen.fill((0,0,0))
            for wall in walls:
                wall.draw_on(screen)

            dead = major_font.render("YOU DIED", 1, (255,255,255))
            screen.blit(dead, (80,250 ))
            if lines == 1:
                s = ''
            else:
                s = 's'

            if lines > high_score:
                high_score = lines
                score_message = "Highscore: "+str(lines)+" line" + s
                score_message = major_info_font.render(score_message, 1, (255,255,255))
                screen.blit(score_message,(55,350))
            else:
                score_message = "Score: "+str(lines)+" line" + s
                score_message = major_info_font.render(score_message,1,(255,255,255))
                screen.blit(score_message,(100,350))

            restart_message = instruction_font.render("Press the spacebar to restart",1,(255,255,255))
            screen.blit(restart_message,(50,450))
            pygame.display.update()
