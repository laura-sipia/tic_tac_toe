import random
import csv

class Player:

    
    def __init__(self, token):
        self.steps_taken = []
        self.token = token
        self.state_value = {}
        self.lr = 0.2
        self.decay_gamma = 0.9
    
    def reset(self):
        self.steps_taken = []
    
    def play_turn(self, actions):
        print(actions)
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
                        max_gain == self.state_value[repr(next_state)]
                        chosen_action = i
            if max_gain == 0:
               chosen_action = random.choice(actions)      
               
        self.steps_taken.append(chosen_action)      
        return chosen_action
       
    def steps_taken(self):
        return self.steps_taken
    
    def token(self):
        return self.token
    
    def update_state_values(self, reward):
        i = len(self.steps_taken) - 1
        while i > -1:
            if i == 0:
                current = repr([self.steps_taken[0]])
            else:
                current = repr(self.steps_taken[:i])
            if current == None:
                print("Current on none")
            if self.state_value.get(current) is None:
                self.state_value[current] = 0
            self.state_value[current] += self.lr * \
                                 (self.decay_gamma * reward - \
                                  self.state_value[current])
            reward = self.state_value[current]
            i = i - 1
    
    def save(self):
        w = csv.writer(open("player_{}.csv".format(self.token), "w"))
        for key, val in self.state_value.items():
            w.writerow([key, val])