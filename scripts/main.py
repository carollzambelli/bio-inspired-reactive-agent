import utils as ut
import socket, json
from agent import Agent
from pynput import keyboard as kdb_read
from config import HOST, PORT, env_id, configs, t_run
from mind import mind
import brian
from brian2 import * 
from topology import topology

dim = 16        
agent = Agent(configs, mind) 
next_rand = [100, 112]
#iAct = None
iAct = 0
    
for exp_id in range(3):
    
    sttMM = "INICIAR"
    idd = " "
    energy = configs["energy"][env_id]
    config_id = "visaoB_"+ str(dim/4)
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
            jobj = ut.wait_answ(sock)                         
            if (('server' in jobj) and (jobj['server'] == 'connected')):
                sttMM = "RESTART" 
                break 
            
        while sttMM == "RESTART":       
            msg = "{\"call\":[\"restart\",1]}"
            sock.sendall(msg.encode('utf-8'))       
            sttMM = "RESETADO"
            break
        
        while sttMM == "RESETADO":   
            jobj = ut.wait_answ(sock)   
            if (('server' in jobj) and (jobj['server'] == 'restarted')): 
                around_map = ["i_ini"]
                i_sense = 0
                memory = None
                flgReward = False
                sttMM = "SENSOR"  
                break
    
        while sttMM == "RECEBER":
            jobj = ut.wait_answ(sock)    
            sttMM = "AVALIAR"                     
            break
        
        while sttMM == "AVALIAR":
            idd = ut.avaliar(jobj, configs, sense)
            i_sense = i_sense + 1
            around_map.append(idd)
            if i_sense < call:
                sttMM = "SENSOR" 
            else:
                sttMM = "PENSAR"   
            break
                
        while sttMM == "SENSOR":
            call = dim
            msg = ut.call_msg(i_sense, mind)
            sense = True
            sttMM = "ENVIAR"
            
        while sttMM == "PENSAR":
            print(sttMM, ": ", config_id, '-', exp_id)
            print(around_map)
            msg, iAct = agent.agent_action(around_map, iAct)  
            ut.log_table(env_id, config_id, exp_id, energy, around_map, iAct)
            energy = energy - 1
            i_sense = -1
            sense = False
            around_map = []
            sttMM = "ENVIAR"   
            break

        while sttMM == "ENVIAR":
            sttMM = ut.enviar(msg, sock)
            break
            
    kdb_read.Listener.stop
    sock.close() 
    print(idd)
    print(f'PROCESSO encerrado em {configs["energy"][env_id]-energy} loops')
            
    