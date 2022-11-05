from brian2 import * 

HOST = '172.23.224.1'   
PORT = 15051
env_id = '16x16'
grid_reach = 4
agent = 4
flag_b = True
iAct =  0 #=100 para os ortogonais
t_run = 400*ms

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
       "sensores":{
        "i_ini" : [0, 0, 0, 0, 0],
        "i_vz"  : [0, 0, 0, 0, 0],
        "i_bfs" : [0, 0, 0, 0, 0],
        "i_b"   : [0, 0, 0, 0, 0],
        "i_s"   : [0, 0, 0, 0, 0],
        "i_bs"  : [0, 0, 0, 0, 0],
        "i_gl"  : [0, 0, 0, 0, 0],
        "i_bf"  : [0, 0, 0, 0, 0],
        "i_fs"  : [0, 0, 0, 0, 0],  
        "i_f"   : [0, 0, 0, 0, 0],
        "i_cl"  : [0, 0, 0, 0, 0],
        "i_died": [0, 0, 0, 0, 0]
    },
    "behind":{
        "0": 2,
        "1": 3,
        "2": 0,
        "3": 1
    },
    "direction":{
        "0": {
            0:"_f",
            1:"_r",
            3:"_l",
            2:"_b",
            "Nr_movefront":0,
            "Nr_moveright":1,
            "Nr_moveleft":3},
        "1": {
            1:"_f",
            2:"_r",
            0:"_l",
            3:"_b",
            "Nr_movefront":1,
            "Nr_moveright":2,
            "Nr_moveleft":0
            },
        "2": {
            2:"_f",
            1:"_r",
            3:"_l",
            0:"_b",
            "Nr_movefront":2,
            "Nr_moveright":1,
            "Nr_moveleft":3},
        "3": {
            3:"_f",
            0:"_r",
            2:"_l",
            1:"_b",
            "Nr_movefront":3,
            "Nr_moveright":0,
            "Nr_moveleft":2
            }
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
        "Nr_nothing_f":21,
        "Nr_breeze_f":22,
        "Nr_flash_f":23,
        "Nr_stench_f":24,
        "Nr_breezeflash_f":25,
        "Nr_breezestench_f":26,
        "Nr_breezeflashstench_f":27,
        "Nr_flashstench_f":28,
        "Nr_danger_f":29,
        "Nr_obstruction_f":30,
        "Nr_goal_f":31,
        "Nr_initial_f":32,
        "Nr_nothing_r":33,
        "Nr_breeze_r":34,
        "Nr_flash_r":35,
        "Nr_stench_r":36,
        "Nr_breezeflash_r":37,
        "Nr_breezestench_r":38,
        "Nr_breezeflashstench_r":39,
        "Nr_flashstench_r":40,
        "Nr_danger_r":41,
        "Nr_obstruction_r":42,
        "Nr_goal_r":43,
        "Nr_initial_r":44,
        "Nr_nothing_l":45,
        "Nr_breeze_l":46,
        "Nr_flash_l":47,
        "Nr_stench_l":48,
        "Nr_breezeflash_l":49,
        "Nr_breezestench_l":50,
        "Nr_breezeflashstench_l":51,
        "Nr_flashstench_l":52,
        "Nr_danger_l":53,
        "Nr_obstruction_l":54,
        "Nr_goal_l":55,
        "Nr_initial_l":56,
        "Nr_nothing_b":57,
        "Nr_breeze_b":58,
        "Nr_flash_b":59,
        "Nr_stench_b":60,
        "Nr_breezeflash_b":61,
        "Nr_breezestench_b":62,
        "Nr_breezeflashstench_b":63,
        "Nr_flashstench_b":64,
        "Nr_danger_b":65,
        "Nr_obstruction_b":66,
        "Nr_goal_b":67,
        "Nr_initial_b":68,
        "Nr_recuar":69,
        "Nr_avaçar":70,
        "Nr_perseguir_f":71,
        "Nr_perseguir_l":72,
        "Nr_perseguir_r":73,
        "Nr_left_right": 74,
        "Nr_front_left": 75,
        "Nr_right_front": 76,
        "Nr_random_all":77,
        "Nr_movefront":78,
        "Nr_moveleft":79,
        "Nr_moveright":80,
        "Nr_moveback":81
        },
    "neuron_interp":{
        "i_vz": "Nr_nothing",
        "i_b": "Nr_breeze",
        "i_f": "Nr_flash",
        "i_s": "Nr_stench",
        "i_bf": "Nr_breezeflash",
        "i_bs": "Nr_breezestench",
        "i_bfs": "Nr_breezeflashstench",
        "i_fs": "Nr_flashstench",
        "i_died": "Nr_danger",
        "i_gl": "Nr_goal",
        "i_ini": "Nr_initial",
        "i_cl": "Nr_obstruction"
        },
    "randomAll":{
        "rand":[[100,103,106,109], [101,104,107,110], [102,105,108,111]],
        "100": "Nr_movefront",
        "101": "Nr_moveleft",
        "102": "Nr_moveright",
        "103": "Nr_movefront",
        "104": "Nr_moveleft",
        "105": "Nr_moveright",
        "106": "Nr_movefront",
        "107": "Nr_moveleft",
        "108": "Nr_moveright",
        "109": "Nr_movefront",
        "110": "Nr_moveleft",
        "111": "Nr_moveright"
        },
    "randomLF":{
        "rand":[[112,114,116,118], [113,115,117,119]],
        "112": "Nr_moveleft",
        "113": "Nr_movefront",
        "114": "Nr_moveleft",
        "115": "Nr_movefront",
        "116": "Nr_moveleft",
        "117": "Nr_movefront",
        "118": "Nr_moveleft",
        "119": "Nr_movefront"
    },
    "randomRL":{
        "rand":[[112,114,116,118], [113,115,117,119]],
        "112": "Nr_moveright",
        "113": "Nr_moveleft",
        "114": "Nr_moveright",
        "115": "Nr_moveleft",
        "116": "Nr_moveright",
        "117": "Nr_moveleft",
        "118": "Nr_moveright",
        "119": "Nr_moveleft"
    },
    "randomFR":{
        "rand":[[112,114,116,118], [113,115,117,119]],
        "112": "Nr_movefront",
        "113": "Nr_moveright",
        "114": "Nr_movefront",
        "115": "Nr_moveright",
        "116": "Nr_movefront",
        "117": "Nr_moveright",
        "118": "Nr_movefront",
        "119": "Nr_moveright"
    }

}


