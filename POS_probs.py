# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 12:41:08 2019

@author: taniya
"""
import re
import os,sys

def format_file(file):
    string=""
    with open(file,'r') as readFile:
        string=readFile.read()
    sentence1=re.split('\n|\s+,',string)
    #print(sentence1)
    len(sentence1) 
    corpus_words=[]
    pos_tags=[]
    for i in sentence1:
        for j in i.split():
            corpus_words.append(j.split("_")[0])
            pos_tags.append(j.split("_")[1])
    
    return(corpus_words,pos_tags)

def generate_counts(corpus_words,pos_tags,w_dir):
    f1=w_dir+"\\POS_tag_counts.txt"
    f2=w_dir+"\\Word_tag_counts.txt"
    f3=w_dir+"\\tag_bigrams_counts.txt"
    
    try:
        os.remove(f1)
        os.remove(f2)
        os.remove(f3)
    except FileNotFoundError:
        pass
    
    pos_tag_counts={}
    for i in pos_tags:
        if i in pos_tag_counts:
            pos_tag_counts[i]+=1
        else:
            pos_tag_counts[i] =1
            
    word_tag_counts={}
    for i in range(len(corpus_words)):
        key = (pos_tags[i],corpus_words[i],)
        if key in word_tag_counts:
            word_tag_counts[key]+=1
        else:
            word_tag_counts[key] =1
            
    tag_bigrams={}
    for i in range(1,len(pos_tags)):
        key = (pos_tags[i-1],pos_tags[i])
        if key in tag_bigrams:
            tag_bigrams[key]+=1
        else:
            tag_bigrams[key] = 1
            
   
            
    with open(f1,'a+') as countfile1:
        for i in pos_tag_counts:
            countfile1.write("%s : %d \n" %(i,pos_tag_counts[i]))
    with open(f2,'a+') as countfile2:
        for i in word_tag_counts:
            countfile2.write("%s : %d \n" %(i,word_tag_counts[i]))
    with open(f3,'a+') as countfile3:
        for i in tag_bigrams:
            countfile3.write("%s : %d \n" %(i,tag_bigrams[i]))
            
    countfile1.close()
    countfile2.close()
    countfile3.close()
    
    print("######################################################")
    print("Count file for POS TAG Counts "+f1)
    print("Count file for WORD TAG Counts "+f2)
    print("Count file for TAG BIGRAMS Counts "+f3)
    print("######################################################")
    return(pos_tag_counts,word_tag_counts,tag_bigrams)
    
def word_likelihood_probabilites(word_tag_counts,pos_tag_counts,w_dir):
    f1=w_dir+"\\Word_likelihood_probabilities.txt"
    try:
        os.remove(f1)
    except FileNotFoundError:
        pass
    
    word_likelihood ={}
    for i in word_tag_counts:
        key="P("+i[1]+"|"+i[0]+")"
        word_likelihood[key] = word_tag_counts[i]/pos_tag_counts[i[0]]
        
    with open(f1,'a+') as probfile:
        for i in word_likelihood:
            probfile.write("%s : %f \n" %(i,word_likelihood[i]))
    probfile.close()
    
    print("######################################################")
    print("Word Likelihood Probability file "+f1)
    print("######################################################")
    
    return(word_likelihood)
    
def tag_transition_probabilities(tag_bigrams,pos_tag_counts,w_dir):
    f1=w_dir+"\\tag_transition_probabilities.txt"
    try:
        os.remove(f1)
    except FileNotFoundError:
        pass
    
    tag_transition={}
    for i in tag_bigrams:
        key="P("+i[1]+"|"+i[0]+")"
        tag_transition[key] = tag_bigrams[i]/pos_tag_counts[i[0]]
        
    with open(f1,'a+') as probfile:
        for i in tag_transition:
            probfile.write("%s : %f \n" %(i,tag_transition[i]))
    probfile.close()
    
    print("######################################################")
    print("Tag Transition Probability file "+f1)
    print("######################################################")
    return(tag_transition)
    
def main():
    working_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    
    if(len(sys.argv)>1):
        file = sys.argv[1]
    else:
        file="POSTaggedTrainingSet.txt"
    
    c_words,p_tags=format_file(file)
    p_tags_counts,word_tag_count,tag_bigrams=generate_counts(c_words,p_tags,working_dir)
    m=word_likelihood_probabilites(word_tag_count,p_tags_counts,working_dir)
    t=tag_transition_probabilities(tag_bigrams,p_tags_counts,working_dir)

if __name__=="__main__":
    main()

