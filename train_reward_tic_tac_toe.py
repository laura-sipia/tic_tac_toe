# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:54:17 2019

@author: laura
"""

import time
import random
from player import Player

ACTIONS = [0,1,2,3,4,5,6,7,8]

state = []
board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]

# If board has tics in all row of a column, all columns in a row or in either
# diagonal
def game_has_ended():
    global state
    global board
    tie = 2
    win = 1
    game_ongoing = 0

    def check_row(row, decorator):
        if row[0] == decorator and row[1] == decorator and row[2] == decorator:
            return True
        return False
    
    def check_column(i, decorator):
        if board[0][i] == decorator and board[1][i] == decorator and board[2][i] == decorator:
                return True
        return False
    
    def check_diagonal(decorator):
        if board[0][0] == decorator and board[1][1] == decorator and board[2][2] == decorator:
            return True
        return False
    
    def check_right_left_diagonal(decorator):
        if board[0][2] == decorator and board[1][1] == decorator and board[2][0] == decorator:
            return True
        
    # If some row has only one kind on decorators
    for row in board:
        if check_row(row, "X") or check_row(row, "O"):
            return win
        
    # If some column has only one kind on decorators
    for i in range(3):
        if check_column(i, "X") or check_column(i, "O"):
            return win
        
    # If right to left diagonal has only one kind of decorators
    if check_diagonal("X") or check_diagonal("O"):
        return win
        
    # If left to right diagonal has only one kind of decorators
    if check_right_left_diagonal("X") or check_right_left_diagonal("O"):
        return win
    
    if len(state) == 9:
        return tie
    
    return game_ongoing
        

# All actions that are not currently used are allowed
def allowed_steps():
    global state
    allowed_actions = []
    for action in ACTIONS:
        if action not in state:
            allowed_actions.append(action)
    return allowed_actions

# Updates the board view
def update_board(action, decorator):
    global board
    if action < 3:
        # First row
        board[0][action] = decorator
    elif action < 6:
        # Second row
        board[1][action-3] = decorator
    else:
        # Third row
        board[2][action-6] = decorator

def train(epochs):
    global state
    global board
    player1 = Player('X')
    player2 = Player('O') 
    for i in range(epochs):
        
        player1.reset()
        player2.reset()
        state = []
        board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]
        
        # Randomly choose beginner
        turn = 1
        GAME_STATUS = 0
        
        # While game has not ended
        while GAME_STATUS == 0:
            # Game has not ended, other players turn
            turn = turn + 1
            # What are the available actions curretly
            actions = allowed_steps()
            # Player takes an action
            if turn % 2 == 0:
                action = player2.play_turn(actions)
                # Update the board state
                state.append(action)
                # Update the board
                update_board(action, player2.token)
            else:
                action = player1.play_turn(actions)    
                # Update the board state
                state.append(action)
                # Update the board
                update_board(action, player1.token)       
            
            if  i > 999990:
                # Show the current situation
                for row in board:
                    print(row)
                print(" ")
                           
                
                #time.sleep(1)
                       
            GAME_STATUS = game_has_ended()
            
        if GAME_STATUS == 1:
            # Who won
            if turn % 2 == 0:
                player2.update_state_values(10, state)
                player1.update_state_values(-5, state)
            else:
                player1.update_state_values(10, state)
                player2.update_state_values(-5, state)
            print("GAME ENDED TO WIN")
            print("  ")
            
        #elif GAME_STATUS == 2:
         #   player1.update_state_values(5, state)
         #   player2.update_state_values(5, state)
          #  print("GAME ENDED TO TIE")
           # print("  ")
    player1.save()
    player2.save()
    

train(1000000)
            
    
    
    
    
    
    