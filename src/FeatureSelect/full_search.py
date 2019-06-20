from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np

from Dao import getDataAndScore
from Util import GetColCombination
from common.FileHelper import checkThenMkdirs
from common.DataHelper import getTargetColumnList,getSerevalColumn

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=196)

def useSVMtoPredictScore(featureMatrix, scoreCol,kernel="rbf",decision_function_shape="ovr"):
    featureMatrix = StandardScaler().fit_transform(featureMatrix)
    precision_array = [];
    for _index in range(10):
        _svc = SVC(kernel=kernel,decision_function_shape = decision_function_shape,degree=2);

        score_array = cross_val_score(_svc,featureMatrix,scoreCol,cv=StratifiedKFold(5,shuffle=True))
        precision_array.append(score_array.mean());

    return np.array(precision_array).mean();

def searchAddOneFeatureOneTime(mark):
    # #"firstCodeTimeFromStart","saveInterval","pasteCount","buildInterval","codeBU","codeBS","scoreUp","successCount","debugTime","debugCount","debugErrorCount",
    # #"failCount","codeBE", "keepError","scoreRemainHigh","useDebug","codeTime","scoreRemainZero","hasBuildError",
    # feature_array = ["codeIntervalCount","totalLength","programTime","avgRemoveErrorTime",
    #                  "testCount","saveCount","longDeleteCount","score",
    #                  "scoreRemainMiddle","generateError","scoreDown","totalCount",
    #                 ];

    # feature_array = ["saveInterval","programTime","totalLength","codeTime","firstCodeTimeFromStart",
    #  "pasteCount","codeIntervalCount","saveCount","longDeleteCount","buildInterval",
    #  "codeBU","score","codeBS","testCount","successCount",
    #  "scoreUp","totalCount","scoreRemainZero","scoreRemainMiddle","avgRemoveErrorTime",
    #  "debugCount","debugTime","debugErrorCount","failCount","codeBE",
    #  "scoreDown","keepError","generateError","useDebug","hasBuildError",
    #  "scoreRemainHigh",
    # ];
    #5"firstCodeTimeFromStart", 16"totalCount",7"longDeleteCount",10"codeBS", 12 "scoreUp",
    #12 "codeBU",13"scoreRemainZero",14"debugCount",14"debugTime",14"debugErrorCount",18"useDebug",19"hasBuildError"
    #"totalLength","pasteCount", 提前移除
    feature_array = ["saveInterval","programTime",
                     "codeIntervalCount","saveCount","buildInterval",
                     "score","codeTime","successCount","testCount",
                   "scoreRemainMiddle","avgRemoveErrorTime",
                    "failCount",
                     "scoreDown","keepError","generateError","codeBE",
                     "scoreRemainHigh",
                    ];

    # feature_array = ["buildInterval","saveInterval","codeIntervalCount","totalLength","programTime","codeTime",
    #                  "avgRemoveErrorTime","testCount",
    #                  "saveCount","scoreRemainMiddle",
    #                  "score","successCount","pasteCount",
    #                 ];

    # feature_array = ["codeIntervalCount","totalLength", "programTime","longDeleteCount",
    #               "avgRemoveErrorTime","testCount","saveCount","scoreRemainMiddle","score","scoreDown","generateError","totalCount",
    #              ];

    dataArray,scoreArray,headerArray = getDataAndScore("concatfeature",mark,needHeader=True)
    del headerArray[0];

    x_array = [];
    y_array = [];
    #逐步添加特征直至完成
    for _count in range(feature_array.__len__()):
        target_feature_name_array = feature_array[:_count+1];
        # print(target_feature_name_array);
        indexList = getTargetColumnList(headerArray,target_feature_name_array);
        # print(indexList)
        featureMatrix = getSerevalColumn(dataArray,indexList)
        precision = useSVMtoPredictScore(featureMatrix,scoreArray)
        print("%d : %.4f"%(_count+1,precision))
        x_array.append(_count+1);
        y_array.append(precision);

    plt.figure()
    plt.plot(x_array,y_array)
    plt.show()


if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark)
        searchAddOneFeatureOneTime(mark)
        # break;