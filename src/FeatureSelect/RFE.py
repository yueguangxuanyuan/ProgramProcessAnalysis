from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.feature_selection import RFECV,RFE
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt

from Dao import getDataAndScore


def useREFToSelectFeature(examMark):
    # Load the digits dataset

    dataMatrix,scoreArray = getDataAndScore("concatfeature",examMark);

    # Create the RFE object and rank each pixel
    clf = RandomForestClassifier(n_estimators=1000, max_depth=None)
    # rfe = RFECV(estimator=clf,step=1,cv=StratifiedKFold(5,shuffle=True),n_jobs=-1)
    rfe = RFE(estimator=clf,step=1)
    rfe.fit(dataMatrix, scoreArray)
    return rfe.ranking_;

def getRefResult(exam_mark):
    #由于挑出来的特征都差不多 这里直接拿第一次的结果做出来
    dataMatrix, scoreArray,header = getDataAndScore("concatfeature", exam_mark,needHeader=True);
    ranking =useREFToSelectFeature(exam_mark);

    print("[",end=" ")
    for _index,_value in enumerate(ranking):
        if _value == 1:
            print(" \""+header[_index+1]+"\",",end="");
    print("]")

if __name__ == "__main__":
    exam_mark_array = ["exam1","exam2","exam3","exam4"];
    for exam_mark in exam_mark_array:
        print(exam_mark)
        getRefResult(exam_mark)

