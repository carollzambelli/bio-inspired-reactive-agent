from brian2 import * 
from matplotlib import pyplot as plt
import json, socket, random
from enum import Enum
from topology import topology


def run_network(t_run, indices, times):
    
    magic_network.schedule = ['start', 'groups', 'synapses', 'thresholds', 'resets', 'end'] 
    Numero_de_run = 0  
    N = len(topology.keys()) 
    vrest = -70.0*mV 
    tau = 2*ms 
    R = 300*Mohm

    eqs = '''
        dv/dt = ((vrest - v) + R*I)/tau : volt (unless refractory)
        I : amp
        '''

    # Criação dos neurônios comuns (neurons)
    neurons = NeuronGroup(N, eqs, threshold='v>-60.0*mV', reset='v=vrest', refractory=3*ms, method='exact') #method='linear')
    neurons.v = -80*mV
    neurons.I = 0*pA 
    
    inp = SpikeGeneratorGroup(N, indices, times, when='before_synapses')
    Stimulus = Synapses(inp, neurons, on_pre='v_post += 11*mV')
    for item in range(N):
        Stimulus.connect(i=item, j=item)

    syn = Synapses(neurons, neurons, 'w : volt', on_pre='v_post += w')
    
    for item in range(N): 
        if ("#" + str(item)) in topology:
            info_json = topology[("#" + str(item))]
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

    state_mon = StateMonitor(neurons, 'v', record = True)
    spike_mon_neurons = SpikeMonitor(neurons)
    spike_mon_input = SpikeMonitor(inp)

    net = Network(neurons, inp, Stimulus, syn)
    net.add(state_mon)
    net.add(spike_mon_neurons)  
    net.add(spike_mon_input)
    net.run(t_run)
    
    return list(set(spike_mon_neurons.i)), spike_mon_neurons


def random_choose(rand_nrs, spikemn):
    
    win, lst, next_n = [], [], []
    
    for j in range(len(rand_nrs)):
        win.append(max([i for i, x in enumerate(list(spikemn.i)) if x in rand_nrs[j]]))
        lst = lst + rand_nrs[j]
    
    Nr_win = rand_nrs[win.index(max(win))]
    
    for j in range(len(Nr_win)):
        next_n.append(max([i for i, x in enumerate(list(spikemn.i)) if x == Nr_win[j]]))
        
    winner = Nr_win[next_n.index(max(next_n))]
    if winner == max(lst):
        next_neuron = min(lst)
    else:
        next_neuron = winner +1
        
    return winner, next_neuron