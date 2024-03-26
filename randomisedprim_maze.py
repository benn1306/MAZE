import random
import pygame as pg

#init class
class Maze:
    def __init__(self):
        self.width = 100 ; self.height = 60
        self.maze =[["u"for _ in range(self.width)]for _ in range(self.height)]
        self.path = "0" ; self.wall = "#"

        self.randomise_maze()

    #function to format maze
    def draw_maze(self):
        #drawing in terminal
        for row in self.maze:
            #each row is on a new line
            print("")
            for cell in row:
                #each cell prints next to each other and if the cell was "u"nvisited it is a wall
                if not cell == "u":
                    print(cell, end="")
                else:
                    print("_", end="")
        print("")

    def screen_maze(self,screen):
        #displaying as pygame screen
        for c_height,row in enumerate(self.maze):
            for c_width,cell in enumerate(row):
                path = pg.Rect(c_width*10,c_height*10,10,10)
                if cell == "u" or cell == self.wall:
                    pg.draw.rect(screen,self.wall_colour,path)
                if cell == self.path:
                    pg.draw.rect(screen,"white",path)
                #Start point and where player has been
                if cell == "X":
                    pg.draw.rect(screen,"red",path)
                #End point
                if cell == "G":
                    pg.draw.rect(screen,"gold",path)
        #drawing the player
        pg.draw.rect(screen,"orange2",(self.pos[1]*10,self.pos[0]*10,10,10))
        pg.display.update()

    #logic for randomising the maze
    def randomise_maze(self):
        #a list for storing the walls (its a botched random prims algorithm)
        self.walls = []
        #random wall colour
        self.wall_colour = random.choice(["black","blue4","darkslategrey","brown4","steelblue"])
        #random start position and appending the areas around the start as the first walls
        start_x = random.randint(1, self.width - 2) ; start_y = random.randint(1, self.height - 2)
        self.maze[start_y][start_x] = "X"
        self.pos = [start_y,start_x]
        self.maze[start_y - 1][start_x] = self.wall ; self.maze[start_y + 1][start_x] = self.wall ; self.maze[start_y][start_x - 1] = self.wall ; self.maze[start_y][start_x + 1] = self.wall
        self.walls.append([start_y - 1,start_x]) ; self.walls.append([start_y + 1,start_x]) ; self.walls.append([start_y,start_x + 1]) ; self.walls.append([start_y,start_x - 1])
        
        #variables for in the loop
        consec_counter = 0
        prev_len = len(self.walls)
        #while the wall list is not empty choose a new random wall from the list
        while self.walls:
            w = random.choice(self.walls)
            
            #if above and below the wall is not gonna give an error,, check if the wall has unvisited cells either side, that arent walls
            if 0 <= w[0]-1 and len(self.maze) > w[0]+1 and 0 <= w[1]-1 and len(self.maze[w[0]])> w[1]+1:   

                if  (self.maze[w[0]-1][w[1]] == "u" and self.maze[w[0]+1][w[1]] == self.path) or (self.maze[w[0]-1][w[1]] == "u" and self.maze[w[0]+1][w[1]] == "u"): 
                    if self.less_than_two(w)<2:
                        self.maze[w[0]][w[1]] = self.path
                        self.neighbours_now_walls(w)
                #same as above but for if the other side was the unvisited one (probs should have used a function here but...)
                if (self.maze[w[0]-1][w[1]] == self.path and self.maze[w[0]+1][w[1]] == "u") or (self.maze[w[0]-1][w[1]] == "u" and self.maze[w[0]+1][w[1]] == "u"): 
                    if self.less_than_two(w)<2:
                        self.maze[w[0]][w[1]] = self.path
                        self.neighbours_now_walls(w)

                #same as above again but for left and right instead of up and down (again a function would def help)     
                if (self.maze[w[0]][w[1]-1] == "u" and self.maze[w[0]][w[1]+1] == self.path) or (self.maze[w[0]][w[1]-1] == "u" and self.maze[w[0]][w[1]+1] == "u"):
                    if self.less_than_two(w)<2:
                        self.maze[w[0]][w[1]] = self.path
                        self.neighbours_now_walls(w)
                if (self.maze[w[0]][w[1]-1] == self.path and self.maze[w[0]][w[1]+1] == "u") or (self.maze[w[0]][w[1]-1] == "u" and self.maze[w[0]][w[1]+1] == "u"):
                    if self.less_than_two(w)<2:
                        self.maze[w[0]][w[1]] = self.path
                        self.neighbours_now_walls(w)
                #removing walls after theyre finished
                else:
                    self.walls.remove(w)
            else:
                self.walls.remove(w)
            
            #so i can see if the walls list hasnt changed (i couldnt figure out how to get it to fully empty it kept stopping at like length 30)
            if prev_len == len(self.walls):
                consec_counter += 1
            else:
                consec_counter = 0
            prev_len = len(self.walls)
            if consec_counter == 150:
                self.walls = []
                #last wall to leave list is the finish point
                self.maze[w[0]][w[1]] = "G" 

    #if its more than two paths touching the cell we dont want it being another path
    def less_than_two(self,c_cell):
        num_of_paths = 0
        if self.maze[c_cell[0]+1][c_cell[1]] == self.path:
            num_of_paths += 1
        if self.maze[c_cell[0]-1][c_cell[1]] == self.path:
            num_of_paths += 1
        if self.maze[c_cell[0]][c_cell[1]+1] == self.path:
            num_of_paths += 1
        if self.maze[c_cell[0]][c_cell[1]-1] == self.path:
            num_of_paths += 1
        return num_of_paths
    
    #if the walls around the cell aren't paths and haven't been walls already it'll make them walls
    def neighbours_now_walls(self,c_cell):
        if self.maze[c_cell[0]-1][c_cell[1]] != self.path and self.maze[c_cell[0]-1][c_cell[1]] != self.wall and self.maze[c_cell[0]-1][c_cell[1]] != "X":
            self.maze[c_cell[0]-1][c_cell[1]] = self.wall
            if not [c_cell[0]-1,c_cell[1]] in self.walls:
                self.walls.append([c_cell[0]-1,c_cell[1]])
        
        if self.maze[c_cell[0]+1][c_cell[1]] != self.path and self.maze[c_cell[0]+1][c_cell[1]] != self.wall and self.maze[c_cell[0]+1][c_cell[1]] != "X":
            self.maze[c_cell[0]+1][c_cell[1]] = self.wall
            if not [c_cell[0]+1,c_cell[1]] in self.walls:
                self.walls.append([c_cell[0]+1,c_cell[1]])

        if self.maze[c_cell[0]][c_cell[1]-1] != self.path and self.maze[c_cell[0]][c_cell[1]-1] != self.wall and self.maze[c_cell[0]][c_cell[1]-1] != "X":
            self.maze[c_cell[0]][c_cell[1]-1] = self.wall
            if not [c_cell[0],c_cell[1]-1] in self.walls:
                self.walls.append([c_cell[0],c_cell[1]-1])
        
        if self.maze[c_cell[0]][c_cell[1]+1] != self.path and self.maze[c_cell[0]][c_cell[1]+1] != self.wall and self.maze[c_cell[0]][c_cell[1]+1] != "X":
            self.maze[c_cell[0]][c_cell[1]+1] = self.wall
            if not [c_cell[0],c_cell[1]+1] in self.walls:
                self.walls.append([c_cell[0],c_cell[1]+1])
    
    #moving around
    def maze_move(self,keys):
        #moving the direction you press
        if  keys.key == pg.K_w or keys.key == pg.K_UP:
            #only move if its not over a wall (no cheating)
            if self.maze[self.pos[0]-1][self.pos[1]] == self.path or self.maze[self.pos[0]-1][self.pos[1]] == "X":
                #moves you onto the position we checked cause its safe now
                self.pos = [self.pos[0]-1,self.pos[1]]
                #making it marked 
                self.maze[self.pos[0]][self.pos[1]] = "X"
            #if you hit the exit it resets
            elif self.maze[self.pos[0]-1][self.pos[1]] == "G":
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

        if  keys.key == pg.K_s or keys.key == pg.K_DOWN:
            if self.maze[self.pos[0]+1][self.pos[1]] == self.path or self.maze[self.pos[0]+1][self.pos[1]] == "X":
                self.pos = [self.pos[0]+1,self.pos[1]]
                self.maze[self.pos[0]][self.pos[1]] = "X"
            elif self.maze[self.pos[0]+1][self.pos[1]] == "G":
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

        if  keys.key == pg.K_a or keys.key == pg.K_LEFT:
            if self.maze[self.pos[0]][self.pos[1]-1] == self.path or self.maze[self.pos[0]][self.pos[1]-1] == "X":
                self.pos = [self.pos[0],self.pos[1]-1]
                self.maze[self.pos[0]][self.pos[1]] = "X"
            elif self.maze[self.pos[0]][self.pos[1]-1] == "G":
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

        if  keys.key == pg.K_d or keys.key == pg.K_RIGHT:
            if self.maze[self.pos[0]][self.pos[1]+1] == self.path or self.maze[self.pos[0]][self.pos[1]+1] == "X":
                self.pos = [self.pos[0],self.pos[1]+1]
                self.maze[self.pos[0]][self.pos[1]] = "X"
            elif self.maze[self.pos[0]][self.pos[1]+1] == "G":
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()
        
#so i can use this in other things if i want
if __name__ == "__main__":
    maze = Maze()
    maze.draw_maze()

    run = True
    #setting up pygame shenanigans
    screen = pg.display.set_mode((1000,600))

    while run:
        maze.screen_maze(screen) 
        #looking if anything happens
        for event in pg.event.get():
            #quit obv
            if event.type == pg.QUIT:
                run = False
            #giving the keyboard inputs to movement handler (that sounds way fancier than it is)
            if event.type == pg.KEYDOWN:
                key = event
                maze.maze_move(key)
    #no errors for ending the program without quitting the window, please
    pg.quit()

