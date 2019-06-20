from Dao import load_data_from_file, get_final_score_map
from common.DataHelper import getOneColumn
from common.MathHelper import normizeDataSet
from config import DATA_MARK
import os
from scipy.stats import ttest_ind, levene
from Dao.DataPre import SCORE_FOLD
import numpy as np


def calculateT(data_mark = None) :
    """
    判断两个群体的平均数 是否存在显著的差异
    :param data_mark:
    :return:
    """
    if data_mark is None:
        data_mark = DATA_MARK;
    _fileName = os.path.join(data_mark, "concatfeature");
    student_data,headerArray = load_data_from_file(_fileName);

    _score_map = get_final_score_map();
    _score_array = [];
    for _student_record in student_data:
        _score_array.append(_score_map[_student_record[0]]);

    featureCount = headerArray.__len__() - 1;

    for index in range(1,featureCount+1) :
        dataArray = getOneColumn(student_data,index);
        value_map = {}
        #按照等地分开
        for _score_index,_score in enumerate(_score_array ):
            if _score not in value_map :
                value_map[_score] = [];
            value_map[_score].append(dataArray[_score_index]);

        print(headerArray[index])
        for _i in range(SCORE_FOLD):
            for _j in range(_i+1, SCORE_FOLD):
                a = value_map[_i];
                b = value_map[_j];
                l, p = levene(*[a,b]);
                t_value, p_value = 0,0;
                if p <= 0.05:
                    t_value,p_value = ttest_ind(a,b,equal_var=False);
                else :
                    t_value, p_value = ttest_ind(a, b, equal_var=True);

                if p_value <= 0.05 :
                    # print( _i,_j,"|", t_value , p_value)
                    print( _i,_j)


def calculateMean(data_mark = None) :
    if data_mark is None:
        data_mark = DATA_MARK;
    _fileName = os.path.join(data_mark, "concatfeature");
    student_data,headerArray = load_data_from_file(_fileName);

    _score_map = get_final_score_map();
    _score_array = [];
    for _student_record in student_data:
        _score_array.append(_score_map[_student_record[0]]);

    featureCount = headerArray.__len__() - 1;

    for index in range(1,featureCount+1) :
        if headerArray[index] in ["saveInterval","score"]:
            dataArray = getOneColumn(student_data,index);
            value_map = {}
            #按照等地分开
            for _score_index,_score in enumerate(_score_array ):
                if _score not in value_map :
                    value_map[_score] = [];
                value_map[_score].append(dataArray[_score_index]);

            print(headerArray[index])
            for _i in range(SCORE_FOLD):
                print(_i,"%.2f"%np.array(value_map[_i]).mean())

if __name__ == "__main__":
    mark_array = ["exam1","exam2","exam3","exam4"];
    for mark in mark_array:
        print(mark)
        # calculateT(mark);
        calculateMean(mark);
        print()