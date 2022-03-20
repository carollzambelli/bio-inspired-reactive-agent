import utils 
import socket, json
from agent import Agent
from pynput import keyboard as kdb_read
from config import HOST, PORT, env_id, configs


#with open('../configs/configs.json') as f1:
#    configs = json.loads(f1.read())
    
#for config_id in configs["agents"]:
for config_id in ["exp_agent3-4"]:

    with open('../experimentos/'+config_id+'.json') as f: 
        experimento = json.loads(f.read())
        
    agent = Agent(configs, experimento) 
        
    for exp_id in range(50):
        
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
                    flgReward = False
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
                else:
                    sttMM = "PENSAR"   
                break
                    
            while sttMM == "SENSOR":
                print(sttMM, i_sense)
                call = utils.total_call(experimento)
                msg = utils.call_msg(i_sense, experimento)
                sense = True
                sttMM = "ENVIAR"
                
            while sttMM == "PENSAR":
                print(sttMM, ": ", config_id, '-', exp_id)
                
                msg, iAct = agent.agent_action(around_map, iAct, memory)  
                utils.log_table(env_id, config_id, exp_id, energy, around_map, iAct)
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
            
    