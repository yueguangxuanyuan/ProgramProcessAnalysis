from sklearn.ensemble import RandomForestClassifier
from Dao.DataPre import getDataAndScore
import numpy as np;


def useRandomForestToPredict(featureFileName,exam_mark=None):
    _data,_score_array,header = getDataAndScore(featureFileName,exam_mark,needHeader=True);
    clf = RandomForestClassifier(n_estimators=10000, max_depth=None);
    clf.fit(_data,_score_array);

    importance_array = clf.feature_importances_;
    indices = np.argsort(importance_array)[::-1];

    for index in range(1,header.__len__()):

        print("%2d) %-*s"%(index,25,header[indices[index-1]+1]))


def useRandomForestGetSequence(featureFileName,n_estimators=10000):

    countArray = None;
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    # mark_array = ["exam1", ];
    for mark in mark_array:
        _data,_score_array,header = getDataAndScore(featureFileName,mark,needHeader=True);

        if countArray is None:
            countArray =[0]*(header.__len__() - 1);

        clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=None);
        clf.fit(_data,_score_array);

        importance_array = clf.feature_importances_;
        indices = np.argsort(importance_array)

        for seq,index in enumerate(indices):
            countArray[index] += seq;

    indices = np.argsort(countArray)[::-1];

    for index in range(indices.__len__()):
        print("%2d) %-*s"%(index+1,25,header[indices[index]+1]))



if __name__ == "__main__":
    # mark_array = ["exam1", "exam2", "exam3", "exam4"];
    # # mark_array = ["exam1", ];
    # for mark in mark_array:
    #     print(mark)
    #     useRandomForestToPredict("concatFeature", mark);

    useRandomForestGetSequence("concatFeature",10000);