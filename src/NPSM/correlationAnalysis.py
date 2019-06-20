from Dao import get_final_score_map
from watwin.datapre import getStudentDataWithHeader
from common.DataHelper import getOneColumn

import numpy as np;
from scipy.stats import pearsonr

def getData(data_name):
    #返回标注好的数据

    _score_map= get_final_score_map();

    _data_matrix,_data_header = getStudentDataWithHeader(data_name);

    _score_array = [];
    for line_index in range(_data_matrix.__len__()):
        uid = _data_matrix[line_index][0];
        _score_array.append(_score_map[uid]);

    return _data_matrix,_data_header,_score_array;

def calculateCorrelation(data_name):
    _data_matrix, _data_header, _score_array = getData(data_name);

    for index in range(1,_data_header.__len__()):
        _feature_array = getOneColumn(_data_matrix,index);

        print(_data_header[index],pearsonr(_feature_array,_score_array));

if __name__ == "__main__":
    examId_List = ["e1", "e2", "e3", "e4"];
    for eid in examId_List:
        print(eid)
        calculateCorrelation("npsm"+"//"+eid+"-programStateRecord")


