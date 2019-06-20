import numpy as np
from sklearn.cluster import KMeans

from Dao import getDataAndScore
from common.DataHelper import getOneColumn

current_feature = None;
score_map = {
    "saveInterval":{0:0,1:0,2:0,3:1,4:1},
    "score":{0:0,1:0,2:1,3:1,4:2},
    "scoreRemainMiddle": {0: 0, 1: 0, 2: 0, 3: 0, 4: 1},
};

def useKMeansToPredict(featureFileName,exam_mark=None):
    featureMatrix, scoreCol,headerArray= getDataAndScore(featureFileName,exam_mark,needHeader=True);
    precision_array = [];
    clusterMap = {"saveInterval":2,"score":3,"scoreRemainMiddle":2}
    for _index in range(0,headerArray.__len__()):
        if headerArray[_index] in clusterMap :
            clf = KMeans(n_clusters=clusterMap[headerArray[_index]]);
            dataArray = getOneColumn(featureMatrix,_index);
            dataArray = np.array(dataArray).reshape(dataArray.__len__(),1);

            clf.fit(dataArray);
            #构建预测模型
            center_array = clf.cluster_centers_
            label_map = {} ;
            for centerIndex,center in enumerate(center_array):
                label_map[centerIndex] = center[0];

            center_array =center_array.reshape(center_array.__len__());
            center_array = sorted(center_array.tolist());
            for label in label_map :
                label_map[label] = center_array.index(label_map[label]);

            #预测
            grade_predict_array = clf.predict(dataArray);

            #判断准确率
            current_score_map = score_map[headerArray[_index]];
            t_t = 0;
            t_f = 0;
            f_t = 0;
            f_f = 0;
            for record_index in range(grade_predict_array.__len__()):
                grade_predict = label_map[grade_predict_array[record_index]];
                true_grade = current_score_map[scoreCol[record_index]];

                if true_grade == 1 and grade_predict ==1 :
                    t_t += 1;
                if true_grade == 1 and grade_predict ==0 :
                    t_f += 1;
                if true_grade == 0 and grade_predict == 1:
                    f_t += 1;
                if true_grade == 0 and grade_predict == 0:
                    f_f += 1;

            print( headerArray[_index] , " : ",t_t,t_f,f_t,f_f);

    # print(precision_array);

if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    for mark in mark_array:
        print(mark)
        useKMeansToPredict("concatFeature",mark);