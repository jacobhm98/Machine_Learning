import monkdata as m
import dtree as d
import random
import numpy as np
import matplotlib.pyplot as plt

def printFirstFourAssignments():
    print("Entropy of the datasets:")
    entropy1 = d.entropy(m.monk1)
    print(entropy1)

    entropy2 = d.entropy(m.monk2)
    print(entropy2)

    entropy3 = d.entropy(m.monk3)
    print(entropy3)

    print("Average information gain of the attributes in the datasets")
    datasets = (m.monk1, m.monk2, m.monk3)
    for dataset in datasets:
        print("New dataset")
        for attribute in m.attributes:
            print("Information gain of attribute: " + str(attribute.name))
            print(d.averageGain(dataset, attribute))

def selectAttributeToSplitOn(dataset):
    index = 0
    maxGain = 0
    for i in range(0, len(m.attributes)):
        if d.averageGain(dataset, m.attributes[i]) > maxGain:
            index = i
            maxGain = d.averageGain(dataset, m.attributes[i])
    return m.attributes[index]


def splitDataset(dataset):
    subsets = []
    splitAttribute = selectAttributeToSplitOn(dataset)
    for value in splitAttribute.values:
        subsets.append(d.select(dataset, splitAttribute, value))
    return [splitAttribute, subsets]

def createTreeManually():
    tree = splitDataset(m.monk1)
    for i in range(0, len(tree[1])):
        tree[1][i] = splitDataset(tree[1][i])
    for firstLevelNode in tree[1]:
        for i in range(0, len(firstLevelNode[1])):
            firstLevelNode[1][i] = d.mostCommon(firstLevelNode[1][i])
    return tree

def compareTrees():
    tree = createTreeManually()
    id1Tree = d.buildTree(m.monk1, m.attributes, 2)
    print("Manually created tree:")
    print(tree)
    print("ID3 created tree 2 levels deep")
    print(id1Tree)
compareTrees()

def assignment5():
    t1 = d.buildTree(m.monk1, m.attributes)
    print("MONK1 training and test accuracy")
    print(d.check(t1, m.monk1))
    print(d.check(t1, m.monk1test))

    t2 = d.buildTree(m.monk2, m.attributes)
    print("MONK2 training and test accuracy")
    print(d.check(t2, m.monk2))
    print(d.check(t2, m.monk2test))

    t3 = d.buildTree(m.monk3, m.attributes)
    print("MONK3 training and test accuracy")
    print(d.check(t3, m.monk3))
    print(d.check(t3, m.monk3test))

def partition(data, fraction):
    ldata = list(data)
    random.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]

def chooseBestTree(trees, valSet):
    maxAccuracy = 0.0
    index = -1
    for i in range(0, len(trees)):
        currAccuracy = d.check(trees[i], valSet) * 100
        if currAccuracy > maxAccuracy:
            maxAccuracy = currAccuracy
            index = i
    return trees[index]

def prunedTree(dataset, fraction):
    trainSet, valSet = partition(dataset, fraction)
    tree = d.buildTree(trainSet, m.attributes)
    validationPerformance = d.check(tree, valSet) * 100
    newValidationPerformance = 101.0
    bestTree = tree
    while validationPerformance < newValidationPerformance:
        tree = bestTree
        validationPerformance = d.check(tree, valSet) * 100
        newTrees = d.allPruned(tree)
        bestTree = chooseBestTree(newTrees, valSet)
        newValidationPerformance = d.check(bestTree, valSet) * 100
    return tree

def errorAndVariance(trainSet, testSet, numIter):
    fractions = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    testError = np.zeros(len(fractions), dtype=float)
    testVariance = np.zeros(len(fractions), dtype=float)
    errors = np.zeros(numIter, dtype=float)
    for i in range(0, len(fractions)):
        for j in range(0, numIter):
            error = (1 - d.check(prunedTree(trainSet, fractions[i]), testSet)) * 100
            errors[j] = error
        testError[i] = errors.mean(dtype=float)
        testVariance[i] = errors.var(dtype=float)
    return testError, testVariance

def plotErrorsAndVariance():
    error1, variance1 = errorAndVariance(m.monk1, m.monk1test, 100)
    error3, variance3 = errorAndVariance(m.monk3, m.monk3test, 100)
    fractions = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    plt.figure()
    plt.subplot(211)
    plt.title("Error vs Fraction of training to validation set")
    plt.xlabel("Fraction of training to validation set")
    plt.ylabel("Error")
    plt.plot(fractions, error1, label="1")
    plt.plot(fractions, error3, label="3")
    plt.legend()

    plt.subplot(212)
    plt.title("Variance vs Fraction of training to validation set")
    plt.xlabel("Fraction of training to validation set")
    plt.ylabel("Variance")
    plt.plot(fractions, variance1, label="1")
    plt.plot(fractions, variance3, label="3")
    plt.legend()

    plt.tight_layout()
    plt.show()
plotErrorsAndVariance()