from config import OUT_ROOT_PATH
from config import DATA_MARK
from common.DataHelper import getOneColumn
from common.FileHelper import checkThenMkdirs
from common.DataHelper import getTargetColumnIndex
from common.MathHelper import normizeDataSet, getMaxAndMin
from Dao import load_data_from_file
import matplotlib.pyplot as plot
import os

_BOX_COUNT = 20;
def drawDataDistribution(dataFileName,data_mark = None):
    if data_mark is None:
        data_mark = DATA_MARK;
    _fileName = os.path.join(data_mark, dataFileName);
    student_data,headerArray = load_data_from_file(_fileName);

    featureCount = headerArray.__len__() - 1;
    for colomnIndex in range(1, featureCount+1):
        data = getOneColumn(student_data, colomnIndex);
        max,min = getMaxAndMin(data)
        boxWidth = (max - min)/_BOX_COUNT;

        x_tags = [];
        rightBorders = [];
        _left=_right = min;
        for _index in range(0,_BOX_COUNT):
            _left = _right;
            _right += boxWidth;
            rightBorders.append(_right);
            x_tags.append("[%.2f,%.2f)"%(_left,_right));

        x_counts = [0]*_BOX_COUNT;

        for _value in data:
            for _index,_border in enumerate(rightBorders):
                if _value <= _border :
                    x_counts[_index] +=1;
                    break;

        #将未分类的归到最后一类去
        unTagCount = data.__len__();
        for _value in x_counts:
            unTagCount -= _value;
        x_counts[_BOX_COUNT-1] += unTagCount;

        xIndex = range(_BOX_COUNT);
        plot.bar(xIndex,x_counts);
        plot.xticks(xIndex,x_tags,rotation=10,fontsize=8);
        for _a,_b in zip(xIndex,x_counts):
            plot.text(_a,_b+0.05,str(_b),ha='center', va= 'bottom');

        title = headerArray[colomnIndex]
        plot.title(title);
        parentPath = OUT_ROOT_PATH +"/"+data_mark + "/distribution/";
        checkThenMkdirs(parentPath);
        plot.savefig(parentPath + title);
        plot.clf();

def checkCodeTime():
    for data_mark in ["exam1","exam2","exam3","exam4"] :
        _fileName = os.path.join(data_mark, "codeCount-15-t2");
        student_data,headerArray = load_data_from_file(_fileName);

        print(data_mark)
        for _line in student_data:
            if _line[3] <= 300:
                print(_line[0]);

        print()


if __name__ == "__main__":
    # mark_array = ["exam1","exam2","exam3","exam4"];
    # file_array = ["saveRecord-t2","BuildTime","buildResultCount-t2","codeCount-15-t2",
    #               "debugCount-t2","scoreCount-t2","scoreTendency-t2"];
    #
    # for mark in mark_array:
    #     for fileName in file_array:
    #         drawDataDistribution(fileName,mark);

    checkCodeTime();