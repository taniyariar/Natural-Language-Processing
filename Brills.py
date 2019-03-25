# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 23:46:49 2019

@author: taniya
"""
import re,os
import sys
from collections import Counter

def format_file(file):
    string=""
    with open(file,'r') as readFile:
        string=readFile.read()
    sentence1=re.split('\\n|\\s+,',string)
    corpus_words=[]
    pos_tags=[]
    for i in sentence1:
        for j in i.split():
            corpus_words.append(j.split("_")[0])
            pos_tags.append(j.split("_")[1])
    
    return(corpus_words,pos_tags)    
    
def unigrams_pos(corpus_words,pos_tags):
    unigrams={}
    for i in range(len(corpus_words)):
        if not corpus_words[i] in unigrams:
            unigrams[corpus_words[i]] = [pos_tags[i]]
        else:
            unigrams[corpus_words[i]].append(pos_tags[i])
            
    return(unigrams)
    
def most_probable_unigrams(unigrams):
    most_probable={}
    for i in unigrams:
        tag_list=unigrams[i]
        N = len(tag_list)
        count=Counter(tag_list)
        most_prob=0
        mtag=""
        for j in count:
            if(count[j]/N > most_prob):
                most_prob = count[j]/N
                mtag=j
        most_probable[i] = mtag 
    
    return(most_probable)
    
def most_probable_corpus(most_probable,corpus_words):
    most_probable_pos=[]
    for i in range(len(corpus_words)):
        #print(i)
        if corpus_words[i] in most_probable:
            #print(most_probable[corpus_words[i]])
            most_probable_pos.append(most_probable[corpus_words[i]])
    
    return(most_probable_pos)
    
def get_best_instance(from_tag,to_tag,template,pos_tags,most_probable_pos):
    if template=="previous tag":
        num_good_transforms = {}
        num_bad_transforms ={}
        best_Z={}
        rule=""
        score= float('-inf') #to pick up the best rule when all the scores are negative
        for i in from_tag:
            for j in to_tag:
                print("From "+i+" to "+j+" if previous tag is ___")
                print("Tag | Num_good_transforms | Num_bad_transforms| best_Z[Score]")
                for k in range(1,len(most_probable_pos)):
                    
                    if(pos_tags[k]==j and most_probable_pos[k] == i):
                        if most_probable_pos[k-1] in num_good_transforms:
                            num_good_transforms[most_probable_pos[k-1]] += 1
                        else:
                            num_good_transforms[most_probable_pos[k-1]] = 1
                            
                    elif(pos_tags[k] == i and most_probable_pos[k] == i):
                        if most_probable_pos[k-1] in num_bad_transforms:
                            num_bad_transforms[most_probable_pos[k-1]] += 1
                        else:
                            num_bad_transforms[most_probable_pos[k-1]] = 1  
                            
                for l in num_good_transforms:
                    if l not in num_bad_transforms:
                        best_Z[l]= (num_good_transforms[l]-0)
                        print(l+" | "+str(num_good_transforms[l])+" | "+str(0)+" | "+str(best_Z[l]))
                    else:
                        best_Z[l]= (num_good_transforms[l]-num_bad_transforms[l])
                        print(l+" | "+str(num_good_transforms[l])+" | "+str(num_bad_transforms[l])+" | "+str(best_Z[l]))

                for l in best_Z:
                    if best_Z[l] > score:
                        rule= ("from "+i+" to "+j+" if "+template+" is "+l)
                        score= best_Z[l] 
        return(rule,score)
        
def input_sentence_result(sentence,most_probable,rules):
    ambi_words=[]
    ambi_tags=[]
    input_sentence_tokens = sentence.split(" ")
    for i in input_sentence_tokens:
        if i.split("_")[1] == "??":
            if i.split("_")[0] in most_probable: 
                ambi_words.append(i.split("_")[0] )
                ambi_tags.append(most_probable[i.split("_")[0]])
        else:
            ambi_words.append(i.split("_")[0])
            ambi_tags.append(i.split("_")[1])
            
    print("Most Probable Tags (for unknown) and known tags :\n ",ambi_tags)
    
    for i in rules:
        if rules[i] > 0:
            print("Using rule "+i+" with score "+str(rules[i]))
            from_tag = re.split("\s+",i)[1]
            to_tag = re.split("\s+",i)[3]
            prev_tag = re.split("\s+",i)[-1]
            for i in range(1,len(ambi_tags)):
                if ambi_tags[i] == from_tag and ambi_tags[i-1]== prev_tag:
                    ambi_tags[i]=to_tag
                    print(ambi_words[i]+" tag changed to "+to_tag)
               
    return(ambi_tags)


def main():
    working_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    if(len(sys.argv)>1):
        file = sys.argv[1]
    else:
        file="POSTaggedTrainingSet.txt"
        
    c_words,pos_tags=format_file(file)
    u_grams_pos=unigrams_pos(c_words,pos_tags)
    mp_u_grams = most_probable_unigrams(u_grams_pos)
    mp_corpus = most_probable_corpus(mp_u_grams,c_words)
    
    rule_set={}
    from_tag=['NN']
    to_tag=['VB']
    template="previous tag"
    print("##################################################")
    r,s=get_best_instance(from_tag,to_tag,template,pos_tags,mp_corpus)
    print("Rule: ",r)
    print("Score: ",s)
    print("##################################################")
    rule_set[r]=s
    
    from_tag=['NN']
    to_tag=['JJ']
    template="previous tag"
    print("##################################################")
    r,s=get_best_instance(from_tag,to_tag,template,pos_tags,mp_corpus)
    print("Rule: ",r)
    print("Score: ",s)
    print("##################################################")
    rule_set[r]=s
    
    print("##################################################")
    sentence_input = "The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??"
    print("Input Sentence: \n",sentence_input)
    s= input_sentence_result(sentence_input,mp_u_grams,rule_set)
    print("Final Tags after applying rules: \n",s)
        
    
    
if __name__=="__main__":
    main()
