from model_file import *



if __name__ == '__main__':
    modello=MinorityGame(3,5,3,'highest_score','random','active')

    market = modello.get_market()
    market_communicator = market.communicator
    print(market, market_communicator)
    
    """ Publish-Subscribe: in this example the market is the publsher and 
     the agents are subscriber. The market sends the history and all the 
      agents receive it """

    # System configuration
    market_address = market_communicator.bind('PUB', alias='main')
    
    for agent in modello.schedule.agents:
        if isinstance(agent,InductiveAgent):
            agent.communicator.connect(market_address, handler=log_message)
    

    # Market Send messages
    market_communicator.send('main', f'{market.history}')


    """ Push:  in this example the agents send information to the market"""

    # System configuration
    for agent in modello.schedule.agents:
        if isinstance(agent,InductiveAgent):
            agent_address = agent.communicator.bind('PUSH', alias='main') 
            market_communicator.connect(agent_address,handler=log_message)
    
    #agents Send messages (just an example on how they can send decisions to market)
    for agent in modello.schedule.agents:
        if isinstance(agent,InductiveAgent):
            agent.communicator.send('main', f'Hi, I am agent {agent.unique_id}, a.k.a {agent.communicator} ')
            s = agent.select_strategy()
            agent.communicator.send('main', f'I select strategy {s} ')
            action = agent.take_action(s,'100')
            agent.communicator.send('main', f'My action is {action} ')


   

    modello.nameserver.shutdown()