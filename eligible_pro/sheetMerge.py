#第一步：调用pandas包
import pandas as pd
#第二步：读取数据
iris = pd.read_excel('./Data/data_4.xlsx',None)#读入数据文件
keys = list(iris.keys())
#第三步：数据合并
iris_concat = pd.DataFrame()
for i in keys:
    iris1 = iris[i]
    iris_concat = pd.concat([iris_concat,iris1])
iris_concat.to_excel('./Data/data_all.xlsx')#数据保存路径
