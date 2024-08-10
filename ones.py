def ones():
    for idx in range(21, 22): # for idx in range(22, 32):
        print(idx)
        shard = 131
        n = idx
        m = 32
        d = {n:[]}
        start = int('11111111111111111101100100000000', 2)
        for i in range(start, 2 ** m):        
            bin_s = str(format(i, f'0{m}b'))
            #print(i, bin_s, idx, len(d[n]))
            #print(idx, len(d[n]))
            if bin_s.count('1') == n:
                d[n].append(bin_s)

            if len(d[n]) == 1000000 or i == ((2 ** m)-1):        
                # for c in d[n]:
                #     print(c)

                print(f"There are {len(d[n])} combinations")

                import json 
                    
                # Convert and write JSON object to file
                with open("data1/"+str(n)+"/ones_"+str(n)+"_"+str(shard)+".json", "w") as outfile: 
                    json.dump(d, outfile)
                d[n] = []
                shard += 1

def ones_move():
    import os
    n = 22
    end = 645123
    for i in range(10,end):
        print(i)
        # Opening JSON file
        out = os.popen("mv data/ones_"+str(n)+"_"+str(i)+".json data3/"+str(n)+"/").read()

def ones_process():
    import json
    n = 22
    d = []
    shard = 1
    end = 645123  #15 1407316, 14 4714356, 13 3473737, 12 2257929, 11 1290245, 10 645123, 9 280489, 8 105184, 7 33659, 6 9062, 5 2014, 4 360, 3 50, 2 5
    # 16 102438, 17 5657228, 18 1513448, 19 3473737, 20 2257929, 21 1290245, 22 645123
    for i in range(1,end):
        print(i)
        # Opening JSON file
        f = open('data/ones_'+str(n)+'_'+str(i)+'.json')
        
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        #print(data)
        
        d += data[str(n)]
        print(len(d))
        # Iterating through the json
        # list
        
        
        # Closing file
        f.close()

        # if len(d) == 1000000 or i == (end-1):
        #     print("shard: ", shard)
        #     with open("data1/"+str(n)+"/ones_"+str(n)+"_"+str(shard)+".json", "w") as outfile: 
        #             json.dump(d, outfile)
        #     d = []
        #     shard += 1


#ones_process()

#ones_move()

ones()



