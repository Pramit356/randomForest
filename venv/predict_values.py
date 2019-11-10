from trainmodel import decision_trees

def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def output_comp(data, names, eachtree):                 #Since we have stored the tree in a DFS manner, it is obvious that the soln is sequential and can be found by traversing eachtree from left to right
    parent = eachtree[0][0]
    #print(data)
    for node in eachtree[1:]:
        #print(node)
        #print(parent)
        if(node[1]==parent and (node[0] in data or node[0] in names)):
            #print("Parent: ", parent)
            parent = node[0]
        if is_number(node[0]) and node[1]==parent:        # Terminate search when finding a numeric value
            val = node[0]
            return val

def find_values(data, names):
    ct_surv = 0
    ct_dead = 0
    for eachtree in decision_trees:
        #print(eachtree)
        val = output_comp(data,names,eachtree)
        #print("val: ", val)
        if val == 1:
            ct_surv+=1
        else:
            ct_dead+=1
    #print(ct_dead, ct_surv)
    if ct_surv>=ct_dead:                            #If more trees predict survived then return survived else dead ( 1-> survived, 0-> dead)
        return 1
    else:
        return 0

