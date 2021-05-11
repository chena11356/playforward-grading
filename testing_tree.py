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

results = {'0': 0, '1': 0, '2': 0, '3':0, '4': 0}

i = 0
while (i < len(df.index)):
  test = df.loc[i]
  small_df = df.drop(df.index[i])

  # Define features and targets columns
  features = ['age', 'gender', 'overallSkillPts', 'gameTime', 'miniGamesWith0Stars', 'miniGamesWith1Star', 'miniGamesWith2Stars', 'miniGamesWith3Stars']

  X = small_df[features]
  y = small_df['grade']

  # Create decision tree
  dtree = DecisionTreeClassifier()
  dtree = dtree.fit(X, y)

  # Test decision tree against one left out grade
  gradeIndex = dtree.predict([[test['age'], test['gender'], test['overallSkillPts'], test['gameTime'], test['miniGamesWith0Stars'], test['miniGamesWith1Star'], test['miniGamesWith2Stars'], test['miniGamesWith3Stars']]])
  diff = abs(gradeIndex[0] - test['grade'])
  results[str(diff)] += 1

  i += 1

for key in results:
  print(key, results[key])