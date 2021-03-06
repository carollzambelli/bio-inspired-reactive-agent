HOST = '192.168.0.11'   
PORT = 15051
env_id = '8x8'

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
    "comando":
    {
        "0": "{\"move\":[\"n\",1]}",
        "1": "{\"move\":[\"e\",1]}",
        "2": "{\"move\":[\"s\",1]}",
        "3": "{\"move\":[\"w\",1]}",
        "4": {"True": "{\"act\":[\"grab\",1]}"},
        "5": {"True": "{\"act\":[\"leave\",1]}"}
    },
    "agents": ["exp_agent3-1","exp_agent3-2","exp_agent3-3", "exp_agent3-4"]
}

# "exp_agent1", "exp_agent2-1", "exp_agent2-2", "exp_agent3-1","exp_agent3-2","exp_agent3-3", "exp_agent3-4"

