import math
from copy import deepcopy

def information_gain(p, n):
    if p==0 or n==0:
        return 0
    elif p==n:
        return 1
    return round(-(p/(p+n))*math.log((p/(p+n)), 2) - (n/(p+n))*math.log((n/(p+n)), 2), 4)

def entropy(pi, ni, p, n):
    entval = 0.0
    for i in range(len(pi)):
        entval+=((pi[i] + ni[i])/(p+n))*information_gain(pi[i], ni[i])
    return round(entval, 4)

def gain_max(ig, entropies):
    max = 0.0
    ind = -1
    for el in entropies:
        if ig - el>max:
            max = ig - el
            ind = entropies.index(el)
    return ind

def getData(data, ind, el):
    data1 = []
    #print(data)
    for i in range(len(data)):
        if data[i][ind] == el:
            temp = data[i]
            temp.pop(ind)
            data1.append(temp)
    return data1

def maketree(data, tree, names, parent):
    global flag
    results = [int(row[0]) for row in data]
    #print(results)
    #print("DATA: ", data)
    #print("Datalen: ", len(data))
    p = 0
    n = 0
    for i in range(len(results)):       #Count positives and negatives
        if results[i]==0:
            n+=1
        else:
            p+=1
    ig = information_gain(p, n)         #Find information gain in each iteration for passed data
    #print("Official ig: ", ig)
    #print("POSITIVE: ",p)
    #print("NEGATIVE: ", n)
    if n == 0:                          #Only positives
        tree.append([1, parent])
        #print("tree: ", tree)
        return tree
    if p==0:                            #Only negatives
        tree.append([0, parent])
        #print("Tree: ", tree)
        return tree
    entropy_val = []                    #Entropy for each attributes on data
    for attr in names:
        if attr != 'Survived':
            pi = []
            ni = []
            col = [row[names.index(attr)] for row in data]          #Separating columns
            unique = list(set(col))                                 #Find unique values for each attributes. Aides in entropy calculation
            unique.sort()
            for i in range(len(unique)):
                pi.append(0)
                ni.append(0)
            for i in range(len(results)):
                if results[i] == 1:
                    pi[unique.index(col[i])] += 1
                elif results[i] == 0:
                    ni[unique.index(col[i])] += 1
            #print(unique)
            #print(attr)
            #print(pi)
            #print(ni)
            entropy_val.append(entropy(pi, ni, p, n))               #Calculating attributes
    #print(entropy_val)
    ind = gain_max(ig, entropy_val)                                 #Find index of attribute with maximum gain
    #print(ind)
    if names[ind+1]!="Survived":                                    #Add that attribute to tree
        tree.append([names[ind+1], parent])

    if (ind != -1):
        parent = names[ind + 1]
        #print("Considered: ", names[ind + 1])
        col = [row[ind + 1] for row in data]
        unique = list(set(col))
        unique.sort()
        names1 = deepcopy(names)                                    #Remove the selected attribute from names list
        names1.pop(ind + 1)
        #print("tree: ", tree)
        for el in unique:                                           #Apply DFS to explore the children of selected attribute
            #print("Considered: ", el)
            if el!="Survived":
                tree.append([el, parent])
            datax = deepcopy(data)                                  #Reduce datasize by fixing value of one column
            data1 = getData(datax, ind + 1, el)
            tree = maketree(data1, tree, names1, el)                #recursively call the same function on reduced data
    else:
        if p>=n:                                                    #Handle conflicts
            tree.append([1, parent])
        else:
            tree.append([0, parent])
    return tree





