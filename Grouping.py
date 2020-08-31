import numpy as np
import copy

def Local(r_v_l, c_v_l): # r_v_l은 np.array, c_v_l은 list
    N = len(r_v_l)
    c_n = [[i] for i in range(N)] # Client number
    rq_list = copy.deepcopy(r_v_l)
    if type(rq_list) == np.ndarray:
        rq_list = rq_list.tolist()
    cache_list = copy.deepcopy(c_v_l)
    
    local = []
    for i in range(N):
        if r_v_l[i] in c_v_l[i] or r_v_l[i][0] == None:
            local.append(i)
            
    local.reverse()
    
    for i in local:
        del c_n[i]
        del rq_list[i]
        del cache_list[i]
    
    return c_n, rq_list, cache_list


def BCG(V, c_n, r_v_l, c_v_l):
    N = len(r_v_l)
    rq_list = copy.deepcopy(r_v_l)
    cache_list = copy.deepcopy(c_v_l)
    
    for v in V:
        if rq_list.count([v]) > 1:
            idx = np.where(np.array(rq_list) == v)[0]
            for i in range(len(idx)-1,0,-1):
                c_n[idx[i-1]] += c_n[idx[i]]
            for i in range(len(idx)-1,0,-1):
                del c_n[idx[i]]
            for i in range(len(idx)-1,0,-1):
                del rq_list[idx[i]]
            for i in range(len(idx)-1,0,-1):
                cache_list[idx[i-1]] = list((set(cache_list[idx[i-1]]) & set(cache_list[idx[i]])))
            for i in range(len(idx)-1,0,-1):
                del cache_list[idx[i]]
        
    return c_n, rq_list, cache_list


def XBCG(V, c_n, r_v_l, c_v_l):
    rq_list = copy.deepcopy(r_v_l)
    cache_list = copy.deepcopy(c_v_l)
    size = len(V)
    
    xbc = 1
    while xbc:
        xbc = None
        for i in range(len(rq_list)):
            for j in range(1,len(rq_list)):
                br = 0
                for k in range(len(rq_list[i])):
                    if not rq_list[i][k] in cache_list[j]:
                        br = 1
                        break
                for k in range(len(rq_list[j])):
                    if not rq_list[j][k] in cache_list[i]:
                        br = 1
                        break
                if not br:
                    if len(rq_list[i]) + len(rq_list[j]) < size:
                        size = len(rq_list[i]) + len(rq_list[j])
                        xbc = [i,j]
                    elif len(rq_list[i]) + len(rq_list[j]) == size and xbc == None:
                        xbc = [i,j]
        if xbc:
            c_n[xbc[0]] += c_n[xbc[1]]
            del c_n[xbc[1]]
            rq_list[xbc[0]] += rq_list[xbc[1]]
            del rq_list[xbc[1]]
            cache_list[xbc[0]] = list((set(cache_list[xbc[0]]) & set(cache_list[xbc[1]])))
            del cache_list[xbc[1]]
        
    return c_n, rq_list, cache_list