from sklearn import model_selection

from Dao import SCORE_FOLD
from common.MathHelper import getprecision
from common.MathHelper import getprecisionWithTorlerate
from math import floor
from common.TagHelper import tagScore
from sklearn.linear_model import LinearRegression

from common.DataHelper import getSerevalColumn
from NPSM.correlationAnalysis import getData
import numpy as np
from scipy.stats import spearmanr
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score

from scipy.stats import spearmanr


import warnings
warnings.filterwarnings("ignore", category=Warning, module="sklearn", lineno=652)

def usLRtoPredict():
    examId_List = ["e1","e2","e3","e4"];
    target_List = ["programStateRecord"];


    print('|数据名称|预测|r^2|spearman|');
    print('|-|-|-|')

    for eid in examId_List :
            for target in target_List :
                dataFileName = eid +"-"+target;
                _data_matrix, _data_header, _score_array = getData("npsm//"+dataFileName);

                _feature_matrix = getSerevalColumn(_data_matrix,[i for i in range(1,_data_header.__len__())]);
                # _feature_matrix = getSerevalColumn(_data_matrix,[1,8]);
                # _feature_matrix = getSerevalColumn(_data_matrix,[1,4,8]);
                # _feature_matrix = getSerevalColumn(_data_matrix,[1,2,3,9]);
                _score_array = np.array(_score_array).reshape(_score_array.__len__(),1)

                _lr = LinearRegression();
                _lr.fit(_feature_matrix, _score_array);
                y_predicted = _lr.predict(_feature_matrix);


                print("|", dataFileName, "|", getprecisionWithTorlerate(_score_array,y_predicted,0.5), "|",getprecisionWithTorlerate(_score_array,y_predicted,1.5),"|",
                      getprecisionWithTorlerate(_score_array, y_predicted, 2.5),"|",r2_score(_score_array,y_predicted),"|",spearmanr(_score_array,y_predicted), "|" ,getprecisionWithTorlerate(_score_array,y_predicted,5));

def usLRtoPredictWithKFold():
    examId_List = ["e1","e2","e3","e4"];
    target_List = ["programStateRecord"];


    print('|数据名称|预测|5分|10分|');
    print('|-|-|-|')

    for eid in examId_List :
            for target in target_List :
                dataFileName = eid +"-"+target;
                _data_matrix, _data_header, _score_array = getData("npsm//"+dataFileName);

                # _feature_matrix = getSerevalColumn(_data_matrix,[i for i in range(1,_data_header.__len__())]);
                _feature_matrix = getSerevalColumn(_data_matrix,[8]);
                _score_array = np.array(_score_array).reshape(_score_array.__len__(),1)

                # kf = KFold(n_splits=5, shuffle=True);
                #
                # accurate_array = [];
                # within_5_array = [];
                # within_10_array = [];
                # r_2_array = [];
                #
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
                #     _lr = LinearRegression(fit_intercept=True);
                #     _lr.fit(X_train, y_train);
                #     y_predicted = _lr.predict(X_test);
                #
                #     accurate_array.append(getprecisionWithTorlerate(y_test, y_predicted, 0.5));
                #     within_5_array.append(getprecisionWithTorlerate(y_test, y_predicted, 1.5));
                #     within_10_array.append(getprecisionWithTorlerate(y_test, y_predicted, 2.5));
                #
                #     y_total_predict = _lr.predict(_feature_matrix)
                #     r_2_array.append(r2_score(_score_array,y_total_predict));
                #
                #
                # print("|", dataFileName, "|", np.array(accurate_array).mean(), "|",np.array(within_5_array).mean(),
                #       "|",np.array(within_10_array).mean(), "|", np.array(r_2_array).mean());

                _lr = LinearRegression(fit_intercept=True);
                precision_array = [];
                for _index in range(10):
                    _scores = model_selection.cross_val_score(_lr,_feature_matrix,_score_array,cv=model_selection.StratifiedKFold(5,shuffle=True),scoring=lr_precision)
                    precision_array.append(_scores.mean());
                print("|", dataFileName, "|",np.array(precision_array).mean(),"|");


def lr_precision(_lr,x_test,y_test):
    y_predict = _lr.predict(x_test)
    return getprecisionWithTorlerate(y_test,y_predict,0.5);

if __name__ == "__main__":
    # usLRtoPredict();
    usLRtoPredictWithKFold()