from watwin.datapre import getStudentData
from common.DataHelper import getTargetColumnIndex
from common.DataHelper import getOneColumn
from common.MathHelper import normizeDataSet
from common.MathHelper import calculatePearsonCorrelation
from Dao import get_final_score_map

# student_data = getStudentData();

import numpy as np;
from scipy.stats import pearsonr

def usePearsonrCalAll():
    examId_List = ["e1","e2","e3","e4"];
    algorithm_List = ["EQ","Watwin"];
    target_List = ["score","finalscore"];

    print('|数据名称|相关系数|p|');
    print('|-|-|-|')

    for al in algorithm_List :
        for target in target_List :
            for eid in examId_List:
                dataFileName = eid +"-"+al +"-"+target;
                student_data = getStudentData(al+"//"+dataFileName);
                # scoreArray = getOneColumn(student_data, 2);
                scoreArray = [];
                final_score_map = get_final_score_map();
                for _line in student_data :
                    scoreArray.append(final_score_map[str(_line[0])]);

                watwinArray  = getOneColumn(student_data,1);
                c,p = pearsonr(scoreArray, watwinArray);
                print("|",dataFileName,"|",c,"|",p,"|");

from sklearn.linear_model import LinearRegression

def scoreAll():
    examId_List = ["e1","e2","e3","e4"];
    algorithm_List = ["EQ","Watwin"];
    target_List = ["score","finalscore"];

    print('|数据名称|r^2|');
    print('|-|-|')
    model = LinearRegression();

    for al in algorithm_List :
        for target in target_List :
            for eid in examId_List:
                dataFileName = eid +"-"+al +"-"+target;
                student_data = getStudentData(al+"//"+dataFileName);

                scoreArray = [];
                final_score_map = get_final_score_map();
                for _line in student_data:
                    scoreArray.append(final_score_map[str(_line[0])]);
                scoreArray = np.array(scoreArray).reshape(scoreArray.__len__(),1);

                watwinArray  = getOneColumn(student_data,1);
                watwinArray = np.array(watwinArray).reshape(watwinArray.__len__(),1);

                score = model.fit(watwinArray,scoreArray).score(watwinArray,scoreArray);
                print("|", dataFileName, "|", score, "|");


def getGradeMap():
    scoreData = getStudentData("finalscore");
    scoreArray = getOneColumn(scoreData, 1);
    scoreArray.sort();

    gradeArray = [40, 50, 70];

    for index in range(gradeArray.__len__()):
        gradeArray[index] = float(gradeArray[index]) * scoreArray.__len__() / 100;

    scoreMap = {};
    for index, value in enumerate(scoreArray):
        if value not in scoreMap:
            grade = -1;
            if index < gradeArray[0]:
                grade = 0;
            elif index < gradeArray[1]:
                grade = 1;
            elif index < gradeArray[2]:
                grade = 2;
            else:
                grade = 3;
            scoreMap[value] = grade;
    return scoreMap;

def scorefinalScoreWithExpDef():
    examId_List = ["e1","e2","e3","e4"];
    algorithm_List = ["EQ","Watwin"];
    target_List = ["finalscore"];

    scoreMap = getGradeMap();

    print('|数据名称|r^2|');
    print('|-|-|')
    model = LinearRegression();

    for al in algorithm_List :
        for target in target_List :
            for eid in examId_List:
                dataFileName = eid +"-"+al +"-"+target;
                student_data = getStudentData(al+"//"+dataFileName);
                scoreArray = getOneColumn(student_data, 2);
                for index in range(scoreArray.__len__()):
                    scoreArray[index] = scoreMap[scoreArray[index]];
                # print(scoreArray);
                scoreArray = np.array(scoreArray).reshape(scoreArray.__len__(),1);
                watwinArray  = getOneColumn(student_data,1);

                watwinArray = np.array(watwinArray).reshape(watwinArray.__len__(),1);
                score = model.fit(watwinArray,scoreArray).score(watwinArray,scoreArray);
                print("|", dataFileName, "|", score, "|");

def usLRtoPredictWithExpDef():
    examId_List = ["e1","e2","e3","e4"];
    algorithm_List = ["EQ","Watwin"];
    target_List = ["finalscore"];

    scoreMap = getGradeMap();
    print('|数据名称|预测准确率|');
    print('|-|-|')

    for al in algorithm_List:
        for eid in examId_List :
            for target in target_List :
                dataFileName = eid +"-"+al +"-"+target;
                student_data = getStudentData(al +"//"+dataFileName);
                # scoreArray = getOneColumn(student_data, 2);
                scoreArray = [];
                final_score_map = get_final_score_map();
                scoreArray = getOneColumn(student_data, 2);
                for index in range(scoreArray.__len__()):
                    scoreArray[index] = scoreMap[scoreArray[index]];

                scoreArray = np.array(scoreArray).reshape(scoreArray.__len__(),1);


                watwinArray  = getOneColumn(student_data,1);
                watwinArray = np.array(watwinArray).reshape(watwinArray.__len__(),1);

                _lr = LinearRegression(fit_intercept=True);
                _lr.fit(watwinArray, scoreArray);
                y_predicted = _lr.predict(watwinArray);

                print("|", dataFileName, "|", getprecisionWithTorlerate(y_predicted,scoreArray,0.5),"|");


