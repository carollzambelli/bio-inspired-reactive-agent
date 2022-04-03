import utils 
import json
import random
import numpy as np

class Agent:
    
    def __init__(self, configs, mind):
        self.configs = configs
        self.mind = mind
        
    def agent_action(self, around_map, iAct):
        
        agents_catalog = {
            1: self.dummy_agent,
            2: self.coward_agent,
            3: self.ortogonal_sense_agent
        }
    
        return agents_catalog[self.mind['agent']](around_map, iAct)

    def dummy_agent(self, around_map, iAct):
        
        explore_map = [around_map[0]]
        final = [0, 0, 0, 0]
        
        for i in range(len(explore_map)):
            key = explore_map[i]
            final = np.add(self.mind["mind"][key], final) 
        
        possible_moves = [i for i,v in enumerate(final) if v >= 0]    
        
        iNext = random.choice(possible_moves)        
        msg = self.configs["comando"][str(iNext)]  
        return msg, iNext

    def coward_agent(self, around_map, iAct):
        
        if iAct != None:
            behind = self.configs['behind'][str(iAct)]
            
        if around_map[0] in self.experimento['lista']:
            iNext = behind
        else:
            iNext = random.choice([0,1,2,3])    
                
        msg = self.configs["comando"][str(iNext)]  
        
        return msg, iNext, None
    
    def ortogonal_sense_agent(self, around_map, iAct):
                                
        explore_map = around_map[1:]
         
        if iAct != None:
            behind = self.configs['behind'][str(iAct)]
            explore_map[behind] = "behind"
            
        print(explore_map)
        final = [0, 0, 0, 0]
        
        for i in range(len(explore_map)):
            call = int(i/4)
            direction = self.configs['comando_map'][str(i%4)]
            key = explore_map[i]            
            final = np.add(self.mind["mind"][str(call)+direction][key], final) 
            
        reward = [i for i,v in enumerate(final) if v > 0]

        if len(reward) > 0:
            max_move = max(final)
            possible_moves = [i for i,v in enumerate(final) if v == max_move]
        else:
            possible_moves = [i for i,v in enumerate(final) if v >= 0]
            
        if len(possible_moves) > 0:
            iNext = random.choice(possible_moves)
            msg = self.configs["comando"][str(iNext)]  
        else:
            iNext = behind
            msg = self.configs["comando"][str(iNext)]    
            
        print(final, possible_moves, iNext)
            
        return msg, iNext
        

        
    


    
