#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'liuxiangfeng'

from pylab import *
import warnings

# 拟合曲线
def build_rate(seriesname, clean_data, dealer_data_origin):
    # 获取数据
    if len(clean_data) <= 0:
        return []
    data = np.array(clean_data, dtype=float)
    data_t = data.T
    ages = data_t[0]
    rates = data_t[1]

    data_origin = np.array(dealer_data_origin, dtype=float)
    data_t_origin = data_origin.T
    ages_origin = data_t_origin[0]
    rates_origin = data_t_origin[1]

    ages_min = int(math.floor(min(ages)))
    ages_max = int(math.ceil(max(ages)))

    # 生成保值率曲线
    x = range(ages_min, ages_max)
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            y = polyfit(ages, rates, 3)
        except np.RankWarning:
            print seriesname + "not enought data"
            return []
    z = polyval(y, x)
    plot(x, z, 'y')

    # 输出结果
    disp(z)

    # 校验结果(get the longest part line)
    z_min = 0
    z_max = len(z) - 1
    d_value = [False]
    for i in range(0, len(z) - 1):
        d_value.append(z[i + 1] < z[i])
    d_value.append(False)
    print d_value
    index = 0
    count = 0
    count_dict = {}
    while index < len(d_value):
        if d_value[index]:
            count += 1
        else:
            if d_value[index - 1]:
                count_dict[count] = index - count
                count = 0
        index += 1
    print count_dict

    if len(count_dict) > 0:
        count_array = count_dict.keys()
        count_max = np.max(count_array)
        count_index = count_dict[count_max]
        print '------------------------------------------'
        print count_index, '-', count_max
        z_min = count_index - 1
        z_max = z_min + count_max + 1
        print z[z_min:z_max]
        print '------------------------------------------'

    # 绘制样本点&图例标注
    scatter(ages_origin, rates_origin, c='g')
    scatter(ages, rates)
    plot(x[z_min:z_max], z[z_min:z_max], 'r')
    title(seriesname)
    xlabel('ages')
    ylabel('rate')

    # 保存数据
    savefig("img/" + seriesname + '.png')
    close()

    return np.append(zeros(ages_min + z_min), z[z_min:z_max])
