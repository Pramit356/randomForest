import csv
from copy import deepcopy

def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

PassengerId = []
Survived = []
Pclass = []
Name = []
Sex = []
Age = []
SibSp = []
Parch = []
Ticket = []
Fare = []
Cabin = []
Embarked = []
names = []
with open('dataset/train.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    flag = 0
    for row in reader:
        if flag == 0:
            names = row
            flag = 1
            continue
        else:
            PassengerId.append(int(row[0]))
            Survived.append(int(row[1]))
            Pclass.append(int(row[2]))
            Name.append(row[3])
            Sex.append(row[4])
            if(row[5]==''):
                Age.append('')
            elif is_number(row[5]):
                Age.append(int(row[5]))
            else:
                Age.append(float(row[5]))
            SibSp.append(int(row[6]))
            Parch.append(int(row[7]))
            Ticket.append(row[8])
            Fare.append(float(row[9]))
            Cabin.append(row[10])
            if row[11]=="":
                row[11] = "S"
            Embarked.append(row[11])
myFile.close()
selected = []

for i in range(len(names)):
    if names[i] == 'Survived':
        selected.append(1)
    else:
        selected.append(0)

Pclass_rel = [[0,0],[0,0],[0,0]]
Sib_rel = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]  #Number of siblings 0 to 8
Parch_rel = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]       # Number of parent, child present between 0 and 6
fare_rel = [[0,0], [0,0], [0,0]]            #Fare sampled into 3 classes with intervals [0, 8.662], [8.662, 26] and [26, 512.329]
embarked_rel = [[0,0], [0,0], [0,0]]        #S, C, Q
cabin_rel = [[0,0], [0,0]]                  # Number present or not present
null_age = 0
survived_ct = 0
farecomp = deepcopy(Fare)

'''
    Fare sampling:
    [0, 8.662] - 'low'
    {8.662, 26] - 'medium'
    (26, 512.329] - 'high'
    
    Cabin sampling
    If a value is given then 'given'
    If null then 'not given'
'''
fare_sampling = [[0, 8.662], [8.662, 26], [26, 512.329]]


total = len(Survived)
for i in range(len(Survived)):
    if Age[i]=="":
        null_age+=1
    if Survived[i]==0:
        Pclass_rel[Pclass[i]-1][0]+=1
        Sib_rel[SibSp[i]][0]+=1
        Parch_rel[Parch[i]][0]+=1
        if Fare[i]>=0 and Fare[i]<=8.662:
            Fare[i] = 'low'
            fare_rel[0][0]+=1
        elif Fare[i]>8.662 and Fare[i]<=26:
            Fare[i] = 'medium'
            fare_rel[1][0]+=1
        else:
            Fare[i] = 'high'
            fare_rel[2][0] += 1
        if Embarked[i] == 'S':
            embarked_rel[0][0]+=1
        elif Embarked[i]=='C':
            embarked_rel[1][0]+=1
        else:
            embarked_rel[2][0]+=1
        if Cabin[i]=="":
            Cabin[i] = 'not given'
            cabin_rel[1][0]+=1
        else:
            Cabin[i] = 'given'
            cabin_rel[0][0]+=1
    else:
        survived_ct+=1
        Pclass_rel[Pclass[i] - 1][1] += 1
        Sib_rel[SibSp[i]][1] += 1
        Parch_rel[Parch[i]][1]+=1
        if Fare[i]>=0 and Fare[i]<=8.662:
            Fare[i] = 'low'
            fare_rel[0][1]+=1
        elif Fare[i]>8.662 and Fare[i]<=26:
            Fare[i] = 'medium'
            fare_rel[1][1]+=1
        else:
            Fare[i] = 'high'
            fare_rel[2][1] += 1
        if Embarked[i] == 'S':
            embarked_rel[0][1]+=1
        elif Embarked[i]=='C':
            embarked_rel[1][1]+=1
        else:
            embarked_rel[2][1]+=1
        if Cabin[i]=="":
            Cabin[i] = 'not given'
            cabin_rel[1][1]+=1
        else:
            Cabin[i] = 'given'
            cabin_rel[0][1]+=1

