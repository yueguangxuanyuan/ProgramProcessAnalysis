from sklearn.linear_model import LinearRegression, LogisticRegressionCV, ElasticNetCV, RidgeCV, LassoCV
from sklearn import model_selection
from sklearn.metrics import classification_report
from math import floor
from common.MathHelper import calculateRSS
from common.MathHelper import normizeMatrix
from common.MathHelper import getprecision
from common.MathHelper import getprecisionWithTorlerate
from config import DATA_MARK
import os
from Dao import load_data_from_file, get_final_score_map, SCORE_FOLD, getDataAndScore
from common.DataHelper import getSerevalColumn;
from scipy.stats import spearmanr
import numpy as np
from sklearn.metrics import r2_score

import warnings
warnings.filterwarnings("ignore", category=Warning, module="sklearn", lineno=652)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sklearn", lineno=841)

def useLRtoPredictScore(targetFileName,exam_mark=None,needNorm=True):
    if exam_mark is None :
        exam_mark = DATA_MARK;

    _file_Relative_Path = os.path.join(exam_mark,targetFileName);
    student_data, headerArray = load_data_from_file(_file_Relative_Path);

    _score_map = get_final_score_map();
    _score_array = [];
    for _student_record in student_data:
        _score_array.append(_score_map[_student_record[0]]);

    targetFeatureIndexArray = [ i for i in range(1,headerArray.__len__())];
    featureMatrix = getSerevalColumn(student_data,targetFeatureIndexArray);

    if needNorm :
        featureMatrix = normizeMatrix(featureMatrix);

    _lr = LinearRegression(fit_intercept=True);
    _lr.fit(featureMatrix,_score_array);
    y_predicted = _lr.predict(featureMatrix);
    # y_predicted.astype(int)

    print()
    # print(headerArray);
    # print(_lr.coef_)
    # print(_lr.intercept_)

    print(getprecisionWithTorlerate(y_predicted,_score_array,0.5),getprecisionWithTorlerate(y_predicted,_score_array,1.5),
          getprecisionWithTorlerate(y_predicted,_score_array,2.5),spearmanr(y_predicted, _score_array),r2_score(_score_array, y_predicted))

    # print(y_predicted.astype(int).tolist());
    # print(_score_array)

from sklearn.model_selection import KFold
def useLRtoPredictScoreWithKFold(targetFileName,exam_mark=None,needNorm=True):
    if exam_mark is None :
        exam_mark = DATA_MARK;

    featureMatrix, _score_array = getDataAndScore(targetFileName,exam_mark);

    if needNorm :
        featureMatrix = normizeMatrix(featureMatrix);

    _lr = LinearRegression(fit_intercept=True);
    precision_array = [];
    for _index in range(10):
        _scores = model_selection.cross_val_score(_lr,featureMatrix,_score_array,cv=model_selection.StratifiedKFold(5,shuffle=True) ,scoring=lr_precision)
        precision_array.append(_scores.mean());
    print( np.array(precision_array).mean())

def lr_precision(_lr,x_test,y_test):
    y_predict = _lr.predict(x_test)
    return getprecisionWithTorlerate(y_test,y_predict,0.5);

from sklearn.metrics import classification_report

def useLRCVtoPredictScore(dataset="default"):
    '''
    针对每个目标值，建立一个one vs other 的分类器
    :return:
    '''
    featureMatrix,scoreCol = (dataset);

    X_train, X_test, y_train, y_test = model_selection.train_test_split(featureMatrix, scoreCol, test_size=0.3,
                                                                        random_state=0);
    _lr = LogisticRegressionCV(class_weight="balanced",penalty="l2",solver="newton-cg",multi_class="multinomial");

    _lr.fit(X_train, y_train);
    y_predicted = _lr.predict(X_test);
    print(y_predicted);

    # print("lr accuracy:",_lr.score(X_test,y_test));
    print("lr accuracy:",getprecision(y_test,y_predicted));
    print(classification_report(y_test,y_predicted));


def useElaticNettoPredictScoreWithKFold(targetFileName,exam_mark=None,needNorm=True):
    if exam_mark is None :
        exam_mark = DATA_MARK;

    featureMatrix,_score_array = getDataAndScore(targetFileName,exam_mark);

    if needNorm :
        featureMatrix = normizeMatrix(featureMatrix);

    _lr = ElasticNetCV(alphas=[0.0001, 0.0005, 0.001, 0.01, 0.1, 1, 10], l1_ratio=[1e-4,.01, .1, .5, .9, .99],  max_iter=5000,cv=model_selection.StratifiedKFold(5,shuffle=True));
    precision_array = [];
    for _index in range(10):
        _scores = model_selection.cross_val_score(_lr,featureMatrix,_score_array,cv=model_selection.StratifiedKFold(5,shuffle=True) ,scoring=lr_precision)
        precision_array.append(_scores.mean());
    print( np.array(precision_array).mean())


def useRidgetoPredictScoreWithKFold(targetFileName,exam_mark=None,needNorm=True):
    if exam_mark is None :
        exam_mark = DATA_MARK;

    featureMatrix, _score_array = getDataAndScore(targetFileName, exam_mark);

    if needNorm :
        featureMatrix = normizeMatrix(featureMatrix);

    _lr = RidgeCV(alphas=[0.0001, 0.0005, 0.001, 0.01, 0.1, 1, 10],cv=model_selection.StratifiedKFold(5,shuffle=True));
    precision_array = [];
    for _index in range(10):
        _scores = model_selection.cross_val_score(_lr,featureMatrix,_score_array,cv=model_selection.StratifiedKFold(5,shuffle=True) ,scoring=lr_precision)
        precision_array.append(_scores.mean());
    print( np.array(precision_array).mean())


def useLassotoPredictScoreWithKFold(targetFileName,exam_mark=None,needNorm=True):
    if exam_mark is None :
        exam_mark = DATA_MARK;

    featureMatrix, _score_array = getDataAndScore(targetFileName, exam_mark);

    if needNorm :
        featureMatrix = normizeMatrix(featureMatrix);

    _lr = LassoCV(alphas=[0.01,0.05, 0.1,0.5, 1, 10],cv=model_selection.StratifiedKFold(5,shuffle=True),tol=1e-4);
    precision_array = [];
    for _index in range(10):
        _scores = model_selection.cross_val_score(_lr,featureMatrix,_score_array,cv=model_selection.StratifiedKFold(5,shuffle=True) ,scoring=lr_precision)
        precision_array.append(_scores.mean());
    print( np.array(precision_array).mean())

if __name__ == "__main__" :
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    # mark_array = [ "exam2", "exam3"];
    for mark in mark_array:
        print(mark , end= " | ")
        # useLRtoPredictScoreWithKFold("concatFeature",mark);
        # useRidgetoPredictScoreWithKFold("concatFeature",mark)
        useLassotoPredictScoreWithKFold("concatFeature",mark)
        # useLRtoPredictScore("concatFeature",mark);
