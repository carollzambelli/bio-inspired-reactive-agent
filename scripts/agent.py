from sympy import E
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
        return agents_catalog[self.mind['agente']](around_map, iAct)
        
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
        lut = [[0,0,0,0], [0,0,0,0], [0,0,0,0]]
        print(lut)
         
        if iAct != None:
            behind = self.configs['behind'][str(iAct)]
        else:
            behind = 1000000000

        for i in range(len(explore_map)):
            dist = int(i/4)
            direction = i%4
            code = self.mind["sensores"][explore_map[i]]
            if code == "recuar" and dist != 0 :
                code = "avançar"
            linha = self.mind["sensor_map"][code]
            lut[linha][direction] = (1 or lut[linha][direction])
            
        final = []
            
        for i in range(4):
                        
            a = [lut[0][i], lut[1][i], lut[2][i]]
            
            avancar = 1
            if 1 in lut[1] and 1 not in lut[0]: avancar = 0
                         
            b = [[lut[0][i]*-2]*3,[1,1,1],[avancar]*3]
            
            print("------------")
            print(a)
            print(b)
            print(np.matmul(a, b))
            
            res = [0 if i<=0 else 1 for i in np.matmul(a, b)]
            print("res=",res)
            final.append(sum(res)/3)
        
        possible_moves = [i for i,v in enumerate(final) if v > 0]
        print(possible_moves)
        possible_moves = list(set(possible_moves) - set([behind])) #agenteA->apagar
            
        if len(possible_moves) > 0:
            iNext = random.choice(possible_moves)
            msg = self.configs["comando"][str(iNext)]  
        else:
            iNext = behind
            msg = self.configs["comando"][str(iNext)]    
            
        print(final, possible_moves, iNext)
            
        return msg, iNext
        

        
    


    
