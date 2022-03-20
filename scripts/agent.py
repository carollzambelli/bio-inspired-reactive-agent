import utils 
import json
import random
import numpy as np

with open('minds/ortogonal_sense_4.json') as f1:
    mind = json.loads(f1.read())

class Agent:
    
    def __init__(self, configs, experimento):
        self.configs = configs
        self.experimento = experimento
        
        
    def agent_action(self, around_map, iAct):
        
        agents_catalog = {
            1: self.dummy_agent,
            2: self.coward_agent,
            3: self.ortogonal_sense_agent
        }
        
        agent_id = self.experimento['agent']
        
        return agents_catalog[agent_id](around_map, iAct)

    def dummy_agent(self, around_map, iAct):
        
        iNext = random.choice([0,1,2,3])        
        msg = self.configs["comando"][str(iNext)]  
        return msg, iNext, None


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
                
        around_map = around_map[1:]
        explore_map = utils.explore(
            around_map[:self.experimento["total_calls"]],
            self.experimento,
            self.experimento["total_calls"])
         
        if iAct != None:
            behind = self.configs['behind'][str(iAct)]
            
        final = mind["final"]
            
        for i in explore_map:
            call = int(i/4)
            direction = i%4
            key = explore_map[i]
            mind[call][key][i]
            final[key] = np.add(mind[call][key][direction], final[key]) 
            
        dataMatrix = np.array([final[i] for i in list(final.keys())])
        possible_moves = [sum(x) for x in zip(*dataMatrix)]
        moves = [i for i,v in enumerate(possible_moves) if v > 0]
        
        if len(moves) > 0:
            # tem que escolher o maior , mas saber quando forem iguais
            pass
        else:
            moves = [i for i,v in enumerate(possible_moves) if v >= 0]
            iNext = random.choice(moves)
            
        msg = self.configs["comando"][str(iNext)]  
            
        return msg, iNext
        

        
    


    
