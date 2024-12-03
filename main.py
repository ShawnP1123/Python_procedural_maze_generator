# imports
import pygame
import random

# cell
class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True
        self.visited = False

# player class
class Player:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def move_up(self):
        if not grid[self.col][self.row].top:
            self.row -= 1

    def move_down(self):
        if not grid[self.col][self.row].bottom:
            self.row += 1

    def move_left(self):
        if not grid[self.col][self.row].left:
            self.col -= 1

    def move_right(self):
        if not grid[self.col][self.row].right:
            self.col += 1

    def draw(self):
        x = self.col * (CELL_SIZE) + MARGIN
        y = self.row * (CELL_SIZE) + MARGIN
        pygame.draw.rect(screen, (0, 255, 0), (x + (CELL_SIZE//3), y + (CELL_SIZE//3), CELL_SIZE // 2, CELL_SIZE // 2))

    def undraw(self):
        x = self.col * (CELL_SIZE) + MARGIN
        y = self.row * (CELL_SIZE) + MARGIN
        pygame.draw.rect(screen, BLACK, (x + (CELL_SIZE//3), y + (CELL_SIZE//3), CELL_SIZE // 2, CELL_SIZE // 2))

# initializations
pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BLACK = (0,0,0)
WHITE = (255,255,255)
start_time = pygame.time.get_ticks()

# determine the size of the grid based on screen size and cell size
CELL_SIZE = 5
MARGIN = 10
GRID_ROWS = int((SCREEN_HEIGHT-(MARGIN*2)) // CELL_SIZE)
GRID_COLS = int((SCREEN_WIDTH-(MARGIN*2)) // CELL_SIZE)

# make the grid
grid = [[cell(col * CELL_SIZE + MARGIN, row * CELL_SIZE + MARGIN) for row in range(GRID_ROWS)] for col in range(GRID_COLS)]

# function for drawing the grid, looks nice but is slow
def draw_grid():
    screen.fill(BLACK)
    
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CELL_SIZE) + MARGIN
            y = row * (CELL_SIZE) + MARGIN
            cell = grid[col][row]
            
            # Draw top wall
            if cell.top:
                pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
            
            # Draw right wall
            if cell.right:
                pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            
            # Draw bottom wall
            if cell.bottom:
                pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
            
            # Draw left wall
            if cell.left:
                pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)

# looks shitty but is very fast
def draw_cell(col, row):
    x = col * (CELL_SIZE) + MARGIN
    y = row * (CELL_SIZE) + MARGIN 
    cell = grid[col][row]
    if not cell.top:
        pygame.draw.line(screen, BLACK, (x+1, y), (x + CELL_SIZE-1 , y), 2)
    if not cell.right:
        pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y+1), (x + CELL_SIZE, y + CELL_SIZE-1 ), 2)
    if not cell.bottom:
        pygame.draw.line(screen, BLACK, (x+1, y + CELL_SIZE), (x + CELL_SIZE-1, y + CELL_SIZE), 2)
    if not cell.left:
        pygame.draw.line(screen, BLACK, (x, y+1), (x, y + CELL_SIZE-1), 2)

# the whole shabam
def generate():

    # initialize more shit
    curr_x_index = random.randint(0, GRID_COLS - 1)
    curr_y_index = GRID_ROWS - 1
    starting_cell = grid[curr_x_index][curr_y_index]
    starting_cell.visited = True
    starting_cell.bottom = False
    cell_mem = [(curr_x_index, curr_y_index)]
    grid[0][0].top = False
    total_cells = GRID_COLS * GRID_ROWS
    visited_cells = 1
    draw_count = 0

    # draw a filled up grid for the program to carve out
    draw_grid()
    
    # the main thingy going on here
    while visited_cells < total_cells:

        # draw only the cells one at a time to increase performance by like 1 million percent
        draw_cell(curr_x_index, curr_y_index)

        # speed it up even more for larger mazes
        if draw_count > 300 * 1/CELL_SIZE:
            pygame.display.flip()
            draw_count = 0
        draw_count += 1
        directions = ["up", "down", "left", "right"]
        
        # filter directions 
        if curr_y_index - 1 < 0 or grid[curr_x_index][curr_y_index - 1].visited:
            directions.remove("up")
        if curr_y_index + 1 >= GRID_ROWS or grid[curr_x_index][curr_y_index + 1].visited:
            directions.remove("down")
        if curr_x_index - 1 < 0 or grid[curr_x_index - 1][curr_y_index].visited:
            directions.remove("left")
        if curr_x_index + 1 >= GRID_COLS or grid[curr_x_index + 1][curr_y_index].visited:
            directions.remove("right")

        # backtrack
        if not directions:
            backpos = cell_mem.pop()
            curr_x_index = backpos[0]
            curr_y_index = backpos[1]
        
        # moving and taking care of cell walls
        else:
            cell_mem.append((curr_x_index, curr_y_index))
            choice = random.choice(directions)
            if choice == "up":
                grid[curr_x_index][curr_y_index].top = False
                curr_y_index -= 1
                grid[curr_x_index][curr_y_index].bottom = False
                grid[curr_x_index][curr_y_index].visited = True
                visited_cells += 1
            elif choice == "down":
                grid[curr_x_index][curr_y_index].bottom = False
                curr_y_index += 1
                grid[curr_x_index][curr_y_index].top = False
                grid[curr_x_index][curr_y_index].visited = True
                visited_cells += 1
            elif choice == "left":
                grid[curr_x_index][curr_y_index].left = False
                curr_x_index -= 1
                grid[curr_x_index][curr_y_index].right = False
                grid[curr_x_index][curr_y_index].visited = True
                visited_cells += 1
            elif choice == "right":
                grid[curr_x_index][curr_y_index].right = False
                curr_x_index += 1
                grid[curr_x_index][curr_y_index].left = False
                grid[curr_x_index][curr_y_index].visited = True
                visited_cells += 1

    # if you dont do this there will be a few cells left untouched for some reason
    # nvm i think i fixed it but i'll leave it here in case
    # force_final_check()

    # make the grid look nice
    draw_grid()
    pygame.display.flip()

    # how long did it take?
    elapsed_time = (pygame.time.get_ticks() - start_time)/1000
    print(f"done in {elapsed_time} seconds")


# just makes sure every cell is connected to another, isn't too slow
def force_final_check():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell = grid[col][row]
            if not cell.visited:
        
                neighbors = []
                if row > 0 and grid[col][row - 1].visited:  
                    neighbors.append(("up", col, row - 1))
                if row < GRID_ROWS - 1 and grid[col][row + 1].visited: 
                    neighbors.append(("down", col, row + 1))
                if col > 0 and grid[col - 1][row].visited:  
                    neighbors.append(("left", col - 1, row))
                if col < GRID_COLS - 1 and grid[col + 1][row].visited: 
                    neighbors.append(("right", col + 1, row))

                if neighbors:

                    direction, nx, ny = random.choice(neighbors)
                    if direction == "up":
                        cell.top = False
                        grid[nx][ny].bottom = False
                    elif direction == "down":
                        cell.bottom = False
                        grid[nx][ny].top = False
                    elif direction == "left":
                        cell.left = False
                        grid[nx][ny].right = False
                    elif direction == "right":
                        cell.right = False
                        grid[nx][ny].left = False
                cell.visited = True


# generate the bitch
generate()
player = Player(0,0)
counter = 0

# just to keep it open and control a player
running = True
while running:
    player.draw()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key state checking
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and counter == 0:
        player.undraw()
        player.move_up()
        counter += 1
    if keys[pygame.K_a] and counter == 0:
        player.undraw()
        player.move_left()
        counter += 1
    if keys[pygame.K_s] and counter == 0:
        player.undraw()
        player.move_down()
        counter += 1
    if keys[pygame.K_d] and counter == 0:
        player.undraw()
        player.move_right()
        counter += 1

    if counter > 0:
        counter += 1
    
    if counter > 55:
        counter = 0


pygame.quit()

    
