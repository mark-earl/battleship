import ctypes, pygame, random, sys

from Grid import Grid
from Ship import Ship
from Cell import Cell

class Game:

    def __init__(self): # Constructor for the "Game" class

        # file paths for the ship images
        carrier_file_path = r"Utils\carrier.png"
        battleship_file_path = r"Utils\battleship.png"
        cruiser_file_path = r"Utils\cruiser.png"
        submarine_file_path = r"Utils\submarine.png"
        destroyer_file_path = r"Utils\destroyer.png"

        # instantiate a grid object
        self.grid = Grid()

        carrier = Ship(5,self.grid.screen,self.grid.cell_width,self.grid.window_border_thickness,carrier_file_path)
        battleship = Ship(4,self.grid.screen,self.grid.cell_width,self.grid.window_border_thickness,battleship_file_path)
        cruiser = Ship(3,self.grid.screen,self.grid.cell_width,self.grid.window_border_thickness,cruiser_file_path)
        submarine = Ship(3,self.grid.screen,self.grid.cell_width,self.grid.window_border_thickness,submarine_file_path)
        destroyer = Ship(2,self.grid.screen,self.grid.cell_width,self.grid.window_border_thickness,destroyer_file_path)

        self.ships = [carrier,battleship,cruiser,submarine,destroyer]

    def config(self): # Initial game set up, what you would do when playing battleship in real life
       
        self.grid.draw_board() # Draw the board

        player_ship_locations = [] # friendly (left board) ship locations
        for ship in self.ships:
            current_ship = ship.draw_player_ships(player_ship_locations)
            for cell in current_ship:
                player_ship_locations.append(cell)
        
        opponent_ship_locations = [] # enemy (right board) ship locations
        for ship in self.ships:
            current_ship = ship.generate_opponent_ship_locations(opponent_ship_locations)
            for cell in current_ship:
                opponent_ship_locations.append(cell)

        pygame.display.flip()

        return player_ship_locations,opponent_ship_locations # return both values, 0 = friendly, 1 = enemy
    
    def calculate_probability(self):
        for col in range(self.grid.cols):
            for row in range(self.grid.rows):
                cell = Cell(col,row,self.grid.screen,self.grid.cell_width,self.grid.grid_border_thickness,self.grid.window_border_thickness,self.grid.window_width,False)
                b_value = col*25 # probability function goes here
                color = (0,0,b_value)
                cell.update_cell_color(color)
        pygame.display.flip()

    
    def player_move(self,opponent_ship_locations,player_moves): # the program user takes his turn

        # 0,0 on opponents board, the upperleft hand corner of the grid, where the two grid lines intersect
        # described as a percentage of the total width and hieght

        origin = (
            ((self.grid.window_width/2) + (self.grid.window_border_thickness))/ self.grid.window_width, # x %
            ((self.grid.window_border_thickness))/ self.grid.window_height # y %
            )
        
        # The percent of the total width (x) and height (y) that the width of one cell takes up
        cell_width_percent_vectors = (
            (self.grid.cell_width/self.grid.window_width), # x %
            (self.grid.cell_width/self.grid.window_height) # y %
        )

        opponent_board_cell_percents = [] # Will stoe pixel ranges, x & y, for each cell EX: [[x_min, x_max],[y_min,y_max]]
        opponent_board_cell_index = [] # Will store the coordinates of the corresponding cell EX: [1,2]

        # Make all of the grid ranges
        for col in range(self.grid.cols):
            for row in range(self.grid.rows):

                x_min = (cell_width_percent_vectors[0]*col) + origin[0]
                x_max = (cell_width_percent_vectors[0]*col) + origin[0]+cell_width_percent_vectors[0]

                y_min = (cell_width_percent_vectors[1]*row) + origin[1]
                y_max = (cell_width_percent_vectors[1]*row)+origin[1]+cell_width_percent_vectors[1]

                opponent_board_cell_percents.append([[x_min,x_max],[y_min,y_max]])
                opponent_board_cell_index.append([col,row])
            


        # Here is the bulk of the logic concerning actually executing a player move
        
        unique_move = False # Assume that the move will be a repeat move
        while not unique_move:

            clicked = False
            while not clicked: # While the user has not moved

                valid_move = False
                while not valid_move: # A valid move is a move in the opponent's grid

                    for event in pygame.event.get(): # Allow the user to quit if they want
                        if event.type == pygame.QUIT:
                            sys.exit()
                
                    player_move = [pygame.mouse.get_pos()[0]/self.grid.window_width,pygame.mouse.get_pos()[1]/self.grid.window_height] # as a percentage of the pygame window

                    if pygame.mouse.get_pressed()[0]: # if the left mouse button is pressed
                        clicked = True
                        while pygame.mouse.get_pressed()[0] != 0: # prevent multiple executions
                            pygame.event.get()
                            continue
                
                        x_min = opponent_board_cell_percents[0][0][0]
                        x_max = opponent_board_cell_percents[-1][0][1]

                        y_min = opponent_board_cell_percents[0][1][0]
                        y_max = opponent_board_cell_percents[-1][1][1]

                        if (x_min <= player_move[0] <= x_max) and (y_min <= player_move[1] <= y_max): # If the move is in the opponent's grid, it is a valid move
                            valid_move = True

            # get the cell to update
            for cell_range in opponent_board_cell_percents:

                x_min = cell_range[0][0]
                x_max = cell_range[0][1]

                y_min = cell_range[1][0]
                y_max = cell_range[1][1]

                if x_min <= player_move[0] <= x_max and y_min <= player_move[1] <= y_max:
                    i = opponent_board_cell_percents.index(cell_range)
                    x = opponent_board_cell_index[i][0]
                    y = opponent_board_cell_index[i][1]

            if [x,y] in player_moves: # If the player has already selected that cell
                unique_move = False
                pop_up_window_title = "Repeat Move"
                pop_up_window_message = "You already moved there"
                ctypes.windll.user32.MessageBoxW(0, pop_up_window_message, pop_up_window_title, 1)  
                

            elif [x,y] not in player_moves:
                unique_move = True
            
        cell = Cell(x,y,self.grid.screen,self.grid.cell_width,self.grid.grid_border_thickness,self.grid.window_border_thickness,self.grid.window_width,False)

        x = cell.x
        y = cell.y

        if [x,y] in opponent_ship_locations: # If there is a ship there
            cell.is_hit()
            is_hit = True
        elif [x,y] not in opponent_ship_locations: # If there is NOT a ship there
            cell.is_miss()
            is_hit = False

        pygame.display.flip()

        return is_hit,[x,y] # return the status of the ship (hit or not) and the cell coordinates
        
    def opponent_move(self,player_ship_locations,opponent_moves): # opponent's move

        unique_move = False # assume a non unique move

        while not unique_move:
            x = random.randint(0,9)
            y = random.randint(0,9)
            if [x,y] not in opponent_moves:
                unique_move = True

        cell = Cell(x,y,self.grid.screen,self.grid.cell_width,self.grid.grid_border_thickness,self.grid.window_border_thickness,self.grid.window_width,True)

        if [cell.x,cell.y] in player_ship_locations:
            cell.is_hit()
            is_hit = True
        elif [cell.x,cell.y] not in player_ship_locations:
            cell.is_miss()
            is_hit = False
        
        return is_hit,[x,y] # return the status of the ship (hit or not) and the cell coordinates
