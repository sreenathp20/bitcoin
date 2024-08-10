def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


for idx in range(32):
    print(idx)
    n = idx
    inp = (32-n)*'0'+n*'1'

    res = permutations(inp, 32)
    #print(list(res))
    l = []
    d = {}
    for i in res:
        s = "".join(i)    
        if s not in d:
            l.append(s)
            d[s] = True
    print(len(l))
    # for i in l:
    #     print(i)
    di = {n:l}

    import json
            
        # Convert and write JSON object to file
    with open("data/ones_"+str(n)+".json", "w") as outfile: 
            json.dump(di, outfile)