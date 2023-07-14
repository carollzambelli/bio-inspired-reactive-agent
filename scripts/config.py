params = {
    "HOST":'172.24.0.1',   
    "PORT":15051,
    "env_id":'8x8',
    "grid_reach":1,
    "agent":3,
    "flag_b":True,
    "moves": 4
}

iAct=0
sttMM = "INICIAR"
idd = " "

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
       "mt":{
           "i_ini" :0,
           "i_vz"  :0,
           "i_bfs" :0,
           "i_b"   :0,
           "i_s"   :0,
           "i_bs"  :0,
           "i_gl"  :1,
           "i_bf"  :1,
           "i_fs"  :1,
           "i_f"   :1,
           "i_cl"  :-1,
           "i_died":-1,
       },
    "orientation":{
        0:[0,3,1,2],
        1:[1,2,0,3],
        2:[2,1,3,0],
        3:[3,0,2,1]
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
    }
}


