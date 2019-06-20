import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from minepy import MINE

# # 从硬盘读取数据进入内存
# wine = pd.read_csv("C:\\Users\\yuegu\\Desktop\\wine.csv")
#
# mine = MINE(alpha=0.6, c=15)
# data_wine_mic = MIC_matirx(wine, mine)

def MIC_matirx(dataframe, mine):

    data = np.array(dataframe)
    n = len(data[0, :])
    result = np.zeros([n, n])

    for i in range(n):
        for j in range(n):
            mine.compute_score(data[:, i], data[:, j])
            result[i, j] = mine.mic()
            result[j, i] = mine.mic()
    RT = pd.DataFrame(result)
    return RT


import seaborn as sns
def ShowHeatMap(DataFrame):
    import matplotlib.pyplot as plt
    import seaborn as sns
    colormap = plt.cm.RdBu
    plt.figure(figsize=(14,12))
    plt.title('MIC of Features', y=1.05, size=15)
    sns.heatmap(DataFrame.astype(float),linewidths=0.1,vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)
    plt.show()
# ShowHeatMap(data_wine_mic)


np.random.seed(42)

size = 750
X = np.random.uniform(0, 1, (size, 14))

#"Friedamn #1” regression problem
Y = (10 * np.sin(np.pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - .5)**2 +
     10 * X[:, 3] + 5 * X[:, 4] + np.random.normal(0, 1))
#Add 3 additional correlated variables (correlated with X1-X3)
X[:, 10:14] = X[:, 0:4] + np.random.normal(0, .025, (size, 4))

names = ["x%s" % i for i in range(1, 15)]

# X[:,14] = Y;

# 构建生成DF数据集
Friedman_regression_data = pd.DataFrame(X)
Friedman_regression_data['y'] = Y

# 获取MIC矩阵
mine = MINE(alpha=0.6, c=15)
data_wine_mic = MIC_matirx(Friedman_regression_data, mine)
# 进行结果可视化
ShowHeatMap(data_wine_mic)

# mine = MINE(alpha=0.6, c=15)
# for _index in range(14):
#     mine.compute_score(Friedman_regression_data[_index],Y);
#     print(_index,mine.mic());