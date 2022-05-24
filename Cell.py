import pygame

class Cell:

    def __init__(self,x,y,screen,cell_width,grid_border_thickness,window_border_thickness,window_width,is_left_board): # Constructor for the "Cell" class

        # Positive x is rightward
        # Positive y is downward
        # Origin of each board is top-left

        # Cell parameters
        self.x = x # index, not actual pixel coords, EX: [2,3] = [x,y]
        self.y = y

        self.hit_color = (255,0,0) # Red
        self.miss_color = (255,255,255) # White

        self.cell_width = cell_width
        self.cell_height = self.cell_width # Square cells
        self.radius = cell_width/3 # Size of the dot to indicate a hit or a miss

        # Screen/window parameters
        self.screen = screen 
        self.grid_border_thickness = grid_border_thickness
        self.window_border_thickness = window_border_thickness
        self.window_width = window_width

        self.friendly_board_origin = ((self.grid_border_thickness+(self.cell_width/2))+self.window_border_thickness, # Upper left hand corner of the left board in pixel coords
        (self.grid_border_thickness+(self.cell_width/2)+self.window_border_thickness))

        self.is_left_board = is_left_board # Are the target cells in the left board or the right board? (bool)

        self.cols = self.rows = 10
    
    def is_hit(self): # update the targeted cell to show that it is hit by a red dot
        if self.is_left_board:
            center_coords = (self.x*self.cell_width+self.friendly_board_origin[0],self.y*self.cell_height+self.friendly_board_origin[1])
        elif not self.is_left_board:
            center_coords = (self.x*self.cell_width+self.friendly_board_origin[0]+(self.window_width/2),self.y*self.cell_height+self.friendly_board_origin[1])
        pygame.draw.circle(self.screen, self.hit_color,center_coords,self.radius)
    
    def is_miss(self): # update the targeted cell to show that is it a miss by a white dot
        if self.is_left_board:
            center_coords = (self.x*self.cell_width+self.friendly_board_origin[0],self.y*self.cell_height+self.friendly_board_origin[1])
        elif not self.is_left_board:
            center_coords = (self.x*self.cell_width+self.friendly_board_origin[0]+(self.window_width/2),self.y*self.cell_height+self.friendly_board_origin[1])
        pygame.draw.circle(self.screen, self.miss_color,center_coords,self.radius)
    
    def update_cell_color(self,color): # this should only be called in the following function
        pygame.draw.rect(self.screen,color,
        (self.window_border_thickness+self.x*self.cell_width+self.window_width/2+1,
        self.window_border_thickness+self.y*self.cell_height+1,
        self.cell_width-1,
        self.cell_height-1))
