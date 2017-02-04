#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'liuxiangfeng'

# 通过人工设定的下限过滤低值样本
def arti_rates_filter(results, arti_rate):
    filter_results = []
    if len(arti_rate) > 0:
        for result in results:
            rate = result[1]
            age = float(result[0])
            age_int = int(age)
            if 0 < age_int < 15:
                age_decimal = age - age_int
                rate1 = arti_rate[age_int]
                rate2 = arti_rate[age_int+1]
                rate_diff = rate1 - rate2
                rate_add = rate_diff * age_decimal
                rate_ref = rate1 - rate_add
                if rate > rate_ref:
                    filter_results.append(result)
    if len(filter_results) < 0:
        return results
    return filter_results