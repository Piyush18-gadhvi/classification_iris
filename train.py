# Python version
import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn

#load libraries
import pandas
#from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import mlflow


#load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length','sepal-width','petal-length','petal-width','class']
dataset = pandas.read_csv(url, names=names)

#shape
#print(dataset.shape)

#head
#print(dataset.head(20))

#descriptions
#print(dataset.describe())

#class distribution
#print(dataset.groupby('class').size())

#box and wisker plots
#dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
#plt.show()

# histograms
#dataset.hist()
#plt.show()

#scatter plot matrix
#scatter_matrix(dataset)
#plt.show()

#split-out validation dataset
array = dataset.values
X = array[:,0:4]
Y = array[:,4]
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
#x_valid=pandas.DataFrame(X_validation)
#x_valid.to_csv("iris_validation.csv")
#y_valid=pandas.DataFrame(Y_validation)
#y_valid.to_csv("Y_iris_validation.csv")
# Test options and evaluation metric
seed = 7
scoring = 'accuracy'

#spot check algorithms

models = []
models.append(('LR', LogisticRegression()))
#models.append(('LDA', LinearDiscriminantAnalysis()))
#models.append(('KNN',KNeighborsClassifier() ))
#models.append(('CART', DecisionTreeClassifier() ))
#models.append(('NB',GaussianNB() ))
#models.append(('SVM', SVC() ))

#evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed, shuffle=True)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    #print(cv_results)
    results.append(cv_results)
    names.append(name)
    msg = "***************"+"%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

#compare algorithms
#    fig = plt.figure()
#    fig.suptitle('Algorithm Comparison')
#   ax = fig.add_subplot(111)
#   plt.boxplot(results)
#   ax.set_xticklabels(names) 
#   plt.show()

#make predicitions on validation dataset

knn = KNeighborsClassifier()
with mlflow.start_run():
    #lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    knn.fit(X_train, Y_train)
    #predicted_qualities = lr.predict(test_x)
    #(rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)
    #print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    #print("  RMSE: %s" % rmse)
    #print("  MAE: %s" % mae)
    #print("  R2: %s" % r2)
    #mlflow.log_param("alpha", alpha)
    #mlflow.log_param("l1_ratio", l1_ratio)
    #mlflow.log_metric("rmse", rmse)
    #mlflow.log_metric("r2", r2)
    #mlflow.log_metric("mae", mae)
    mlflow.sklearn.log_model(knn, "model")
#    predictions = knn.predict(X_validation)
#    print(accuracy_score(Y_validation, predictions))
#    print(confusion_matrix(Y_validation, predictions))
#    print(classification_report(Y_validation, predictions))
