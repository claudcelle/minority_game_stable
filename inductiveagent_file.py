import numpy as np
from mesa import Agent
import random
from utilities_file import *
from osbrain import run_agent



class InductiveAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #self.market = self.model.get_market()
        
        self.strategies = self.model.init_strategies()
        self.scores = self.model.init_scores()
        self.capital = None
        self.last_action = None
        self.last_selected_strategy = None
        self.last_information = None

        self.communicator = None

        if model.communication == 'active':
            
            self.communicator = run_agent(str(self.unique_id))



    def select_strategy(self):
        # Selezione della strategia in base al tipo di selezione specificato nel modello
        strategy_selection = self.model.strategy_selection
        if strategy_selection == 'random':
            return self.select_random_strategy()
        elif strategy_selection == 'highest_score':
            return self.select_highest_score_strategy()
        else:
            raise ValueError("Tipo di selezione strategia non valido")
        
    def select_random_strategy(self):
        # Selezione casuale di una strategia
        return random.choice(self.strategies)
    
    def select_highest_score_strategy(self):
        # Selezione della strategia con lo score più alto
        max_score = np.max(self.scores)
        max_score_indices = np.where(self.scores == max_score)[0]
        selected_strategy_index = random.choice(max_score_indices)
        return self.strategies[selected_strategy_index]

    def take_action(self,selected_strategy,last_information):
        
        """ get information from the market (last m bits of history) 
        and convert it into an integer """
        market = self.model.get_market()
        information = array_to_integer(last_information)
        
        """ # convert selected strategies in binary format """
        binary_selected_strategy = integer_to_padded_binary(selected_strategy,self.model.memory)

        """ # select action """
        action = int(binary_selected_strategy[information])
        
        return to_spin(action)
    
    # 
    def evaluate_strategies(self):
        market = self.model.get_market()
        """ create an empty list to fill with the evaluation for each strategy """
        evaluation=[]

        for strategy in self.strategies:

            """ calculate the action that a certain strategy would have performed if
              it was called """
            virtual_action = self.take_action(strategy,self.last_information)

            """ Gives a positive mark to strategy if predicted the correct minority group """
            
            if virtual_action == market.minority:
                evaluation.append(0.01)
            else: 
                evaluation.append(-0.01)

        return np.array(evaluation)

    def update_scores(self):
        strategy_evaluation = self.evaluate_strategies()
        return self.scores+strategy_evaluation
        

    def step(self):
        print(f'Agent {self.unique_id} passing step ')

    def step_1(self):
        #print(f'Agent {self.unique_id} doing 1st step')
        self.last_information = self.model.get_information()
        self.last_selected_strategy = self.select_strategy() 
        self.last_action = self.take_action(self.last_selected_strategy,self.last_information)
        #print(f'Agent {self.unique_id} selected_strategy :{self.last_selected_strategy} => {integer_to_padded_binary( self.last_selected_strategy,self.model.memory)}')
        #print(f'Agent {self.unique_id} action :{self.last_action}')

    def step_2(self):
        #print(f'Agent {self.unique_id} passing step 2')
        pass

    def step_3(self):
        #print(self.scores)
        #print(f'Agent {self.unique_id}')
        #for index, strategy in enumerate(self.strategies):
        #    print(f'{strategy} => {integer_to_padded_binary( strategy,self.model.memory)} \n')
        strategies_evaluations = self.evaluate_strategies()
        #print(strategies_evaluations)
        self.scores = self.update_scores()
        
            #print(f'{strategies_evaluations[index]}')
        #print(self.scores)

    def step_4(self):
        pass
    