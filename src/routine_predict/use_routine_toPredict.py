from sklearn import model_selection
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.naive_bayes import GaussianNB

from Dao import get_final_score_map
from Util import GetColCombination
from common.MathHelper import getprecisionWithTorlerate
from config import DATA_ROOT_PATH
from common.DataHelper import getOneColumn
from sklearn.svm import SVC

from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr,spearmanr
from common.DataHelper import getTargetColumnList,getSerevalColumn
import matplotlib.pyplot as plt
import os
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=196)

exam_mark = "exam2"

# data_name = "routine_percent"
# featureSize = 3
# header = ["back","stick","forward"];
# target_col = [0,1,2]

data_name = "routine_nine_percent"
featureSize = 9
header = ["FF","FS","FB","SF","SS","SB","BF","BS","BB"];
target_col = [0, 1, 3, 4, 7]
# target_col = [0, 4, 7]

needSplitScore=True;
spliteK=3;

def load_routine_data(needHeader = False):
    datPath  = os.path.join(DATA_ROOT_PATH,exam_mark,data_name);

    id_array = [];
    data_matrix = [];

    infile = open(datPath, "r");
    for _line in infile:
        _line = _line.rstrip("\n")
        _linedata = _line.split(",")

        user_id = _linedata[0];
        id_array.append(user_id);

        data = [float(_linedata[i]) for i in range(1,featureSize+1)];
        data_matrix.append(data);

    scoreMap = get_final_score_map(None);
    scoreArray = [];
    for _id in id_array:
        scoreArray.append(scoreMap[_id]);

    if needSplitScore :
        scoreArray = split_score_to_k_fold(scoreArray,spliteK)

    #筛选特征
    data_matrix = np.array(data_matrix)[:,target_col];
    the_header = np.array(header)[target_col];

    if needHeader :
        return data_matrix,scoreArray,the_header;
    else:
        return data_matrix,scoreArray,


def calculate_pearson():
    data_matrix,scoreArray,header = load_routine_data(True);

    for _index,_value in enumerate(header):

        data_col = getOneColumn(data_matrix,_index);
        p,pvalue = pearsonr(data_col,scoreArray);
        sp,sp_pvalue= spearmanr(data_col,scoreArray)
        print(_value , p ,pvalue,sp,sp_pvalue);

def use_LR_to_fit():
    data_matrix, scoreArray = load_routine_data();
    _lr = LinearRegression(fit_intercept=True);
    _lr.fit(data_matrix, scoreArray);

    predict = _lr.predict(data_matrix);

    p, pvalue = pearsonr(predict, scoreArray);
    sp, sp_pvalue = spearmanr(predict, scoreArray)
    print( p, pvalue, sp, sp_pvalue);

def draw_scatter():
    data_matrix,scoreArray,header = load_routine_data(True);

    for _index,_value in enumerate(header):
        data_col = getOneColumn(data_matrix,_index);

        plt.figure();
        plt.scatter(data_col,scoreArray);
        plt.title(_value);
        plt.show();

def split_score_to_k_fold(score_array,N = 3):
    _score_array = sorted(score_array);
    gap = _score_array.__len__()/N;
    pre_score = -1;
    score_to_index_map = {};
    for index,score in enumerate(_score_array):
        if score == pre_score :
            continue;
        else :
            fold_index = int(index/gap);
            score_to_index_map[score] = fold_index;
            pre_score = score;

    for _index in range(score_array.__len__()):
        score_array[_index] = score_to_index_map[score_array[_index]];
    return score_array;

def use_svm_to_predict():
    data_matrix, scoreArray, header = load_routine_data(True);
    _svc = SVC(kernel="rbf", decision_function_shape="ovr", degree=2);
    _svc.fit(data_matrix,scoreArray);
    print(_svc.score(data_matrix,scoreArray));

    precision_array = []
    for _index in range(10):
        clf = SVC(kernel="rbf", decision_function_shape="ovr", degree=2);
        scores = cross_val_score(clf, data_matrix, scoreArray, cv=StratifiedKFold(5, shuffle=True));
        precision_array.append(scores.mean())
    print(np.array(precision_array).mean())

