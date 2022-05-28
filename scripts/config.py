from brian2 import * 

HOST = '192.168.0.15'   
PORT = 15051
env_id = '16x16'
t_run = 500*ms

configs = {
    "states":
    {
        "flgCollided": {"True": "i_cl"},
        "flgCannot": {"True": "i_cn"},
        "flgGrabbed": {"True": "i_gb"},
        "flgDied": {"True": "i_died"},
        "jsense":
        {
            "0": "i_vz",
            "1":{
                "goal": "i_gl",
                "initial": "i_ini",
                "breeze": "i_b",
                "flash": "i_f",
                "stench": "i_s"
            },
            "2":{
                "breeze_flash": "i_bf",
                "flash_breeze": "i_bf",
                "breeze_stench": "i_bs",
                "stench_breeze": "i_bs",
                "flash_stench": "i_fs",
                "stench_flash": "i_fs"
            },
            "3": "i_bfs"
        }
    },
    "behind":{
        "0": 2,
        "1": 3,
        "2": 0,
        "3": 1
    },
    "atrator":{
        "0": [1,3],
        "1": [0,2],
        "2": [1,3],
        "3": [0,2]
    },
    "comando":{
        "0": "{\"move\":[\"n\",1]}",
        "1": "{\"move\":[\"e\",1]}",
        "2": "{\"move\":[\"s\",1]}",
        "3": "{\"move\":[\"w\",1]}",
        "4": {"True": "{\"act\":[\"grab\",1]}"},
        "5": {"True": "{\"act\":[\"leave\",1]}"}
    },
    "energy":{
        "4x4": 20,
        "5x5": 25,
        "8x8": 65,
        "10x10": 100,
        "16x16": 200
    },
    "call":{
        "0": "{\"call\":[\"n\",1]}",
        "1": "{\"call\":[\"e\",1]}",
        "2": "{\"call\":[\"s\",1]}",
        "3": "{\"call\":[\"w\",1]}"
    },
    "neuron_num":{
        "Nr_nothing":21,
        "Nr_breeze":22,
        "Nr_flash":23,
        "Nr_stench":24,
        "Nr_breezeflash":25,
        "Nr_breezestench":26,
        "Nr_breezeflashstench":27,
        "Nr_flashstench":28,
        "Nr_danger":29,
        "Nr_obstruction":30,
        "Nr_goal":31,
        "Nr_initial":32,
        "Nr_reserva":33,
        "Nr_boundary":34,
        "Nr_cannot":35,
        "Nr_grabbed":36,
        "Nr_grab":44,
        "Nr_leave":45,
        "Nr_movenorth":41,
        "Nr_movesouth":42,
        "Nr_moveeast":43,
        "Nr_movewest":46,
        "Nr_calllenorth":47,
        "Nr_callsouth":48,
        "Nr_calleast":49,
        "Nr_callwest":50
        },
    "neuron_interp":{
        "i_vz":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_b":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_f": {"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_s":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_bf":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_bs":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_bfs": {"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_fs":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_died":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_gl":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_ini": {"@0": [0],"@100": ["neuron_n"],"@500": ["end"]},
        "i_cl":{"@0": [0],"@100": ["neuron_n"],"@500": ["end"]}
        }
}


