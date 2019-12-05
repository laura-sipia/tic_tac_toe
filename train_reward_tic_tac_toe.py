# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:54:17 2019

@author: laura
"""

import numpy as np
from player import Player
from humanplayer import HumanPlayer

BOARD_SIZE = 3
board = np.zeros((BOARD_SIZE,BOARD_SIZE))
boardHash = None

# If board has tics in all row of a column, all columns in a row or in either
# diagonal
def gameHasEnded():
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
        if check_row(row, 1) or check_row(row, -1):
            return win
        
    # If some column has only one kind on decorators
    for i in range(3):
        if check_column(i, 1) or check_column(i, -1):
            return win
        
    # If right to left diagonal has only one kind of decorators
    if check_diagonal(1) or check_diagonal(-1):
        return win
        
    # If left to right diagonal has only one kind of decorators
    if check_right_left_diagonal(1) or check_right_left_diagonal(-1):
        return win
    
    for place in board:
        if any(i == 0 for i in place):
            return game_ongoing
    
    return tie
     
def getBoardHash():
    global boardHash
    global board
    boardHash = str(board.reshape(BOARD_SIZE*BOARD_SIZE))
    return boardHash

# All actions that are not currently used are allowed
def allowedSteps():
    allowed_positions = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i,j] == 0:
                allowed_positions.append((i,j))
    return allowed_positions

# Updates the board view
def updateBoard(position, decorator):
    global board
    board[position] = decorator

def show_board():
    global board
    for i in range(0, BOARD_SIZE):
        print('----------------')
        out = '|'
        for j in range(0,BOARD_SIZE):
            if board[i,j] == 1:
                token = 'x'
            if board[i,j] == -1:
                token = 'o'
            if board[i,j] == 0:
                token = ' '
            out += token + '|'
        print (out)
    print('-----------------')

def train(epochs):
    global board
    global boardHash
    player1 = Player(-1)
    player2 = Player(1) 
    for i in range(epochs):
        
        player1.reset()
        player2.reset()
        boardHash = None
        board = np.zeros((BOARD_SIZE,BOARD_SIZE))
        
        # Randomly choose beginner
        turn = 1
        GAME_STATUS = 0
        
        # While game has not ended
        while GAME_STATUS == 0:
            # Game has not ended, other players turn
            turn = turn + 1
            # What are the available actions curretly
            positions = allowedSteps()
            # Player takes an action
            if turn % 2 == 0:
                action = player2.playTurn(positions, board)
                boardHash = getBoardHash()
                # Update the board
                updateBoard(action, player2.token)
                player2.addStep(boardHash)
            else:
                action = player1.playTurn(positions, board)    
                boardHash = getBoardHash()
                # Update the board
                updateBoard(action, player1.token)    
                player1.addStep(boardHash)
            
            if  i > 49990:
                # Show the current situation
                show_board()
                print(" ")
                           
                
                #time.sleep(1)
                       
            GAME_STATUS = gameHasEnded()
            
        if GAME_STATUS == 1:
            # Who won
            if turn % 2 == 0:
                player2.updateStateValues(1)
                player1.updateStateValues(0)
            else:
                player1.updateStateValues(1)
                player2.updateStateValues(0)
            print("GAME ENDED TO WIN")
            print("  ")
            
        elif GAME_STATUS == 2:
            player1.updateStateValues(0.1)
            player2.updateStateValues(0.5)
            print("GAME ENDED TO TIE")
            print("  ")
    player1.save()
    player2.save()
    
def doYouWantToPlay():
    while True:
        response = str(input("Do you want to play:"))
        if response == 'y':
            return True
        elif response == 'n':
            return False
    

def trainWithHuman():
    global board
    global boardHash
    PLAY = True
    player1 = Player(-1)
    player2 = HumanPlayer(1) 
    while PLAY:
        
        player1.reset()
        boardHash = None
        board = np.zeros((BOARD_SIZE,BOARD_SIZE))
        
        turn = 1
        GAME_STATUS = 0
        
        # While game has not ended
        while GAME_STATUS == 0:
            # Game has not ended, other players turn
            turn = turn + 1
            # What are the available actions curretly
            positions = allowedSteps()
            # Player takes an action
            if turn % 2 == 0:
                action = player2.playTurn(positions)
                boardHash = getBoardHash()
                # Update the board
                updateBoard(action, player2.token)
                player2.addStep(boardHash)
            else:
                action = player1.playTurn(positions, board)    
                boardHash = getBoardHash()
                # Update the board
                updateBoard(action, player1.token)    
                player1.addStep(boardHash)
            
            show_board()
            print(" ")
                       
            GAME_STATUS = gameHasEnded()
            
        if GAME_STATUS == 1:
            # Who won
            if turn % 2 == 0:
                player2.updateStateValues(1)
                player1.updateStateValues(0)
            else:
                player1.updateStateValues(1)
                player2.updateStateValues(0)
            print("GAME ENDED TO WIN")
            print("  ")
            
        elif GAME_STATUS == 2:
            player1.updateStateValues(0.1)
            player2.updateStateValues(0.5)
            print("GAME ENDED TO TIE")
            print("  ")
        PLAY = doYouWantToPlay()
    player1.save()

#train(50000)
           
trainWithHuman()
    
    
    
    
    