from DataScientist import DataScientist

pokerDataSet = DataScientist("handCSV.csv")
print(pokerDataSet.getDataAsNumpyArray())
pokerDataSet.printDataDescriptors()
#pokerDataSet.plotLine("Position", "Wins")
pokerDataSet.trainAndTestClassifier()