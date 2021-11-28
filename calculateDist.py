from math import*

def readData(file_path):
    for line in open(file_path):
        print(line)

def calculateDist(Lat_A,Lng_A,Lat_B,Lng_B):
    ra=6378.140 # 赤道半径
    rb=6356.755 # 极半径
    flatten=(ra-rb)/ra # 地球偏率

    rad_lat_A=radians(Lat_A)
    rad_lng_A=radians(Lng_A)
    rad_lat_B=radians(Lat_B)
    rad_lng_B=radians(Lng_B)
    pA=atan(rb/ra*tan(rad_lat_A))
    pB=atan(rb/ra*tan(rad_lat_B))
    xx=acos(sin(pA)*sin(pB)+cos(pA)*cos(pB)*cos(rad_lng_A-rad_lng_B))
    c1=(sin(xx)-xx)*(sin(pA)+sin(pB))**2/cos(xx/2)**2
    c2=(sin(xx)+xx)*(sin(pA)-sin(pB))**2/sin(xx/2)**2
    dr=flatten/8*(c1-c2)
    distance=ra*(xx+dr)
    return distance

if __name__ == '__main__':
    # Lat_A=32.060255; Lng_A=118.796877 # 南京
    # Lat_B=39.904211; Lng_B=116.407395 # 北京
    Lat_A = float(input("请输入第一个坐标的经度"))
    Lng_A = float(input("请输入第一个坐标的维度"))
    Lat_B = float(input("请输入第二个坐标的经度"))
    Lng_A = float(input("请输入第二个坐标的维度"))
    distance=calculateDist(Lat_A,Lng_A,Lat_B,Lng_B)
    print('(Lat_A, Lng_A)=({0:.6f},{1:.6f})'.format(Lat_A,Lng_A))
    print('(Lat_B, Lng_B)=({0:.6f},{1:.6f})'.format(Lat_B,Lng_B))
    print('Distance={0:.3f} km'.format(distance))
