import pygame

class Grid:

    def __init__(self): # Constructor for the "Grid" class

        # Window parameters
        self.window_height = 800 # Laptop = 600, PC = 800
        self.window_width = self.window_height*2
        self.window_color= (0,0,0) # Black
        self.window_border_thickness = self.window_height*0.035

        # Board parameters
        self.board_width = self.window_height-(self.window_border_thickness*2)
        self.board_height = self.board_width
        self.board_color = (100,100,100) # Gray
        self.board_friendly_center = (self.window_width*(1/4),self.window_height/2)
        self.board_enemy_center = (self.window_width*(3/4),self.window_height/2)
        
        # Grid parameters
        self.rows = 10 # Battelship will alwys be played on a 10x10 grid
        self.cols = self.rows # Battleship is a square grid
        self.cell_width = (self.board_height)/self.rows # The space between two grid lines, aka cell width

        # Grid border parameters
        self.grid_border_thickness = 1 # The lines dividing up all of the different grid positions
        self.grid_border_friendly_color = (0,0,255) # Blue
        self.grid_border_enemy_color = (0,255,0) # Green

        # Screen parameters
        self.screen = pygame.display.set_mode((self.window_width,self.window_height)) # Initialize a rectagle window

        # Divider parameters
        self.divider_color = (255,255,255) # White
        self.divider_thickness = 1

        # Aesthetic parameters
        icon_path = r"Utils\battleship-icon.jpg"
        self.program_icon = pygame.image.load(icon_path)
        self.window_title = "BATTLESHIP"

        # Font parameters
        self.font = 'Arial'
        self.font_color = (255,255,255) # White
        self.font_size = int(self.window_height/32)
       
        

    def draw_board(self): # Draw an empty battleship baord (no ships) on the screen

        # Title and icon
        pygame.display.set_caption(self.window_title)
        pygame.display.set_icon(self.program_icon)

        # Base window
        self.screen.fill(self.window_color)

        # Game board - friendly overlay
        pygame.draw.rect(
            self.screen, # Screen that the rectangle is drawn on
            self.board_color, # Color of the rectangle

            # Rectangle parameters
            (self.board_friendly_center[0]-(self.board_width/2), # left
            self.board_friendly_center[1]-(self.board_height/2), # top
            self.board_width, # width
            self.board_height) # height
            )

        # Game board - enemy overlay
        pygame.draw.rect(
            self.screen, # Screen that the rectangle is drawn on
            self.board_color, # Color of the rectangle

            # Rectangle parameters
            (self.board_enemy_center[0] - self.board_width/2, # left
            self.board_enemy_center[1] - self.board_height/2, # top
            self.board_width, # width
            self.board_height) # height
        )

        # Friendly (left) Board
        for col in range(0, self.cols+1): # Columns*
            
            x_1 = x_2 = (self.cell_width*col)+self.window_border_thickness+(self.grid_border_thickness/2) # Verticle lines

            y_1 = self.window_border_thickness
            y_2 = self.window_border_thickness+self.board_height-1

            pygame.draw.line(
                self.screen, # Screen that the line is drawn on
                self.grid_border_friendly_color, # Color of the line

                (x_1,y_1), # Starting position [x,y]
                (x_2,y_2), # Ending position [x,y]

                self.grid_border_thickness) # Line thickness
        
        for row in range(0, self.rows+1): # Rows*
            
            x_1 = self.window_border_thickness
            x_2 = self.window_border_thickness+self.board_width
            y_1 = y_2 = self.cell_width*row+self.window_border_thickness # Horizontal Lines
            
            pygame.draw.line(
                self.screen, # Screen that the line is drawn on
                self.grid_border_friendly_color, # Color of the line
                
                (x_1,y_1), # Starting position [x,y]
                (x_2,y_2), # Ending position [x,y]
                self.grid_border_thickness) # Line thickness

        # Enemey (right) Board
        for col in range(0, self.cols+1): # Columns*
            
            x_1 = x_2 = (self.cell_width*col)+(self.window_width/2)+(self.window_border_thickness) # Vertical Lines

            y_1 = self.window_border_thickness
            y_2 = self.window_border_thickness+self.board_height-1

            pygame.draw.line(
                self.screen, # Screen that the line is drawn on
                self.grid_border_enemy_color, # Color of the line

                (x_1,y_1), # Starting position [x,y]
                (x_2,y_2), # Ending position [x,y]

                self.grid_border_thickness) # Line thickness
                    
        for row in range(0, self.rows+1): # Rows*
            
            x_1 = self.window_border_thickness + (self.window_width/2)
            x_2 = self.window_border_thickness+self.board_width + (self.window_width/2)
            y_1 = y_2 = self.cell_width*row+self.window_border_thickness
            
            pygame.draw.line(
                self.screen, # Screen that the line is drawn on
                self.grid_border_enemy_color, # Color of the line
                
                (x_1,y_1), # Starting position [x,y]
                (x_2,y_2), # Ending position [x,y]
                self.grid_border_thickness) # Line thickness

        # *+1 ensures that the cells are completely surronded

        # Board divider
        pygame.draw.line(self.screen,self.divider_color,((self.window_width/2),0),((self.window_width/2),self.window_height),self.divider_thickness)

        # Game board labels
        cols = ['1','2','3','4','5','6','7','8','9','10']
        rows = ['A','B','C','D','E','F','G','H','I','J']
        font = pygame.font.SysFont(self.font, self.font_size)

        # Friendly board
        for label in range(0, len(cols)): # columns
            textsurface = font.render(cols[label], False, self.font_color)
            self.screen.blit(textsurface,(label*self.cell_width+(self.cell_width *3/4),0))
        
        for label in range(0, len(rows)): # rows
            textsurface = font.render(rows[label], False, self.font_color)
            self.screen.blit(textsurface,((self.window_border_thickness/3),label*self.cell_width+(self.cell_width *3/4)))
        
        # Enemy board
        for label in range(0, len(cols)): # columns
            textsurface = font.render(cols[label], False, self.font_color)
            self.screen.blit(textsurface,(label*self.cell_width+(self.cell_width *3/4)+self.window_width/2,0))
        
        for label in range(0, len(rows)): # rows
            textsurface = font.render(rows[label], False, self.font_color)
            self.screen.blit(textsurface,((self.window_border_thickness/3)+self.window_width/2,label*self.cell_width+(self.cell_width *3/4)))
