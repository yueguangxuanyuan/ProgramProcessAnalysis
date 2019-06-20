from watwin.datapre import getStudentData

_student_data = getStudentData();

#采用撒点图展示
import numpy as np
import matplotlib.pyplot as plt

from common.DataHelper import  getOneColumn

def showWatwinAndScore():
    x = np.arange(1,_student_data.__len__()+1);
    y1 = getOneColumn(_student_data,1);
    y2 = getOneColumn(_student_data,2);

    # for i in range(len(y2)):
    #     y2[i] = 10*(1-y2[i]);

    fig = plt.figure();

    #设置标题
    #fig.set_title('Scatter Plot')
    #设置X轴标签
    #plt.xlabel('X')
    #设置Y轴标签
    #plt.ylabel('Y')
    #画散点图
    plt.scatter(x,y1,c='r',marker='x');
    plt.scatter(x,y2,color='c',marker='+');

    #显示所画的图
    plt.show();

if __name__ == "__main__" :
    showWatwinAndScore();