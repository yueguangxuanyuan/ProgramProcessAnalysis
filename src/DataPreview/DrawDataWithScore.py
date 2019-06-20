from config import OUT_ROOT_PATH
from config import DATA_MARK
from common.DataHelper import getOneColumn
from common.FileHelper import checkThenMkdirs
from common.MathHelper import normizeDataSet
from Dao import get_final_score_map
from Dao import load_data_from_file
import matplotlib.pyplot as plot
import os
import numpy as np

def drawDataWithScorePic(dataFileName,needNorminize = False,out_mark = None) :
    '''
    画出特征的一元分布图
    :param needNormize:
    :return:
    '''
    _fileName = os.path.join(DATA_MARK,dataFileName);

    student_data,headerArray = load_data_from_file(_fileName);

    _score_map = get_final_score_map(None);

    _score_array = [];
    for _student_record in student_data:
        _score_array.append(_score_map[_student_record[0]]);

    if needNorminize :
        _score_array = normizeDataSet(_score_array);

    #遍历所有的特征
    for colomnIndex in range(1, headerArray.__len__()):
        data = getOneColumn(student_data, colomnIndex);

        # if headerArray[colomnIndex] == "avgRemoveErrorTime":
        #     for index in range(data.__len__()):
        #         if data[index] > 300:
        #             data[index] = 300;

        if (needNorminize):
            data = normizeDataSet(dataSetA=data);

        plot.scatter(_score_array, data ,s=2);
        title = headerArray[colomnIndex]+"-score";
        if(needNorminize):
            title += "-nominized";
        plot.title(title);
        plot.xlabel("score");
        plot.ylabel(headerArray[colomnIndex]);

        parentPath = OUT_ROOT_PATH +"/"+ DATA_MARK +"/scatterWithScore/";
        checkThenMkdirs(parentPath);
        if out_mark is not None:
            title += "-"+out_mark;
        plot.savefig(parentPath+ title);
        plot.clf();

def drawDataWithScorePicSpecific(dataFileName,needNorminize = False,out_mark = None) :
    '''
    画出特征的一元分布图
    :param needNormize:
    :return:
    '''
    _fileName = os.path.join(DATA_MARK,dataFileName);

    student_data,headerArray = load_data_from_file(_fileName);

    _score_map = get_final_score_map(None);

    _score_array = [];
    for _student_record in student_data:
        _score_array.append(_score_map[_student_record[0]]);

    if needNorminize :
        _score_array = normizeDataSet(_score_array);

    #遍历所有的特征
    for colomnIndex in range(1, headerArray.__len__()):
        if headerArray[colomnIndex] == "codeIntervalCount":
            data = getOneColumn(student_data, colomnIndex);

            data = np.array(data);
            data = data - data.mean();
            data = data.__abs__()

            plot.scatter(_score_array, data ,s=2);
            # title = "dev-"+headerArray[colomnIndex]+"-score";
            title = headerArray[colomnIndex]+"-score";
            if(needNorminize):
                title += "-nominized";
            plot.title(title);
            plot.xlabel("score");
            plot.ylabel(headerArray[colomnIndex]);

            parentPath = OUT_ROOT_PATH +"/"+ DATA_MARK +"/scatterWithScore/";
            checkThenMkdirs(parentPath);
            if out_mark is not None:
                title += "-"+out_mark;
            plot.savefig(parentPath+ title);
            plot.clf();

if __name__ == '__main__' :
    # codeCount
    # gapArray = [10,15,30,60,120];
    # # gapArray = [60];
    # for gap in gapArray:
    #     # drawDataWithScorePic("codeCount-"+str(gap)+"-t2",out_mark=str(gap));
    #     drawDataWithScorePicSpecific("codeCount-"+str(gap)+"-t2",out_mark=str(gap));

    # drawDataWithScorePic("saveRecord-t2");
    # drawDataWithScorePic("debugCount-t2");
    # drawDataWithScorePic("scoreTendency-t2");

    # drawDataWithScorePic("scoreCount-t2");
    drawDataWithScorePic("buildResultCount-t2");
    drawDataWithScorePic("BuildTime");
    # drawDataWithScorePic("debugCount-t2");
    # drawDataWithScorePic("pasteCount-t2")
    # drawDataWithScorePic("deleteRecord-t2")

    # drawDataWithScorePicSpecific("codeCount-"+str(5)+"-t2",out_mark=str(5));
