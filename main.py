# coding : utf-8
import pandas as pd
import time
import json
import math
import os
import 数据清理模块 as 数据控制
import 全局参数
import 看板模块

总收入全行业排名=0
总项目全行业排名=0
高价值项目全行业排名=0


省合同金额信息={}
省项目数量={}
省50万收入以上项目数量={}
省300万收入以上项目={}
def 分省数据处理(idx, dfall):
    sheng = str(dfall.loc[idx,'省份'])
    if '智慧校园' == str(dfall.loc[idx,'细分行业']):
        if pd.isnull(dfall.loc[idx,'2022年签约合同总金额(万元)']) is not True:
            temp = dfall.loc[idx,'2022年签约合同总金额(万元)']
            #tmd有的项目有多个项目金额，我真是醉了
            if '\n' in str(temp):
                temp = temp.split('\n')[0]
            m = float(temp) if float(temp) > 0 else 0
            省合同金额信息[sheng] = 省合同金额信息.get(sheng, 0) + (m)
            if m > 0:
                省项目数量[sheng] = 省项目数量.get(sheng, 0) + 1
            if m > 50:
                省50万收入以上项目数量[sheng] = 省50万收入以上项目数量.get(sheng, 0) + 1
            if m > 300:
                省300万收入以上项目[sheng] = 省300万收入以上项目.get(sheng, 0) + 1


def 本行业数据(dfall):
    print('行业数据处理')
    行业数据列表 = []
    行业数据模板 = {'行业名称': '', '总项目数': 0, '50万以上项目': 0, '总金额': 0}
    hangyeMoneyList = []
    hangyeProjectList = []
    for hy in 全局参数.行业列表:
        sumMoney = 0.0
        sumProject = 0
        sumAllProject = 0
        for idx in range(dfall.shape[0]):
            hangye = (str(dfall.loc[idx, '细分行业']))
            if hy == hangye:
                分省数据处理(idx, dfall)
                temp = dfall.loc[idx, '2022年签约合同总金额(万元)']
                # tmd有的项目有多个项目金额，我真是醉了
                if '\n' in str(temp):
                    temp = temp.split('\n')[0]
                sumMoney = sumMoney + float(temp if float(temp) > 0 else 0)
                if dfall.loc[idx, '项目属性'] == '省级' and dfall.loc[idx, '2022年签约合同总金额(万元)'] > 50:
                    sumProject = sumProject + 1
                if dfall.loc[idx, '2022年签约合同总金额(万元)'] > 0:
                    sumAllProject = sumAllProject + 1
        # print('{}行业 总项目数{}，50万以上项目有{}个，共{}万元'.format(hy,sumAllProject,sumProject,round(sumMoney)))
        d1 = {'name': hy, 'value': round(sumMoney)}
        d2 = {'name': hy, 'value': sumProject}
        hangyeMoneyList.append(d1)
        hangyeProjectList.append(d2)

        行业数据模板['行业名称'] = hy
        行业数据模板['总项目数'] = sumAllProject
        行业数据模板['50万以上项目'] = sumProject
        行业数据模板['总金额'] = sumMoney
        行业数据列表.append(行业数据模板.copy())

    global 总收入全行业排名
    global 高价值项目全行业排名
    global 总项目全行业排名
    # print('===行业金额排序===')
    t = sorted(行业数据列表, key=lambda x: x['总金额'], reverse=True)
    # print(t)
    for idx in range(len(t)):
        if t[idx]['行业名称'] == '智慧校园':
            总收入全行业排名 = idx + 1
    # print('===行业50万以上项目排序===')
    t = sorted(行业数据列表, key=lambda x: x['50万以上项目'], reverse=True)
    # print(t)
    for idx in range(len(t)):
        if t[idx]['行业名称'] == '智慧校园':
            高价值项目全行业排名 = idx + 1
    # print('===行业总项目数排序===')
    t = sorted(行业数据列表, key=lambda x: x['总项目数'], reverse=True)
    # print(t)
    for idx in range(len(t)):
        if t[idx]['行业名称'] == '智慧校园':
            总项目全行业排名 = idx + 1

    # 输出数据json
    jd = json.dumps(hangyeMoneyList, ensure_ascii=False)
    fileObject = open('./excel/json/hangyeICT.json', 'w')
    fileObject.write(jd)
    fileObject.close()
    jd = json.dumps(hangyeProjectList, ensure_ascii=False)
    fileObject = open('./excel/json/hangyeProject.json', 'w')
    fileObject.write(jd)
    fileObject.close()

