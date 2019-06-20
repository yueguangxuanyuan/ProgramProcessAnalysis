from Dao import load_data_from_file, get_final_score_map
from common.DataHelper import getOneColumn
from common.MathHelper import normizeDataSet
from config import DATA_MARK
import os
from scipy.stats import f_oneway,levene
from Dao.DataPre import SCORE_FOLD
import numpy as np


def calculateF(data_mark = None) :
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

        dataArray = [];
        for _score in value_map:
            dataArray.append(value_map[_score]);

        l,p = levene(*dataArray);
        if p <= 0.05:
            pass
            # print(headerArray[index],"levene Test show warning (p = %.2f)"%p);
        else :
            f,p = f_oneway(*dataArray);
            if p <= 0.05 :
                print(headerArray[index],f,p);

if __name__ == "__main__":
    mark_array = ["exam1","exam2","exam3","exam4"];
    for mark in mark_array:
        print(mark)
        calculateF(mark);
        print()