#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json

FILE_NAME = "data/information.json"

if __name__ == '__main__':
    num = 3
    mall = []
    ma = []
    mb = []
    td = []
    p = []
    c = []

    all = []

    mall.append([0, 3, 10, 42])
    mall.append([1, 22, 5, 39])
    mall.append([2, 10, 5, 60])
    mall.append([3, 17, 14, 37])
    mall.append([4, 4, 24, 44])
    mall.append([5, 14, 24, 53])
    mall.append([6, 6, 13, 51])
    mall.append([7, 27, 20, 46])
    mall.append([8, 13, 20, 56])

    ma.append([[0, 3, 10, 42], [1, 22, 5, 39]])
    ma.append([[3, 17, 14, 37], [4, 4, 24, 44]])
    ma.append([[6, 6, 13, 51], [7, 27, 20, 46]])

    mb.append([[2, 10, 5, 60]])
    mb.append([[5, 14, 24, 53]])
    mb.append([[8, 13, 20, 56]])

    td.append([{"point": 10, "put": [0], "get": [2]}, {"point": 5, "put": [1, 2]}])
    td.append([{"point": 14, "put": [3], "get": [5]}, {"point": 24, "put": [4, 5]}])
    td.append([{"point": 13, "put": [6], "get": [8]}, {"point": 20, "put": [7, 8]}])

    for i in range(num):
        p.append([118958877.0, 32114745.0])
        c.append(0.0)

    all.append(num)
    all.append(mall)
    all.append(ma)
    all.append(mb)
    all.append(td)
    all.append(p)
    all.append(c)

    f = open(FILE_NAME, "w")
    json.dump(all, f)
    f.close()