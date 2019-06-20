dataName = 't3_4-score'
from config import DATA_ROOT_PATH
from config import FEATURE_DELIMITER
from config import NULL_OCCUPY
from common.Typehelper import strToType

def getStudentData(dataFileName = None):
    # 读入数据文件
    filePath = DATA_ROOT_PATH + dataName;
    if dataFileName is not None:
        filePath = DATA_ROOT_PATH + dataFileName

    _datafile = open(filePath, 'r');

    # 读取头部信息
    _headerLine = _datafile.readline().rstrip('\n');
    headerArray = _headerLine.split(FEATURE_DELIMITER);
    # print(headerArray);

    _headerTypeLine = _datafile.readline().rstrip('\n');
    headerTypeArray = _headerTypeLine.split(FEATURE_DELIMITER);
    # print(headerTypeArray);

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
                    print(record_array[0]);
                    exit(-1);

        _student_data.append(record_array);
    return _student_data;


def getStudentDataWithHeader(dataFileName = None):
    # 读入数据文件
    filePath = DATA_ROOT_PATH + dataName;
    if dataFileName is not None:
        filePath = DATA_ROOT_PATH + dataFileName

    _datafile = open(filePath, 'r');

    # 读取头部信息
    _headerLine = _datafile.readline().rstrip('\n');
    headerArray = _headerLine.split(FEATURE_DELIMITER);

    _headerTypeLine = _datafile.readline().rstrip('\n');
    headerTypeArray = _headerTypeLine.split(FEATURE_DELIMITER);

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
                    print(record_array[0]);
                    exit(-1);

        _student_data.append(record_array);
    return _student_data,headerArray;


