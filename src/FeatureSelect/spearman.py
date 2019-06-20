from Dao import load_data_from_file, get_final_score_map
from common.DataHelper import getOneColumn
from common.MathHelper import normizeDataSet
from config import DATA_MARK
import os
from scipy.stats import spearmanr

def calculateSpearman(dataFileName,data_mark = None,neadNorm =False) :
    if data_mark is None:
        data_mark = DATA_MARK;
    _fileName = os.path.join(data_mark, dataFileName);
    student_data,headerArray = load_data_from_file(_fileName);

    _score_map = get_final_score_map();
    _score_array = [];
    for _student_record in student_data:
        _score_array.append(_score_map[_student_record[0]]);

    featureCount = headerArray.__len__() - 1;

    if(neadNorm):
        _score_array =normizeDataSet(_score_array);

    for index in range(1,featureCount+1) :
        dataArray = getOneColumn(student_data,index);
        if (neadNorm):
            dataArray = normizeDataSet(dataArray);
        pValue,p = spearmanr(dataArray,_score_array);
        print(headerArray[index],pValue,p);
        # if p <= 0.05 :
        #     # print(headerArray[index],pValue);
        #     print(headerArray[index]);

if __name__ == "__main__":
    mark_array = ["exam1","exam2","exam3","exam4"];
    file_array = ["saveRecord-t2","BuildTime","buildResultCount-t2","codeCount-15-t2",
                  "debugCount-t2","scoreCount-t2","scoreTendency-t2","deleteRecord-t2",
                  "pasteCount-t2"];

    for mark in mark_array:
        print(mark)
        for fileName in file_array:
            calculateSpearman(fileName,mark);
        print()