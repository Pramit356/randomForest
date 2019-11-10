import csv
from decisionTree import maketree

no_of_trees = 10                                #by default 10
max_elements = int(891/no_of_trees)
#max_elements = 5
decision_trees = []                             #holds all trees
el_ct = 0

with open('dataset/pre_train.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    data = []
    flag = 0
    for row in reader:
        if flag == 0:                                                       #The first row is for names of attributes
            names = row
            flag = 1
        else:
            data.append(row)
            el_ct+=1
        if el_ct == max_elements:                                                           #At a time do only 89 elements per tree
            decision_trees.append(maketree(data, [], names, 'root'))
            el_ct = 0
#print(decision_trees)
print("All 10 decision trees: ")
for el in decision_trees:
    print(el)