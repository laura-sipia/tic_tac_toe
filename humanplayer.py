# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 00:07:17 2019

@author: laura
"""
class HumanPlayer:
    def __init__(self, token):
        self.token = token
        return
    
    def playTurn(self, positions):
        try:
            while True:
                row = int(input("Input your action row:"))
                col = int(input("Input your action col:"))
                action = (row, col)
                if action in positions:
                    return action
        except ValueError:
            self.playTurn(positions)
    def addStep(self, state):
        pass

    def updateStateValues(self, reward):
        pass

    def reset(self):
        pass