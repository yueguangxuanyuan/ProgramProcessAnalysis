
def tagScore(scoreArray,keyValueList = []) :
    '''
    对Score 进行处理，打上不同的tag
    这里假设每一段数据上都至少有一个数据，比如目标分类有3种，测试集需要至少每种包含一个测试用例

    keyValueList 会覆盖整个测试用例，e.g  [20,60,80] ->    <=20 <=60 <=80 80
    :param scoreArray:
    :param keyValueList:
    :return:
    '''
    reVal = [];
    tagList = [];
    if keyValueList.__len__() == 0 :
        #这个里采取默认的分类,直接取十位数以上
        for scoreItem in scoreArray:
            reVal.append(int(scoreItem / 10));
        for _index in range(0,11) :
            tagList.append(str(_index));
    else:
        #按照keyValueList分段

        for scoreItem in scoreArray:
            newScoreVal = keyValueList.__len__();
            for _index,_value in enumerate(keyValueList) :
                if scoreItem <= _value :
                    newScoreVal = _index;
                    break;
            reVal.append(newScoreVal);

        _lastBorder = -1;# 为了最小段包含0  所以强行写-1
        for _index, _value in enumerate(keyValueList):
            tagList.append(str(_index)+":("+str(_lastBorder) + ","+str(_value)+"]");
            _lastBorder = _value;
        tagList.append("other");
    return reVal,tagList;

if __name__ == "__main__" :
    wholeString = "L[2.0,1212,3.0]";
    listString = wholeString.lstrip("L");
    listString =listString.strip("[]");
    listArray = listString.split(",");
    targetList = [];
    for _value in listArray:
        targetList.append(float(_value));
    print(targetList);