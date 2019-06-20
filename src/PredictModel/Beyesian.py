import warnings

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn import model_selection
from sklearn.model_selection import cross_val_score,KFold,StratifiedKFold
from Dao import getDataAndScore
import numpy as np

warnings.filterwarnings("ignore", category=Warning, module="sklearn", lineno=652)

def useGaussianNBtoPredictScore(featureFileName,exam_mark=None):
    featureMatrix, scoreCol = getDataAndScore(featureFileName,exam_mark);
    precision_array = [];
    for _index in range(10):
        clf = GaussianNB();
        scores = cross_val_score(clf,featureMatrix,scoreCol,cv=StratifiedKFold(5,shuffle=True));
        precision_array.append(scores.mean())
    # print(precision_array);
    print(np.array(precision_array).mean())

if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark, end=" ")
        useGaussianNBtoPredictScore("concatFeature",mark);
        # useMultinomialNBtoPredictScore("concatFeature",mark);