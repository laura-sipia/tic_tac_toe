import random
import csv
import numpy as np

BOARD_SIZE = 3

class Player:
   
    
    def __init__(self, token):
        self.steps_taken = []
        self.token = token
        self.state_value = {}
        self.lr = 0.2
        self.decay_gamma = 0.9
        
        self.initialize_state_value()
        
    def initialize_state_value(self):
        file = 'player_-1.csv'
        with open(file) as fp:
           for cnt, line in enumerate(fp):
               if len(line) != 1:
                   dict_k_v = line.rsplit(',', 1)
                   self.state_value[dict_k_v[0]] = float(dict_k_v[1])
                   print("Line {}: {}".format(dict_k_v[0], float(dict_k_v[1])))          
    
    def reset(self):
        self.steps_taken = []
    
    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_SIZE * BOARD_SIZE))
        return boardHash
    
    def playTurn(self, positions, current_board):
        chosen_action = 0
        # 1/10 times player chooses a random action
        if random.random() > self.decay_gamma:
            idx = np.random.choice(len(positions))
            chosen_action = positions[idx]
        else:
            # Let's find action that has the biggest value
            max_gain = 0
            for i in positions:             
                next_state = current_board.copy()
                next_state[i] = self.token
                next_boardHash = self.getHash(next_state)
                # If state with given action is None initialize with 0
                if self.state_value.get(next_boardHash) == None:
                    pass
                else:
                    # Else let's check if it's larger that the maximim value 
                    # we have found so far
                    if self.state_value.get(next_boardHash) >= max_gain:
                        max_gain = self.state_value[next_boardHash]
                        chosen_action = i
            if max_gain == 0:
               idx = np.random.choice(len(positions))
               chosen_action = positions[idx]    

        return chosen_action
    
    def addStep(self, step):
        self.steps_taken.append(step)
    
    def token(self):
        return self.token
    
    def updateStateValues(self, reward):
        for st in reversed(self.steps_taken):
            if self.state_value.get(st) is None:
                self.state_value[st] = 0
            self.state_value[st] += self.lr * (self.decay_gamma * reward - self.state_value[st])
            reward = self.state_value[st]
    
    
    def save(self):
        w = csv.writer(open("player_{}.csv".format(self.token), "w"))
        for key, val in self.state_value.items():
            w.writerow([key, val])