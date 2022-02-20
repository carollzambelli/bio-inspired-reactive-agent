import utils 
import random


class Agent:
    
    def __init__(self, configs, experimento):
        self.configs = configs
        self.experimento = experimento

    def dummy_agent(self, around_map, iAct, memory, flgReward):
        
        iNext = random.choice([0,1,2,3])        
        msg = self.configs["comando"][str(iNext)]  
        return msg, iNext, None, False


    def coward_agent(self, around_map, iAct, memory, flgReward):
        
        if iAct != None:
            behind = self.configs['behind'][str(iAct)]
            
        if around_map[0] in self.experimento['lista']:
            iNext = behind
        else:
            iNext = random.choice([0,1,2,3])    
                
        msg = self.configs["comando"][str(iNext)]  
        
        return msg, iNext, None, False

    def ortogonal_sense_agent(self, around_map, iAct, memory, flgReward):
        
        around_map = around_map[1:]
        explore_map = utils.explore(
            around_map[:self.experimento["total_calls"]],
            self.experimento,
            self.experimento["total_calls"])
        
                        
        if iAct != None:
            behind = self.configs['behind'][str(iAct)]
            explore_map[behind] = [1,0] #força o agente a não voltar de onde veio
            
        print(explore_map)

        if self.experimento["mind"]["goal"] in explore_map:
            possible_moves = [
                i for i, j in enumerate(explore_map) if j == self.experimento["mind"]["goal"]]   
            flgReward = True  
        elif self.experimento["mind"]["ok"]  in explore_map:
            possible_moves = [
                i for i, j in enumerate(explore_map) if j == self.experimento["mind"]["ok"]]
        else:
            possible_moves = [behind]
        
        iNext = random.choice(possible_moves)
        msg = self.configs["comando"][str(iNext)]  
        
        return msg, iNext, possible_moves, flgReward


    def diag_sense_agent(self, around_map, iAct, memory, flgReward):
        
        around_map = around_map[1:]
        msg, iNext, possible_moves, flgReward = self.ortogonal_sense_agent(around_map, iAct, memory, flgReward)
        
        explore_map_diag = utils.explore(
            around_map[self.experimento["total_calls"]:],
            self.experimento,
            self.experimento["total_calls_diag"])
        
        if (self.experimento["mind"]["goal"] in explore_map_diag) or (memory != None):
            possible_moves_d = [
                i for i, j in enumerate(explore_map_diag) if j == self.experimento["mind"]["goal"]]
            memory = utils.diag_moves(self.experimento, possible_moves_d, possible_moves, memory) 
            
        if (flgReward == False) and (memory != None):
            if len(memory) > 0:
                iNext = memory[0]   
                flgReward = True     
            
        msg = self.configs["comando"][str(iNext)]  
        
        return msg, iNext, memory, flgReward
    
    
    def agent_action(self, around_map, iAct, memory, flgPossuiReward):
        
        agents_catalog = {
            1: self.dummy_agent,
            2: self.coward_agent,
            3: self.ortogonal_sense_agent,
            4: self.diag_sense_agent
        }
        
        agent_id = self.experimento['agent']
        
        return agents_catalog[agent_id](around_map, iAct, memory, flgPossuiReward)