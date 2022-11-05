import utils as ut
import socket
from agent import Agent
from pynput import keyboard as kdb_read
from config import HOST, PORT, configs, agent, flag_b, env_id, iAct

agent = Agent(configs, agent) 

for grid_reach in [4]:
    for exp_id in range(50):
        
        sttMM = "INICIAR"
        idd = " "
        energy = configs["energy"][env_id]
        config_id = "SNN_"+ str(grid_reach)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_address = (HOST, PORT)

        while idd != "YOU WIN"  and idd != "YOU DIED" and energy > 0:  
            
            while sttMM == "INICIAR":
                # Start connection with EnvSim 
                print(sttMM)
                sock.connect(server_address)
                sttMM = "RSPCONN"                  
                break
            
            while sttMM == "RSPCONN":
                # Start connection with EnvSim 
                print(sttMM)
                jobj = ut.wait_answ(sock)                         
                if (('server' in jobj) and (jobj['server'] == 'connected')):
                    sttMM = "RESTART" 
                    break 
                
            while sttMM == "RESTART":  
                # Reestart connection 
                msg = "{\"call\":[\"restart\",1]}"
                sock.sendall(msg.encode('utf-8'))       
                sttMM = "RESETADO"
                break
            
            while sttMM == "RESETADO":  
                # Reset the Envisim to clear all informations 
                jobj = ut.wait_answ(sock)   
                if (('server' in jobj) and (jobj['server'] == 'restarted')): 
                    X = ["i_ini"]
                    i_sense = 0
                    memory = None
                    flgReward = False
                    sttMM = "SENSOR"  
                    break
        
            while sttMM == "RECEBER":
                # Receive data from Envsim
                jobj = ut.wait_answ(sock)    
                sttMM = "AVALIAR"                     
                break
            
            while sttMM == "AVALIAR":
                # Code the data from EnvSim before give to agent
                idd = ut.avaliar(jobj, configs, sense)
                i_sense = i_sense + 1
                X.append(idd)
                if i_sense < call:
                    sttMM = "SENSOR" 
                else:
                    sttMM = "PENSAR"   
                break
                    
            while sttMM == "SENSOR":
                # Request data from EnvSim
                call = grid_reach*4
                msg = ut.call_msg(i_sense, grid_reach*4)
                sense = True
                sttMM = "ENVIAR"
                
            while sttMM == "PENSAR":
                # Agent decision
                print(sttMM, ": ", config_id, '-', exp_id)
                msg, iAct, X_ = agent.agent_action(X, iAct, flag_b)  
                ut.log_table(env_id, config_id, exp_id, energy, X, iAct, X_)
                energy = energy - 1
                i_sense = -1
                sense = False
                X = []
                sttMM = "ENVIAR"   
                break

            while sttMM == "ENVIAR":
                # Send agent movement decision to EnvSim
                sttMM = ut.enviar(msg, sock)
                break
                
        kdb_read.Listener.stop
        sock.close() 
        print(idd)
        print(f'PROCESSO encerrado em {configs["energy"][env_id]-energy} loops')
            
    