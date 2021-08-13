import socket, json, random
import numpy as np
import random
from enum import Enum
#from q_learning import QAgent
from pynput import keyboard as kdb_read
from pynput.keyboard import Key, Controller


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
        #if jobj['outcome'] == 'died': raise Exception("morreu")
        #elif jobj['outcome'] == 'left': raise Exception("saiu")
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
              
    return idd

def calc_score_map(around_map, experimento, call):
    
    score_map = [
        experimento["scores"][around_map[x]] for x in range(len(around_map)) 
        ]
        
    if len(score_map) > 4:
       score_map_lst = np.array_split(score_map, call/4)
       score_map = score_map[:4]
       print(score_map, score_map_lst)
       for i in range(len(score_map_lst)-1):
           for j in range(4):
               score_map[j] = [score_map[j][0], (score_map[j][1] or score_map_lst[i+1][j][1])]
               
    return score_map


def diag_moves(experimento, possible_moves_d, possible_moves, memory):
    
    if memory == None:
        atrator = random.choice(possible_moves_d)
        memory = experimento['diag_move'][str(atrator)]
        if memory[0][0] in possible_moves:
            memory = memory[0]
        elif memory[1][0] in possible_moves:
            memory = memory[1]
        else:
            memory = []
    else:
        memory = memory[1:]
    
    print(memory)

    return memory
    

def agent_action(configs, experimento, around_map, iAct, memory):  
    
    print('AROUND: ', around_map)
    flgPossuiReward = False
        
    score_map = calc_score_map(around_map[:experimento["total_calls"]], experimento, experimento["total_calls"])
   
    if iAct != None:
        behind = configs['behind'][str(iAct)]
        score_map[behind] = 'behind'
    
    print('score_map: ', score_map)
        
    if experimento["mind"]["goal"] in score_map:
        possible_moves = [i for i, j in enumerate(score_map) if j == experimento["mind"]["goal"]]
        flgPossuiReward = True
    elif experimento["mind"]["ok"]  in score_map:
        possible_moves = [i for i, j in enumerate(score_map) if j == experimento["mind"]["ok"]]
    elif "behind"  in score_map:
        possible_moves = [i for i, j in enumerate(score_map) if j == experimento["mind"]["behind"]]
        
    iNext = random.choice(possible_moves)
        
    if experimento["diagonal"] == "ON" :
        score_map_diag = calc_score_map(around_map[experimento["total_calls"]:], experimento, experimento["total_calls_diag"])
        print('score_map_diag: ', score_map_diag)
        if (experimento["mind"]["goal"] in score_map_diag) or (memory != None):
            possible_moves_d = [i for i, j in enumerate(score_map_diag) if j == experimento["mind"]["goal"]]
            memory = diag_moves(experimento, possible_moves_d, possible_moves, memory)
   
    if (flgPossuiReward == False) and (memory != None):
        if len(memory) > 0:
            iNext = memory[0]        
        
    msg = configs["comando"][str(iNext)]  
    
    return msg, iNext, score_map, memory

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


    
    
    
    

