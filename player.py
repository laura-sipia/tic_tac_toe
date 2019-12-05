import random
import csv

class Player:

    
    def __init__(self, token):
        self.steps_taken = []
        self.token = token
        self.state_value = {}
        self.lr = 0.2
        self.decay_gamma = 0.9
        #self.initialize_state_value()
        
    def initialize_state_value(self):
        file = 'player_O.csv'
        with open(file) as fp:
           for cnt, line in enumerate(fp):
               if len(line) != 1:
                   dict_k_v = line.rsplit(',', 1)
                   self.state_value[dict_k_v[0]] = float(dict_k_v[1])
                   print("Line {}: {}".format(dict_k_v[0], float(dict_k_v[1])))          
    
    def reset(self):
        self.steps_taken = []
    
    def play_turn(self, actions):
        chosen_action = 0
        # 1/10 times player chooses a random action
        if random.random() > self.decay_gamma:
            chosen_action = random.choice(actions)  
        else:
            # Let's find action that has the biggest value
            max_gain = 0
            for i in actions:             
                next_state = self.steps_taken.copy()
                next_state.append(i)
                if next_state == None:
                    print("Next state on none")
                # If state with given action is None initialize with 0
                if self.state_value.get(repr(next_state)) == None:
                    pass
                else:
                    # Else let's check if it's larger that the maximim value 
                    # we have found so far
                    if self.state_value.get(repr(next_state)) > max_gain:
                        max_gain = self.state_value[repr(next_state)]
                        chosen_action = i
            if max_gain == 0:
               chosen_action = random.choice(actions)      
               
        self.steps_taken.append(chosen_action)      
        return chosen_action
       
    def steps_taken(self):
        return self.steps_taken
    
    def token(self):
        return self.token
    
    def update_state_values(self, reward, state):
        # If player has one with 3 steps, reward is higher
        if len(self.steps_taken) == 3 and reward == 10:
           reward = reward*3
        state_iter = len(state) -1
        i = len(self.steps_taken) - 1
        while state_iter > -1 and i > -1:
            # Only add reward to those steps that current player has taken
            if self.steps_taken[i] == state[state_iter]:
                if state_iter == 0:
                    current = repr([state[0]])
                else:
                    current = repr(state[:(state_iter+1)])
                if current == None:
                    print("Current on none")
                if self.state_value.get(current) is None:
                    self.state_value[current] = 0
                self.state_value[current] += self.lr * \
                                     (self.decay_gamma * reward - \
                                      self.state_value[current])
                reward = self.state_value[current]
                i = i - 1
            
            state_iter = state_iter - 1
    
    
    def save(self):
        w = csv.writer(open("player_{}.csv".format(self.token), "w"))
        for key, val in self.state_value.items():
            w.writerow([key, val])