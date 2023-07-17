import random
import numpy as np
from config import params

class Agent:
    
    def __init__(self, configs, agent):
        self.configs = configs
        self.agent = agent
        self.mt = configs["mt"]
        self.grid_reach = params["grid_reach"]
        self.moves = params["moves"]
        
    def agent_action(self, around_map, iAct, flag_b):
        
        agents_catalog = {
            1: self.dummy_agent,
            2: self.coward_agent,
            3: self.markov_agent,
        }
        return agents_catalog[self.agent](around_map, iAct, flag_b)
        
    def dummy_agent(self, around_map, iAct=None, flag_b = False):
        
        if 'i_cl' in around_map[1:]:
            possible_moves = [1,2,3,4] - around_map[1:].index('i_cl')
         
        iActn = random.choice(possible_moves)        
        msg = self.configs["comando"][str(iActn)]  
        return msg, iActn

    def coward_agent(self, around_map, iAct=None, flag_b = False):
        
        if iAct != None:
            behind = self.configs['orientation'][str(iAct)][3]
            
        if around_map[0] in self.experimento['lista']:
            iActn = behind
        else:
            iActn = random.choice([0,1,2,3])    
                
        msg = self.configs["comando"][str(iActn)]  
        
        return msg, iActn, None

    def markov_agent(self, around_map, iAct, flag_b = False):
        
        envsim_info = around_map[1:]
        print(envsim_info, iAct)

        # Correct from <N,E,S,W> to <F,L,R,B>
        orientation = self.configs["orientation"][iAct]

        # Create a transition matrix for the turn
        mts = np.zeros((self.grid_reach, self.moves))
        for i in range(self.grid_reach):
            for j in range(self.moves):
                state = self.mt[envsim_info[self.grid_reach*i + orientation[j]]]
                if (i > 0) and (state == "i_died"):
                    mts[i][j] = 0
                else:
                    mts[i][j] = state

        print(mts)
        # Converge the matrix in one array for decision
        mt = [0,0,0,0]
        for i in range(self.grid_reach):
            mt = mts[i]*self.grid_reach + mt

        print(mt)
        # Assign the correct probabilities to transition matrix

        moves = {
            "foward": mt[0], 
            "left": mt[1],  
            "right": mt[2], 
            "back": mt[3]   
        }

        # For reward states, normalize the probabilities
        keys = [k for k,v in moves.items() if v > 0]
        values = [v for k,v in moves.items() if v > 0]

        if len(keys) > 0:
            arr = np.array(np.array(values) / min(values))
            arr1 = arr / sum(arr) # Sum total to 1.0
        else:
            keys = [k for k,v in moves.items() if v == 0 ]
            values = [v for k,v in moves.items() if v == 0]
            #Remove, if its possible, the back movement
            #if len(keys) > 0 and "back" in keys:
            #    id = keys.index("back")
            #    keys.remove("back")
            #    values.remove(values[id])
            p = [1/len(values)]*len(values)
            values = np.array(values) + np.array(p)

        for key in list(moves.keys()):
            if key in keys:
                moves[key] = values[keys.index(key)]
            else:
                moves[key] = 0
            
        move_options = list(moves.values())
        val_rand = random.random()  # random value between 0] --> 1]

        print(values, move_options, val_rand)

        tmp_value = 0
        for i in range(len(move_options)):
            tmp_value = move_options[i] + tmp_value
            if tmp_value > val_rand:
                iActn = orientation[i] #back to <N,E,S,W>
                break

        msg = self.configs["comando"][str(iActn)]
        print(msg, iActn, orientation, i)
        return msg, iActn
    

    #Denifir políticas em cima deste agente