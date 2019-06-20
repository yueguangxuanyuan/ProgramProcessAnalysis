import numpy as np
from sklearn.cluster import KMeans

from Dao import getDataAndScore
from common.DataHelper import getOneColumn

current_feature = None;
score_map = {
    "saveInterval":{0:0,1:0,2:0,3:1,4:1},
    "score":{0:0,1:0,2:1,3:1,4:2},
    "scoreRemainMiddle": {0: 0, 1: 0, 2: 0, 3: 0, 4: 1},
    "scoreUp":{0: 0, 1: 0, 2: 1, 3: 1, 4: 2},
};

def useObserveToPredict(featureFileName,exam_mark=None):
    featureMatrix, scoreCol,headerArray= getDataAndScore(featureFileName,exam_mark,needHeader=True);
    precision_array = [];
    gapMap = {"saveInterval":[60],"score":[40,80],"scoreRemainMiddle":[80],"scoreUp":[40,80]}
    for _index in range(0,headerArray.__len__()):
        if headerArray[_index] in gapMap :
            dataArray = getOneColumn(featureMatrix,_index);
            dataArray = np.array(dataArray).reshape(dataArray.__len__(),1);


            #构建预测模型
            sortArray = sorted(dataArray)
            gap = gapMap[headerArray[_index]];
            for gap_index in range(gap.__len__()):
                gap[gap_index] = sortArray [(int)(gap[gap_index]/100*sortArray.__len__())];

            #预测
            predict = [];
            for record_index in range(dataArray.__len__()):
                predict_val = gap.__len__();
                for gap_index,gap_value in enumerate(gap):
                    if dataArray[record_index] <= gap_value:
                        predict_val = gap_index;
                        break;
                predict.append(predict_val);

            #判断准确率
            precision = 0.0;
            current_score_map = score_map[headerArray[_index]];
            for record_index in range(dataArray.__len__()):
                true_grade = current_score_map[scoreCol[record_index]];
                if true_grade == predict[record_index]:
                    precision += 1;

            print(headerArray[_index] , "%.4f"%(precision/dataArray.__len__()));

    # print(precision_array);

if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark)
        useObserveToPredict("concatFeature",mark);