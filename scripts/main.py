import utils 
import socket, json, random
import pandas as pd
from datetime import date
from enum import Enum
from pynput import keyboard as kdb_read
from pynput.keyboard import Key, Controller

    
with open('../configs/configs.json') as f1:
    configs = json.loads(f1.read())
    
HOST = '192.168.0.11'   
PORT = 15051


for config_id in ["exp_sensor1", "exp_sensor2", "exp_sensor3", "exp_sensor4", "exp_sensor5"]:

    hoje = str(date.today())
    #config_id = 'exp_sensor5' 
    save_path = f'../results/{config_id}_{hoje}.txt'


    df = pd.DataFrame(
        columns=['env', 'config', 'exp', 'energy', 'current',
                'next_state', 'next_move'])

    with open('../configs/'+config_id+'.json') as f:
        experimento = json.loads(f.read())
        

    for exp_id in range(50):
        
        env_id = '10x10'
        sttMM = "INICIAR"
        idd = " "
        
        energy = experimento["energy"][env_id]
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_address = (HOST, PORT)

        while idd != "YOU WIN"  and idd != "YOU DIED" and energy > 0:    
            while sttMM == "INICIAR":
                print(sttMM)
                sock.connect(server_address)
                sttMM = "RSPCONN"                   
                break
            
            while sttMM == "RSPCONN":
                print(sttMM)
                jobj = utils.wait_answ(sock)                         
                if (('server' in jobj) and (jobj['server'] == 'connected')):
                    sttMM = "RESTART" 
                    break 
                
            while sttMM == "RESTART":       
                print(sttMM)
                msg = "{\"call\":[\"restart\",1]}"
                sock.sendall(msg.encode('utf-8'))       
                sttMM = "RESETADO"
                break
            
            while sttMM == "RESETADO":   
                print(sttMM)    
                jobj = utils.wait_answ(sock)   
                if (('server' in jobj) and (jobj['server'] == 'restarted')): 
                    around_map = ["i_ini"]
                    i_sense = 0
                    iAct = None
                    memory = None
                    sttMM = "SENSOR"  
                    break
        
            while sttMM == "RECEBER":
                print(sttMM)
                jobj = utils.wait_answ(sock)    
                sttMM = "AVALIAR"                     
                break
            
            while sttMM == "AVALIAR":
                print(sttMM)
                idd = utils.avaliar(jobj, configs, sense)
                i_sense = i_sense + 1
                around_map.append(idd)
                if i_sense < call:
                    sttMM = "SENSOR" 
                elif ((i_sense - call) < experimento["total_calls_diag"]) and (experimento["diagonal"] == "ON"): 
                    sttMM = "SENSOR-DIAG"
                else:
                    sttMM = "PENSAR"   
                break
                    
            while sttMM == "SENSOR":
                print(sttMM, i_sense)
                call = experimento["total_calls"]
                msg = experimento["call"][str(i_sense)]
                sense = True
                sttMM = "ENVIAR"
                
            while sttMM == "SENSOR-DIAG":
                print(sttMM, (i_sense - call))
                msg = experimento["call-diag"][str((i_sense - call))]
                sense = True
                sttMM = "ENVIAR"
            
            while sttMM == "PENSAR":
                print(sttMM, ": ", config_id, '-', exp_id)
                
                msg, iAct, score_map, memory  = utils.agent_action(
                    configs, experimento, around_map[1:], iAct, memory)  
                            
                df = utils.log_table(df, env_id, config_id, exp_id, energy, around_map, iAct)
                            
                energy = energy - 1
                i_sense = -1
                sense = False
                around_map = []
                sttMM = "ENVIAR"   
                break

            while sttMM == "ENVIAR":
                print(sttMM)
                print(msg)
                sttMM = utils.enviar(msg, sock)
                break
                
        kdb_read.Listener.stop
        sock.close() 
        print(idd)
        print(f'PROCESSO encerrado em {experimento["energy"][env_id]-energy} loops')
            
    df.to_csv(save_path, sep = ';', header=None, index=None, mode='a')