tot_percent_surv = survived_ct/total
percentsurv = []
sibsurv = []
parchsurv = []
faresurv = []
embarkedsurv = []
cabinsurv = []
for i in range(len(Pclass_rel)):
    val = Pclass_rel[i][1]/(Pclass_rel[i][1]+Pclass_rel[i][0])
    val1 = fare_rel[i][1] / (fare_rel[i][1] + fare_rel[i][0])
    val2 = embarked_rel[i][1]/ (embarked_rel[i][1] + embarked_rel[i][0])
    percentsurv.append(val)
    faresurv.append(val1)
    embarkedsurv.append(val2)
for i in range(len(cabin_rel)):
    val = cabin_rel[i][1]/(cabin_rel[i][1]+cabin_rel[i][0])
    cabinsurv.append(val)
for i in range(len(Sib_rel)):
    if Sib_rel[i][1]+Sib_rel[i][0]!=0:
        val = Sib_rel[i][1]/(Sib_rel[i][1]+Sib_rel[i][0])
    else:
        val = 0
    sibsurv.append(val)
for i in range(len(Parch_rel)):
    if Parch_rel[i][1]+Parch_rel[i][0]!=0:
        val = Parch_rel[i][1]/(Parch_rel[i][1]+Parch_rel[i][0])
    else:
        val = 0
    parchsurv.append(val)


print("Total fraction of people survived = ",tot_percent_surv)
print()
print("Distribution based on Pclass: ",list(set(Pclass)))
print("[Not survived, Survived]: ", Pclass_rel)
print("Fraction estimates: ",percentsurv)
print("On observation of the fraction estimates, we see that the fraction of class 1 survivors "
      "is more than class 2 which in turn is more than class 3")
print("The passenger class affects the chances of survival")
print()
print()
siblings = [0, 1, 2, 3, 4, 5, 6, 7, 8]
print("Distribution based on siblings: ",siblings)
print("[Not survived, Survived]: ", Sib_rel)
print("Fraction estimates: ",sibsurv)
print("Although a justification can be made on the dataset that people with less siblings have a greater chance of dying, "
      "but as we oberved the number of survivors and deaths is nearly same in most cases and we observe that the bulk of the"
      " values is concentrated on the value for sibsp = 0, so we cannot justify it for classifying")
print("So SibSp does not affect chances of survival")
print()
print()
selected[names.index('Pclass')] = 1
print("Number of tuples with age not present: ",null_age)
print("As number of passengers with absence of age is more, we dont consider them")
print()
print()
print("Number of unique names: ", len(set(Name)))
print("As number of unique names in the training set ("+str(len(set(Name)))+
      ") is equal to total number of people in the dataset ("+str(len(Name))+"), we can say name does not determine survival")
print()
print()
print("Distribution based on number of parents and/or children: ",list(set(Parch)))
print("[Not survived, Survived]: ",Parch_rel)
print("Fraction estimated: ",parchsurv)
print("Passengers with zero parents or children had a lower likelihood of survival than otherwise, "
      "but that survival rate was only slightly less than the overall population survival rate")
print("So Parch does not affect chances of survival")
print()
print()
fares = ['low', 'medium', 'high']
print("Distribution based on ticket fare: ",fares)
print("[Not survived, Survived]: ", fare_rel)
print("Fraction estimated: ",faresurv)
print("According to the fraction estimates, as the fare increases likelihood of survival also increases")
print("So fare is considered for estimation")
selected[names.index('Fare')] = 1
print()
print()
print("Distribution based on boat at which embarked ['S', 'C', 'Q']: ")
print('[Not survived, Survived]: ', embarked_rel)
print("Fraction estimated: ", embarkedsurv)
print("According to the fraction estimates, people in boat type C have greater chance of survival")
print("So Embarked is considered for estimation")
selected[names.index('Embarked')] = 1
print()
print()
cabinfo = ['given', 'not given']
print("Distribution based on presence of cabin: ",cabinfo)
print('[Not survived, Survived]: ', cabin_rel)
print("Fraction estimated: ",cabinsurv)
print("According to the fraction estimates, the people whose cabins are mentioned have a greater chance of survival")
print("So cabin presence is considered for estimation")
selected[names.index('Cabin')] = 1
print()
print()
print("As number of unique tickets in the training set ("+str(len(set(Ticket)))+
      ") is equal to total number of people in the dataset ("+str(len(Ticket))+
      "), we can say ticket number is alphanumeric and is unique and should not be considered for decision")
