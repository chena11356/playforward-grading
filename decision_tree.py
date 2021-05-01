# Following tutorial: https://www.w3schools.com/python/python_ml_decision_tree.asp

import pandas
from sklearn import tree
import pydotplus
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimg

df = pandas.read_json("dataGrades.json")

print(df)