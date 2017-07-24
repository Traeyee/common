#!usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *


def distEclud_1(PntA, PntB):
    return abs(PntA - PntB)


def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)


def randCent(dataSet, k):
    # 获得数据单位的维数，即一维、二维、多维
    n = shape(dataSet)[1]

    # create centroid mat
    # 创建K个数据点
    centroids = array(mat(zeros((k, n))))

    # create random cluster centers, within bounds of each dimension
    for j in range(n):
        # 获得所有第j维的最小值
        minJ = min(dataSet[:, j])
        # 第j维的最大值 - 第j维的最小值
        rangeJ = float(max(dataSet[:, j]) - minJ)
        # 质心集的第j维 = 范围内的随机数
        db = minJ + rangeJ * random.rand(k, 1)
        centroids[:, j] = (minJ + rangeJ * random.rand(k, 1))[:, 0]
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    """

    :param dataSet:
    :param k: 簇数
    :param distMeas: 距离方法
    :param createCent: 创建质心方法
    :return:
    """
    # 默认是二维图

    # 取其第一维数，即简单来说，若数据是一维点则取向量维数，若是二维点则取行数
    # 最后就明白其实取的就是数据的Size
    m = shape(dataSet)[0]

    # create mat to assign data points
    # to a centroid, also holds SE of each point
    # 创造m个二维的数据点
    clusterAssment = mat(zeros((m, 2)))

    # 创建质心--reviewing
    # 这个是自动根据维数创建，是automatic的
    centroids = createCent(dataSet, k)

    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        # for each data point assign it to the closest centroid
        for i in range(m):
            # 对于每个数据

            # inf来自于包
            minDist = inf
            minIndex = -1
            for j in range(k):
                # 对于每个质心（也就是簇数）
                # 计算与质心距离
                db1 = centroids[j, :]
                db2 = dataSet[i, :]
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        # recalculate centroids
        for cent in range(k):
            # get all the point in this cluster
            db = clusterAssment[:, 0]
            db2 = db.A
            db3 = cent
            db4 = (db == db3)
            db5 = nonzero(db4)
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            if 0 == ptsInClust.shape[0]:
                centroids[cent, :] = dataSet[clusterAssment[:, 1].argmax()]
            else:
                # assign centroid to mean
                centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


if __name__ == "__main__":
    # a1 = [1, 2]; a2 = [2, 3]
    # print str(distEclud(array(a1), array(a2)))
    # array2_test = [[1, 2], [2, 3], [3, 1], [78, 0]]
    # ce, cl = kMeans(array(array2_test), 3, distEclud)
    # list_test = [[1], [2], [3], [50], [51], [70], [1000], [1010], [1004]]
    # ce, cl = kMeans(array(list_test), 3, distEclud)
    # list_test = [[1, 1, 1], [0, 0, 0], [11, 11, 11], [2, 3, 3], [7, 8, 9]]
    # ce, cl = kMeans(array(list_test), 3, distEclud)
    # print cl
    pass