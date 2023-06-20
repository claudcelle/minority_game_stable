
import numpy as np
from mesa import  Model
from mesa import time
import random
from mesa.datacollection import DataCollector


from osbrain import  run_nameserver

from inductiveagent_file import * 
from market_file import *


class MinorityGame(Model):
    def __init__(self, memory, num_agents, num_strategies, strategy_selection, history_initialization, temperature = 1,communication=None):
        self.memory = memory
        self.num_agents = num_agents
        self.num_strategies = num_strategies
        self.strategy_selection = strategy_selection
        self.history_initialization = history_initialization 
        self.temperature = temperature
        
        self.schedule = time.StagedActivation(self,['step_1','step_2','step_3','step_4'])

        self.datacollector = DataCollector(model_reporters={'Activity' : lambda m: m.get_activity()})
        self.nameserver = None

        self.communication = communication
        
        if self.communication == 'active':
            self.nameserver=run_nameserver()

        if num_agents % 2 != 0:
            self.num_agents = num_agents
        else:
            raise ValueError('ERROR: Number_of_agents must be odd')  
        
        if memory > 0:
            self.memory = memory
        else:
            raise ValueError('ERROR: Memory must be greater than zero') 
        
        if num_strategies > 1:

            self.num_strategies = num_strategies
        else:
            raise ValueError('Error: at least two strategy')
        

        
        if strategy_selection not in ['random','highest_score','thermal_score']:
    
            raise ValueError("Tipo di selezione strategia non valido")
        
        if history_initialization not in ['random','data']:
            
            raise ValueError("Tipo di inizializzazione storia non valido")
        

         # Creazione del mercato con la storia
        market = Market(0, self)
        market.history = self.init_history()
        #self.schedule.append(market)
        self.schedule.add(market)

        
            
        # Creazione degli agenti con le strategie
        for i in range(1,self.num_agents + 1):
            
            agent = InductiveAgent(i, self)
            self.schedule.add(agent)

        
        

        # print(self.nameserver.agents())
        # for agent in self.schedule.agents:
        #     agent.communicator.log_info('hello dhn')


        


    
    def init_history(self):
        # Inizializzazione della storia di mercato in base al tipo di inizializzazione specificato nel modello
        
        if self.history_initialization == 'random':
            return np.random.randint(2, size=self.memory)
        elif self.history_initialization == 'data':
            raise ValueError('not implemented yet')
        else:
            raise ValueError("Tipo di selezione strategia non valido")

    def init_strategies(self):
        l = []
        while(len(l)<self.num_strategies):
            s = random.randint(0, 2**2**self.memory)
            if s not in l:
                l.append(s)
        return np.array(l)

    def init_scores(self):
        return np.zeros(self.num_strategies)
        

    def calculate_activity(self):
        actions = self.get_actions()
        return sum(actions)
    

    def get_activity(self):
        market = self.get_market()
        return market.activity
                

    def calculate_minority(self):
        # activity = self.get_activity()
        # return -np.sign(activity)
        actions = self.get_actions()
        return -np.sign(sum(actions))
    
    def get_minority(self):
        market = self.get_market()
        return market.minority
    
    def get_information(self):
        market = self.get_market()
        return market.history[-self.memory:]

    def update_history(self):
        market = self.get_market()
        minority = self.get_minority()
        market.history = np.append(market.history,minority)
        
    # returns the set of inductive agents 
    def get_agents(self):
        agents_set=set()
        for agent in self.schedule.agents:
            if isinstance(agent, InductiveAgent):
                agents_set.add(agent)
        return agents_set
    
    #return a list of the actions taken by each agent at last turn
    def get_actions(self):
        agents_set= self.get_agents()
        actions_list = []
        for agent in agents_set:
            action = agent.last_action
            actions_list.append(action)
        return np.array(actions_list)

    def get_market(self):
        return self.schedule.agents[0]

    def print_agent_strategies(self):
        # Stampa le strategie di tutti gli agenti
        for agent in self.schedule.agents[-self.num_agents:]:
            if isinstance(agent, InductiveAgent):
                print(f"Agente {agent.unique_id}: strategies {agent.strategies} scores {agent.scores}")
    
    def print_market_history(self):
        market = self.get_market()
        print(f"Market History: {market.history}")

    def step(self):
        market = self.get_market()
        #print(f'Time step: {self.schedule.steps}')
        #print(f'Available information: {market.history[-self.memory:]} => {array_to_integer(market.history[-self.memory:])}')
        self.schedule.step()
        self.datacollector.collect(self)
        #print(f'Time step: {self.schedule.steps}')
