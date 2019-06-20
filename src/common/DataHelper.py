

def getOneColumn(matrix , columnIndex):
    '''
    抽取二维数组的一列
    :param matrix:
    :param colomnIndex:
    :return:
    '''
    reVal = [];
    for line in matrix:
        reVal.append(line[columnIndex]);
    return reVal;

def getOneColumn2D(matrix , columnIndex):
    '''
    抽取二维数组的一列
    :param matrix:
    :param colomnIndex:
    :return:
    '''
    reVal = [];
    for line in matrix:
        newline = [];
        newline.append(line[columnIndex])
        reVal.append(newline);
    return reVal;

def getSerevalColumn(matrix, columnList) :
    '''
    筛选出二维数组中指定的几列
    :param matrix:
    :param columnList:
    :return:
    '''
    reVal = [];
    for line in matrix:
        lineContent = [];
        for columnIndex in columnList :
            lineContent.append(line[columnIndex]);
        reVal.append(lineContent);
    return reVal;

def getTargetColumnIndex(headerArray, colName):
    '''
    从表头中找到 指定列名的索引
    :param headerArray:
    :param colName:
    :return: index or -1
    '''
    targetIndex = -1;
    for index, item in enumerate(headerArray):
        if item == colName:
            targetIndex = index;
            break;
    return targetIndex;

def getTargetColumnList(headerArray,colNameList):
    '''
    筛选出一串col index
    :param headerArray:
    :param colNameList:
    :return:
    '''
    reVal = [];
    for colName in colNameList :
        reVal.append(getTargetColumnIndex(headerArray,colName));
    return reVal;