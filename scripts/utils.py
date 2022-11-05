import socket, json, random
import numpy as np
import random
import pandas as pd
import config
from enum import Enum
from datetime import date
from pynput import keyboard as kdb_read
from pynput.keyboard import Key, Controller



def wait_answ(sock):                           
    respEnviSim = ''
    while respEnviSim == '':
        try:
            respEnviSim = sock.recv(256)    # recebe até 256 bytes
            jobj = json.loads(respEnviSim)  # converte a string em objeto Json
            #print("R: ", jobj)              # imprime a mensagem recebida  
            return jobj
        except socket.error as e: 
            raise Exception("Socket error: ", str(e))
            
            
def enviar(msg, sock):
    while msg != 'esc':
        try: 
            sock.sendall(msg.encode('utf-8'))   
            #print ("E: ", msg)                  
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

def call_msg(i_sense, grid_reach):
    
    if i_sense > grid_reach:
        id = int((i_sense - grid_reach)/4) + 1
        msg = config.configs["call-diag"][str(i_sense%4)]
    else:
        id = int(i_sense/4) + 1
        msg = config.configs["call"][str(i_sense%4)]
     
    return msg[:-3] + str(id) + msg[-2:]
    

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
    
def log_table(env_id, config_id, exp_id, energy, around_map, iAct, X):
    
    df = pd.DataFrame({
        'env': [env_id],
        "config": [config_id],
        "exp": [exp_id],
        "energy": [energy],
        "died_1": X['i_died'][1] + X['i_cl'][1],
        "died_2": X['i_died'][2] + X['i_cl'][2],
        "died_3": X['i_died'][3] + X['i_cl'][3],
        "died_4": X['i_died'][4] + X['i_cl'][4],
        "perseguir_1": X['i_gl'][1] + X['i_bf'][1] + X['i_fs'][1] + X['i_f'][1],
        "perseguir_2": X['i_gl'][2] + X['i_bf'][2] + X['i_fs'][2] + X['i_f'][2],
        "perseguir_3": X['i_gl'][3] + X['i_bf'][3] + X['i_fs'][3] + X['i_f'][3],
        "perseguir_4": X['i_gl'][4] + X['i_bf'][4] + X['i_fs'][4] + X['i_f'][4],
        "current": [around_map[0]],
        "next_state": [around_map[1:][iAct]],
        "next_move": [iAct]
        })
    
    #hoje = str(date.today())
    save_path = f'../results/{env_id}/{config_id}.txt'
    df.to_csv(save_path, sep = ';', header=None, mode='a')
    
    return 0


    
    
     
    
