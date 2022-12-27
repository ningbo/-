# coding : utf-8
import pandas as pd
import json
import warnings
import time


warnings.simplefilter('ignore')

def 主逻辑():
    时间进度 = 1
    w = time.strftime("%W", time.localtime())
    时间进度 = float(w) / 52.14

    def 钱赋值(数据):
        for idx in range(31):
            看板.iloc[2 + idx:3 + idx, 2:3] = 数据[idx]
            看板.iloc[2 + idx:3 + idx, 3:4] = 数据[idx] / 看板.iloc[2 + idx:3 + idx, 1:2]
            看板.iloc[2 + idx:3 + idx, 4:5] = 数据[idx] - 时间进度 * 看板.iloc[2 + idx:3 + idx, 1:2]

    def 高品质商品房赋值(数据):
        for idx in range(31):
            看板.iloc[2 + idx:3 + idx, 6:7] = 数据[idx]
            看板.iloc[2 + idx:3 + idx, 7:8] = 数据[idx] / 看板.iloc[2 + idx:3 + idx, 5:6]
            看板.iloc[2 + idx:3 + idx, 8:9] = 数据[idx] - 时间进度 * 看板.iloc[2 + idx:3 + idx, 5:6]

    def 总商品房赋值(数据):
        for idx in range(31):
            看板.iloc[2 + idx:3 + idx, 10:11] = 数据[idx]
            看板.iloc[2 + idx:3 + idx, 11:12] = 数据[idx] / 看板.iloc[2 + idx:3 + idx, 9:10]
            看板.iloc[2 + idx:3 + idx, 12:13] = 数据[idx] - 时间进度 * 看板.iloc[2 + idx:3 + idx, 9:10]

    def 双域专网赋值(数据):
        for idx in range(30):
            看板.iloc[2 + idx:3 + idx, 14:15] = 数据[idx]
            看板.iloc[2 + idx:3 + idx, 15:16] = 数据[idx] / 看板.iloc[2 + idx:3 + idx, 13:14]
            看板.iloc[2 + idx:3 + idx, 16:17] = 数据[idx] - 时间进度 * 看板.iloc[2 + idx:3 + idx, 13:14]

    看板 = pd.read_excel('./excel/model/指标看板.xlsx')
    with open("./excel/json/data.json") as f:
        result = json.load(f)

    钱 = []
    高品质商品房 = []
    总商品房 = []
    双域专网 = []
    for 省数据 in result:
        钱.append(省数据['value'])
        总商品房.append(省数据['value2'])
        高品质商品房.append(省数据['value3'])
        双域专网.append(省数据['value4'])

    钱赋值(钱)
    高品质商品房赋值(高品质商品房)
    总商品房赋值(总商品房)
    双域专网赋值(双域专网)

    看板.to_excel('./excel/model/指标看板_result.xlsx', engine='xlsxwriter', index=False)

    print('看板结束')
