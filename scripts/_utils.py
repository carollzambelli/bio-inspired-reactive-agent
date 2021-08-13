import socket, json, random
import numpy as np
import random


def wait_answ(sock):                           
    respEnviSim = ''
    while respEnviSim == '':
        try:
            respEnviSim = sock.recv(256)    # recebe até 256 bytes
            jobj = json.loads(respEnviSim)  # converte a string em objeto Json
            print("R: ", jobj)              # imprime a mensagem recebida  
            return jobj
        except socket.error as e: 
            raise Exception("Socket error: ", str(e))
            
            
def enviar(msg, sock):
    while msg != 'esc':
        try: 
            sock.sendall(msg.encode('utf-8'))   
            print ("E: ", msg)                  
            next_state = "RECEBER"   
            msg = 'esc'                        
        except socket.error as e: 
            raise Exception("Socket error: ", str(e))   
    return next_state

def avaliar(jobj, configs, sense):
    
    flgGrabbed = False
    flgCannot = False
    flgCollided = False
    flgPossuiReward = False  
    flgDied = False  
    jsense = None
    
    if 'server' in jobj: jrasc = jobj['server'] 
    
    elif 'outcome' in jobj:
        if jobj['outcome'] == 'died': flgDied = True 
        elif jobj['outcome'] == 'grabbed': flgGrabbed = True
        elif jobj['outcome'] == 'cannot': flgCannot = True
        
    elif 'collision' in jobj:
        if jobj['collision'] == 'boundary': flgCollided = True
        
    elif 'sense' in jobj: jsense = jobj['sense']  
    
    else:
        raise Exception("Valores fora da avaliação estabelecida")
    
    
    if jsense == None:
        if flgCollided: idd = configs["states"]['flgCollided'][str(flgCollided)]
        if flgCannot: idd = configs["states"]['flgCannot'][str(flgCannot)]
        if flgGrabbed: idd = configs["states"]['flgCannot'][str(flgGrabbed)]
        if flgDied: idd = configs["states"]['flgDied'][str(flgDied)]
                    
    else:  
        if type(jsense) != list:
            jsense = [str(jsense)]
        if len(jsense) == 0: 
            idd = configs["states"]["jsense"][str(0)]
        elif len(jsense) == 1: 
            idd = configs["states"]["jsense"][str(1)][jsense[0]]
        elif len(jsense) == 2: 
            idd = configs["states"]["jsense"][str(2)][jsense[0]+"_"+jsense[1]]
        elif  len(jsense) == 3:
            idd = configs["states"]["jsense"][str(3)]
        else:
            raise Exception("Valores fora da política estabelecida")
        
        if sense == False:
            if idd == "i_gl": idd = "YOU WIN"
            elif idd == "i_died": idd = "YOU DIED"
              
    return idd, flgPossuiReward

def diag_moves(experimento, possible_moves, atrator_moves, next_move_memory, contador):
    
    if next_move_memory == []:
        atrator = random.choice(possible_moves)
        next_move_memory = experimento['atrator'][atrator]
        for move in next_move_memory:
            if move in possible_moves:
                atrator_moves.append(True)
            else:
                atrator_moves.append(False)
    else:
        contador = contador + 1   
    
    if atrator_moves[contador] == True:
        iNext = next_move_memory[contador]
        flgatrator = True
    else: 
        iNext = 0
        flgatrator = False
        next_move_memory = []
        
    print('-----ATRATOR-----: ', next_move_memory, atrator_moves, contador)
    return iNext, flgatrator, atrator_moves, next_move_memory, contador


def agent_decision(score_map, iAct, configs, experimento):
    
    flgatrator = False
    
    if len(score_map) > 4:
       score_map_lst = np.array_split(score_map, experimento["total_calls"]/4)
       score_map = score_map[:4]
       print(score_map, score_map_lst)
       for i in range(len(score_map_lst)-1):
           for j in range(4):
               score_map[j] = [score_map[j][0], (score_map[j][1] or score_map_lst[i+1][j][1])]
   
    if iAct != None:
        behind = configs['behind'][str(iAct)]
        score_map[behind] = 'behind'
    
    print('score_map: ', score_map)
    
    if experimento["mind"]["goal"] in score_map:
        possible_moves = [i for i, j in enumerate(score_map) if j == experimento["mind"]["goal"]]
        iNext = random.choice(possible_moves)
        flgatrator = True
    elif experimento["mind"]["ok"]  in score_map:
        possible_moves = [i for i, j in enumerate(score_map) if j == experimento["mind"]["ok"]]
        iNext = random.choice(possible_moves)
    elif "behind" in score_map:
        iNext = behind
    
    return iNext, flgatrator
            

def agent_action_diag(configs, experimento, around_map, diag_map, iAct,
                      atrator_moves, next_move_memory, contador):  
    
    flgatrator_d = False
    
    print('AROUND: ', around_map)
    print('DIAG: ', diag_map)
        
    score_map = [
        experimento["scores"][around_map[x]] for x in range(len(around_map)) ]
    
    score_map_diag = [
            experimento["scores"][diag_map[x]] for x in range(len(diag_map)) ]
    
    iNext_a, flgatrator_a = agent_decision(score_map, iAct, configs, experimento)
    
    if experimento["mind"]["goal"] in score_map_diag:
        possible_moves = [i for i, j in enumerate(score_map) if j == experimento["mind"]["ok"]]
        iNext_d, flgatrator_d, atrator_moves, next_move_memory, contador = diag_moves(
            experimento, possible_moves, 
            atrator_moves, next_move_memory, contador)
    
    if (flgatrator_a == False) and (flgatrator_d == True):
        iNext = iNext_d
    else:
        iNext = iNext_a

    msg = configs["comando"][str(iNext)]  
    
    return msg, iNext, atrator_moves, next_move_memory, contador


def agent_action(configs, experimento, around_map, iAct):  
    
    print('AROUND: ', around_map)
        
    score_map = [
        experimento["scores"][around_map[x]] for x in range(len(around_map))]
    
    iNext, flgatrator = agent_decision(score_map, iAct, configs, experimento)
        
    msg = configs["comando"][str(iNext)]  
    
    return msg, iNext
    

def log_table(df, env_id, config_id, exp_id, energy, around_map, iAct):
    
    df = df.append({
        'env': env_id,
        "config": config_id,
        "exp": exp_id,
        "energy": energy,
        "current": around_map[0],
        "next_state": around_map[1:][iAct],
        "next_move": iAct
        }, ignore_index=True)
    
    return df



'''
def atrator(configs, possible_moves, reward_memory, direcao, map):
        
    op = [1,1,-1,-1]
    
    if direcao == None:
        casas = int(map.index([0,1]))/4
        direcao = map.index([0,1])%4
        reward_memory[0] = direcao
        reward_memory[1] = [0,0,0,0]
        reward_memory[1][direcao] = op[direcao]*casas
    else:    
        if reward_memory[0] != 0:
            if direcao in possible_moves:
                iNext = direcao 
                reward_memory[0] = op[direcao]*(-1)
            else:
                lst = set(possible_moves).intersection(
                    configs["atrator"][str(direcao)])
                iNext = random.choice(lst)
                reward_memory[1][iNext] = op[iNext]
        else:
            pos = next((i for i, x in enumerate(reward_memory) if x), None)
            iNext = pos
            reward_memory[1][pos] = op[pos]*(-1)
    
    print(direcao, reward_memory)
                    
    return reward_memory, iNext, direcao

'''