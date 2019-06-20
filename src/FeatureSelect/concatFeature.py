import os
from Dao import load_data_from_file
from common.FileHelper import checkThenMkdirs
from config import OUT_ROOT_PATH
from config import DATA_ROOT_PATH
from config import NULL_OCCUPY

def concatFeature(file_name_array,feature_name_array,mark):
    data_map = {};

    feature_type_map = {};

    for file_name in file_name_array:
        target_source = os.path.join(mark,file_name);
        student_data,headerarray,headerTypeArray = load_data_from_file(target_source,needType=True);

        for index,featureName in enumerate(headerarray):
            if featureName in feature_name_array :
                feature_type_map[featureName] = headerTypeArray[index];

                for student_record in student_data :
                    uid = int(student_record[0]);
                    if uid not in data_map :
                        data_map[uid] = {};

                    data_map[uid][featureName] = student_record[index];


    records = data_map.items();
    sorted(records);

    parentPath = DATA_ROOT_PATH + "/" + mark + "/";
    checkThenMkdirs(parentPath);
    output_filePath = parentPath + "concatfeature";

    output_file = open(output_filePath,"w");

    output_file.write("uId");
    for featureName in feature_name_array :
        output_file.write(",");
        output_file.write(featureName);
    output_file.write("\n")

    output_file.write("String");
    for featureName in feature_name_array :
        output_file.write(",");
        output_file.write(feature_type_map[featureName]);
    output_file.write("\n")

    for uid,valueMap in records :
        if valueMap.__len__() == feature_name_array.__len__():
            output_file.write(str(uid));
            for featureName in feature_name_array:
                output_file.write(",");
                output_file.write(str(valueMap[featureName]));
            output_file.write("\n")

    output_file.close();


def concatAllFeature(file_name_array,mark):
    data_map = {};

    feature_name_array = [];
    feature_type_map = {};
    ignore_feature_array = ["finalTestScore","buildCount","useDebug","longDeleteCount","hasBuildError",
                            "debugCount","pasteCount","totalLength"];
    feature_count = 0;
    for file_name in file_name_array:
        target_source = os.path.join(mark,file_name);
        student_data,headerarray,headerTypeArray = load_data_from_file(target_source,needType=True);

        for _header_index in range(1,headerarray.__len__()):
            if headerarray[_header_index] not in ignore_feature_array:
                feature_name_array.append(headerarray[_header_index]);

        for index,featureName in enumerate(headerarray):
            if featureName in feature_name_array :
                feature_count +=1;
                feature_type_map[featureName] = headerTypeArray[index];
                for student_record in student_data :
                    uid = int(student_record[0]);
                    if uid not in data_map :
                        data_map[uid] = {};
                        for _ocuppy_featureName in feature_name_array:
                            data_map[uid][_ocuppy_featureName] = NULL_OCCUPY;
                    data_map[uid][featureName] = student_record[index];

                for uid in data_map:
                    if data_map[uid].__len__() < feature_count:
                        data_map[uid][featureName] = NULL_OCCUPY;


    records = data_map.items();
    sorted(records);

    parentPath = DATA_ROOT_PATH + "/" + mark + "/";
    checkThenMkdirs(parentPath);
    output_filePath = parentPath + "concatfeature";

    output_file = open(output_filePath,"w");

    output_file.write("uId");
    for featureName in feature_name_array :
        output_file.write(",");
        output_file.write(featureName);
    output_file.write("\n")

    output_file.write("String");
    for featureName in feature_name_array :
        output_file.write(",");
        output_file.write(feature_type_map[featureName]);
    output_file.write("\n")

    for uid,valueMap in records :
        if valueMap.__len__() == feature_name_array.__len__():
            output_file.write(str(uid));
            for featureName in feature_name_array:
                output_file.write(",");
                output_file.write(str(valueMap[featureName]));
            output_file.write("\n")

    output_file.close();



if __name__ == "__main__":
    mark_array = ["exam1", "exam2", "exam3", "exam4"];
    file_array = ["saveRecord-t2","BuildTime","buildResultCount-t2","codeCount-15-t2",
                  "debugCount-t2","scoreCount-t2","scoreTendency-t2","deleteRecord-t2",
                  "pasteCount-t2"];


    # # #  pearson
    # feature_name_array = ["firstCodeTimeFromStart","buildInterval","codeTime","saveCount","saveInterval",
    #                       "codeBS","successCount","testRemainZero", "testRemainMiddle","testUp",
    #                      "score", "programTime"]



    # # 按照百分之20 划百分比，,spearman
    # feature_name_array = ["firstCodeTimeFromStart","codeTime","saveCount","saveInterval","successCount",
    #                       "testRemainZero", "testRemainMiddle","testUp","testDown","testCount",
    #                       "score","programTime",]

    # #按照百分之20划百分比，分析编程过程特征,基于MIC的方式度量特征
    # feature_name_array = ["firstCodeTimeFromStart","codeIntervalCount","saveCount","saveInterval","codeTime",
    #                       "buildInterval", "debugTime","debugErrorCount","testRemainZero","score",
    #                       "programTime",]

    #按照百分之20划分 采用贪婪的方式得到的结果
    # feature_name_array =["saveInterval", "programTime", "totalLength", "pasteCount",
    #                   "codeIntervalCount","saveCount","buildInterval",
    #                   "score","codeTime","successCount","testCount",
    #                 "scoreRemainMiddle","avgRemoveErrorTime",
    #                 ];"pasteCount",
    feature_name_array = ["saveInterval", "programTime","totalLength",
                          "codeIntervalCount", "saveCount", "buildInterval",
                          "score", "codeTime", "successCount", "testCount",
                          "testRemainMiddle", "avgRemoveErrorTime",
                          ];

    # #按照百分之20划分 采用基于随机森林的REF方式得到的结果
    # feature_name_array = [  "saveCount", "saveInterval", "codeBU", "codeBS", "programTime",
    #                         "buildInterval", "successCount", "codeTime", "codeIntervalCount", "firstCodeTimeFromStart",
    #                         "debugTime", "testCount", "longDeleteCount", "pasteCount", "totalLength",]

    for mark in mark_array:
        print(mark)
        concatFeature(file_array,feature_name_array, mark);
        # concatAllFeature(file_array,mark)
        print()