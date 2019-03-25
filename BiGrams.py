import re,os
import pandas as pd
import numpy as np 
import sys

"""importing file to extract sentences and tokens for creating corpus unigrams and bigrams 
frequency dictionaries"""

def format_file(file):
    read_file=open(file,'r')
    string_file=read_file.read()
    sentences=string_file.replace('\n',' ')
    sentences=re.split('\\s+\.\\s+',sentences)
    
    sentence_tokens = []
    corpus_words=[]
    for i in sentences:
        word_list=re.split('\\s+',i)
        #print(word_list)
        corpus_words+=word_list
        sentence_tokens.append(word_list)
    
    return(sentence_tokens,corpus_words)
    
def get_unigram_count(c_words):
        unigrams={}
        for i in c_words:
            if i in unigrams:
                unigrams[i]+=1
            else:
                unigrams[i]=1
        return unigrams

def get_bigram_count(s_tokens):
    bigrams={}
    for i in s_tokens:
        for j in range(1,len(i)):
            if(i[j-1],i[j]) in bigrams:
                bigrams[i[j-1],i[j]]+=1
            else:
                bigrams[i[j-1],i[j]]=1
    return bigrams

def no_smoothing(bigrams,unigrams,w_dir):
    f1=w_dir+"\\no_smoothing_count.txt"
    f2=w_dir+"\\no_smoothing_prob.txt"
    
    try:
        os.remove(f1)
        os.remove(f2)
    except FileNotFoundError:
        pass
    
    bigrams_prob={}
    for i in bigrams:
        c_i=bigrams[i]
        wi=i[1]
        wj=i[0]
        if wj in unigrams:
            wj_count=unigrams[wj]
            key_prob="P("+wi+"|"+wj+")"
            bigrams_prob[key_prob]=round((c_i/wj_count),4)
    
    #print(len(bigrams_prob))
    
    with open(f1,'a+') as countfile:
        for i in bigrams:
            countfile.write("%s : %d \n" %(i,bigrams[i]))
        
    with open(f2,'a+') as probfile:
        for i in bigrams_prob:
            probfile.write("%s : %f \n" %(i,bigrams_prob[i]))
        
    countfile.close()
    probfile.close()
    return f1,f2

def add1_smoothing(bigrams,unigrams,corpus_words,w_dir):
    f1=w_dir+"\\add1_smoothing_countStar.txt"
    f2=w_dir+"\\add1_smoothing_prob.txt"
        
    try:
        os.remove(f1)
        os.remove(f2)
    except FileNotFoundError:
        pass

    new_bigrams_countStar ={}
    new_bigrams_prob={}
    V = len(unigrams)
    N = len(corpus_words)
    for i in bigrams:
        prb = round((bigrams[i]+1)/(unigrams[i[0]]+V),4)
        countStar =round((bigrams[i]+1)*(N/(N+V)),4)
        if prb > 0:
            key="P("+i[1]+"|"+i[0]+")"
            new_bigrams_prob[key]=prb
        if countStar >0:
            new_bigrams_countStar[i]=countStar  
    
    unseen_bigrams_prob={}
    unseen_bigrams_countStar={}
    for i in corpus_words:
        word0=i
        word1=r'.+'
        if (word0,word1) not in bigrams:
            prb = round(1/(unigrams[word0]+V),4)
            countStar =round(1*(N/(N+V)),4)
            if prb > 0:
                key="P("+word1+"|"+word0+")"
                unseen_bigrams_prob[key]=prb
                #print(word0,word1,prb,unigrams[word0],countStar)
            if countStar > 0:
                unseen_bigrams_countStar[(word0,word1)]=countStar
    
    add1_smoothing_countStar = {**unseen_bigrams_countStar,**new_bigrams_countStar}
    with open(f1,'a+') as countfile:
        for i in add1_smoothing_countStar:
            countfile.write("%s : %f \n" %(i,add1_smoothing_countStar[i]))
         
    add1_smoothing_prob = {**unseen_bigrams_prob,**new_bigrams_prob}
    with open(f2,'a+') as probfile:
        for i in add1_smoothing_prob:
            probfile.write("%s : %f \n" %(i,add1_smoothing_prob[i]))
        
    countfile.close()
    probfile.close()
    
    return f1,f2

