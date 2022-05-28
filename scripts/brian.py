from brian2 import * 
from matplotlib import pyplot as plt
import json, socket, random
from enum import Enum

def ler_topology_json():
    with open("Topology17.json", "r", encoding="utf8") as f:
        return json.load(f)

def ler_stimulus_json():
    with open("Stimulus17.json", "r", encoding="utf8") as f:
        return json.load(f)

def escrever_stimulus_json(dados):
    with open("Stimulus17.json", "w", encoding="utf8") as f: #abre um arquivo, w é para escrever o arquivo, encoding é para ajustar os acentos
        json.dump(dados, f, ensure_ascii=False) #ensure_ascii é para ajustar os acentos

stimulus_file = {
"@0": [0],
"@500": ["end"]
}
escrever_stimulus_json(stimulus_file)

# Nomes dos neurônios
Nr_nothing=21
Nr_breeze=22
Nr_flash=23
Nr_stench=24
Nr_breezeflash=25
Nr_breezestench=26
Nr_breezeflashstench=27
Nr_flashstench=28
Nr_danger=29
Nr_obstruction=30
Nr_goal=31
Nr_initial=32
Nr_reserva=33
Nr_boundary=34
Nr_cannot=35
Nr_grabbed=36
Nr_grab=44
Nr_leave=45

Nr_movenorth=41
Nr_movesouth=42
Nr_moveeast=43
Nr_movewest=46

Nr_calllenorth=47
Nr_callsouth=48
Nr_calleast=49
Nr_callwest=50

# Cria e roda a SNN 1 vez
magic_network.schedule = ['start', 'groups', 'synapses', 'thresholds', 'resets', 'end'] # Para sincronizar input com neurons no Brian2. Input dispara neurons sem delay
data_topology = ler_topology_json()
t_run = 500*ms  # Tempo para o Brian(SNN) rodar, sempre em blocos de 500ms
Numero_de_run = 0  # Guarda quantas vezes a rede Brian(SNN) rodou
N = len(data_topology.keys()) # Número de neurônios
vrest = -70.0*mV # Potencial de repouso
tau = 2*ms 
R = 100*Mohm
   
# Modelo LIF - Leaky Integrate and Fire
eqs = '''
    dv/dt = ((vrest - v) + R*I)/tau : volt (unless refractory)
    I : amp
    '''
# Criação dos neurônios comuns (neurons)
neurons = NeuronGroup(N, eqs, threshold='v>-60.0*mV', reset='v=vrest', refractory=3*ms, method='exact') #method='linear')
neurons.v = -80*mV
neurons.I = 0*pA 
   
# Criação dos neurônios de estímulo (Número de input = Número de neurons)
# indices = array([0, 100]) # Qual neurônio dispara
# times = array([100, 100])*ms # Tempo de disparo do neurônio
# input = SpikeGeneratorGroup(N, indices, times, when='before_synapses')

# Criação dos neurônios de estímulo (Número de input = Número de neurons)
semente = random.randrange(100,200) # Random Integer no intervalo
indices = array([0, 100]) # Qual neurônio dispara
times = array([100, semente])*ms # Tempo de disparo do neurônio
input = SpikeGeneratorGroup(N, indices, times, when='before_synapses')

# Sinapses input-neurons (todos conectados)
Stimulus = Synapses(input, neurons, on_pre='v_post += 11*mV')
for item in range(N):
    Stimulus.connect(i=item, j=item);

# Sinapses da topologia - arquivo Json
syn = Synapses(neurons, neurons, 'w : volt', on_pre='v_post += w')

for item in range(N): # Todos os neurônios
    if ("#" + str(item)) in data_topology:
        info_json = data_topology[("#" + str(item))]
        if info_json["syns"]:
            info_json_syns = info_json["syns"]
            n_connections = len(info_json_syns)
            for xpto in range(n_connections):
                liga_json = info_json_syns[xpto][0]
                delay_json = info_json_syns[xpto][1]
                w_json = info_json_syns[xpto][2]
                syn.connect(i=item, j=liga_json) 
                syn.w[item, liga_json] = w_json*mV
                syn.delay[item, liga_json] = delay_json*ms

# Funções para extrair dados da simulação 
spike_mon_neurons = SpikeMonitor(neurons)
spike_mon_input = SpikeMonitor(input)

# Para o "multiple run"
net = Network(neurons, input, Stimulus, syn)
net.add(spike_mon_neurons)  # manually add the monitors
net.add(spike_mon_input)  # manually add the monitors
net.run(t_run)
net.store()
Numero_de_run = Numero_de_run + 1
quem_disparou2 = spike_mon_neurons.spike_trains() #coloca em um dicionario: "neuronio,tempos de disparo"

Num_disparos_Nr_rotateright = len(quem_disparou2.get(Nr_rotateright))      
Num_disparos_Nr_rotateleft = len(quem_disparou2.get(Nr_rotateleft))
Num_disparos_Nr_moveforward = len(quem_disparou2.get(Nr_moveforward))      

# função que faz a leitura de stimulus.json e atualiza input no Brian2
def atualizar_input():
    data_stimulus = ler_stimulus_json()
    tempo_fire = data_stimulus.keys()
    dummy_tempo = array([], dtype=float)
    dummy_neuroindice = array([], dtype=int)
    for item in tempo_fire:
        if (item) in tempo_fire:
            info = data_stimulus[item]
            for idx in range(len(info)):
                xpto = item.replace("@", "")
                dummy_tempo = np.append(dummy_tempo,xpto)            
                dummy_neuroindice = np.append(dummy_neuroindice,info[idx])
    dummy_tempo = dummy_tempo[:-1]
    dummy_neuroindice = dummy_neuroindice[:-1]
    tempo = numpy.zeros(len(dummy_tempo))  
    neuroindice = numpy.zeros(len(dummy_tempo))
    for item in range(len(dummy_tempo)):
        tempo[item] = dummy_tempo[item]
        neuroindice[item] = dummy_neuroindice[item]
    times1 = tempo*ms
    indices1 = neuroindice
    input.set_spikes(indices1, times1 + Numero_de_run*t_run)