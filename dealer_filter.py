#!/usr/bin/python
# -*- coding: utf-8 -*-
import decimal

__author__ = 'liuxiangfeng'

# 读取文本文件
def file_read(src_file):
    result = []
    file_object = open(src_file, "r")
    try:
        for line in file_object.readlines():
            result.append(long(line.split('\n')[0]))
    finally:
        file_object.close()

    return result

# 诚信车商过滤器
def dealer_filter(data, good_dealer, newprices):
    clean_data = []
    for row in data:
        dealerid = row[2]
        if dealerid in good_dealer:
            modelid = row[3]
            ages = row[0]
            if 0 < ages < 20:
                try:
                    newprice = newprices[modelid]
                    if newprice and row[0] > 0:
                        rate = row[1] / decimal.Decimal(newprice)
                        if 0 < rate < 1:
                            row = list(row)
                            row[1] = rate
                            clean_data.append(row)
                except:
                    print 'no new price: ', modelid
    return clean_data
