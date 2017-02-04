#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'liuxiangfeng'

import MySQLdb

# 获取数据库数据
def getSeries(series_id, citys):
    # series_id = '410426'
    # citys = [-1]
    # 打开数据库连接
    db = MySQLdb.connect("127.0.0.1", "root", "mysql", "dbwww58com_carsample_2016")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    database = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    sql = ''
    for i in database:
        sql += "SELECT DATEDIFF(publish_dt,license_dt) / 365, sale_price, dealer_id, modelid FROM `t_car_sample_" + i + "`" \
               " WHERE NOT ISNULL(license_dt) AND sale_price > 0 AND modelid > 0 " \
               " AND seriesid = " + series_id + \
               " AND city in ("
        n = 0
        for city in citys:
            if n != 0:
                sql += ","
            sql += str(-city)
            n += 1

        sql += ") "
        if i != database[-1]:
            sql += ' UNION '

    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    # wexcel(results, 'result/test.xls')
    return results
