mind = {
    "name" :"visao_3a",
    "agent": 3,
    "total_calls": 16,
    "diagonal": "OFF",
    "total_calls_diag": 0,
    "call":{
        "0": "{\"call\":[\"n\",1]}",
        "1": "{\"call\":[\"e\",1]}",
        "2": "{\"call\":[\"s\",1]}",
        "3": "{\"call\":[\"w\",1]}"
    },
    "mind":{
        "0_norte":{
            "i_ini":  [0, 0, 0, 0],
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0],
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [1, 0, 0, 0], 
            "i_bf":   [1, 0, 0, 0], 
            "i_fs":   [1, 0, 0, 0], 
            "i_f" :   [1, 0, 0, 0], 
            "behind": [0, 0, 0, 0], 
            "i_cl":   [-1, 0, 0, 0], 
            "i_died": [-1, 0, 0, 0]
        },
        "0_west":{
            "i_ini":  [0, 0, 0, 0],
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0],
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [0, 1, 0, 0], 
            "i_bf":   [0, 1, 0, 0], 
            "i_fs":   [0, 1, 0, 0], 
            "i_f" :   [0, 1, 0, 0], 
            "behind":  [0, 0, 0, 0], 
            "i_cl":   [0, -1, 0, 0], 
            "i_died": [0, -1, 0, 0]
        },
        "0_sul":{
            "i_ini":  [0, 0, 0, 0],
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0],
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [0, 0, 1, 0], 
            "i_bf":   [0, 0, 1, 0], 
            "i_fs":   [0, 0, 1, 0], 
            "i_f" :   [0, 0, 1, 0], 
            "behind":  [0, 0, 0, 0], 
            "i_cl":   [0, 0, -1, 0], 
            "i_died": [0, 0, -1, 0]
        },
        "0_east":{
            "i_ini":  [0, 0, 0, 0],
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0],
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [0, 0, 0, 1], 
            "i_bf":   [0, 0, 0, 1], 
            "i_fs":   [0, 0, 0, 1], 
            "i_f" :   [0, 0, 0, 1], 
            "behind":  [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, -1], 
            "i_died": [0, 0, 0, -1]
        },
        "1_norte":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [0.1, 0, 0, 0],
            "i_bf":   [0.1, 0, 0, 0],
            "i_fs":   [0.1, 0, 0, 0],
            "i_f" :   [0.1, 0, 0, 0], 
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        },
        "1_west":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [0, 0.1, 0, 0],
            "i_bf":   [0, 0.1, 0, 0],
            "i_fs":   [0, 0.1, 0, 0],
            "i_f" :   [0, 0.1, 0, 0],
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        },
        "1_sul":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [0, 0, 0.1, 0],
            "i_bf":   [0, 0, 0.1, 0],
            "i_fs":   [0, 0, 0.1, 0],
            "i_f" :   [0, 0, 0.1, 0],
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        },
        "1_east":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0],
            "i_gl":   [0, 0, 0, 0.1],
            "i_bf":   [0, 0, 0, 0.1],
            "i_fs":   [0, 0, 0, 0.1],
            "i_f" :   [0, 0, 0, 0.1],
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        },
        "2_norte":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0], 
            "i_gl":   [0.1, 0, 0, 0], 
            "i_bf":   [0.1, 0, 0, 0], 
            "i_fs":   [0.1, 0, 0, 0], 
            "i_f" :   [0.1, 0, 0, 0], 
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        },
        "2_weast":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0], 
            "i_gl":   [0, 0.1, 0, 0],
            "i_bf":   [0, 0.1, 0, 0],
            "i_fs":   [0, 0.1, 0, 0],
            "i_f" :   [0, 0.1, 0, 0],
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        },
        "2_sul":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0], 
            "i_gl":   [0, 0, 0.1, 0],
            "i_bf":   [0, 0, 0.1, 0],
            "i_fs":   [0, 0, 0.1, 0],
            "i_f" :   [0, 0, 0.1, 0],
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        },
        "2_east":{
            "i_ini":  [0, 0, 0, 0], 
            "i_vz":   [0, 0, 0, 0], 
            "i_bfs":  [0, 0, 0, 0], 
            "i_b":    [0, 0, 0, 0], 
            "i_s":    [0, 0, 0, 0], 
            "i_bs":   [0, 0, 0, 0], 
            "i_gl":   [0, 0, 0, 0.1],
            "i_bf":   [0, 0, 0, 0.1],
            "i_fs":   [0, 0, 0, 0.1],
            "i_f" :   [0, 0, 0, 0.1],
            "behind": [0, 0, 0, 0], 
            "i_cl":   [0, 0, 0, 0], 
            "i_died": [0, 0, 0, 0]
        }
    }
}