def good_turing_discounting(unigrams,bigrams,corpus_words,w_dir):
    f1=w_dir+"\\GT_countStar.txt"
    f2=w_dir+"\\GT_prob.txt"
    
    try:
        os.remove(f1)
        os.remove(f2)
    except FileNotFoundError:
        pass
    
    N = len(corpus_words)
    bucket_NC= {}

    for key, value in sorted(bigrams.items()):
        bucket_NC.setdefault(value, []).append(key)
        
    GT_unseen_prob={}
    for i in corpus_words:
        word0=i
        word1=r'.+'
        if (word0,word1) not in bigrams:
            prb=len(bucket_NC[1])/N
            if prb > 0:
                key="P("+word1+"|"+word0+")"
                GT_unseen_prob[key]=prb
                
    GT_seen_prob={}
    GT_seen_count={}
    Nb= sum(bigrams.values())
    for i in bucket_NC:
        #print("bucket with freqency of frequency as ",i)
        for j in bucket_NC[i]:
            Nd = len(bucket_NC[i])
            if i+1 in bucket_NC:
                Nn= len(bucket_NC[i+1])
            else:
                Nn= 0
            c_star= round((bigrams[j]+1)*Nn/Nd,4)
            p_star = round(c_star/Nb,4)
            if p_star > 0:
                key="P("+j[1]+"|"+j[0]+")"
                GT_seen_prob[key]=p_star
            if c_star > 0:
                GT_seen_count[j]=c_star
                
    with open(f1,'a+') as countfile:
        for i in GT_seen_count:
            countfile.write("%s : %f \n" %(i,GT_seen_count[i]))
         
    GT_prob = {**GT_seen_prob,**GT_unseen_prob}
    with open(f2,'a+') as probfile:
        for i in GT_prob:
            probfile.write("%s : %f \n" %(i,GT_prob[i]))
            
    countfile.close()
    probfile.close()
    
    return f1,f2
    

def main():
    working_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    
    if(len(sys.argv)>1):
        file = sys.argv[1]
    else:
        file="C:\\Users\\taniy\\Desktop\\Spring19\\CS6320-NLP\\HWS\\HW2\\HW2_F18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Windows.txt"
    
    
    
    s_tokens,c_words=format_file(file)
    u_grams= get_unigram_count(c_words)
    b_grams=get_bigram_count(s_tokens)
    c_no_smoothing,p_no_smoothing = no_smoothing(b_grams,u_grams,working_dir)
    c_add1_smoothing,p_add1_smoothing = add1_smoothing(b_grams,u_grams,c_words,working_dir)
    c_GT,p_GT = good_turing_discounting(u_grams,b_grams,c_words,working_dir)
    
    
    print("############################################")
    print("PROCESSING INFORMATION")
    print("Total Sentences -> ",len(s_tokens))
    print("Total Words -> ",len(c_words))
    print("Total Unigrams -> ",len(u_grams))
    print("Total Bigrams -> ",len(b_grams))
    print("############################################")
    print("Working Directory -> ",working_dir)
    print("############################################")
    print("No Smoothing Output files Location")
    print("############################################")
    print("Count Output File -> ",c_no_smoothing)
    print("Probability Output File -> ",p_no_smoothing)
    print("############################################")
    print("Add 1 Smoothing Output files Location")
    print("############################################")
    print("Count Output File -> ",c_add1_smoothing)
    print("Probability Output File -> ",p_add1_smoothing)
    print("############################################")
    print("Good Turing Discounting Output files Location")
    print("############################################")
    print("Count Output File -> ",c_GT)
    print("Probability Output File -> ",p_GT)


if __name__=="__main__":
    main()

