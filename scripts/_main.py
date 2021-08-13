from numpy.lib.twodim_base import diag
import utils 
import socket, json
from datetime import date
import pandas as pd
from pynput import keyboard as kdb_read


with open('../configs/configs.json') as f1:
    configs = json.loads(f1.read())
    
HOST = '192.168.0.11'   
PORT = 15051

df = pd.DataFrame(
    columns=['env', 'config', 'exp', 'energy', 'current',
             'next_state', 'next_move'])

for config_id in ["exp_sensor1", "exp_sensor2"]:

    #config_id = 'exp_sensor3'

    with open('../configs/'+config_id+'.json') as f:
        experimento = json.loads(f.read())

    for exp_id in range(50):
        
        env_id = '5x5'
        sttMM = "INICIAR"
        energy = experimento["energy"][env_id]
        idd = " "
        diagonal = experimento["diagonal"]
        diag_map = []
        i_sense_diag = 0
        atrator_moves = []
        next_move_memory = []
        contador = 0
        sense_d = False

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
                    sttMM = "SENSOR"  
                    break
        
            while sttMM == "RECEBER":
                print(sttMM)
                jobj = utils.wait_answ(sock)    
                sttMM = "AVALIAR"                     
                break
            
            while sttMM == "AVALIAR":
                print(sttMM)
                idd, flgPossuiReward = utils.avaliar(jobj, configs, sense)
                if i_sense == -1:
                    around_map.append(idd)
                i_sense = i_sense + 1
                if i_sense < call:
                    around_map.append(idd)
                    sttMM = "SENSOR"  
                elif diagonal == "ON":
                    call_diag = experimento["total_calls_diag"]
                    if (i_sense_diag == 0) and (sense_d == False):
                        sttMM = "SENSOR-DIAG"
                    elif (i_sense_diag < call_diag-1) and (sense_d == True):
                        i_sense_diag = i_sense_diag + 1
                        diag_map.append(idd)
                        sttMM = "SENSOR-DIAG"
                    else:
                        sttMM = "PENSAR"  
                        sense_d = False
                        diag_map.append(idd)
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
                print(sttMM, i_sense_diag)
                msg = experimento["call-diag"][str(i_sense_diag)]
                sense_d = True
                sttMM = "ENVIAR"
            
            while sttMM == "PENSAR":
                print(sttMM, ": ", config_id, '-', exp_id)
                
                if diagonal == "ON":
                    msg, iAct, atrator_moves, next_move_memory, contador = utils.agent_action_diag(
                        configs, experimento,  around_map[1:], diag_map, iAct,
                        atrator_moves, next_move_memory, contador)  
                else:
                    msg, iAct = utils.agent_action(configs, experimento,  around_map[1:], iAct)
                
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
        
    hoje = str(date.today())
    save_path = f'../results/{config_id}_{hoje}.txt'
    df.to_csv(save_path, sep = ';', header=None, index=None, mode='a')