# Natural-Language-Processing
-> BiGrams

Compute the Bigram Model(counts and probabilities) on a given corpus for following three scenarios:

1. No Smoothing

2. Add-one Smoothing

3. Good-Turing Discounting based Smoothing

Run Command:  ```python BiGrams.py <path of the file CorpusTreebank2.txt>```


-> Brills

Implement Brill’s transformation-based POS tagging algorithm using ONLY the previous word’s tag to extract the best transformation rule to:

i. Transform “NN” to “JJ”

ii. Transform “NN” to “VB”

Using the learnt rules, fill out the missing POS tags (for the words “standard” and “work”) in the following sentence:

The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??

Run Command: ```python Brills.py <path of the file POSTaggedTrainingSet.txt>```

-> POS Probabilities

Compute the bigram models (counts and probabilities) required by Naïve Bayesian Classification (Bigram) based POS Tagging.

Run Command: ```python POS_probs.py <path of the file POSTaggedTrainingSet.txt>```

-> ViterbiHMM

The Viterbi algorithm to compute the most likely weather sequence and probability for any given observation sequence. Example observation sequences: 331, 122313, 331123312, etc.

The Given HMM:
![The HMM](https://github.com/taniyariar/Natural-Language-Processing/blob/master/hmm.PNG)

Run Command: ```python ViterbiHMM.py```
