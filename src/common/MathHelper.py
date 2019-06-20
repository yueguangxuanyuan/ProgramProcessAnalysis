from math import sqrt

def getMean(inputList):
    '''
    计算样本平均值
    :param inputList:
    :return:mean
    '''
    sum = 0 ;
    for value in inputList :
        sum += value;
    mean = sum/inputList.__len__();
    return mean

def getStandardDeviation(inputList) :
    '''
    计算样本集的标准差
    :param inputList:
    :return:
    '''
    mean = getMean(inputList);
    sum = 0;
    for value in inputList :
        sum =sum + (value - mean)**2;
    denominator = inputList.__len__()-1;
    if denominator < 1 :
        denominator = 1;
    return  sqrt(sum/denominator);

def calculatePearsonCorrelation(datasetA,datasetB) :
    '''
    计算皮尔森相关系数
    :param datasetA:
    :param datasetB:
    :return:
    '''
    meanA = getMean(datasetA);
    sdA = getStandardDeviation(datasetA);
    meanB = getMean(datasetB);
    sdB = getStandardDeviation(datasetB);

    sum = 0.0 ;
    for index,value in enumerate(datasetA) :
        sum += (value-meanA)*(datasetB[index] - meanB);

    denominator = (datasetA.__len__() - 1) * sdA *sdB;
    if denominator <= 0 :
        denominator = 1;
    return  sum/denominator;

def getMaxAndMin(dataset):
    import copy
    datasetCopy = copy.deepcopy(dataset);
    datasetCopy.sort();
    return datasetCopy[datasetCopy.__len__()-1],datasetCopy[0];

def normizeDataSet(datasetA):
    max,min = getMaxAndMin(datasetA);
    gap = max -min;
    if gap == 0:
        return  datasetA;
    for index,value in enumerate(datasetA) :
        datasetA[index] = (value - min) / gap;
    return datasetA;

def normizeMatrix(matrix):
    colCount = matrix[0].__len__();
    lineCount = matrix.__len__();
    from common.DataHelper import getOneColumn
    for _index in range(0,colCount):
        dataset = getOneColumn(matrix,_index);
        dataset = normizeDataSet(dataset);
        for _line_index in range(0,lineCount) :
            matrix[_line_index][_index] = dataset[_line_index];
    return matrix;

def normizeDataSetZscore(dataSetA) :
    mean = getMean(dataSetA);
    sdA = getStandardDeviation(dataSetA);
    if sdA <= 0:
        sdA = 1;

    for index,value in enumerate(dataSetA):
        dataSetA[index] = (value - mean) / sdA;

    return dataSetA;

def normizeMatrixZscore(matrix):
    colCount = matrix[0].__len__();
    lineCount = matrix.__len__();
    from common.DataHelper import getOneColumn
    for _index in range(0,colCount):
        dataset = getOneColumn(matrix,_index);
        dataset = normizeDataSetZscore(dataset);
        for _line_index in range(0,lineCount) :
            matrix[_line_index][_index] = dataset[_line_index];
    return matrix;

def calculateRSS(y_test,y_predict):
    value = 0;
    for _index,_value in enumerate(y_test):
        value += (_value - y_predict[_index])**2;
    return value/y_test.__len__();

def getprecision(test,predict):
    sameCount = 0;
    for _index,_value in enumerate(test):
        if(_value == predict[_index]) :
            sameCount = sameCount +1;
    return sameCount/test.__len__();

def getprecisionWithTorlerate(test,predict,torlerateRange = 1):
    sameCount = 0;
    for _index,_value in enumerate(test):
        if(abs(predict[_index] - _value) <=torlerateRange ) :
            sameCount = sameCount +1;
    return sameCount/test.__len__();

if __name__ == "__main__" :
    #print(calculatePearsonCorrelation([1,2],[3,4]));
    print (normizeDataSet([2,1,3]));
    print(calculateRSS([1,2],[1,3]));