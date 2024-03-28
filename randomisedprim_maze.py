import random
import pygame as pg

#init class cause objects >>
class Maze:
    def __init__(self):
        self.width = 15 ; self.height = 15
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
                    pg.draw.rect(screen,"white",path,2)
                #End point
                if cell == "G":
                    pg.draw.rect(screen,"yellow2",path)
                #if they click to solve
                if cell == "A":
                    pg.draw.rect(screen,"blue",path)
                    pg.draw.rect(screen,"white",path,2)
        #drawing the player
        pg.draw.rect(screen,"red1",(self.pos[1]*10,self.pos[0]*10,10,10))
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
        self.start_pos = self.pos
        self.end_pos = [-1,-1]
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
                self.end_pos = [w[0],w[1]]
                self.maze[w[0]][w[1]] = "G" 
        self.maze_untracked = self.maze
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
            if self.maze[self.pos[0]-1][self.pos[1]] == self.path or self.maze[self.pos[0]-1][self.pos[1]] == "X" or self.maze[self.pos[0]-1][self.pos[1]] == "A":
                #moves you onto the position we checked cause its safe now
                self.pos = [self.pos[0]-1,self.pos[1]]
                #making it marked 
                self.maze[self.pos[0]][self.pos[1]] = "X"
            #if you hit the exit it resets
            elif self.maze[self.pos[0]-1][self.pos[1]] == "G":
                #make maze bigger if you finish it (but not too big)
                if not self.width >= 100:
                    self.width = int(self.width*1.2)
                    if self.width > 100:
                        self.width = 100
                if not self.height >= 60:
                    self.height = int(self.height*1.2)
                    if self.height > 60:
                        self.height = 60
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

        if  keys.key == pg.K_s or keys.key == pg.K_DOWN:
            if self.maze[self.pos[0]+1][self.pos[1]] == self.path or self.maze[self.pos[0]+1][self.pos[1]] == "X" or self.maze[self.pos[0]+1][self.pos[1]] == "A":
                self.pos = [self.pos[0]+1,self.pos[1]]
                self.maze[self.pos[0]][self.pos[1]] = "X"
            elif self.maze[self.pos[0]+1][self.pos[1]] == "G":
                if not self.width >= 100:
                    self.width = int(self.width*1.2)
                    if self.width > 100:
                        self.width = 100
                if not self.height >= 60:
                    self.height = int(self.height*1.2)
                    if self.height > 60:
                        self.height = 60
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

        if  keys.key == pg.K_a or keys.key == pg.K_LEFT:
            if self.maze[self.pos[0]][self.pos[1]-1] == self.path or self.maze[self.pos[0]][self.pos[1]-1] == "X" or self.maze[self.pos[0]][self.pos[1]-1] == "A":
                self.pos = [self.pos[0],self.pos[1]-1]
                self.maze[self.pos[0]][self.pos[1]] = "X"
            elif self.maze[self.pos[0]][self.pos[1]-1] == "G":
                if not self.width >= 100:
                    self.width = int(self.width*1.2)
                    if self.width > 100:
                        self.width = 100
                if not self.height >= 60:
                    self.height = int(self.height*1.2)
                    if self.height > 60:
                        self.height = 60
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

        if  keys.key == pg.K_d or keys.key == pg.K_RIGHT:
            if self.maze[self.pos[0]][self.pos[1]+1] == self.path or self.maze[self.pos[0]][self.pos[1]+1] == "X" or self.maze[self.pos[0]][self.pos[1]+1] == "A":
                self.pos = [self.pos[0],self.pos[1]+1]
                self.maze[self.pos[0]][self.pos[1]] = "X"
            elif self.maze[self.pos[0]][self.pos[1]+1] == "G":
                if not self.width >= 100:
                    self.width = int(self.width*1.2)
                    if self.width >100:
                        self.width = 100
                if not self.height >= 60:
                    self.height = int(self.height*1.2)
                    if self.height > 60:
                        self.height = 60
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

        #go back to start if space
        if keys.key == pg.K_SPACE:
            self.pos = self.start_pos
        #exit path if enter pressed ; only if an exit exists (get bug every so often on smallest maze size where exit doesnt form)
        if keys.key == pg.K_RETURN:
            if self.end_pos != [-1,-1]:
                self.solve_maze()
            else: 
                self.maze = [["u"for _ in range(self.width)]for _ in range(self.height)]
                self.randomise_maze()

    #finding end point from start point
    def solve_maze(self):
        #defining start
        start = self.start_pos
        #starting the path with the start
        self.solved_path = [start]
        #adding to visited list
        self.visited = [start]
        self.solve_logic()
        
    #recursive search (I think DFS but not sure)
    def solve_logic(self):
        #if the last thing in the list is the end point then return after converting the path to a new colour
        if self.solved_path[-1] == self.end_pos:
            if not "A" in self.maze:
                for i in self.solved_path:
                    if not self.maze[i[0]][i[1]] == "G":
                        self.maze[i[0]][i[1]] = "A"
            return
        
        #looking at last item in list
        cell = self.solved_path[-1]
        #if its not been visited and isnt a wall follow this path till it is
        if not [cell[0]+1,cell[1]] in self.visited and (self.maze[cell[0]+1][cell[1]] == "X" or self.maze[cell[0]+1][cell[1]] == self.path or self.maze[cell[0]+1][cell[1]] == "G"):
            self.visited.append([cell[0]+1,cell[1]])
            self.solved_path.append([cell[0]+1,cell[1]])
            self.solve_logic()
        
        if not [cell[0]-1,cell[1]] in self.visited and (self.maze[cell[0]-1][cell[1]] == "X" or self.maze[cell[0]-1][cell[1]] == self.path or self.maze[cell[0]-1][cell[1]] == "G"):
            self.visited.append([cell[0]-1,cell[1]])
            self.solved_path.append([cell[0]-1,cell[1]])
            self.solve_logic()

        if not [cell[0],cell[1]+1] in self.visited and (self.maze[cell[0]][cell[1]+1] == "X" or self.maze[cell[0]][cell[1]+1] == self.path or self.maze[cell[0]][cell[1]+1] == "G"):
            self.visited.append([cell[0],cell[1]+1])
            self.solved_path.append([cell[0],cell[1]+1])
            self.solve_logic()

        if not [cell[0],cell[1]-1] in self.visited and (self.maze[cell[0]][cell[1]-1] == "X" or self.maze[cell[0]][cell[1]-1] == self.path or self.maze[cell[0]][cell[1]-1] == "G"):
            self.visited.append([cell[0],cell[1]-1])
            self.solved_path.append([cell[0],cell[1]-1])
            self.solve_logic()

        
        #if your at the end of a path the get rid of that path back to where it last branched
        cell = self.solved_path[-1] 
        if self.maze[cell[0]][cell[1]] != self.end_pos:
            self.solved_path.remove(cell)
        return



#so i can use this in other things if i want
if __name__ == "__main__":
    maze = Maze()
    run = True
    #setting up pygame shenanigans
    screen = pg.display.set_mode((maze.width * 10,maze.height * 10))
    pg.display.set_caption("maze")
    while run:
        #adjust screensize with maze size
        if maze.width * 10 != screen.get_width():
            screen = pg.display.set_mode((maze.width * 10,maze.height * 10))
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
