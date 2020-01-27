from predict_values import find_values
import csv
names = []
data = []
outputs = []
with open('dataset/pre_test.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    flag = 0
    for row in reader:
        if flag == 0:
            names = row
            flag = 1
            continue
        else:
            data = row
            outputs.append(find_values(data, names))                    #Finding output values
#print(outputs)

output_compare = []
with open('dataset/compare.csv', newline='') as myFile:                 #Reading from test scores given as answer in compare.csv
    reader = csv.reader(myFile)
    flag = 0
    for row in reader:
        if flag == 0:
            names = row
            flag = 1
            continue
        else:
            output_compare.append(int(row[1]))

# print(output_compare)
# print(len(output_compare))

match = 0
#Accuracy estimation
for i in range(len(outputs)):
    if output_compare[i] == outputs[i]:
        match+=1
print("No of matched results: ", match)
print("Total results in test data: 418")
print("Accuracy on test data = ", str((match/len(outputs))*100))