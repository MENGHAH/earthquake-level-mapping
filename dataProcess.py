import xlrd
import operator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from math import*
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata
from geopy.distance import geodesic

col = 100 # 经度的分割数量(全局变量)
row = 100 # 维度的分割数量(全局变量)
R = 50 # 设定的半径,单位是km

# 地图划分范围
gansu_lon_a = 90
gansu_lon_b = 110
gansu_lat_a = 27
gansu_lat_b = 47

# 经度：lon(-180~180); 维度：lat(-90~90)
def getDistance(lonA, latA, lonB, latB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra

    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)

    try:
        pA = atan(rb / ra * tan(radLatA))
        pB = atan(rb / ra * tan(radLatB))
        x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
        c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
        c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (x + dr)
        distance = distance / 1000
        return distance
    except:
        return 0

# 计算每个交点的I值
def calculate_I(fixed_lon, fixed_lat, eligible_data, M):
    res = []
    for data in eligible_data:
        x = data[0] # 经度
        y = data[1] # 维度
        z = data[2] # 当前点的震级
        distance = data[3] # 与固定点的距离
        if distance < exp(1):
            distance = exp(1)
        if M == 0:
            M = 1
        a = z / (M*log(distance))
        res.append(a)
    I = np.sum(res)
    return I

def get_all_I(filename):
    counter = 0
    all_I = []

    # 经纬度切分，保留两位有效数字
    all_lon = np.round(np.linspace(gansu_lon_a, gansu_lon_b, row),2)
    all_lat = np.round(np.linspace(gansu_lat_a, gansu_lat_b, col),2)

    data = xlrd.open_workbook(filename) # 打开excel文件
    table = data.sheets()[0] # 读取第一个sheet
    n_rows = table.nrows # table的行数

    for fixed_lon in all_lon: # 经度
        for fixed_lat in all_lat: # 维度
            eligible_data = []
            magnitude_max = 0 # 先假定最大震级为0
            magnitude_min = 12 # 先假定最小震级为12
            for v in range(1, n_rows): # 循环读取表格中的每行数据
                values = table.row_values(v) # 每一行的数据放在一个列表里面
                x = values[0] # 经度 lon
                y = values[1] # 维度 lat
                z = values[2] # 震级
                distance = getDistance(fixed_lon, fixed_lat, x, y)
                if distance <= R:
                    values.append(distance)
                    eligible_data.append(values) # 把符合条件的数据存储起来
                    if z > magnitude_max:
                        magnitude_max = z
                    if z < magnitude_min:
                        magnitude_min = z
            M = magnitude_max - magnitude_min # 最大最小的震级差
            # I = round(calculate_I(fixed_lat, fixed_lon, eligible_data, M),1) # 保留一位有效数字
            I = int(calculate_I(fixed_lon, fixed_lat, eligible_data, M)) # 对I取整

            print("fixed_lon: ", fixed_lon)
            print("fixed_lat: ", fixed_lat)
            print("I: ", I)

            all_I.append([fixed_lon, fixed_lat, I])
    np.savetxt(r'data_I.txt',all_I, fmt="%.1f") # 把数据保存到txt文档中
    return all_I # (经度，维度，I值)

# 绘制甘肃等值线图并显示
def gansuMap(filename):
    all_I = get_all_I(filename)
    fig = plt.figure(figsize=(5,5)) # 定义画布大小
    m3 = Basemap(llcrnrlon=92.2, llcrnrlat=32.5, urcrnrlon=108.77, urcrnrlat=42.95,
                 projection='lcc', lat_1=33, lat_2=45, lon_0=100)
    m3.readshapefile("./shapefile/gadm36_CHN_shp/gadm36_CHN_3",  'china', drawbounds=True)

    parallels = np.arange(-90., 90., 1) # 纬度，范围为[-90,90]间隔为1
    m3.drawparallels(parallels,labels=[False, True, True, False])
    meridians = np.arange(-180., 180., 1) # 经度，范围为[-180,180]间隔为1
    m3.drawmeridians(meridians,labels=[True, False, False, True])

    X = []
    Y = []
    I = []
    for data in all_I:
        X.append(data[0])
        Y.append(data[1])
        I.append(data[2])
    print("X: ", len(X))
    print("Y: ", len(Y))
    print("I: ", len(I))
    print(I)

    xi = np.round(np.linspace(gansu_lon_a, gansu_lon_b, row),2) # 经度
    yi = np.round(np.linspace(gansu_lat_a, gansu_lat_b, col),2) # 维度

    # 使用griddata函数来将离散的数据格点插值到固定网格上[xi,yi]
    # 这里插值函数设置值为'linear'为线性插值,还有“nearest”和“cubic”
    # zi = matplotlib.mlab.griddata(np.array(X), np.array(Y), np.array(I),
    #                               xi, yi, interp='linear')
    zi = griddata((X, Y), I, (xi[None,:], yi[:,None]), method='nearest')
    x1, y1 = m3(*(xi, yi))
    # 网格化经纬度网格：调用meshgrid函数来生成后面需要的网格化的数据格点xx,yy
    xx, yy = np.meshgrid(x1, y1)
    # 绘图等值线:contour
    m3.contour(xx, yy, zi)
    plt.show()

if __name__ == '__main__':
    filename = "./Data/data_4.xlsx"
    gansuMap(filename)
