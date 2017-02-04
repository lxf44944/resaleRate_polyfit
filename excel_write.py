#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'liuxiangfeng'

import xlwt

# 写入excel
def wexcel(data, outEfile):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('clean_result')

    for i, row in enumerate(data):
        for j, e in enumerate(row):
            sheet1.write(i, j, e)

    book.save(outEfile)
