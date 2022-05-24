import pygame, random

class Ship:

    def __init__(self,length,screen,cell_width,window_border_thickness,ship_file_path): # Constructor for the "Ship" class

        # Ship parameters
        self.length = length
        self.ship_file_path = ship_file_path

        # Other parameters
        self.screen = screen
        self.cell_width = cell_width
        self.width = length*self.cell_width
        self.height = self.width/self.length
        self.window_border_thickness = window_border_thickness

        
    def draw_player_ships(self,restricted_cells): # Draw all of the friendly (left board) ships with RNG (random number generation)

        repeat = True # assume that the current generation will be invalid

        while (repeat):
            self.origin = [random.randint(0,9),random.randint(0,9)] # generate a random origin
            self.orientation = random.getrandbits(1) # 0 = right, 1 = up

            if self.origin[0] + self.length > 9: # If the ship can't lay sideways
                self.origin[0] = self.origin[0] - self.length + 1
            if self.origin[1] + self.length > 9: # If the ship can't lay upright
                self.origin[1] = self.origin[1] - self.length + 1
            
            spaces_occupied = []

            if self.orientation == 0: # horizontal
                for num in range(self.length):
                        spaces_occupied.append([self.origin[0]+num,self.origin[1]])
            elif self.orientation == 1: # vertical
                for num in range(self.length):
                    spaces_occupied.append([self.origin[0],self.origin[1]+num])

            for cell in spaces_occupied:
                if cell in restricted_cells: # if the cell is in the restricted list, restart while loop
                    repeat = True
                    break
                else: # otherwise, move on, but iterate through all cells in this for loop to ensure no repeats
                    repeat = False
            
        
        ship_img = pygame.image.load(self.ship_file_path) # load the ship image from a local file
        ship_img = pygame.transform.scale(ship_img,(self.width,self.height)) # scale the image to fit the game board

        if self.orientation == 0: # horizontal
            imagerect = self.origin[0]*self.cell_width+self.window_border_thickness,self.origin[1]*self.cell_width+self.window_border_thickness,self.width,self.height
            self.screen.blit(ship_img, imagerect)

        elif self.orientation == 1: # vertical
            imagerect = self.origin[0]*self.cell_width+self.window_border_thickness,self.origin[1]*self.cell_width+self.window_border_thickness,self.height,self.width
            ship_img = pygame.transform.rotate(ship_img,90) # rotate the image to be vertical
            self.screen.blit(ship_img, imagerect)

        self.screen.blit(ship_img, imagerect)

        return spaces_occupied # return the spaces [x,y] that the ship that was drawn takes up
    
    def generate_opponent_ship_locations(self,restricted_cells): # Generate random ship locations for the enemy (right board)

        repeat = True # assume that the current generation will be invalid

        while (repeat):
            self.origin = [random.randint(0,9),random.randint(0,9)] # generate a random origin
            self.orientation = random.getrandbits(1) # 0 = right, 1 = up

            if self.origin[0] + self.length > 9: # If the ship can't lay sideways
                self.origin[0] = self.origin[0] - self.length + 1
            if self.origin[1] + self.length > 9: # If the ship can't lay upright
                self.origin[1] = self.origin[1] - self.length + 1
            
            spaces_occupied = []

            if self.orientation == 0: # horizontal
                for num in range(self.length):
                        spaces_occupied.append([self.origin[0]+num,self.origin[1]])
            elif self.orientation == 1: # vertical
                for num in range(self.length):
                    spaces_occupied.append([self.origin[0],self.origin[1]+num])

            for cell in spaces_occupied:
                if cell in restricted_cells: # if the cell is in the restricted list, restart while loop
                    repeat = True
                    break
                else: # other wise, move on, but iterate through all cells in this for loop to ensure no respeats
                    repeat = False
                    
        return spaces_occupied # return the spaces [x,y] that the current ship takes up