print()
print()
Sex_rel = [[0,0],[0,0]]

for i in range(len(Survived)):
    if Survived[i]==0:
        if Sex[i]=='male':
            Sex_rel[0][0]+=1
        else:
            Sex_rel[1][0] += 1
    else:
        if Sex[i]=='male':
            Sex_rel[0][1]+=1
        else:
            Sex_rel[1][1] += 1
print("Distribution based on gender: ",Sex_rel)
malePercent = Sex_rel[0][1]/(Sex_rel[0][1]+Sex_rel[0][0])
femalePercent = Sex_rel[1][1]/(Sex_rel[1][1]+Sex_rel[1][0])
print("Percentage male population survived: ",malePercent)
print("Percentage female population survived: ",femalePercent)
print("As female deaths are less than males, the chances of female survival is more. "
      "So we must consider gender of the person for decision tree")
selected[names.index('Sex')] = 1
#These lines of code prove that Pclass and  Fare are not related and Fare must be taken into consideration
minmaxfare = [[999,0], [999,0], [999,0]]
print()
for i in range(len(Survived)):
    if farecomp[i]==0:
        continue
    if Pclass[i]== 1:
        if farecomp[i]<minmaxfare[0][0]:
            minmaxfare[0][0] = farecomp[i]
        if farecomp[i]>minmaxfare[0][1]:
            minmaxfare[0][1] = farecomp[i]
    elif Pclass[i] == 2:
        if farecomp[i]<minmaxfare[1][0]:
            minmaxfare[1][0] = farecomp[i]
        if farecomp[i]>minmaxfare[1][1]:
            minmaxfare[1][1] = farecomp[i]
    else:
        if farecomp[i]<minmaxfare[2][0]:
            minmaxfare[2][0] = farecomp[i]
        if farecomp[i]>minmaxfare[2][1]:
            minmaxfare[2][1] = farecomp[i]
print('For each class [1, 2, 3], [minfare, maxfare]: ', minmaxfare)
print("Fare sampling assigned: ", fare_sampling)
print("Sor class and fare are not correlated")
print()
with open('dataset/pre_train.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    for i in range(len(PassengerId)):
        if i==0:
            temp = []
            for j in range(len(names)):
                if selected[j] == 1:
                    temp.append(names[j])
            writer.writerow(temp)
        else:
            temp = []
            for j in range(len(names)):
                if selected[j] == 1:
                    el = names[j]
                    if names[j] == 'Pclass':
                        if str(vars()[el][i]) == '1':
                            temp.append('A1')
                        elif str(vars()[el][i]) == '2':
                            temp.append('B2')
                        else:
                            temp.append('C3')
                    else:
                        temp.append(str(vars()[el][i]))
            writer.writerow(temp)
writeFile.close()

selected.pop(1)
names.remove('Survived')
#Doing the same with the test set
with open('dataset/test.csv', newline='') as myFile:
    with open('dataset/pre_test.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        reader = csv.reader(myFile)
        flag = 0
        for row in reader:
            temp = []
            if flag==0:
                for i in range(len(selected)):
                    if selected[i]==1:
                        temp.append(row[i])
                writer.writerow(temp)
                flag=1
            else:
                for i in range(len(selected)):
                    if selected[i]==1:
                        if(names[i] == 'Pclass'):
                            if row[i] == '1':
                                row[i] = 'A1'
                            elif row[i] == '2':
                                row[i] = 'B2'
                            else:
                                row[i] = 'C3'
                        if names[i] == 'Fare':
                            if float(row[i]) >= 0 and float(row[i]) <= 8.662:
                                row[i] = 'low'
                            elif float(row[i]) > 8.662 and float(row[i]) <= 26:
                                row[i] = 'medium'
                            else:
                                row[i] = 'high'
                        if names[i] == 'Cabin':
                            if row[i] == '':
                                row[i] = 'not given'
                            else:
                                row[i] = 'given'
                        temp.append(row[i])
                writer.writerow(temp)
myFile.close()
writeFile.close()