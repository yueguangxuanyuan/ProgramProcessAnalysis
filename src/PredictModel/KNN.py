import warnings

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score,KFold,StratifiedKFold
from sklearn.preprocessing import StandardScaler

from Dao import getDataAndScore
import numpy as np

warnings.filterwarnings("ignore", category=Warning, module="sklearn", lineno=652)

def useKNNtoPredictScore(featureFileName,exam_mark=None,neighbour = 3):
    featureMatrix, scoreCol = getDataAndScore(featureFileName,exam_mark);
    featureMatrix = StandardScaler().fit_transform(featureMatrix)
    precision_array = [];
    for _index in range(10):
        clf = KNeighborsClassifier(neighbour);
        scores = cross_val_score(clf,featureMatrix,scoreCol,cv=StratifiedKFold(5,shuffle=True));
        precision_array.append(scores.mean())
    # print(precision_array);
    print(np.array(precision_array).mean())

if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark, end=" ")
        useKNNtoPredictScore("concatFeature",mark,1);
        # useKNNtoPredictScore("concatFeature",mark,3);
        # useKNNtoPredictScore("concatFeature",mark,5);
