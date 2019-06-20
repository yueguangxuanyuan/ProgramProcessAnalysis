from sklearn.svm import SVR
from sklearn import model_selection
from sklearn.model_selection import cross_val_score,KFold,StratifiedKFold
from sklearn.preprocessing import StandardScaler
import numpy as np
from Dao import getDataAndScore
from common.MathHelper import getprecisionWithTorlerate;

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=196)
warnings.filterwarnings("ignore", category=Warning, module="sklearn", lineno=652)

def useSVMtoPredictScore(featureFileName,exam_mark=None,kernel="rbf"):
    featureMatrix, scoreCol = getDataAndScore(featureFileName,exam_mark);
    featureMatrix = StandardScaler().fit_transform(featureMatrix)
    precision_array = [];
    for _index in range(10):
        _svc = SVR(kernel=kernel,degree=2);

        score_array = cross_val_score(_svc,featureMatrix,scoreCol,cv=StratifiedKFold(5,shuffle=True),scoring=getScore)
        # print(score_array.mean());
        precision_array.append(score_array.mean());

    # print(precision_array);
    print(np.array(precision_array).mean())

def getScore(_svr ,x_test,y_test):
    y_predict = _svr.predict(x_test);
    return getprecisionWithTorlerate(y_test,y_predict,0.5);

if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark, end=" ")
        # useSVMtoPredictScore("concatFeature", mark ,kernel="linear");
        useSVMtoPredictScore("concatFeature", mark ,kernel="rbf");