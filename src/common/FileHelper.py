import os

def checkThenMkdirs(targetFolderPath):
    # 去除首位空格
    realFolderPath = targetFolderPath.strip()
    isExists = os.path.exists(realFolderPath);
    if not isExists:
        os.makedirs(realFolderPath);

