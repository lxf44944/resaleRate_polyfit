#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'liuxiangfeng'

import xlrd

# 打开excel文件
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)


# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file, colnameindex, by_index):
    data = open_excel(file)
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    list = {}
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            list[long(row[0])] = row[by_index]
    return list


# 根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_dict(file):
    data = open_excel(file)
    table = data.sheet_by_index(0)
    nrows = table.nrows  # 行数
    list = {}
    for rownum in range(0, nrows):
        row = table.row_values(rownum)
        if row:
            list[row[0]] = row
    return list


def excel_list(file_name):
    data = open_excel(file_name)
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    row_list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            row_list.append(row)
    return row_list


def excel_table_rows_rates(file_name):
    data = open_excel(file_name)
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    row_map = {}
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            row_map[str(int(row[0])) + '_' + str(int(row[1]))] = row[2:]
    return row_map