def 各行业指标完成情况(dfall):
    print('全行业数据处理')
    行业数据列表=[]
    行业数据模板={'行业名称':'','总项目数':0,'50万以上项目':0,'总金额':0,'专网项目数':0}
    hangyeMoneyList=[]
    hangyeProjectList=[]
    for hy in 全局参数.行业列表:
        sumMoney=0.0
        sumProject=0
        sumAllProject=0
        专网项目数=0
        for idx in range(dfall.shape[0]):
            hangye = (str(dfall.loc[idx,'细分行业']))
            if hy == hangye:
                分省数据处理(idx, dfall)
                temp = dfall.loc[idx,'2022年签约合同总金额(万元)']
                #tmd有的项目有多个项目金额，我真是醉了
                if '\n' in str(temp):
                    temp = temp.split('\n')[0]
                sumMoney = sumMoney + float(temp if float(temp) > 0 else 0)
                if dfall.loc[idx,'项目属性']=='省级' and dfall.loc[idx,'2022年签约合同总金额(万元)'] > 50:
                    sumProject = sumProject + 1
                if dfall.loc[idx,'2022年签约合同总金额(万元)'] > 0:
                    sumAllProject = sumAllProject + 1
                if dfall.loc[idx,'是否为专网项目'] == '是':
                    专网项目数 = 专网项目数+1
        行业数据模板['行业名称']=hy
        行业数据模板['总项目数']=sumAllProject
        行业数据模板['50万以上项目']=sumProject
        行业数据模板['总金额']=sumMoney
        行业数据模板['专网项目数']=专网项目数
        # 行业数据列表.append(行业数据模板.copy())
        for 行业指标 in 全局参数.全行业指标:
            if hy == 行业指标['name']:
                金额完成率 = sumMoney/行业指标['value'][0]
                总项目完成率 = sumAllProject/行业指标['value'][1]
                高品质项目成率 = sumProject/行业指标['value'][2]
                try:
                    专网项目占比 = round(专网项目数/sumAllProject,2)
                except:
                    专网项目占比 = 0
                print('{},目标收入{} 实际{} 完成率{}, 目标总项目{} 实际{} 完成率{},目标50万项目{} 实际{} 完成率{} 专网项目数{} 占比{},'.format(hy,行业指标['value'][0],round(sumMoney,2),round(金额完成率,2),行业指标['value'][1],sumAllProject,round(总项目完成率,2),行业指标['value'][2],sumProject,round(高品质项目成率,2),专网项目数,专网项目占比))


