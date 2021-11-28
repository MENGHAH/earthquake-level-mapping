# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from matplotlib.mlab import griddata
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from scipy.interpolate import griddata as gd

# 设置基本图片画板
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, axisbg='w', frame_on=False)

# 提取数据
data = pd.read_csv('data_I.txt', delim_whitespace=True)
norm = Normalize()

#设置地图边界值
lllon = 21
lllat = -18
urlon = 34
urlat = -8

#初始化地图
m = Basemap(
    projection = 'merc',
    llcrnrlon = lllon, llcrnrlat = lllat, urcrnrlon = urlon, urcrnrlat = urlat,
    resolution='h')

# 将经纬度点转换为地图映射点
data['projected_lon'], data['projected_lat'] = m(*(data.Lon.values, data.Lat.values))

# 生成经纬度的栅格数据
numcols, numrows = 2, 2
xi = np.linspace(data['projected_lon'].min(), data['projected_lon'].max(), numcols)
yi = np.linspace(data['projected_lat'].min(), data['projected_lat'].max(), numrows)

print("xi", xi)
print('yi', yi)
xi, yi = np.meshgrid(xi, yi)

print("meshgrid_xi: ", xi)
print("meshgrid_yi: ", yi)


# 插值
x, y, z = data['projected_lon'].values, data['projected_lat'].values, data.Z.values

print("x: ", x)
print("y: ", y)
print("z: ", z)
zi = gd(
    (data[['projected_lon', 'projected_lat']]),
    data.Z.values,
    (xi, yi),
    method='cubic')

print("zi: ", zi)

assert 1>2

# 设置地图细节
m.drawmapboundary(fill_color = 'white')
m.fillcontinents(color='#C0C0C0', lake_color='#7093DB')
m.drawcountries(
    linewidth=.75, linestyle='solid', color='#000073',
    antialiased=True,
    ax=ax, zorder=3)

m.drawparallels(
    np.arange(lllat, urlat, 2.),
    color = 'black', linewidth = 0.5,
    labels=[True, False, False, False])
m.drawmeridians(
    np.arange(lllon, urlon, 2.),
    color = '0.25', linewidth = 0.5,
    labels=[False, False, False, True])

# 等值面图绘制
con = m.contourf(xi, yi, zi, zorder=4, alpha=0.6, cmap='jet')
# 插入测绘点
m.scatter(
    data['projected_lon'],
    data['projected_lat'],
    color='#545454',
    edgecolor='#ffffff',
    alpha=.75,
    s=50 * norm(data['Z']),
    cmap='jet',
    ax=ax,
    vmin=zi.min(), vmax=zi.max(), zorder=4)

# 插入色标、名称和范围
cbar = plt.colorbar(con,orientation='horizontal', fraction=.057, pad=0.05)
cbar.set_label("Mean Rainfall - mm")

m.drawmapscale(
    24., -9., 28., -13,
    100,
    units='km', fontsize=10,
    yoffset=None,
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#000000',
    fontcolor='#000000',
    zorder=5)

plt.title("Mean Rainfall")
plt.savefig("rainfall.png", format="png", dpi=300, transparent=True)
plt.show()