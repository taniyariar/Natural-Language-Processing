#defining the given HMM
iprob={'hot':0.8,'cold':0.2}
tprob={'hot':{'hot':0.7,'cold':0.3},'cold':{'hot':0.4,'cold':0.6}}
oprob = {'hot':{'1':0.2,'2':0.4,'3':0.4},'cold':{'1':0.5,'2':0.4,'3':0.1}}
q = ['hot','cold']

def calculate_trellis(trellis,ele,index,q):
    for i in range(len(q)):
        max_t = 0
        max_s =""
        for k in range(len(q)):
            #print(q[k],q[i])
            #print(q[i],ele)
            #print(trellis[q[k]][index-1][0])
            p_t = (trellis[q[k]][index-1][0]*tprob[q[k]][q[i]]*oprob[q[i]][ele])
            if max_t < p_t:
                max_t = p_t
                max_s = q[k]
        #print("from state ", max_s,max_t)
        if q[i] in trellis:
            trellis[q[i]] += [(max_t,max_s)]
        else:
            trellis[q[i]] = [(max_t,max_s)]
            
        #print(trellis)

def backpropagate_trellis(trellis,q,in_sequence):
    path = []
    prob_flag = True
    prob_trellis = 0
    for i in range(len(q)-1):
        for k in range(len(in_sequence),1,-1):  
            print(k)
            #print(in_sequence[k])
            if prob_flag:
                if (trellis[q[i]][k-1][0]) >= (trellis[q[i+1]][k-1][0]):
                    prob_trellis = trellis[q[i]][k-1][0]
                    path.append(q[i])
                else:
                    prob_trellis = trellis[q[i+1]][k-1][0]
                    path.append(q[i+1])
                prob_flag = False
                    
            #print(path)
            #print(trellis[path[-1]][k-1][1])
            path.append(trellis[path[-1]][k-1][1])
            
            
    #print(path)
    return(path[::-1],prob_trellis)
        

def main():
    in_sequence = input("Enter the sequence \n ")
    initial_prob_tag = True
    trellis = {}
    p_max = 0
    for i in range(0,len(in_sequence)):
        #print(i)
        if initial_prob_tag == True and i == 0:
            for k in q:
                p_trellis = iprob[k]*oprob[k][in_sequence[i]]
                if k in trellis:
                    trellis[k] += [(p_trellis,k)]
                else:
                    trellis[k] = [(p_trellis,k)]
                p_max = max(p_max,p_trellis)
            initial_prob_tag = False
            #print(trellis)
        else:
            calculate_trellis(trellis,in_sequence[i],i,q)
        
    trellis_path, trellis_prob = (backpropagate_trellis(trellis,q,in_sequence))
    
    print("##################################################")
    print("The Most likely Weather Sequence")
    print(*trellis_path,sep=" >>>> ")
    print("##################################################")
    print("The probability of the given observation Sequence")
    print(trellis_prob)
    print("##################################################")
    for i in trellis:
        print("Emmission to State >>>", i )
        print("Observation\tProbability\t\t\tState")
        for k in range(len(in_sequence)):
            print(in_sequence[k]+"\t\t"+str(trellis[i][k][0])+"\t\t"+trellis[i][k][1])
        print("\n")
    
    
    
if __name__ == "__main__":
    main()