#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'liuxiangfeng'

from dao import *
from dealer_filter import *
from excel_read import *
from excel_write import *
from polyfit import *
from arti_rates_filter import *

if __name__ == '__main__':
    rates = [np.insert(range(0, 21), 0, -1)]
    new_price = excel_table_byindex('data/new_price.xlsx', 0, 1)
    good_dealer = file_read('data/vip_id')
    series_data = excel_table_byindex('data/series.xlsx', 0, 1)
    local_data = excel_table_byindex('data/local.xls', 0, 2)
    arti_rates = excel_dict('data/ar.xlsx')
    # car_data = excel_table('data/car_data.xlsx')
    province_dict = {}
    all_city = []
    for cid in local_data.keys():
        pid = local_data.get(cid)
        if pid != 0:
            all_city.append(cid)
        if pid in province_dict.keys():
            city_array = province_dict.get(pid)
            city_array.append(cid)
            province_dict[pid] = city_array
        else:
            city_array = [cid]
            province_dict[pid] = city_array

    limit = 100

    for series in series_data:
        series_id = str(series)

        # 根据该车系全国样本生成保值率
        all_data = getSeries(series_id, all_city)
        all_dealer_data = dealer_filter(all_data, good_dealer, new_price)
        all_dealer_data_origin = all_dealer_data
        if len(all_dealer_data) > 0 and series in arti_rates.keys():
            all_dealer_data = arti_rates_filter(all_dealer_data, arti_rates[series])
        else:
            continue
        all_rate_result = build_rate(series_id, all_dealer_data, all_dealer_data_origin)
        rates.append(np.insert(np.insert(np.insert(all_rate_result, 0, 0), 0, series_id), 0, len(all_dealer_data)))

        # 区分城市生成保值率
        for province_id in province_dict.get(0):
            data = getSeries(series_id, province_dict.get(province_id))
            series_name = series_id + '_' + str(province_id)
            dealer_data = []

            if len(data) < limit:
                print series_name, ' data count: ', len(data)
                continue
            else:
                dealer_data = dealer_filter(data, good_dealer, new_price)
            # print 'dealer_data: ', dealer_data
            # clean_data = lof.outliers(1, dealer_data)
            # print 'clean_data: ', clean_data

            dealer_data_origin = dealer_data
            if len(dealer_data) > 0 and series in arti_rates.keys():
                dealer_data = arti_rates_filter(dealer_data, arti_rates[series])

            # 本城市不够但全国数据量够，不生成本城市
            if len(dealer_data) < limit < len(all_dealer_data):
                print series_name, ' dealer_data count:', len(dealer_data)
                continue

            # 最终参与计算的样本太少则不生成保值率
            if len(dealer_data) < limit / 2:
                print series_name, ' dealer_data count not enough:', len(dealer_data)
                continue

            # rate_result = []
            # if len(dealer_data) == len(all_dealer_data):
            #     rate_result = all_rate_result
            #     province_id = - province_id
            # else:


            # 生成保值率
            rate_result = build_rate(series_name, dealer_data, dealer_data_origin)

            # 无法生成保值率的不保存
            if len(rate_result) <= 0:
                print series_name, ' has no result'
                continue

            # 根据样本数据量给定样本等级
            level = len(dealer_data)
            # if len(dealer_data) > limit * 2:
            #     level = 3
            # elif len(dealer_data) > limit:
            #     level = 2
            # else:
            #     level = 1

            rates.append(np.insert(np.insert(np.insert(rate_result, 0, province_id), 0, series_id), 0, level))

    # 保存数据
    wexcel(rates, 'result/rates.xls')