def useGaussianNBtoPredictScore():
    data_matrix, scoreArray, header = load_routine_data(True);
    clf = GaussianNB();
    clf.fit(data_matrix,scoreArray);
    print(clf.score(data_matrix,scoreArray));

    precision_array = []
    for _index in range(10):
        clf = GaussianNB();
        scores = cross_val_score(clf,data_matrix,scoreArray,cv=StratifiedKFold(5,shuffle=True));
        precision_array.append(scores.mean())
    print(np.array(precision_array).mean())


from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabaz_score
from scipy.spatial.distance import cdist
def useKmeanToCluster():
    data_matrix, scoreArray, header = load_routine_data(True);

    x_array = [];
    score_array = [];
    dis_array = [];
    for _cluster_n in range(2,15):
        kmeans = KMeans(n_clusters=_cluster_n)
        y_predict = kmeans.fit_predict(data_matrix);
        score = calinski_harabaz_score(data_matrix,y_predict);
        avg_distance = sum(np.min(cdist(data_matrix,kmeans.cluster_centers_),axis=1));
        x_array.append(_cluster_n);
        score_array.append(score);
        dis_array.append(avg_distance);
        print(_cluster_n,score,avg_distance);

    plt.figure()
    plt.plot(x_array,score_array,label="score");
    plt.legend();
    plt.show();
    plt.figure()
    plt.plot(x_array, dis_array, label="distance");
    plt.legend();
    plt.show();

    # #按照肘部原则，将数据聚成4类
    # kmeans = KMeans(n_clusters=5)
    # y_predict = kmeans.fit_predict(data_matrix);
    # plt.scatter(scoreArray,y_predict,c=y_predict,marker="o",s=8);
    # plt.show();

def lr_precision(_lr,x_test,y_test):
    y_predict = _lr.predict(x_test)
    return getprecisionWithTorlerate(y_test,y_predict,0.5);

def use_lr_with_kfold():
    data_matrix, scoreArray, header = load_routine_data(True);
    _lr = LinearRegression(fit_intercept=True);
    precision_array = [];
    for _index in range(10):
        _scores = model_selection.cross_val_score(_lr, data_matrix, scoreArray,
                                                  cv=model_selection.StratifiedKFold(5, shuffle=True),
                                                  scoring=lr_precision)
        precision_array.append(_scores.mean());
    print(np.array(precision_array).mean())

def tryAllFeatureCompositeWithNB():
    data_matrix, scoreArray, header = load_routine_data(True);
    clf = GaussianNB();

    compositeGenerator = GetColCombination(header);

    for _n in range(1,header.__len__()+1):
        compositeGenerator.setCompositeNum(_n);

        canFind,colArray = compositeGenerator.getNextComposite();
        while canFind:
            print(colArray,end=" : ")
            colIndexArray = getTargetColumnList(header,colArray);
            data = getSerevalColumn(data_matrix,colIndexArray)
            precision_array = []
            for _index in range(10):
                scores = cross_val_score(clf, data, scoreArray, cv=StratifiedKFold(5, shuffle=True));
                precision_array.append(scores.mean())
            print(np.array(precision_array).mean())

            canFind, colArray = compositeGenerator.getNextComposite();

def tryAllFeatureCompositeWithSVM():
    data_matrix, scoreArray, header = load_routine_data(True);
    clf = SVC(kernel="poly", decision_function_shape="ovr", degree=2);

    compositeGenerator = GetColCombination(header);

    for _n in range(1,header.__len__()+1):
        compositeGenerator.setCompositeNum(_n);

        canFind,colArray = compositeGenerator.getNextComposite();
        while canFind:
            print(colArray,end=" : ")
            colIndexArray = getTargetColumnList(header,colArray);
            data = getSerevalColumn(data_matrix,colIndexArray)
            precision_array = []
            for _index in range(10):
                scores = cross_val_score(clf, data, scoreArray, cv=StratifiedKFold(5, shuffle=True));
                precision_array.append(scores.mean())
            print(np.array(precision_array).mean())

            canFind, colArray = compositeGenerator.getNextComposite();

if __name__ == "__main__":
    # draw_scatter();
    # calculate_pearson()
    # use_LR_to_fit();

    # use_svm_to_predict();
    # useGaussianNBtoPredictScore();
    # use_lr_with_kfold()
    # useKmeanToCluster();

    tryAllFeatureCompositeWithNB()
    # tryAllFeatureCompositeWithSVM()
