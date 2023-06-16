import numpy as np
from mesa import Agent
from utilities_file import *
from osbrain import run_agent


class Market(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        self.history = None
        self.information = None
        self.activity = None
        #self.last_activity = None
        self.minority = None
        #self.last_minority = None
        self.communicator = None

        if model.communication == 'active':
            
            self.communicator = run_agent(name= 'Market')


    def step(self):
        print('Market passing step')

    def step_1(self):
        #print('Market passing step_1') 
        pass

    def step_2(self):
        #print('Market doing its stuff')
        self.activity = self.model.calculate_activity()
        #print(f'Market activity : {self.activity}')
        self.minority = self.model.calculate_minority()
        #print(f'Market minority : {self.minority}')
        

    def step_3(self):
        #print('Market passing step_3')
        pass

    def step_4(self):
        self.history = np.append(self.history,int(rev_to_spin(self.minority)))
        
