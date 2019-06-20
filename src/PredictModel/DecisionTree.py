from sklearn.model_selection import KFold,cross_val_score,StratifiedKFold
from Dao import load_data_from_file, get_final_score_map, getDataAndScore
from config import DATA_MARK
from common.DataHelper import getSerevalColumn
from common.MathHelper import getprecision
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import os
import numpy as np
import graphviz

import warnings
warnings.filterwarnings("ignore", category=Warning, module="sklearn", lineno=652)

def useDecisionTreeToClassify(featureFileName,exam_mark=None,needOutputpdf=False,max_depth =None):
    _feature_matrix,_score_array,headerArray = getDataAndScore(featureFileName,exam_mark,needHeader=True);

    _dt = DecisionTreeClassifier(max_depth=max_depth,min_samples_leaf=2);
    _dt.fit(_feature_matrix, _score_array);

    #输出图像
    if(needOutputpdf) :
        feature_names = [];
        for featureIndex in range(1,headerArray.__len__()):
            feature_names.append(headerArray[featureIndex]);

        dot_data = export_graphviz(_dt, out_file=None,
                             feature_names=None,
                             filled=True, rounded=True,
                             special_characters=True);

        graph = graphviz.Source(dot_data, directory='out/');
        graph.render(mark + "-decisionTree");

def useDecisionTreeToClassifyWithKFold(featureFileName,exam_mark=None,max_depth =None):
    _feature_matrix, _score_array = getDataAndScore(featureFileName, exam_mark);

    # kf = KFold(n_splits=5,shuffle=True);
    # accurate_array = [];
    # for train_index_array, test_index_array in kf.split(_feature_matrix):
    #     X_train = [];
    #     X_test = [];
    #     y_train = [];
    #     y_test = [];
    #     for train_index in train_index_array:
    #         X_train.append(_feature_matrix[train_index]);
    #         y_train.append(_score_array[train_index]);
    #
    #     for test_index in test_index_array:
    #         X_test.append(_feature_matrix[test_index]);
    #         y_test.append(_score_array[test_index])
    #
    #     _dt = DecisionTreeClassifier(max_depth=max_depth);
    #     _dt.fit(X_train, y_train);
    #     score = _dt.score(X_test,y_test);
    #
    #     accurate_array.append(score);
    # print(np.array(accurate_array).mean())

    precision_array = [];
    for _index in range(10):
        _dt = DecisionTreeClassifier(max_depth=max_depth);
        score_array = cross_val_score(_dt,_feature_matrix,_score_array,cv=StratifiedKFold(5,shuffle=True))
        precision_array.append(score_array.mean())
    # print(precision_array);
    print(np.array(precision_array).mean())


if __name__ == "__main__" :
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark,end=" ")
        useDecisionTreeToClassifyWithKFold("concatFeature",mark);
        # useDecisionTreeToClassify("concatFeature",mark,needOutputpdf=True,max_depth=None);
