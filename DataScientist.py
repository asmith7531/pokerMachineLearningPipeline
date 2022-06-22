import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray
from pandas import DataFrame
from sklearn import svm
from sklearn.model_selection import train_test_split


class DataScientist:

    def __init__(self, dataSetName: str):
        self.dataSetName = dataSetName
        self.dataFrame = pd.read_csv(dataSetName)


    def normalizeJSON(self) -> None:
        """not used since we switched to building a csv file"""
        self.dataFrame = pd.json_normalize(self.data[0])
        print(self.dataFrame)

    def printDataFrame(self) -> None:
        print(self.dataFrame)

    def getDataAsNumpyArray(self) -> ndarray:
        numpyArray = self.dataFrame.values
        return numpyArray

    def printDataDescriptors(self) -> None:
        print(self.dataFrame.describe())

    def getColumnStat(self, column: str, statistic: str) -> DataFrame:
        descriptiveStats = self.dataFrame.describe()
        thisColumnsStat = descriptiveStats.at[statistic, column]
        return thisColumnsStat

    def getDataSortedByColumn(self, column: str) -> DataFrame:
        descriptiveStats = self.dataFrame.filter(regex=column)
        return descriptiveStats

    def getQuery(self, column: str, boolOperator: str, value: str) -> DataFrame:
        query = column + boolOperator + value
        print(query)
        return self.dataFrame.query(query)

    def removeColumn(self, column: str or list) -> DataFrame:
        return self.DataFrame.drop(columns=[column])

    def removeIncompleteMissing(self) -> DataFrame:
        return self.dataFrame.dropna()

    def replaceIncompleteInstances(self, stat: str) -> DataFrame:
        replacedDataFrame = self.dataFrame.copy()
        for column in self.dataFrame.columns:
            thisColumnStat = self.getColumnStat(column, stat)
            replacedDataFrame.fillna(thisColumnStat, inplace=True)
        return replacedDataFrame

    def graphColumnHistogram(self, column: str, bins=10) -> None:
        self.dataFrame.plot.hist(column=column, by="Win", bins=bins, figsize=(15, 15), cumulative=True)
        plt.savefig("figs/" + self.dataSetName + "_bar_" + column + ".png")
        return

    def graphAllHistograms(self) -> None:
        for column in self.dataFrame:
            if column != 'Win':
                self.graphColumnHistogram(column)
        return

    def plotLine(self, xAxisColumn, yAxisColumn):
        self.dataFrame.plot.scatter(x=xAxisColumn, y=pd.value_counts(yAxisColumn))
        plt.savefig("figs/" + self.dataSetName + "_plot_" + xAxisColumn + "_" + yAxisColumn + ".png")

    def graphTwoColumnsAsScatterPlot(self, xAxisColumn: str, yAxisColumn: str) -> None:
        self.dataFrame.plot.scatter(x=xAxisColumn, y=yAxisColumn, c="Win", cmap="viridis")
        plt.savefig("figs/" + self.dataSetName + "_scatter_" + xAxisColumn + "_" + yAxisColumn + ".png")
        return

    def graphAllPairwiseScatterPlots(self) -> None:
        lastX = []
        for xcolumn in self.dataFrame:
            lastX.append(xcolumn)
            for ycolumn in self.dataFrame:
                if (xcolumn != ycolumn) and (ycolumn not in lastX) and (ycolumn != 'Win') and (xcolumn != 'Win'):
                    self.graphTwoColumnsAsScatterPlot(xcolumn, ycolumn)
            print(lastX)
        return

    def trainAndTestClassifier(self, testSize=0.25) -> None:
        numpyArray = self.getDataAsNumpyArray()
        """slice out columns 10 to 15"""
        numpyArray = np.delete(numpyArray, np.s_[10:16], axis=1)
        features = numpyArray[:, 0:-1]
        features = features.astype("int")
        labels = numpyArray[:, -1]
        labels = labels.astype("int")
        splits = train_test_split(features, labels)
        trainFeatures = splits[0]
        testFeatures = splits[1]
        trainLabels = splits[2]
        testLabels = splits[3]
        self.classifier = svm.SVC()
        self.classifier.fit(trainFeatures, trainLabels)
        accuracy = self.classifier.score(testFeatures, testLabels)
        print("The accuracy of the model is: " + str(accuracy * 100) + "%")

    def classifyUnseenInstance(self, instanceFeatures: list) -> None:
        if self.classifier is None:
            self.trainAndTestClassifier()
        predictedLabel = self.classifier.predict([instanceFeatures])
        winLose = ["Win", "Lose"]
        print("The predicted species is " + winLose[int(predictedLabel)])