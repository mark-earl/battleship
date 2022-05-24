
# The objective of this program is to create an alogirithm that assists a player
# wishing to play the game "Battleship"

import pygame
from Game import Game

game = Game()

def main():

    player_win_condition = 0
    opponent_win_condition = 0

    ship_locations = game.config() # [player, opponent]
    player_ship_locations = ship_locations[0]
    opponent_ship_locations = ship_locations[1]

    player_moves = []
    opponent_moves = []

    winner = False

    # game.calculate_probability() # WIP


    while not winner:

        # player (program user)
        player_move = game.player_move(opponent_ship_locations,player_moves)

        x_y = player_move[1]
        player_has_hit_opponent_ship = player_move[0]

        player_moves.append(x_y)

        if player_has_hit_opponent_ship:
            player_win_condition += 1
        pygame.display.flip()

        # opponent (computer)
        opponent_move = game.opponent_move(player_ship_locations,opponent_moves)

        x_y = opponent_move[1]
        opponent_has_hit_player_ship = opponent_move[0]

        opponent_moves.append(x_y)
        
        if opponent_has_hit_player_ship:
            opponent_win_condition += 1
        pygame.display.flip()

        # checking to see if either side has won or not
        if player_win_condition == 17:
            winner = True
            print("YOU WIN, press \"X\" to close")
        elif opponent_win_condition == 17:
            winner = True
            print("YOU LOSE, press \"X\" to close")

    # waiting for the user to close the program
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

pygame.init()
main()
pygame.quit()
