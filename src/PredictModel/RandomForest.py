from sklearn.ensemble import RandomForestClassifier
import os
from Dao.DataPre import getDataAndScore
from sklearn.model_selection import cross_val_score,KFold,LeaveOneOut,LeavePOut,StratifiedKFold
import numpy as np;

import warnings
warnings.filterwarnings("ignore", category=Warning, module="sklearn", lineno=652)
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=542)

def useRandomForestToPredict(featureFileName,exam_mark=None):
    precision_array = [];
    for _index in range(10):
        _data,_score_array = getDataAndScore(featureFileName,exam_mark);
        clf = RandomForestClassifier(n_estimators=100, max_depth=None);
        scores = cross_val_score(clf,_data,_score_array,cv=StratifiedKFold(5,shuffle=True),n_jobs=4);
        # print(scores.mean());
        precision_array.append(scores.mean())

    # print(precision_array);
    print(np.array(precision_array).mean())

if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark,end = " ")
        useRandomForestToPredict("concatFeature", mark);


