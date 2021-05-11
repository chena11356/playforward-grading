# Following tutorial: https://www.w3schools.com/python/python_ml_decision_tree.asp

import pandas
from sklearn import tree
import pydotplus
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimg
import json

# Import supervised data from json
df = pandas.read_json("dataGrades.json")

# Transform non-numerical data to numerical
d = {'male': 0, 'female': 1}
df['gender'] = df['gender'].map(d)

d = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
df['grade'] = df['grade'].map(d)

# Define features and targets columns
features = ['age', 'gender', 'overallSkillPts', 'gameTime', 'miniGamesWith0Stars', 'miniGamesWith1Star', 'miniGamesWith2Stars', 'miniGamesWith3Stars']

X = df[features]
y = df['grade']

# Create decision tree and save it as an image
dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)
data = tree.export_graphviz(dtree, out_file=None, feature_names=features)
graph = pydotplus.graph_from_dot_data(data)
graph.write_png('mydecisiontree.png')

img=pltimg.imread('mydecisiontree.png')


# Import unsupervised data from json
df2 = pandas.read_json("dataNoGrades.json")
d = {'male': 0, 'female': 1}
df2['gender'] = df2['gender'].map(d)

# Iterate through unsupervised data and predict grades 
gradeByIndex = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E'}
jsonData = []
printableResults = {'A': 0, 'B': 0, 'C': 0, 'D':0, 'E': 0}
for index, row in df2.iterrows():
  gradeIndex = dtree.predict([[row['age'], row['gender'], row['overallSkillPts'], row['gameTime'], row['miniGamesWith0Stars'], row['miniGamesWith1Star'], row['miniGamesWith2Stars'], row['miniGamesWith3Stars']]])
  grade = gradeByIndex[str(gradeIndex[0])]
  jsonData.append({
        'patientID': row['patientID'], 
        'ipadID': row['ipadID'], 
        'age': row['age'], 
        'gender': row['gender'], 
        'overallSkillPts': row['overallSkillPts'], 
        'gameTime': row['gameTime'], 
        'miniGamesWith0Stars': row['miniGamesWith0Stars'], 
        'miniGamesWith1Star': row['miniGamesWith1Star'], 
        'miniGamesWith2Stars': row['miniGamesWith2Stars'], 
        'miniGamesWith3Stars': row['miniGamesWith3Stars'], 
        'grade': grade
      })
  printableResults[grade] += 1

f = open('generatedGradeData.json', 'w+')
f.write(json.dumps(jsonData))
f.close()

for key in printableResults:
  print(key, printableResults[key])