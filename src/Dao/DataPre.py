from config import DATA_ROOT_PATH, DATA_MARK
from config import FEATURE_DELIMITER
from config import NULL_OCCUPY
from common.Typehelper import strToType
from common.DataHelper import getOneColumn, getSerevalColumn, getTargetColumnList
import os
from common.DataHelper import getOneColumn
from config import OUT_ROOT_PATH

def load_data_from_file(fileName,needRemoveNULL = True,needType =False):
    # 读入数据文件
    _dataPath = os.path.join(DATA_ROOT_PATH,fileName);
    _datafile = open(_dataPath, 'r');

    # 读取头部信息
    _headerLine = _datafile.readline().rstrip('\n');
    headerArray = _headerLine.split(FEATURE_DELIMITER);

    _headerTypeLine = _datafile.readline().rstrip('\n');
    headerTypeArray = _headerTypeLine.split(FEATURE_DELIMITER);

    zero_for_null_occupy = ["pasteCount", "totalLength", "averageLength", "debugCount", "debugTime", "useDebug","debugErrorCount",
                            "longDeleteCount","successCount","failCount","totalCount","scoreRemainMiddle","scoreRemainHigh",
                            "scoreUp","scoreDown"];
    one_for_null_occupy = ["scoreRemainZero"];

    axis_map = {"totalCount":"buildCount","scoreDown":"testDown","scoreRemainHigh":"testRemainHigh",
                "scoreUp":"testUp","scoreRemainZero":"testRemainZero","scoreRemainMiddle":"testRemainMiddle",
                }
    for _index in range(headerArray.__len__()):
        if headerArray[_index] in axis_map :
            headerArray[_index] = axis_map[headerArray[_index]];

    # 读取数据
    _student_data = [];
    for _line_record in _datafile:
        _line_record = _line_record.rstrip('\n');
        record_array = _line_record.split(FEATURE_DELIMITER);
        for _index, _value in enumerate(record_array):
            if (_value != NULL_OCCUPY):
                try:
                    record_array[_index] = strToType(headerTypeArray[_index], record_array[_index]);
                except:
                    print(_dataPath,"record read fail",record_array[0]);
                    exit(-1);
            elif headerArray[_index] in zero_for_null_occupy:
                record_array[_index] = 0;  # 进行默认值填充
            elif headerArray[_index] in one_for_null_occupy:
                record_array[_index] = 1;

        _student_data.append(record_array);

    if needRemoveNULL :
        # 移除空值行
        _index_of_line_contain_null = [];
        for _index, _line in enumerate(_student_data):
            for item in _line:
                if item == NULL_OCCUPY:
                    _index_of_line_contain_null.append(_index);
                    break;
        # print(index_of_line_contain_null);
        _index_of_line_contain_null.reverse();
        for _index in _index_of_line_contain_null:
            del _student_data[_index]

    if needType :
        return _student_data,headerArray,headerTypeArray;
    else:
        return _student_data,headerArray;

_final_score_map = None;

SCORE_FOLD = None;
def get_final_score_map(tag = SCORE_FOLD):
    global _final_score_map;
    if tag == SCORE_FOLD:
        if _final_score_map is None:
            fileName = "finalscore";
            if SCORE_FOLD is not None :
                fileName += "-"+str(SCORE_FOLD);
            _final_score_array,_header_array = load_data_from_file(fileName);
            _final_score_map ={};
            for _line_record in _final_score_array:
                _final_score_map[_line_record[0]] = _line_record[1];
        return _final_score_map;
    else:
        fileName = "finalscore";
        if tag is not None:
            fileName += "-" + str(tag);
        _final_score_array, _header_array = load_data_from_file(fileName);
        temp_map = {};
        for _line_record in _final_score_array:
            temp_map[_line_record[0]] = _line_record[1];
        return temp_map;

def split_score_to_k_fold(N = 10):
    _final_score_matrix, _header_array,_header_type_array = load_data_from_file("finalscore",needType=True);
    _score_array = getOneColumn(_final_score_matrix,1);
    _score_array = sorted(_score_array);
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

    for _line in _final_score_matrix:
        _line[1] = score_to_index_map[_line[1]];

    out_file_path = os.path.join(OUT_ROOT_PATH,"finalscore-"+str(N));

    out_file = open(out_file_path,"w");
    for index,value in enumerate(_header_array) :
        if index != 0 :
            out_file.write(",");
        out_file.write(value)
    out_file.write("\n")

    for index,value in enumerate(_header_type_array) :
        if index != 0 :
            out_file.write(",");
        out_file.write(value)
    out_file.write("\n")

    for _line in _final_score_matrix :
        for index,value in enumerate(_line) :
            if index != 0 :
                out_file.write(",");
            out_file.write(str(value))
        out_file.write("\n")
    out_file.close()


def getDataAndScore(featureFileName,exam_mark=None,needHeader = False):
    if exam_mark is None:
        exam_mark = DATA_MARK;

    _file_Relative_Path = os.path.join(exam_mark, featureFileName);
    student_data, headerArray = load_data_from_file(_file_Relative_Path);

    _feature_matrix = getSerevalColumn(student_data,[i for i in range(1,headerArray.__len__())])

    # index_array = [1, 1, 1, 1, 1, 2, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 4];
    # target_index_array = [];
    # for _index,_value in enumerate(index_array):
    #     if _value == 1:
    #         target_index_array.append(_index+1);
    # _feature_matrix = getSerevalColumn(student_data, target_index_array)

    # feature_array = ["saveInterval", "programTime", "totalLength", "pasteCount",
    #                   "codeIntervalCount","saveCount","buildInterval",
    #                   "score","codeTime","successCount","testCount",
    #                 "scoreRemainMiddle","avgRemoveErrorTime",
    #                 ];
    # _feature_matrix = getSerevalColumn(student_data,getTargetColumnList(headerArray,feature_array))

    # _score_map = get_final_score_map(None);
    _score_map = get_final_score_map();
    _score_array = [];
    for record in student_data:
        _score_array.append(_score_map[record[0]]);

    # sorted_score_array = sorted(_score_array);
    # gap = _score_array.__len__() / 10;
    # pre_score = -1;
    # score_to_index_map = {};
    # for index, score in enumerate(sorted_score_array):
    #     if score == pre_score:
    #         continue;
    #     else:
    #         fold_index = int(index / gap);
    #         score_to_index_map[score] = fold_index;
    #         pre_score = score;
    #
    # for index,value in enumerate(_score_array):
    #     _score_array[index] = score_to_index_map[value];

    if needHeader :
        return _feature_matrix,_score_array,headerArray;
    else:
        return _feature_matrix,_score_array;

def getCommonUidList():
    exam_mark_array = ["exam1","exam2","exam3","exam4"];
    commonUidList = None;
    for exam_mark in exam_mark_array:
        fileRelativePath = os.path.join(exam_mark,"concatfeature")
        _data,_header = load_data_from_file(fileRelativePath,needRemoveNULL=True);
        uidList = [];
        for record in _data:
            uidList.append(record[0]);
        if commonUidList is None:
            commonUidList = uidList;
        else:
            commonUidList = set(commonUidList).intersection(set(uidList));
            commonUidList = list(commonUidList);

    return commonUidList.__len__();

if __name__ == "__main__":
    split_score_to_k_fold(2);

    # print(getCommonUidList())