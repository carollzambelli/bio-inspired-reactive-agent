from sympy import E, expand_log
import utils 
import json
import random
import numpy as np
import brian as br
from config import configs, t_run

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
            
        # se recuar = 1 e perseguir = 1, mesma direção desconsidera perseguir 
        for i in range(4):
            if lut[0][i] == lut[1][i]:
                lut[1][i] = 0
            
        final = []
            
        for i in range(4):
                        
            a = [lut[0][i], lut[1][i], lut[2][i]]
            
            avancar = 1
            if 1 in lut[1]: avancar = 0
                         
            b = [[lut[0][i]*-2]*3,[1,1,1],[avancar]*3]
            
            res = [0 if i<=0 else 1 for i in np.matmul(a, b)]
            final.append(sum(res)/3)
        
        possible_moves = [i for i,v in enumerate(final) if v > 0]
        possible_moves = list(set(possible_moves) - set([behind])) #agenteA->comentar
            
        if len(possible_moves) > 0:
            iNext = random.choice(possible_moves)
            msg = self.configs["comando"][str(iNext)]  
        else:
            iNext = behind
            msg = self.configs["comando"][str(iNext)]    
                        
        return msg, iNext
        

    def ortogonal_sense_brianagent(self, around_map, iAct):   
        
        explore_map = around_map[1:]

        for i in explore_map:
            stimulus_file = {
                "@0": [0],
                "@100": [configs['neuron_num'][i]],
                "@500": ["end"]
                }
            br.escrever_stimulus_json(stimulus_file) 

        br.net.restore()
        br.atualizar_input()
        br.net.run(t_run)
        br.net.store()

        quem_disparou = br.spike_mon_neurons.spike_trains() 

        #Num_disparos_Nr_rotateright = len(quem_disparou.get(Nr_rotateright))      
        #Num_disparos_Nr_rotateleft = len(quem_disparou.get(Nr_rotateleft))
        #Num_disparos_Nr_moveforward = len(quem_disparou.get(Nr_moveforward))  

        pass
    


    
