# SeekTruth.py : Classify text objects into two categories
#
# Parth Verma (paverma), Shivam Balajee (shbala), Jagrut Dhirajkumar Chaudhari (jagchau)
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import re
import math

def load_file(filename):
    words_to_ignore = [
'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'
]
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            words = []
            for w in parsed[1].split():
                word = re.sub(r'[^a-zA-Z]', '', w).lower()
                if word not in words_to_ignore:
                    words.append(word)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(words if len(parsed)>1 else [])

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    truth_probablities = {}
    deceptive_probablities = {}

    truth_words = []
    deceptive_words = []

    for i in range(len(train_data['labels'])):
        if train_data['labels'][i] == 'truthful':
            truth_words += train_data['objects'][i]
        if train_data['labels'][i] == 'deceptive':
            deceptive_words += train_data['objects'][i]

    truths_len = len(truth_words)
    deceptives_len = len(deceptive_words)
    alpha = 1

    for word in truth_words:
        if word not in truth_probablities:
            p = (truth_words.count(word) + alpha)/truths_len
            truth_probablities[word] = p
    for word in deceptive_words:
        if word not in deceptive_probablities:
            p = (deceptive_words.count(word) + alpha)/deceptives_len
            deceptive_probablities[word] = p

    truth_prior = truths_len / (truths_len + deceptives_len)
    deceptive_prior = 1 - truth_prior

    results = []
    for words in test_data['objects']:
        prob_of_truth = math.log(truth_prior)
        prob_of_deceptive = math.log(deceptive_prior)
        for word in words:
            prob_of_truth += math.log(truth_probablities[word]) if word in truth_probablities else math.log(alpha / truths_len)
            prob_of_deceptive += math.log(deceptive_probablities[word]) if word in deceptive_probablities else math.log(alpha / deceptives_len)
        results.append('truthful' if prob_of_truth >= prob_of_deceptive else 'deceptive')

    return results
    


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"]))])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