# 把所有的数据转换成 网页可以识别的数据格式
def 保存为json数据(dfall):
    print('数据保存处理')
    year = '2022'
    data = []  # 各省数据
    shiData = []  # 每省各地市数据
    # 初始化
    for sheng in 全局参数.省份列表:
        dataUnit = {'name': sheng, 'value': 0, 'value2': 0, 'value3': 0, 'value4': 0}  # 0是钱，2是高品质数，3是总数，4是双域
        data.append(dataUnit)
    for shi in 全局参数.地市列表:
        dataUnit = {'name': shi, 'value': 0, 'value2': 0, 'value3': 0, 'value4': 0}
        shiData.append(dataUnit)

    for idx in range(dfall.shape[0]):
        hangye = (str(dfall.loc[idx, '细分行业']))
        if '智慧校园' == hangye:
            sheng = dfall.loc[idx, '省份']
            shi = dfall.loc[idx, '地市']

            # 判断是不是双域专网
            if '是' == dfall.loc[idx, '是否2022年5G双域专网项目']:
                for dataUnit in data:  # 处理省的数据
                    if dataUnit['name'] == sheng:
                        dataUnit['value4'] = dataUnit['value4'] + 1
                for dataUnit in shiData:  # 处理市的数据
                    if dataUnit['name'] == shi:
                        dataUnit['value4'] = dataUnit['value4'] + 1

            # 有收入
            if pd.isnull(dfall.loc[idx, '{}年签约合同总金额(万元)'.format(year)]) != True:
                for dataUnit in data:  # 处理省的数据
                    if dataUnit['name'] == sheng:
                        dataUnit['value'] = round(
                            dataUnit['value'] + float(dfall.loc[idx, '{}年签约合同总金额(万元)'.format(year)]), 2)
                        dataUnit['value2'] = dataUnit['value2'] + 1
                        if float(dfall.loc[idx, '{}年签约合同总金额(万元)'.format(year)]) > 50 and '省级' == dfall.loc[idx, '项目属性']:
                            dataUnit['value3'] = dataUnit['value3'] + 1
                for dataUnit in shiData:  # 处理市的数据
                    if dataUnit['name'] == shi:
                        dataUnit['value'] = round(
                            dataUnit['value'] + float(dfall.loc[idx, '{}年签约合同总金额(万元)'.format(year)]), 2)
                        dataUnit['value2'] = dataUnit['value2'] + 1
                        if float(dfall.loc[idx, '{}年签约合同总金额(万元)'.format(year)]) > 50 and '省级' == dfall.loc[idx, '项目属性']:
                            dataUnit['value3'] = dataUnit['value3'] + 1

    # print(data)
    jd = json.dumps(data, ensure_ascii=False)
    fileObject = open('./excel/json/data.json', 'w')
    fileObject.write(jd)
    fileObject.close()

    jd = json.dumps(shiData, ensure_ascii=False)
    fileObject = open('./excel/json/shiData.json', 'w')
    fileObject.write(jd)
    fileObject.close()

    sumMoney = 0
    sumProject = 0
    sumGaoZhiLiangProject = 0
    for d in data:
        sumMoney = sumMoney + d['value']
        sumProject = sumProject + d['value2']
        sumGaoZhiLiangProject = sumGaoZhiLiangProject + d['value3']
    jd = json.dumps([{"ict": "{}万".format(int(sumMoney)), "project": "{}个".format(sumProject),
                      "gaozhiliangproject": "{}个".format(sumGaoZhiLiangProject), "ictCount": "{}".format(sumMoney),
                      "projectCount": "{}".format(sumProject),
                      "gaozhiliangprojectCount": "{}".format(sumGaoZhiLiangProject)}], ensure_ascii=False)
    fileObject = open('./excel/json/tou.json', 'w')
    fileObject.write(jd)
    fileObject.close()

    w = time.strftime("%W", time.localtime())
    全年时间进度 = float(w) / 52.14

    print('----------------------------------')
    print('DICT带动合同收{}万元，进度{}%，超时间进度{}pp，全行业排第{}'.format(round(sumMoney), round(sumMoney / 253000 * 100),
                                                         round((sumMoney / 253000 - 全年时间进度) * 100), 总收入全行业排名))
    print('高品质商品房{}个，进度{}%，超时间进度{}pp，全行业排第{}'.format(sumGaoZhiLiangProject, round(sumGaoZhiLiangProject / 300 * 100),
                                                     round((sumGaoZhiLiangProject / 300 - 全年时间进度) * 100), 高价值项目全行业排名))
    print('5G总项目数{}个，进度{}%，超时间进度{}pp，全行业排第{}'.format(sumProject, round(sumProject / 1000 * 100),
                                                     round((sumProject / 1000 - 全年时间进度) * 100), 总项目全行业排名))
    print('----------------------------------')

if __name__ == '__main__':
    全量项目数据集 = 数据控制.解析合并项目数据()
    本行业数据(全量项目数据集)
    各行业指标完成情况(全量项目数据集)
    保存为json数据(全量项目数据集)
    看板模块.主逻辑()