from sklearn import model_selection
from common.MathHelper import getprecision
from common.MathHelper import getprecisionWithTorlerate
from math import floor
from common.TagHelper import tagScore
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from Dao import SCORE_FOLD
from scipy.stats import spearmanr

def usLRtoPredict():
    examId_List = ["e1","e2","e3","e4"];
    algorithm_List = ["EQ","Watwin"];
    target_List = ["finalscore"];


    print('|数据名称|预测|5分|10分|');
    print('|-|-|-|')

    for al in algorithm_List:
        for eid in examId_List :
            for target in target_List :
                dataFileName = eid +"-"+al +"-"+target;
                student_data = getStudentData(al +"//"+dataFileName);
                # scoreArray = getOneColumn(student_data, 2);
                scoreArray = [];
                final_score_map = get_final_score_map();
                for _line in student_data:
                    scoreArray.append(final_score_map[str(_line[0])]);

                scoreArray = np.array(scoreArray).reshape(scoreArray.__len__(),1);

                watwinArray  = getOneColumn(student_data,1);
                watwinArray = np.array(watwinArray).reshape(watwinArray.__len__(),1);
                _lr = LinearRegression(fit_intercept=True);
                _lr.fit(watwinArray, scoreArray);
                y_predicted = _lr.predict(watwinArray);
                print("|", dataFileName, "|", getprecisionWithTorlerate(y_predicted, scoreArray, 0.5), "|",
                      getprecisionWithTorlerate(y_predicted, scoreArray, 1.5),
                      "|", getprecisionWithTorlerate(y_predicted, scoreArray, 2.5), "|",
                      r2_score(scoreArray, y_predicted), "|", spearmanr(y_predicted, scoreArray));


def usLRtoPredictWithKFold():
    examId_List = ["e1","e2","e3","e4"];
    algorithm_List = ["EQ","Watwin"];
    target_List = ["finalscore"];


    print('|数据名称|预测|5分|10分|');
    print('|-|-|-|')

    for al in algorithm_List:
        for eid in examId_List :
            for target in target_List:
                dataFileName = eid +"-"+al +"-"+target;
                student_data = getStudentData(al +"//"+dataFileName);
                # scoreArray = getOneColumn(student_data, 2);
                scoreArray = [];
                final_score_map = get_final_score_map();
                for _line in student_data:
                    scoreArray.append(final_score_map[str(_line[0])]);

                scoreArray = np.array(scoreArray).reshape(scoreArray.__len__(),1);


                watwinArray  = getOneColumn(student_data,1);
                watwinArray = np.array(watwinArray).reshape(watwinArray.__len__(),1);

                kf = KFold(n_splits=10, shuffle=True);
                accurate_array = [];
                within_5_array = [];
                r_2_array = [];
                within_10_array = [];

                for train_index_array, test_index_array in kf.split(watwinArray):
                    X_train = [];
                    X_test = [];
                    y_train = [];
                    y_test = [];
                    for train_index in train_index_array:
                        X_train.append(watwinArray[train_index]);
                        y_train.append(scoreArray[train_index]);

                    for test_index in test_index_array:
                        X_test.append(watwinArray[test_index]);
                        y_test.append(scoreArray[test_index])

                    _lr = LinearRegression(fit_intercept=True);
                    _lr.fit(X_train, y_train);
                    y_predicted = _lr.predict(X_test);

                    accurate_array.append(getprecisionWithTorlerate(y_predicted, y_test,0.5));
                    within_5_array.append(getprecisionWithTorlerate(y_test, y_predicted, 1.5));
                    within_10_array.append(getprecisionWithTorlerate(y_test, y_predicted, 2.5));
                    r_2_array.append(r2_score(y_test, y_predicted));

                print("|", dataFileName, "|", np.array(accurate_array).mean(), "|", np.array(within_5_array).mean(),
                      "|", np.array(within_10_array).mean(), "|", np.array(r_2_array).mean());


if __name__ == "__main__":

    # usePearsonrCalAll()
    # scoreAll();
    # scorefinalScoreWithExpDef();
    usLRtoPredictWithExpDef()

    # usLRtoPredict();
    # usLRtoPredictWithKFold();