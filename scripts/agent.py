import random as r
import numpy as np
from brian2 import * 
from config import configs, t_run
import brian


class Agent:
    
    def __init__(self, configs, agent):
        self.configs = configs
        self.agent = agent
        #falta o experimento do coward
        
    def agent_action(self, around_map, iAct, flag_b):
        
        agents_catalog = {
            1: self.dummy_agent,
            2: self.coward_agent,
            3: self.ortogonal_sense_agent,
            4: self.ortogonal_sense_brianagent
        }
        return agents_catalog[self.agent](around_map, iAct, flag_b)
        
    def dummy_agent(self, around_map, iAct=None, flag_b = False):
        
        if 'i_cl' in around_map[1:]:
            possible_moves = [1,2,3,4] - around_map[1:].index('i_cl')
         
        iNext = random.choice(possible_moves)        
        msg = self.configs["comando"][str(iNext)]  
        return msg, iNext

    def coward_agent(self, around_map, iAct=None, flag_b = False):
        
        if iAct != None:
            behind = self.configs['behind'][str(iAct)]
            
        if around_map[0] in self.experimento['lista']:
            iNext = behind
        else:
            iNext = random.choice([0,1,2,3])    
                
        msg = self.configs["comando"][str(iNext)]  
        
        return msg, iNext, None

    def world_code(self, around_map, iAct, flag_b):

        if iAct != 100:
            behind = self.configs['behind'][str(iAct)]

        print(iAct)
        
        k = int((len(around_map)-1)/4)
        if k > 1:
            for j in range(5,5+4*(k-1)):
                if (around_map[j] == 'i_died') | (around_map[j] == 'i_cl'):
                    around_map[j] = 'i_vz'
        print(around_map)
        tmp = [[around_map[0]],0,0,0,0]
        
        for i in range(1,5):
            tmp[i] = [around_map[i+4*(j)] for j in range(k)]
            
        print(tmp)
        X = {
        "i_ini" : [0, 0, 0, 0, 0],
        "i_vz"  : [0, 0, 0, 0, 0],
        "i_bfs" : [0, 0, 0, 0, 0],
        "i_b"   : [0, 0, 0, 0, 0],
        "i_s"   : [0, 0, 0, 0, 0],
        "i_bs"  : [0, 0, 0, 0, 0],
        "i_gl"  : [0, 0, 0, 0, 0],
        "i_bf"  : [0, 0, 0, 0, 0],
        "i_fs"  : [0, 0, 0, 0, 0],  
        "i_f"   : [0, 0, 0, 0, 0],
        "i_cl"  : [0, 0, 0, 0, 0],
        "i_died": [0, 0, 0, 0, 0]
    }
        for i in range(5):
            for sense in tmp[i]:
                X[sense][i] = 1

        print(X)
        return behind, X
    
    def ortogonal_sense_agent(self, around_map, iAct, flag_b): #flag de 2B
                                         
        behind, X = self.world_code(self, around_map, iAct, flag_b)

        if sum(X['i_died']) | sum(X['i_cl']) >= 3:
            iNext = behind
            print("RECUAR")
        else:
            X_morte = list(
            set([i for i, x in enumerate(X['i_died'][1:]) if x == 1] +\
                [i for i, x in enumerate(X['i_cl'][1:]) if x == 1])
            ) 
            print(X_morte)
            X_perseguir, X_avancar = [], []
            for j in range(4):
                for sense in ['i_gl', 'i_f', 'i_bf', 'i_fs', 'i_bfs']:
                    if (X[sense][j+1] == 1) & (j not in X_morte): 
                        X_perseguir.append(j)
                    elif j not in X_morte:
                        X_avancar.append(j)
            
            X_avancar = list(set(X_avancar))
            X_perseguir = list(set(X_perseguir))

           
            if (flag_b) & (iAct != 100):
                print("2B")
                if behind in X_perseguir: X_perseguir.remove(behind)
                if behind in X_avancar: X_avancar.remove(behind)

            print(X_avancar, X_perseguir)

            if len(X_perseguir) > 0:
                print("PERSEGUIR")
                iNext = r.choice(X_perseguir)
            else:
                print("AVANÇAR")
                iNext = r.choice(X_avancar)

            
        msg = self.configs["comando"][str(iNext)]    
                        
        return msg, iNext, X
        
    def ortogonal_sense_brianagent(self, around_map, iAct, flag_b = True):   
        
        behind, X = self.world_code(around_map, iAct, flag_b)

        explore_map = around_map[1:]
        indices = [0]

        count_f, count_r, count_l = 0,0,0
        for i in range(len(explore_map)):

            value = explore_map[i]
            if (int(i/4) != 0) and value in ['i_cl', 'i_died']:
                value = "i_vz"

            neuron = configs["neuron_interp"][value] + \
                     configs["direction"][str(iAct)][int(i%4)]
            
            neuron_n = configs['neuron_num'][neuron]
            
            if neuron_n in [23,25,27,28,31]:
                count_f +=  1
                if count_f > 1: neuron_n = 21
            elif neuron_n in [35,37,39,40,43]:
                count_l +=  1
                if count_l > 1: neuron_n = 33
            elif neuron_n in [55,47,49,51,52]:
                count_r +=  1
                if count_r > 1: neuron_n = 45
                
            indices.append(neuron_n)
            
        next_rand = [r.randint(100, 111), r.randint(112, 119)]
        for i in range(len(next_rand)):
            indices.append(next_rand[i])

        print("iniciando rede brian")
        val = brian.run_network(t_run, indices)
        
        if val == "behind":
            iNext = self.configs['behind'][str(iAct)]
        else:
            iNext = configs["direction"][str(iAct)][val]

        print(val, iNext, iAct)
        msg = self.configs["comando"][str(iNext)]    

        return msg, iNext, X


    