import utils
import socket
from agent import Agent
from pynput import keyboard as kdb_read
from config import params, configs, iAct, sttMM, idd

#exp_id = número do experimento
#iAct = ação a ser executada no mundo

agent = Agent(configs, params["agent"]) 

for exp_id in range(50): 

    energy = configs["energy"][params["env_id"]]
    config_id = "MK_"+ str(params["grid_reach"])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_address = (params["HOST"], params["PORT"])

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
            jobj = utils.wait_answ(sock)                         
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
            jobj = utils.wait_answ(sock)   
            if (('server' in jobj) and (jobj['server'] == 'restarted')): 
                around_map = ["i_ini"]
                i_sense = 0
                memory = None
                flgReward = False
                sttMM = "SENSOR"  
                break
    
        while sttMM == "RECEBER":
            # Receive data from Envsim
            jobj = utils.wait_answ(sock)    
            sttMM = "AVALIAR"                     
            break
        
        while sttMM == "AVALIAR":
            # Code the data from EnvSim before give to agent
            idd = utils.avaliar(jobj, configs, sense)
            i_sense = i_sense + 1
            around_map.append(idd)
            if i_sense < call:
                sttMM = "SENSOR" 
            else:
                sttMM = "PENSAR"   
            break
                
        while sttMM == "SENSOR":
            # Request data from EnvSim
            call = params["grid_reach"]*4
            msg = utils.call_msg(i_sense, params["grid_reach"]*4)
            sense = True
            sttMM = "ENVIAR"
            
        while sttMM == "PENSAR":
            # Agent decision
            print(sttMM, ": ", config_id, '-', exp_id)
            msg, iAct = agent.agent_action(around_map, iAct, params["flag_b"])  
            utils.log_table(params["env_id"], config_id, exp_id, energy, around_map, iAct)
            energy = energy - 1
            i_sense = -1
            sense = False
            around_map = []
            sttMM = "ENVIAR"   
            break

        while sttMM == "ENVIAR":
            # Send agent movement decision to EnvSim
            sttMM = utils.enviar(msg, sock)
            break
            
    kdb_read.Listener.stop
    sock.close() 
    print(idd)
    print(f'PROCESSO encerrado em {configs["energy"][params["env_id"]]-energy} loops')
            
    