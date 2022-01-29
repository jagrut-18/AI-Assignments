# Assignment 3

# AI Text Recognition - Implementation of HMM with MAP inference and Viterbi Algorithm

## Initial Probability
Initial Probability is calculated by counting the occurences of a letter as an initial letter and dividing it by the total words in the training data.

## Transition Probability
Transition Probability is calculated by counting transitions between two letters and dividing it by the total occurences of the first letter.

## Emission Probability
Emission Probability is calculated by comparing each pixel in test and training data. After counting matched and unmatched pixels, and considering m% noise, we can calculate it by (1 - m)^matched * m^unmatched

## Simple
For this method, we return the characters with the maximum emission probability for all the given characters. For new words, we have also applied laplace smoothing for the probabilities.

## Viterbi
For Viterbi, we create two tables which are V_table and which_table. Then we populate the first column using the initial and emission probabilities. After that using the populated data and the transition probability, we calculate the remaining values. Using backtracking, we return the most likely path.

