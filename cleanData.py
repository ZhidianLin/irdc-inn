import pathlib
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import openpyxl
from dataSource import *
from pandas.api.types import CategoricalDtype
import datetime
import openpyxl
import openpyxl

taskSorterBZ = CategoricalDtype(
    ['重新编辑', '文件传输中', '文件上传失败', '运营审核中', '标注中', '返工确认中', '验收中', "任务暂停",
     '终止任务申请中', '任务终止', '任务完成'],
    ordered=True
)

dcp_feeDict = {
    "对象存储SSD": 411.66,
    "对象存储HDD":82.25,
   "文件存储HDD":61.25,
   "文件存储SSD":234.3
}

oc_feeDict = {
    "NVIDIA 1080（张）":297.9273,
    "NVIDIA P100（张）":1276.8308,
    "NVIDIA P4（张）":468.1713,
    "NVIDIA T4（张）":680.9774,
    "NVIDIA TITAN Xp（张）":553.2935,
    "NVIDIA V100（张）":2766.4668,
    "GeForce_GTX_TITAN_X（张）":340.4882,
    "Quadro_RTX_4000（张）":340.4882,
    "STPU（张）":0,
    "当月内存（G）":4.2312,
    "CPUG（核）":21.1559,
    "CPU-HIGH（核）":84.6233,
    "HDD（G）":0.1385,
    "SDD（G）":0.5885,
    "nvme（G）":0.5885,
    "Bcache（G）":0.1385,
    "OSS服务（G）":0.1385,
    "FS服务（G）":0.1385,
}

profit_center = {
    "IRDC":['PL111', 'SSC03', ],
    "SCG":['SCG08', 'SCG00', 'SCG01', 'SCG09', 'SCG03', 'PL081', 'PL080'],
    "IBG":['IBG00', 'PL060'],
    "ABG":['PL059'],
    "Z":['Z1', 'Z2'],
}

estimate_min = 80
estimate_max = 120
logic_min = 90
logic_max = 120

cn_logic_day = 22
sg_logic_day = 21
abzb_logic_day = 22

本月业务线维度 = 本月业务线维度()
本月员工所属部门 = 本月员工所属部门维度()
本月岗位名称 = 本月岗位名称维度()
本月资源池 = 本月资源池维度()
本月WBS维度 = 本月WBS维度()
上月WBS维度 = 上月WBS维度()
本月人员维度= 本月人员维度()


def cleanMY(data, year, month):
    data = data[data['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    return data


def getCertainUserWBS(data, userName):
    data = data[data['员工姓名'] == userName].reset_index(drop=True)
    return data

def getCertainUserDays(data, userName):
    data = data[data['员工姓名'] == userName].reset_index(drop=True)
    return data

def getCertainWBS(data, wbsName):
    data = data[data['项目名称'] == wbsName].reset_index(drop=True)
    return data
def getCertainWBSFilter(data, wbsName):
    data = data[data['项目名称'] == wbsName].reset_index(drop=True)
    return data
def getAllWBS():
    data = readhistroyData(工时历史总表汇总(), 'WBS维度')
    return data


def cleanCurMonStaff(data):
    cur_mon_staff = data
    cur_mon_staff['预估填报率'] = pd.to_numeric(cur_mon_staff['预估填报率'], errors='coerce')
    cur_mon_staff = cur_mon_staff.replace(np.nan, 0, regex=True)
    cur_mon_staff['理论填报率'] = pd.to_numeric(cur_mon_staff['理论填报率'], errors='coerce')
    cur_mon_staff = cur_mon_staff.replace(np.nan, 0, regex=True)
    return cur_mon_staff

clean本月人员维度 = cleanCurMonStaff(本月人员维度)

def filterCurMonStaff(data, tableValue, filterValue):
    return cleanCurMonStaff(data)[cleanCurMonStaff(data)[tableValue] == filterValue]
def filterData(data, tableValue, filterValue):
    return data[data[tableValue] == filterValue].reset_index(drop=True)

def filterDataMulti(data, tableValue1, filterValue1, tableValue2, filterValue2):
    temp = data[data[tableValue1] == filterValue1].reset_index(drop = True)
    temp = temp[temp[tableValue2] == filterValue2].reset_index(drop = True)
    return temp

def monStaff_businessLine(data, businessLine):
    return cleanCurMonStaff(data)[cleanCurMonStaff(data).业务线.str.contains(businessLine)]

def cleanstaff_apartment_tb():
    staff_apartment_tb = 本月业务线维度
    return staff_apartment_tb.iloc[0:-1, :]

def cleanbusiness_line_tb():
    business_line_tb = 本月业务线维度
    业务线汇总 = business_line_tb.iloc[0:-1, :]
    return 业务线汇总.replace('inf%', None)


def cleanstaff_apartment_table():
    staff_apartment_tb = 本月员工所属部门
    return staff_apartment_tb.iloc[0:-1, :]

def cleanstaff_ziyuanchi_table():
    staff_apartment_tb = 本月资源池
    return staff_apartment_tb.iloc[0:-1, :]

def cleanstaff_title_table():
    staff_apartment_tb = 本月岗位名称
    return staff_apartment_tb.iloc[0:-1, :]
#
def cleanbusiness_line_table():
    business_line_tb = 本月员工所属部门
    业务线汇总 = business_line_tb.iloc[0:-1, :]
    return 业务线汇总.replace('inf%', None)

def clean_bl_table(data):
    business_line_tb = data
    业务线汇总 = business_line_tb.iloc[0:-1, :]
    return 业务线汇总.replace('inf%', None)

def clean固定资产by部门(data):
    df = pd.DataFrame(list(set(data['员工所属部门'])), columns=['员工所属部门'])
    for i in range(len(df)):
        df.loc[i,'员工数'] = len(list(set(data[data['员工所属部门'] == df.loc[i,'员工所属部门']]['实际保管人'])))

    for i in range(len(df)):
        df.loc[i,'总值'] = round(data[data['员工所属部门'] == df.loc[i, '员工所属部门']]['总值'].sum(), 2)
        df.loc[i,'净值'] = round(data[data['员工所属部门'] == df.loc[i, '员工所属部门']]['净值'].sum(), 2)
        df.loc[i,'折旧'] = round(data[data['员工所属部门'] == df.loc[i, '员工所属部门']]['折旧'].sum(), 2)
        df.loc[i,'总值人均'] = round(data[data['员工所属部门'] == df.loc[i, '员工所属部门']]['总值'].sum()/df.loc[i,'员工数'], 2)
        df.loc[i,'净值人均'] = round(data[data['员工所属部门'] == df.loc[i, '员工所属部门']]['净值'].sum()/df.loc[i,'员工数'], 2)
        df.loc[i,'折旧人均'] = round(data[data['员工所属部门'] == df.loc[i, '员工所属部门']]['折旧'].sum()/df.loc[i,'员工数'], 2)

    for i in range(len(df)):
        df.loc[i,'部门折旧人均'] = round(df['折旧'].sum() / df['员工数'].sum(), 2)
        df.loc[i,'部门折旧部门平均'] = round(df['折旧'].sum() / len(list(set(data['员工所属部门']))), 2)
    return df


def clean固定资产by资源池(data):
    df = pd.DataFrame(list(set(data['资源池'])), columns=['资源池'])
    for i in range(len(df)):
        df.loc[i,'员工数'] = len(list(set(data[data['资源池'] == df.loc[i,'资源池']]['实际保管人'])))

    for i in range(len(df)):
        df.loc[i,'总值'] = round(data[data['资源池'] == df.loc[i, '资源池']]['总值'].sum(), 2)
        df.loc[i,'净值'] = round(data[data['资源池'] == df.loc[i, '资源池']]['净值'].sum(), 2)
        df.loc[i,'折旧'] = round(data[data['资源池'] == df.loc[i, '资源池']]['折旧'].sum(), 2)
        df.loc[i,'总值人均'] = round(data[data['资源池'] == df.loc[i, '资源池']]['总值'].sum()/df.loc[i,'员工数'], 2)
        df.loc[i,'净值人均'] = round(data[data['资源池'] == df.loc[i, '资源池']]['净值'].sum()/df.loc[i,'员工数'], 2)
        df.loc[i,'折旧人均'] = round(data[data['资源池'] == df.loc[i, '资源池']]['折旧'].sum()/df.loc[i,'员工数'], 2)

    for i in range(len(df)):
        df.loc[i,'资源池折旧人均'] = round(df['折旧'].sum() / df['员工数'].sum(), 2)
        df.loc[i,'资源池折旧平均'] = round(df['折旧'].sum() / len(list(set(data['资源池']))), 2)
    return df

def staff_apartment_table(data):
    # remove staff not countable'
    # staff apartment logic working hour
    logic_wh_staff_apart = data.groupby(['员工所属部门', '工作地点', '员工姓名']).agg(
        {'实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_sg = logic_wh_staff_apart[logic_wh_staff_apart['工作地点'] == '新加坡'].groupby(
        ['员工所属部门']).agg({'员工姓名': pd.Series.nunique, '实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_sg['理论人天'] = sg_logic_day * logic_wh_staff_apart_sg['员工姓名']
    logic_wh_staff_apart_cn = logic_wh_staff_apart[logic_wh_staff_apart['工作地点'] != '新加坡'].groupby(
        ['员工所属部门']).agg({'员工姓名': pd.Series.nunique, '实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_cn['理论人天'] = cn_logic_day * logic_wh_staff_apart_cn['员工姓名']
    logic_wh_staff_apart_cn

    # sum up df of cn and sg logic working hour
    logic_wh_staff_apartment = logic_wh_staff_apart_sg.append(logic_wh_staff_apart_cn, ignore_index=True)
    logic_wh_staff_apartment = logic_wh_staff_apartment.groupby(["员工所属部门"]).agg(
        {'员工姓名': 'sum', '实际人天': 'sum', '预估人天': 'sum', '理论人天': 'sum'}).reset_index()
    logic_wh_staff_apartment['实际人均'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['预估人均'] = logic_wh_staff_apartment['预估人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['理论人均'] = logic_wh_staff_apartment['理论人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['预估填报率'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment[
        '预估人天'] * 100
    logic_wh_staff_apartment['理论填报率'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment[
        '理论人天'] * 100

    # add sum row
    new_index = len(logic_wh_staff_apartment)
    logic_wh_staff_apartment.loc[new_index] = logic_wh_staff_apartment.sum()
    logic_wh_staff_apartment.loc[new_index, '员工所属部门'] = "Total"
    logic_wh_staff_apartment.loc[new_index, '实际人均'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '预估人均'] = logic_wh_staff_apartment.loc[new_index, '预估人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '理论人均'] = logic_wh_staff_apartment.loc[new_index, '理论人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment['部门实际人均'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                               logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '预估填报率'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                            logic_wh_staff_apartment.loc[new_index, '预估人天'] * 100
    logic_wh_staff_apartment.loc[new_index, '理论填报率'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                            logic_wh_staff_apartment.loc[new_index, '理论人天'] * 100

    for j in range(len(logic_wh_staff_apartment)):
        if logic_wh_staff_apartment.loc[j, '预估填报率'] < estimate_min:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '不满'
        elif logic_wh_staff_apartment.loc[j, '预估填报率'] > estimate_max:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '超载'
        else:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '合理'

    for j in range(len(logic_wh_staff_apartment)):
        if logic_wh_staff_apartment.loc[j, '理论填报率'] < logic_min:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '不满'
        elif logic_wh_staff_apartment.loc[j, '理论填报率'] > logic_max:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '超载'
        else:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '合理'

    logic_wh_staff_apartment = logic_wh_staff_apartment.round(decimals=1).rename(columns={'员工姓名': '员工数'})
    logic_wh_staff_apartment = logic_wh_staff_apartment.replace(np.inf, 0)
    logic_wh_staff_apartment.insert(len(logic_wh_staff_apartment.columns) - 8, '部门实际人均',
                                    logic_wh_staff_apartment.pop('部门实际人均'))
    # # move total row to the last row
    logic_wh_staff_apartment.iloc[logic_wh_staff_apartment.index[logic_wh_staff_apartment['员工所属部门'] == "Total"],:]

    logic_wh_staff_apartment['部门实际人均'] = list(本月员工所属部门维度()['部门实际人均'])[0]
    return logic_wh_staff_apartment[:-1].sort_values(by=['实际人天']).reset_index(drop=True)

def staff_groupBy_table(data, groupBy):
    # remove staff not countable'
    # staff apartment logic working hour
    logic_wh_staff_apart = data.groupby([groupBy, '工作地点', '员工姓名']).agg(
        {'实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_sg = logic_wh_staff_apart[logic_wh_staff_apart['工作地点'] == '新加坡'].groupby(
        [groupBy]).agg({'员工姓名': pd.Series.nunique, '实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_sg['理论人天'] = sg_logic_day * logic_wh_staff_apart_sg['员工姓名']
    logic_wh_staff_apart_cn = logic_wh_staff_apart[logic_wh_staff_apart['工作地点'] != '新加坡'].groupby(
        [groupBy]).agg({'员工姓名': pd.Series.nunique, '实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_cn['理论人天'] = cn_logic_day * logic_wh_staff_apart_cn['员工姓名']
    logic_wh_staff_apart_cn

    # sum up df of cn and sg logic working hour
    logic_wh_staff_apartment = logic_wh_staff_apart_sg.append(logic_wh_staff_apart_cn, ignore_index=True).copy()
    logic_wh_staff_apartment = logic_wh_staff_apartment.groupby([groupBy]).agg(
        {'员工姓名': 'sum', '实际人天': 'sum', '预估人天': 'sum', '理论人天': 'sum'}).reset_index()
    logic_wh_staff_apartment['实际人均'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['预估人均'] = logic_wh_staff_apartment['预估人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['理论人均'] = logic_wh_staff_apartment['理论人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['预估填报率'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment[
        '预估人天'] * 100
    logic_wh_staff_apartment['理论填报率'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment[
        '理论人天'] * 100

    # add sum row
    new_index = len(logic_wh_staff_apartment)
    logic_wh_staff_apartment.loc[new_index] = logic_wh_staff_apartment.sum()
    logic_wh_staff_apartment.loc[new_index, groupBy] = "Total"
    logic_wh_staff_apartment.loc[new_index, '实际人均'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '预估人均'] = logic_wh_staff_apartment.loc[new_index, '预估人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '理论人均'] = logic_wh_staff_apartment.loc[new_index, '理论人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment['部门实际人均'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                               logic_wh_staff_apartment.loc[new_index, '员工姓名']
    try:
        logic_wh_staff_apartment.loc[new_index, '预估填报率'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                            logic_wh_staff_apartment.loc[new_index, '预估人天'] * 100
        logic_wh_staff_apartment.loc[new_index, '理论填报率'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                            logic_wh_staff_apartment.loc[new_index, '理论人天'] * 100
    except:
        pass

    try:
        if logic_wh_staff_apartment.loc[new_index, '预估填报率'] == np.inf:
            logic_wh_staff_apartment.loc[new_index, '预估填报率'] = 0
        if logic_wh_staff_apartment.loc[new_index, '理论填报率'] == np.inf:
            logic_wh_staff_apartment.loc[new_index, '理论填报率'] = 0
    except:
        pass


    for j in range(len(logic_wh_staff_apartment)):
        if logic_wh_staff_apartment.loc[j, '预估填报率'] < estimate_min:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '不满'
        elif logic_wh_staff_apartment.loc[j, '预估填报率'] > estimate_max:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '超载'
        else:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '合理'

    for j in range(len(logic_wh_staff_apartment)):
        if logic_wh_staff_apartment.loc[j, '理论填报率'] < logic_min:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '不满'
        elif logic_wh_staff_apartment.loc[j, '理论填报率'] > logic_max:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '超载'
        else:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '合理'

    logic_wh_staff_apartment = logic_wh_staff_apartment.round(decimals=1).rename(columns={'员工姓名': '员工数'})
    logic_wh_staff_apartment = logic_wh_staff_apartment.replace(np.inf, 0)
    logic_wh_staff_apartment.insert(len(logic_wh_staff_apartment.columns) - 8, '部门实际人均',
                                    logic_wh_staff_apartment.pop('部门实际人均'))
    # # move total row to the last row
    logic_wh_staff_apartment.iloc[logic_wh_staff_apartment.index[logic_wh_staff_apartment[groupBy] == "Total"],:]

    logic_wh_staff_apartment['部门实际人均'] = list(本月员工所属部门维度()['部门实际人均'])[0]
    return logic_wh_staff_apartment[:-1].sort_values(by=['实际人天']).reset_index(drop=True)

def staff_岗位名称_table(data):
    # remove staff not countable'
    # staff apartment logic working hour
    logic_wh_staff_apart = data.groupby(['岗位名称', '工作地点', '员工姓名']).agg(
        {'实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_sg = logic_wh_staff_apart[logic_wh_staff_apart['工作地点'] == '新加坡'].groupby(
        ['资源池']).agg({'员工姓名': pd.Series.nunique, '实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_sg['理论人天'] = sg_logic_day * logic_wh_staff_apart_sg['员工姓名']
    logic_wh_staff_apart_cn = logic_wh_staff_apart[logic_wh_staff_apart['工作地点'] != '新加坡'].groupby(
        ['资源池']).agg({'员工姓名': pd.Series.nunique, '实际人天': 'sum', '预估人天': 'sum'}).reset_index()
    logic_wh_staff_apart_cn['理论人天'] = cn_logic_day * logic_wh_staff_apart_cn['员工姓名']
    logic_wh_staff_apart_cn

    # sum up df of cn and sg logic working hour
    logic_wh_staff_apartment = logic_wh_staff_apart_sg.append(logic_wh_staff_apart_cn, ignore_index=True)
    logic_wh_staff_apartment = logic_wh_staff_apartment.groupby(["岗位名称"]).agg(
        {'员工姓名': 'sum', '实际人天': 'sum', '预估人天': 'sum', '理论人天': 'sum'}).reset_index()
    logic_wh_staff_apartment['实际人均'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['预估人均'] = logic_wh_staff_apartment['预估人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['理论人均'] = logic_wh_staff_apartment['理论人天'] / logic_wh_staff_apartment['员工姓名']
    logic_wh_staff_apartment['预估填报率'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment[
        '预估人天'] * 100
    logic_wh_staff_apartment['理论填报率'] = logic_wh_staff_apartment['实际人天'] / logic_wh_staff_apartment[
        '理论人天'] * 100

    # add sum row
    new_index = len(logic_wh_staff_apartment)
    logic_wh_staff_apartment.loc[new_index] = logic_wh_staff_apartment.sum()
    logic_wh_staff_apartment.loc[new_index, '岗位名称'] = "Total"
    logic_wh_staff_apartment.loc[new_index, '实际人均'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '预估人均'] = logic_wh_staff_apartment.loc[new_index, '预估人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '理论人均'] = logic_wh_staff_apartment.loc[new_index, '理论人天'] / \
                                                          logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment['部门实际人均'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                               logic_wh_staff_apartment.loc[new_index, '员工姓名']
    logic_wh_staff_apartment.loc[new_index, '预估填报率'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                            logic_wh_staff_apartment.loc[new_index, '预估人天'] * 100
    logic_wh_staff_apartment.loc[new_index, '理论填报率'] = logic_wh_staff_apartment.loc[new_index, '实际人天'] / \
                                                            logic_wh_staff_apartment.loc[new_index, '理论人天'] * 100

    for j in range(len(logic_wh_staff_apartment)):
        if logic_wh_staff_apartment.loc[j, '预估填报率'] < estimate_min:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '不满'
        elif logic_wh_staff_apartment.loc[j, '预估填报率'] > estimate_max:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '超载'
        else:
            logic_wh_staff_apartment.loc[j, '预估填报'] = '合理'

    for j in range(len(logic_wh_staff_apartment)):
        if logic_wh_staff_apartment.loc[j, '理论填报率'] < logic_min:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '不满'
        elif logic_wh_staff_apartment.loc[j, '理论填报率'] > logic_max:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '超载'
        else:
            logic_wh_staff_apartment.loc[j, '理论填报'] = '合理'

    logic_wh_staff_apartment = logic_wh_staff_apartment.round(decimals=1).rename(columns={'员工姓名': '员工数'})
    logic_wh_staff_apartment = logic_wh_staff_apartment.replace(np.inf, 0)
    logic_wh_staff_apartment.insert(len(logic_wh_staff_apartment.columns) - 8, '部门实际人均',
                                    logic_wh_staff_apartment.pop('部门实际人均'))
    # # move total row to the last row
    logic_wh_staff_apartment.iloc[logic_wh_staff_apartment.index[logic_wh_staff_apartment['员工所属部门'] == "Total"],:]

    logic_wh_staff_apartment['部门实际人均'] = list(本月员工所属部门维度()['部门实际人均'])[0]
    return logic_wh_staff_apartment[:-1].sort_values(by=['实际人天']).reset_index(drop=True)


def groupBy_act_days_percentage(data, groupBy):
    groupByData = data.groupby(groupBy).agg({"总人天":'sum'}).reset_index()
    sumDays = groupByData['总人天'].sum()
    wbs_percentage = {}
    for i in range(len(groupByData)):
        wbs_percentage[groupByData.loc[i,groupBy]] = groupByData.loc[i,groupBy] + ', ' + str(round(groupByData.loc[i,'总人天'] / sumDays *100,1)) + '%'
    for i in range(len(data)):
        data.loc[i,groupBy] = wbs_percentage[data.loc[i,groupBy]]
    return data

def groupBy_top_act_percentage(data, groupBy):
    groupByData = data.groupby(groupBy).agg({"总人天":'sum'}).reset_index()
    sumDays = groupByData['总人天'].sum()
    wbs_percentage = {}
    for i in range(len(groupByData)):
        wbs_percentage[groupByData.loc[i,groupBy]] = groupByData.loc[i,groupBy] + ', ' + str(round(groupByData.loc[i,'总人天'] / sumDays *100,1)) + '%'
    for i in range(len(data)):
        data.loc[i,groupBy] = wbs_percentage[data.loc[i,groupBy]]
    return data


def 业务线pie(type, data):
    业务线汇总 = data
    业务线pie = 业务线汇总[["员工所属部门", "员工数", type]]
    return 业务线pie.groupby('员工所属部门').agg({'员工数': 'sum', type: 'sum'})


def 业务线pieFilter(type,data):
    业务线pie = data[["员工所属部门", "员工数", type]]
    return 业务线pie.groupby('员工所属部门').agg({'员工数': 'sum', type: 'sum'})


def 资源池pieFilter(type, data, groupBy):
    业务线pie = data[[groupBy, type]]
    return 业务线pie.groupby(groupBy).agg({type: 'sum'})


def 资源池pie(type):
    cur_mon_staff = clean本月人员维度
    return cur_mon_staff.groupby('资源池').agg({type: 'sum'})

def 岗位pie(type):
    cur_mon_staff = clean本月人员维度
    return cur_mon_staff.groupby('岗位名称').agg({type: 'sum'})

def 固定资产pie(data):
    固定资产pie = data[["员工所属部门", '折旧','净值','总值']]
    data = 固定资产pie.groupby('员工所属部门').agg({'折旧': 'sum', '净值': 'sum', '总值': 'sum'}).reset_index(drop=True)
    return data


def 业务线汇总(type):
    cur_mon_staff = clean本月人员维度
    业务线汇总 = cur_mon_staff[["业务线", "员工组", type]].rename(columns={type: "总人天"})
    业务线汇总['工时类别'] = 业务线汇总['业务线'].apply(lambda row: type[0:2])
    return 业务线汇总

def wbsType(data, type):
    data = data[data['WBS类型'] == type]
    data = data[data['员工所属部门'] != 0 ]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)

def wbsTypeFilter(type, name):
    data = readhistroyData(工时历史总表汇总(), '合并底表')
    data = data[data['资源池'] == name]
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()]
    data = data[data['WBS类型'] == type]
    data = data[data['员工所属部门'] != 0 ]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)

def wbsTypeFilterBL(data, WBStype, name, year, month):
    data = data[data['员工所属部门'] == name]
    data = data[data['工时年份'] == year]
    data = data[data['工时月份'] == month]
    data = data[data['WBS类型'].isin(WBStype)]
    data = data[data['资源池'] != 0]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)

def wbsTypeFilterBL2(data, wBStype,  year, month):
    data = data[data['工时年份'] == year]
    data = data[data['工时月份'] == month]
    data = data[data['WBS类型'].isin(wBStype)]
    data = data[data['资源池'] != 0]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)


def wbsTypeFilterBL3(data, year, month):
    data = data[data['工时年份'] == year]
    data = data[data['工时月份'] == month]
    data = data[data['资源池'] != 0]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)


def notPL111wbsType(data):
    data = data[~data['利润中心'].isin(['PL111','Z1','Z2'])]
    data = data[data['员工所属部门'] != 0]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)

def notPL111wbsTypeFilter(name):
    data = readhistroyData(工时历史总表汇总(), '合并底表')
    data = data[data['资源池'] == name]
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()]
    data = data[data['利润中心'] != 'PL111']
    data = data[data['员工所属部门'] != 0]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)


def notPL111wbsTypeFilterBL(name,year, month):
    data = readhistroyData(工时历史总表汇总(), '合并底表')
    data = data[data['员工所属部门'] == name]
    data = data[data['工时年份'] == year]
    data = data[data['工时月份'] == month]
    data = data[data['利润中心'] != 'PL111']
    data = data[data['资源池'] != 0]
    data = data[data['实际人天'] > 0]
    return data.reset_index(drop=True)


def filterWBSLen(df, value):
    try:
        data = df[df['实际人天'] > 0 ].reset_index(drop=True)
        data = data[data['WBS类型'] == value].reset_index(drop=True)
        indicator = len(list(set(list(data['项目名称']))))
        if indicator == 0:
            indicator = None
    except:
        indicator = None
    return indicator


def returnWBS_Bl_num(df, value, bl):
    try:
        data = df[df['实际人天'] > 0 ].reset_index(drop=True)
        data = data[data['WBS类型'] == value].reset_index(drop=True)
        data = data[data['WBS所属部门'].isin(bl)].reset_index(drop=True)
        # data = data[data['利润中心'].isin(['PL111'])].reset_index(drop=True)
        indicator = len(list(data['项目名称']))
        if indicator == 0:
            indicator = None
    except:
        indicator = None
    return indicator

def returnWBS_Bl_num3(df, value, bl, pm):
    try:
        data = df[df['实际人天'] > 0].reset_index(drop=True)
        data = data[data['WBS类型'] == value].reset_index(drop=True)
        data = data[data['WBS所属部门'].isin(bl)].reset_index(drop=True)
        # data = data[data['利润中心'].isin(['PL111'])].reset_index(drop=True)
        data = data[~data['PM姓名'].isin(pm)].reset_index(drop=True)
        indicator = len(list(data['项目名称']))
        if indicator == 0:
            indicator = None
    except:
        indicator = None
    return indicator

def returnWBS_Bl_num2(df, value):
    try:
        data = df[df['实际人天'] > 0].reset_index(drop=True)
        data = data[data['WBS类型'] == value].reset_index(drop=True)
        indicator = len(list(data['项目名称']))
        if indicator == 0:
            indicator = None
    except:
        indicator = None
    return indicator
def returnWBS_Bl_actDays(df, value):
    try:
        indicator = df[df['WBS类型'] == value]['实际人天'].sum()
        if indicator == 0:
            indicator = None
    except:
        indicator = None
    return indicator


def not_fill_wh(data, year, month):
    data = data[data['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    data = cleanCurMonStaff(data)
    data0 = data[data['缺填日期'] != np.nan]
    data0 = data0[data0['缺填日期'] != 0]
    data2 = data[data['多填日期'] != np.nan]
    data2 = data2[data2['多填日期'] != 0]
    data3 = data0.append(data2, ignore_index=True).drop_duplicates().reset_index(drop=True)
    return data3[['员工姓名','缺填日期','多填日期','员工所属部门','资源池']]


def 对比业务线汇总(type1,type2):
    temp = 业务线汇总(type1).append(业务线汇总(type2)).reset_index(drop=True)
    return temp.groupby(["业务线", "员工组","工时类别"]).agg({"总人天":'sum'}).reset_index()
def 部门汇总(data, type, attri):
    部门汇总 = data[["员工所属部门", attri, type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['员工所属部门'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比部门汇总(data, type1,type2, attri):
    temp = 部门汇总(data, type1, attri).append(部门汇总(data, type2, attri)).reset_index(drop=True)
    return temp.groupby(["员工所属部门", attri,"工时类别"]).agg({"总人天":'sum'}).reset_index()


def 对比部门汇总资源池细分(data, type1,type2,type3, attri):
    temp = 部门汇总(data, type1, attri).append(部门汇总(data, type2, attri)).append(部门汇总(data, type3, attri)).reset_index(drop=True)
    return temp.groupby(["员工所属部门", attri,"工时类别"]).agg({"总人天":'sum'}).reset_index()


def 部门汇总BL(data, type, attri):
    部门汇总 = data[["资源池", attri, type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['资源池'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比部门汇总资源池细分BL(data, type1,type2,type3, attri):
    temp = 部门汇总BL(data, type1, attri).append(部门汇总BL(data, type2, attri)).append(部门汇总BL(data, type3, attri)).reset_index(drop=True)
    return temp.groupby(["资源池", attri,"工时类别"]).agg({"总人天":'sum'}).reset_index()


def 资源池汇总(data, type, attri):
    部门汇总 = data[["资源池", attri, type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['资源池'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比资源池汇总(data, type1,type2, attri):
    temp = 资源池汇总(data, type1, attri).append(资源池汇总(data, type2, attri)).reset_index(drop=True)
    return temp.groupby(["资源池", attri,"工时类别"]).agg({"总人天":'sum'}).reset_index()

def 部门汇总2(data, type, attri):
    部门汇总 = data[["员工所属部门", attri, type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['员工所属部门'].apply(lambda row: type[0:2])
    return 部门汇总





def 对比部门汇总2(data, type1, attri):
    temp = 部门汇总2(data, type1, attri).reset_index(drop=True)
    return temp.groupby(["员工所属部门", attri,"工时类别"]).agg({"总人天":'sum'}).reset_index()


def 部门汇总2BL(data, type, attri):
    部门汇总 = data[["资源池", attri, type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['资源池'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比部门汇总2BL(data, type1, attri):
    temp = 部门汇总2BL(data, type1, attri).reset_index(drop=True)
    data = temp.groupby(["资源池", attri,"工时类别"]).agg({"总人天":'sum'}).reset_index()
    return data

def wbsQuick(data, axis, type1, attri):
    部门汇总 = data[[axis, attri, type1]].rename(columns={type1: "总人天"})
    return 部门汇总

def wbsQuickCheck(data, axis, type1, attri):
    temp = wbsQuick(data, axis,type1, attri).reset_index(drop=True)
    data = temp.groupby([axis, attri]).agg({"总人天":'sum'}).reset_index()
    data['总人天'] = data['总人天'].round(decimals=1)
    return data

def groupByProfit(data, axis):
    data = data[['利润中心', axis, '实际人天']].rename(columns={'实际人天': "总人天"})
    for i in range(len(data)):
        for k,v in profit_center.items():
            if data.loc[i,'利润中心'] in v:
                data.loc[i, '合并利润中心'] = k
    data['总人天'] = data['总人天'].round(decimals=1)
    data = data.groupby(['合并利润中心', axis]).agg({"总人天": 'sum'}).reset_index()
    return data

def 部门汇总固定资产(data, type, attri):
    部门汇总 = data[["员工所属部门", attri, type]].rename(columns={type: "总金额"})
    部门汇总['金额占比'] = 部门汇总['员工所属部门'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比部门汇总固定资产(data, type1, attri):
    temp = 部门汇总固定资产(data, type1, attri).reset_index(drop=True)
    return temp.groupby(["员工所属部门", attri,"金额占比"]).agg({"总金额":'sum'}).reset_index()


def 部门汇总dcp(data, type, attri, sumValue, valuePercentage, facCol):
    部门汇总 = data[[facCol, attri, type]].rename(columns={type: sumValue})
    部门汇总[valuePercentage] = 部门汇总[facCol].apply(lambda row: type[0:2])
    return 部门汇总

def 对比汇总dcp(data, type1, attri, sumValue, valuePercentage, facCol):
    temp = 部门汇总dcp(data, type1, attri, sumValue, valuePercentage, facCol).reset_index(drop=True)
    data = temp.groupby([facCol, attri,valuePercentage]).agg({sumValue:'sum'}).reset_index()
    return data






def 总库存固定资产(data, type1, attri):
    部门汇总 = data[["资产月份", attri, type1]].rename(columns={type1: "总金额"})
    部门汇总['金额占比'] = 部门汇总['资产月份'].apply(lambda row: type1[0:2])
    return 部门汇总

def 对比总库存固定资产(data, type1, attri):
    temp = 总库存固定资产(data, type1, attri).reset_index(drop=True)
    temp = temp.groupby(["资产月份", attri,"金额占比"]).agg({"总金额":'sum'}).reset_index()
    return temp


def 总库存固定资产数量(data, type1, attri):
    部门汇总 = data[["资产月份", attri, type1]].rename(columns={type1: "总个数"})
    部门汇总['个数占比'] = 部门汇总['资产月份'].apply(lambda row: type1[0:2])
    return 部门汇总

def 对比总库存固定资产数量(data, type1, attri):
    temp = 总库存固定资产数量(data, type1, attri).reset_index(drop=True)
    return temp.groupby(["资产月份", attri,"个数占比"]).agg({"总个数":'sum'}).reset_index()



def 部门汇总固定资产数量(data, type, attri):
    部门汇总 = data[["员工所属部门", attri, type]].rename(columns={type: "总个数"})
    部门汇总['个数占比'] = 部门汇总['员工所属部门'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比部门汇总固定资产数量(data, type1, attri):
    temp = 部门汇总固定资产数量(data, type1, attri).reset_index(drop=True)
    temp = temp.groupby(["员工所属部门", attri,"个数占比"]).agg({"总个数":'count'}).reset_index()
    return temp



def 资源池汇总固定资产(data, type, attri):
    部门汇总 = data[["资源池", attri, type]].rename(columns={type: "总金额"})
    部门汇总['金额占比'] = 部门汇总['资源池'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比资源池汇总固定资产(data, type1, attri):
    temp = 资源池汇总固定资产(data, type1, attri).reset_index(drop=True)
    return temp.groupby(["资源池", attri,"金额占比"]).agg({"总金额":'sum'}).reset_index()



def 资源池汇总固定资产数量(data, type, attri):
    部门汇总 = data[["资源池", attri, type]].rename(columns={type: "总个数"})
    部门汇总['个数占比'] = 部门汇总['资源池'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比资源池汇总固定资产数量(data, type1, attri):
    temp = 资源池汇总固定资产数量(data, type1, attri).reset_index(drop=True)
    return temp.groupby(["资源池", attri,"个数占比"]).agg({"总个数":'count'}).reset_index()



def 分区汇总(data, type, attri, name):
    部门汇总 = data[["分区", attri, type]].rename(columns={type: name})
    部门汇总['类别'] = 部门汇总['分区'].apply(lambda row: type[0:6])
    return 部门汇总


def 对比分区gpu0(data, type1, attri, fee, name, leibie):
    temp = 分区汇总(data, type1, attri, name).reset_index(drop=True)
    sum_use_nodes = data.groupby(['分区']).agg({'使用节点数':'sum'}).reset_index()
    sum_nodes_by_apartment = temp.groupby(["分区", attri,"类别"]).agg({"总使用节点数":'sum'}).reset_index()
    for i in range(len(sum_nodes_by_apartment)):
        for j in range(len(sum_use_nodes)):
            if sum_nodes_by_apartment.loc[i,'分区'] == sum_use_nodes.loc[j,'分区']:
                sum_nodes_by_apartment.loc[i,'使用率'] = round(sum_nodes_by_apartment.loc[i,'总使用节点数']/sum_use_nodes.loc[j,'使用节点数'],2)

    # fee['总价'] = fee['总价'].astype(float)
    for i in range(len(sum_nodes_by_apartment)):
        for j in range(len(fee)):
            if sum_nodes_by_apartment.loc[i,'分区'] == fee.loc[j,'分区']:
                sum_nodes_by_apartment.loc[i,'费用'] = round(fee.loc[j,'总价'] * sum_nodes_by_apartment.loc[i,'使用率'],2)
    sum_nodes_by_apartment['类别'] = leibie
    return sum_nodes_by_apartment

def 对比分区gpu(data, type1, attri, name):
    temp = 分区汇总(data, type1, attri, name).reset_index(drop=True)
    data = temp.groupby(["分区", attri,"类别"]).agg({"总使用节点数":'sum'}).reset_index()
    return data

def 对比分区gpu2(data, type1, attri, name):
    temp = 分区汇总(data, type1, attri, name).reset_index(drop=True)
    data = temp.groupby(["分区", attri,"类别"]).agg({"总累计时长":'sum'}).reset_index()
    return data



def 部门汇总3(data, type, attri):
    部门汇总 = data[["资源池", attri, type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['资源池'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比部门汇总3(data, type1, attri):
    temp = 部门汇总3(data, type1, attri).reset_index(drop=True)
    return temp.groupby(["资源池", attri,"工时类别"]).agg({"总人天":'sum'}).reset_index()
#
def 部门汇总4(data, type):
    部门汇总 = data[["工时月份", "项目名称", type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['工时月份'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比部门汇总4(data, type1,type2):
    temp = 部门汇总4(data, type1).append(部门汇总4(data, type2)).reset_index(drop=True)
    return temp.groupby(["工时月份", "项目名称", "工时类别"]).agg({"总人天":'sum'}).reset_index()
#
# #
# def 部门汇总5(data, type):
#     部门汇总 = data[["员工所属部门", "员工姓名", type]].rename(columns={type: "总人天"})
#     部门汇总['工时类别'] = 部门汇总['员工所属部门'].apply(lambda row: type[0:2])
#     return 部门汇总
#
# def 对比部门汇总5(data, type1,type2):
#     temp = 部门汇总5(data, type1).append(部门汇总5(data, type2)).reset_index(drop=True)
#     return temp.groupby(["员工所属部门", "员工姓名","工时类别"]).agg({"总人天":'sum'}).reset_index()

# def 部门汇总2(data, type):
#     部门汇总 = data[["工时月份", "项目名称", type]].rename(columns={type: "总人天"})
#     部门汇总['工时类别'] = 部门汇总['工时月份'].apply(lambda row: type[0:2])
#     return 部门汇总
#
# def 对比部门汇总2(data, type1,type2):
#     temp = 部门汇总2(data, type1).append(部门汇总2(data, type2)).reset_index(drop=True)
#     return temp.groupby(["工时月份", "项目名称", "工时类别"]).agg({"总人天":'sum'}).reset_index()


def wbs汇总(data, color, type):
    部门汇总 = data[["员工所属部门","工时月份", color, type]].rename(columns={type: "总人天"})
    部门汇总['工时类别'] = 部门汇总['工时月份'].apply(lambda row: type[0:2])
    return 部门汇总

def 对比wbs汇总(data, color, type1,type2):
    temp = wbs汇总(data, color, type1).append(wbs汇总(data, color, type2)).reset_index(drop=True)
    return temp.groupby(["工时月份", color, "工时类别"]).agg({"总人天":'sum'}).reset_index()


def groupByWl(data, dict, indexList, dictHead, indexHead):
    data = data.groupby([dictHead,indexHead]).agg({'实际人天':sum}).reset_index()
    for i in list(dict.keys()):
        tempList = []
        temp = data[data[dictHead] == i].reset_index(drop=True)
        for j in indexList:
            try:
                smdf = temp[temp[indexHead] == j].reset_index(drop=True)
                tempList.append(smdf.loc[0, '实际人天'])
            except:
                tempList.append(0)
        dict[i].extend(tempList)
    return pd.DataFrame(dict, index=indexList).reset_index()


# 预估业务线汇总 = cur_mon_staff[["业务线", "员工组", "预估人天"]].rename(columns={"预估人天": "总工时"})
# 预估业务线汇总['工时类别'] = 预估业务线汇总['业务线'].apply(lambda row: '预估')

# cur_mon_staff['预估填报率'] = cur_mon_staff['预估填报率'].astype(int)
# cur_mon_staff['理论填报率'] = cur_mon_staff['理论填报率'].astype(int)

# last_mon_wbs = pd.read_csv(DATA_PATH.joinpath("11月WBS维度.csv"))
# cur_mon_wbs = pd.read_csv(DATA_PATH.joinpath("12月WBS维度.csv"))

def logic_rate_abnormal_tb(data):
    data = cleanCurMonStaff(data)
    理论填报filterData = data[['员工姓名', '员工组', '员工所属部门','资源池', '实际人天', '理论人天', '理论填报率', '理论填报' ]]
    return 理论填报filterData[~理论填报filterData['理论填报'].str.contains('合理')]

def cleanDF资源池(data, name):
    return data[data['资源池'] == name].reset_index(drop=True)

def cleanDF员工部门(data, name):
    return data[data['员工所属部门'] == name].reset_index(drop=True)

def actual_wbs_tb(data):
    try:
        return data.loc[(data['实际人天'] > 0) & (data['WBS类型'] != 'Z')].reset_index(drop=True)
    except:
        return pd.DataFrame()

def wbs_type_number(data):
    wbs_type = ['P','R','D','M']
    data = actual_wbs_tb(data)
    testdict =  dict(data['WBS类型'].value_counts())
    diff = set(wbs_type).difference(set(list(testdict.keys())))
    if len(diff) == 1:
        testdict[list(diff)[0]] = 0
    else:
        for i in list(diff):
            testdict[i] = 0
    return testdict


def 本月wbs预估不满():
    本月WBS维度.loc[(本月WBS维度['WBS类型'] != 'Z') & (本月WBS维度['预估填报'] == '不满')]

def 本月wbs预估超载():
    本月WBS维度.loc[(本月WBS维度['WBS类型'] != 'Z') & (本月WBS维度['预估填报'] == '超载')]


def 新增wbs(new_wbs, last_wbs):
    new_wbs = new_wbs[new_wbs['实际人天'] > 0 ]
    new_wbs = new_wbs[~new_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    last_wbs = last_wbs[last_wbs['实际人天'] > 0]
    last_wbs = last_wbs[~last_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    return list(set(list(new_wbs['项目编号'])).difference(set(list(last_wbs['项目编号']))))

def 减少wbs(new_wbs, last_wbs):
    new_wbs = new_wbs[new_wbs['实际人天'] > 0 ]
    new_wbs = new_wbs[~new_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    last_wbs = last_wbs[last_wbs['实际人天'] > 0]
    last_wbs = last_wbs[~last_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    return list(set(list(last_wbs['项目编号'])).difference(set(list(new_wbs['项目编号']))))

def 新增wbs_tb(new_wbs, last_wbs):
    new_wbs = new_wbs[new_wbs['实际人天'] > 0 ]
    new_wbs = new_wbs[~new_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    last_wbs = last_wbs[last_wbs['实际人天'] > 0]
    last_wbs = last_wbs[~last_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    return new_wbs[new_wbs["项目编号"].isin(list(set(list(new_wbs["项目编号"])).difference(
        set(list(last_wbs["项目编号"])))))].reset_index(drop=True).sort_values(by=["实际人天","项目编号"],ascending=False)

def 减少wbs_tb(new_wbs, last_wbs):
    new_wbs = new_wbs[new_wbs['实际人天'] > 0 ]
    new_wbs = new_wbs[~new_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    last_wbs = last_wbs[last_wbs['实际人天'] > 0]
    last_wbs = last_wbs[~last_wbs['WBS类型'].isin(['Z'])].reset_index(drop=True)
    return last_wbs[last_wbs["项目编号"].isin(list(set(list(last_wbs["项目编号"])).difference(
        set(list(new_wbs["项目编号"])))))].reset_index(drop=True).sort_values(by=["实际人天","项目编号"],ascending=False)


def 新增固定资产(new, last):
    return list(set(list(new['资产代码'])).difference(set(list(last['资产代码']))))

def 减少固定资产(new, last):
    return list(set(list(last['资产代码'])).difference(set(list(new['资产代码']))))


def cleanUser(new, id, usedVolumn):
    new = new.drop([id], axis=1)
    new = new.groupby(['用户名','员工所属部门','资源池','岗位名称','员工组', '单项资源类型']).agg({usedVolumn:sum, '费用(元)':sum}).reset_index()
    for i in range(len(new)):
        new.loc[i,id] = new.loc[i, '用户名'] + new.loc[i, '单项资源类型']
    return new

def 新增Tb(new, last, id, usedVolumn):
    temp = pd.DataFrame(columns=['用户名','员工所属部门','资源池','岗位名称','员工组','资源类型','新增使用量','新增费用'])
    totalNew = list(set(list(new[id])).difference(set(list(last[id]))))
    for i in range(len(new)):
        for j in range(len(last)):
            if new.loc[i,id] == last.loc[j,id] and new.loc[i,usedVolumn] != last.loc[j,usedVolumn]:
                if new.loc[i,usedVolumn] > last.loc[j,usedVolumn]:
                    new_row = []
                    new_row.append(new.loc[i,'用户名'])
                    new_row.append(new.loc[i, '员工所属部门'])
                    new_row.append(new.loc[i, '资源池'])
                    new_row.append(new.loc[i, '岗位名称'])
                    new_row.append(new.loc[i, '员工组'])
                    new_row.append(new.loc[i, id])
                    new_row.append(new.loc[i, usedVolumn] - last.loc[j,usedVolumn])
                    new_row.append(new.loc[i, '费用(元)'] - last.loc[j, '费用(元)'])
                    temp.loc[len(temp)] = new_row

    appendDf = new[new[id].isin(totalNew)].reset_index(drop=True)
    appendDf = appendDf[['用户名','员工所属部门','资源池','岗位名称','员工组',id, usedVolumn,"费用(元)"]]
    appendDf.rename(columns={usedVolumn:"新增使用量","费用(元)":"新增费用",id:"资源类型"}, inplace= True)

    temp = temp.append(appendDf,ignore_index=True)
    temp = temp.sort_values(by=['新增费用'], ascending=False).reset_index(drop=True)

    temp['新增使用量'] = temp['新增使用量'].round(decimals=3)
    temp['新增费用'] = temp['新增费用'].round(decimals=3)
    return temp

def 减少Tb(new, last, id, usedVolumn):
    temp = pd.DataFrame(columns=['用户名','员工所属部门','资源池','岗位名称','员工组','资源类型','减少使用量','减少费用'])
    totalLast = list(set(list(last[id])).difference(set(list(new[id]))))
    for i in range(len(new)):
        for j in range(len(last)):
            if new.loc[i,id] == last.loc[j,id] and new.loc[i,usedVolumn] != last.loc[j,usedVolumn]:
                if new.loc[i,usedVolumn] < last.loc[j,usedVolumn]:
                    new_row = []
                    new_row.append(last.loc[j,'用户名'])
                    new_row.append(last.loc[j, '员工所属部门'])
                    new_row.append(last.loc[j, '资源池'])
                    new_row.append(last.loc[j, '岗位名称'])
                    new_row.append(last.loc[j, '员工组'])
                    new_row.append(last.loc[j, id])
                    new_row.append(last.loc[j, usedVolumn] - new.loc[i,usedVolumn])
                    new_row.append(last.loc[j, '费用(元)'] - new.loc[i, '费用(元)'])
                    temp.loc[len(temp)] = new_row

    appendDf = last[last[id].isin(totalLast)].reset_index(drop=True)
    appendDf = appendDf[['用户名','员工所属部门','资源池','岗位名称','员工组',id, usedVolumn,"费用(元)"]]
    appendDf.rename(columns={usedVolumn:"减少使用量","费用(元)":"减少费用",id:"资源类型"}, inplace= True)

    temp = temp.append(appendDf,ignore_index=True)
    temp = temp.sort_values(by=['减少费用'], ascending=False).reset_index(drop=True)

    temp['减少使用量'] = temp['减少使用量'].round(decimals=3)
    temp['减少费用'] = temp['减少费用'].round(decimals=3)
    return temp

def 新增固定资产_tb(new, last, tableValue1, tableValue2):
    return new[new[tableValue1].isin(list(set(list(new[tableValue1])).difference(set(list(last[tableValue1])))))].reset_index(drop=True).sort_values(by=[tableValue2,tableValue1],ascending=False)

def 减少固定资产_tb(new, last, tableValue1, tableValue2):
    return last[last[tableValue1].isin(list(set(list(last[tableValue1])).difference(set(list(new[tableValue1])))))].reset_index(drop=True).sort_values(by=[tableValue2,tableValue1],ascending=False)






def wbs部门pie(data, type):
    wbs = data[['WBS所属部门','实际人天','预估人天']]
    return wbs.groupby('WBS所属部门').agg({type: 'sum'})

def wbs类型pie(data, type):
    wbs = data[['WBS类型','实际人天','预估人天']]
    data =  wbs.groupby('WBS类型').agg({type: 'sum'})
    return data

def wbs类型pie细分(data, type):
    wbs = data[['WBS类型','实际人天','预估人天']].copy()
    wbs['实际人天'] = wbs['实际人天'].round(1)
    wbs['预估人天'] = wbs['预估人天'].round(1)
    data = wbs.groupby('WBS类型').agg({type: 'sum'})
    return data

def notActiveWbs_pie(data):
    wbs = data[['WBS未活跃时长','项目名称']]
    data = wbs.groupby('WBS未活跃时长').agg({'项目名称': 'count'}).reset_index()
    return data


def wbs员工组pie细分(data, groupBy):
    wbs = data[[groupBy, '实际人天','预估人天']].copy()
    wbs['实际人天'] = wbs['实际人天'].round(1)
    wbs['预估人天'] = wbs['预估人天'].round(1)
    if groupBy == "员工组":
        wbs = wbs.replace(['正式员工','外包员工'],['正式','外包'])
    elif groupBy == "资源池":
        wbs = replaceDF(wbs)
    data = wbs.groupby(groupBy).agg({'实际人天': 'sum', '预估人天': 'sum'})
    data= data.reset_index()
    return data


def wbs员工组pie细分Quick(data, groupBy):
    wbs = data[[groupBy, '实际人天','预估人天',"理论人天"]].copy()
    wbs['实际人天'] = wbs['实际人天'].round(1)
    wbs['预估人天'] = wbs['预估人天'].round(1)
    wbs['理论人天'] = wbs['理论人天'].round(1)
    if groupBy == "员工组":
        wbs = wbs.replace(['正式员工','外包员工'],['正式','外包'])
    elif groupBy == "资源池":
        wbs = replaceDF(wbs)
    data = wbs.groupby(groupBy).agg({'实际人天': 'sum', '预估人天': 'sum', '理论人天': 'sum'})
    data= data.reset_index()
    return data

def replaceDF(data):
    return data.replace(['算法SDK资源池','业务开发资源池','测试运维资源池','架构平台资源池','创新算法资源池'],
                          ['算法SDK', '业务开发', '测试运维', '架构平台','创新算法'],)

def 历史WBS类型人天(data):
    data = data[data['工时年份'] == datetime.datetime.now().year]
    monthList = list(set(data['工时月份']))
    df = pd.DataFrame(columns=['月份','D','P','R','M','Z'])
    df['月份'] = monthList
    temp = data.groupby(['工时月份','WBS类型']).agg({'实际人天':'sum'}).reset_index()

    for j in ['D', 'P', 'R', 'M', 'Z']:
        tempDf = temp[temp['WBS类型'] == j].reset_index(drop=True)
        for i in range(len(df)):
            for k in range(len(tempDf)):
                try:
                    if tempDf.loc[k,'工时月份'] == df.loc[i,'月份']:
                        df.loc[i,j] = tempDf.loc[k,'实际人天']
                except:
                    df.loc[i,j] = 0

    df = df.fillna(0)
    return df


def 历史资源总费用细分(dcp, sumResDf):
    monthList = list(set(dcp['资源月份']))
    df = pd.DataFrame(columns=['月份', 'DCP', 'OC', 'Diamond', 'GPU', '固资折旧'])
    df['月份'] = monthList
    for i in range(len(sumResDf)):
        try:
            sumResDf.loc[i,'类别'] = sumResDf.loc[i,'类别'].split('-')[0]
        except:
            pass

    for i in ['DCP', 'OC', 'Diamond', 'GPU', '固资折旧']:
        tempDf = sumResDf[sumResDf['类别'] == i].reset_index(drop=True)
        for j in range(len(df)):
            # for k in range(len(tempDf)):
            try:
                tempDf2 = tempDf[tempDf['month'] == df.loc[j,'月份']].reset_index(drop=True)
                df.loc[j, i] = tempDf2['费用(元)'].sum()
            except:
                df.loc[j, i] = 0

    df = df.fillna(0)
    return df



def wbs_top5_actual(data):
    data = data.sort_values(by='实际人天',ascending=False)
    data = data[~data['WBS类型'].isin(['Z'])].reset_index(drop=True).head(10)
    rate = 1
    for i in range(len(data)):
        data.loc[i, 'Rate'] = 'Top '+ str(int(rate))
        rate += 1
    data.insert(0, '项目名称', data.pop('项目名称'))
    data.insert(1, 'WBS所属部门', data.pop('WBS所属部门'))
    data.insert(2, 'PM姓名', data.pop('PM姓名'))
    data.insert(0, 'Rate', data.pop('Rate'))
    data.pop('WBS年份')
    return data



def wbs_top5_actualFilter(data):
    data = data.sort_values(by='实际人天',ascending=False)
    data = data[~data['WBS类型'].isin(['Z'])].reset_index(drop=True)
    rate = 1
    for i in range(len(data)):
        data.loc[i, 'Rate'] = 'Top '+ str(int(rate))
        rate += 1
    data.insert(0, '项目名称', data.pop('项目名称'))
    data.insert(1, 'WBS所属部门', data.pop('WBS所属部门'))
    data.insert(2, 'PM姓名', data.pop('PM姓名'))
    data.insert(0, 'Rate', data.pop('Rate'))
    data.pop('WBS年份')
    return data


def sku_to_PL111():
    data = 本月合并底表()
    data = data[data['员工所属部门'] == '创新孵化-冰箱'].reset_index(drop=True)
    data = data[data['实际人天'] > 0].reset_index(drop=True)
    return data[data['利润中心'] == 'PL111'].reset_index(drop=True)

def bzBill_top5():
    data = monthly_bz_cur.sort_values(by='费用（元）',ascending=True).reset_index(drop=True).head(10)
    rate = 1
    for i in range(len(data)):
        data.loc[i, 'Rate'] = 'Top '+ str(int(rate))
        rate += 1
    data = data[['Rate','业务线','任务ID','任务名称','创建人','创建时间','实际完成时间','预算单名称','利润中心','账单确认','费用（元）']]
    return data

def biaozhu_top5_distribution():
    data = monthly_bz_cur.sort_values(by='费用（元）',ascending=False).reset_index(drop=True).head(10)
    rate = 1
    for i in range(len(data)):
        data.loc[i, 'Rate'] = 'Top '+ str(int(rate))
        rate += 1
    others_act_days = biaozhuTask['费用（元）'].sum() - data['费用（元）'].sum()
    other_row = {'费用（元）':others_act_days,'Rate':'Others'}
    data = data.append(other_row, ignore_index=True)
    return data

def wbs_top5_distribution(data):
    curWBSData = data
    data = data.sort_values(by='实际人天',ascending=False)
    data = data[~data['WBS类型'].isin(['Z'])].reset_index(drop=True).head(10)
    rate = 1
    for i in range(len(data)):
        data.loc[i, 'Rate'] = 'Top '+ str(int(rate))
        rate += 1
    data.insert(4, 'PM姓名', data.pop('PM姓名'))
    data.insert(0, 'Rate', data.pop('Rate'))
    others_act_days = curWBSData['实际人天'].sum() - data['实际人天'].sum()
    other_row = {'项目名称':'非Top10WBS','实际人天':others_act_days,'Rate':'非Top10WBS'}
    data = data.append(other_row, ignore_index=True)
    return data

def wbs_top_distributionFilter(dataSource):
    data = dataSource.sort_values(by='实际人天',ascending=False)
    data = data[~data['WBS类型'].isin(['Z'])].reset_index(drop=True).head(10)
    rate = 1
    for i in range(len(data)):
        data.loc[i, 'Rate'] = 'Top '+ str(int(rate))
        rate += 1
    data.insert(4, 'PM姓名', data.pop('PM姓名'))
    data.insert(0, 'Rate', data.pop('Rate'))
    others_act_days = dataSource['实际人天'].sum() - data['实际人天'].sum()
    other_row = {'项目名称':'非Top10WBS','实际人天':others_act_days,'Rate':'非Top10WBS'}
    data = data.append(other_row, ignore_index=True)
    return data



def 固定资产top10(data, sortBy):
    data = data.sort_values([sortBy], ascending=False).reset_index(drop=True)
    top10Index = []
    for i in range(len(data)):
        if len(list(set(top10Index))) < 10:
            top10Index.append(data.loc[i,'实际保管人'])
        else:
            break
    # top10Name = list(set(data['实际保管人']))[:10]
    top10df = data[data['实际保管人'].isin(top10Index)]
    return top10df






def logic_rate_abnormal_tb_WBS(data):
    理论填报filterData = data[['WBS所属部门', '项目编号', '项目名称', 'WBS类型',  'PM姓名', '实际人天', '预估人天','预估填报率','预估填报']]
    理论填报filterData = 理论填报filterData[~理论填报filterData['WBS类型'].isin(['Z'])]
    理论填报filterData = 理论填报filterData[理论填报filterData['实际人天'] > 0 ]
    return 理论填报filterData[~理论填报filterData['预估填报'].str.contains('合理')]

# def less_1_yr_wbs(data):
#     now = datetime.now().date() - timedelta(days=365)
#     less_one_yr = []
#     for i in range(len(data)):
#         wbs_date = datetime(2000 + data.loc[i, 'WBS年份'], data.loc[i, 'WBS月份'], 1).date()
#         if now > wbs_date:
#             less_one_yr.append(i)
#     return less_one_yr

def wbs_abg(df, value):
    data = df[df['实际人天'] > 0]
    data = data[~data['WBS类型'].isin(['Z'])]
    data = data[~data['WBS所属部门'].isin(['智慧娱乐', '中东云平台', '海外研发中心',"海外智能终端与应用","新零售业务",'创新业务部'])]
    temp = []
    for i, row in data.iterrows():
        if row['项目编号'][2:4] == value:
            temp.append(i)
    return data.loc[temp]

def get_wbs_list(df, reName):
    last = df[df['WBS类型'] !='Z'].rename(columns={'预估人天':reName})
    last = last[last['实际人天'] == 0]
    return list(last['项目编号'])

def find_common(list1, list2):
    common = []
    for i in list1:
        if i in (list2):
            common.append(i)
    return common

def est_twice_wbs():
    last = 上月WBS维度.rename(columns={'预估人天':'上月预估'})
    cur = 本月WBS维度.rename(columns={'预估人天': '本月预估'})
    cur_wbs_list = get_wbs_list(本月WBS维度, '本月预估')
    last_wbs_list = get_wbs_list(上月WBS维度, '上月预估')
    common = find_common(cur_wbs_list, last_wbs_list)
    last_common = last[last['项目编号'].isin(common)].reset_index(drop=True)
    cur_common = cur[cur['项目编号'].isin(common)].reset_index(drop=True)
    for i in range(len(last_common)):
        for j in range(len(cur_common)):
            if last_common.loc[i, '项目编号'] == cur_common.loc[j, '项目编号']:
                last_common.loc[i, '本月预估'] = cur_common.loc[j, '本月预估']
    try:
        data = last_common[['项目编号', '项目名称', 'PM姓名', '上月预估', '本月预估']]
        return data
    except:
        return pd.DataFrame()

def checkDfNone(df):
    if len(df) >  0:
        return df
    else:
        return None


def not_fill_workHour_twice():
    cur = 本月未填工时名单()
    last = 上月未填工时名单()
    cur_no_list = list(cur['员工姓名'])
    last_no_list = list(last['员工姓名'])
    common = find_common(cur_no_list,last_no_list)
    # cur_common = cur[cur['员工姓名'].isin(common)].reset_index(drop=True)
    for j in range(len(cur)):
        if cur.loc[j, '员工姓名'] in common:
            cur.loc[j, '未填次数'] = '2'
        else:
            cur.loc[j, '未填次数'] = '1'
    return cur.sort_values(by=['未填次数','员工组'],ascending=False).reset_index(drop=True)[['员工姓名', '员工组', '员工所属部门', '业务线', '工作地点', '岗位名称', '资源池','未填次数']]

def expires_morethan_a_year(date_str):
    """date_str format must be like this: 09/25/2022"""
    contract_end_date = datetime.strptime(date_str, "%d/%m/%Y")
    today = datetime.now()
    one_year = timedelta(days=365)
    one_year_within = today - one_year
    return contract_end_date < one_year_within

# def get_more_than1yr_wbs():
#     data = 本月WBS维度[['项目编号','项目名称','WBS所属部门','WBS年份','WBS月份']].reset_index(drop = True)
#     more_than1yr = []
#     for i in range(len(data)):
#         month = int(data.loc[i,'WBS月份'])
#         if month == 0:
#             month = 10
#         year = data.loc[i,'WBS年份']
#         if expires_morethan_a_year(str(month)+'/1/20'+str(int(year))) == True:
#             more_than1yr.append(i)
#     return data.loc[more_than1yr].drop_duplicates().reset_index(drop = True)

def act_no_est_df():
    data = 本月WBS维度
    data = data[data['预估人天'] == 0]
    data = data[~data['WBS类型'].isin(['Z'])]
    if len(data) > 0:
        return data[['项目编号', '项目名称', 'PM姓名', '实际人天','预估人天']]
    else:
        return pd.DataFrame()

def est_no_act_df():
    data = 本月WBS维度
    data = data[data['实际人天'] == 0]
    data = data[~data['WBS类型'].isin(['Z'])]
    if len(data) > 0:
        return data[['项目编号', '项目名称', 'PM姓名', '实际人天','预估人天']]
    else:
        return pd.DataFrame()

# def clean_gpu_usage():
#     gpu_df = 历史GPU使用情况()
#     gpu_df.columns = ['日期', '时间', '分区', '使用量']
#     gpu_df = gpu_df[gpu_df['分区'] != 'Util%'].reset_index(drop=True)
#     gpu_df['分区'] = gpu_df['分区'].str.replace('IRDCSG', 'SG2/IRDCSG')
#     gpu_df['分区'] = gpu_df['分区'].str.replace('vi_irdc', 'ABUD/vi_irdc')
#     gpu_df['分区'] = gpu_df['分区'].str.replace('IRDC_Share', 'SH40/IRDC_Share')
#     gpu_df['分区'] = gpu_df['分区'].str.replace('IRDC_A100_40G', 'SH1024/IRDC_A100_40G')
#     gpu_df['分区'] = gpu_df['分区'].str.replace('IRDC_V100_16G', 'SH1988/IRDC_V100_16G')
#     gpu_df['分区'] = gpu_df['分区'].str.replace('IRDC_1080Ti', 'SH40/IRDC_1080Ti')
#
#     for i in range(len(gpu_df)):
#         gpu_df.loc[i, 'year'] = gpu_df.loc[i, '日期'].split('/')[0]
#         gpu_df.loc[i, 'month'] = gpu_df.loc[i, '日期'].split('/')[1]
#     for i in range(len(gpu_df)):
#         gpu_df.loc[i, 'Time'] = gpu_df.loc[i, '时间'][0:2]
#         gpu_df.loc[i, 'Used'] = gpu_df.loc[i, '使用量'].split("/")[0]
#         gpu_df.loc[i, 'All'] = gpu_df.loc[i, '使用量'].split("/")[1]
#
#     # caculate usage percentage
#     for i in range(len(gpu_df)):
#         gpu_df.loc[i, '使用率'] = round(int(gpu_df.loc[i, 'Used']) / int(gpu_df.loc[i, 'All']) * 100, 2)
#
#     gpu_df[["year", "month", 'Time', 'Used', 'All']] = gpu_df[["year", "month", 'Time', 'Used', 'All']].apply(pd.to_numeric)
#     return gpu_df.reset_index(drop=True)
#     # return gpu_df[gpu_df['Time'].isin([10, 14, 18, 22])].reset_index(drop=True)

def clean_gpu_avg_usage():
    gpu_df_per_day = 历史GPU使用情况().groupby(['日期', '分区']).agg({'使用率': 'sum', '时间': 'count'}).reset_index()
    for i in range(len(gpu_df_per_day)):
        gpu_df_per_day.loc[i, '使用率'] = round(
            gpu_df_per_day.loc[i, '使用率'] / gpu_df_per_day.loc[i, '时间'], 2)
    return gpu_df_per_day

def monthly_gpu():
    data = 历史GPU用户使用情况()
    data = data[data['year'] == 本年()]
    data = data[data['month'] == 本月()].reset_index(drop=True)
    data = data[['用户','分区','员工组','员工所属部门','资源池','岗位名称',
                 '日期','Time','使用节点数','累计使用时长']].sort_values(by=['累计使用时长']).sort_values(by=['使用节点数'], ascending=True).reset_index(drop=True)
    return data

def monthly_gpu资源池(data):
    data = data[data['year'] == 本年()]
    data = data[data['month'] == 本月()].reset_index(drop=True)
    data = data[['用户','分区','员工组','员工所属部门','资源池','岗位名称',
                 '日期','Time','使用节点数','累计使用时长']].sort_values(by=['累计使用时长']).sort_values(by=['使用节点数'], ascending=True).reset_index(drop=True)
    return data

def gpu_avg_sum_nodes(data):
    return data.groupby(['日期','分区']).agg({'使用节点数': 'sum'}).reset_index()


def gpu_avg_sum_time(data):
    return data.groupby(['日期','分区']).agg({'累计使用时长': 'sum'}).reset_index()


def clean_gpu_avg_sum_nodes(data):
    data = data.groupby(['用户','员工组','员工所属部门','资源池','岗位名称']).agg({'使用节点数': 'sum'}).reset_index()
    data['使用节点数'] = data['使用节点数'].apply(lambda r: np.round(r, decimals=2))
    return data.sort_values(by=['使用节点数'], ascending=True).reset_index(drop=True)

def clean_gpu_avg_sum_time(data):
    data = data.groupby(['用户','员工组','员工所属部门','资源池','岗位名称']).agg({'累计使用时长': 'sum'}).reset_index()
    data['累计使用时长'] = data['累计使用时长'].apply(lambda r: np.round(r, decimals=2))
    return data.sort_values(by=['累计使用时长'], ascending=True).reset_index(drop=True)

def clean_固定资产top10(data, sumValue):
    data = data.groupby(['实际保管人','员工组','员工所属部门','资源池','岗位名称','设备类型','资产状态','用途']).agg({sumValue: 'sum'}).reset_index()
    data[sumValue] = data[sumValue].apply(lambda r: np.round(r, decimals=2))
    return data.sort_values(by=[sumValue], ascending=False).reset_index(drop=True)

def clean_gpu_user(list):
    data = 历史GPU用户使用情况()
    data = data[data['员工所属部门'].isin(list)].reset_index(drop=True)
    data = data.groupby(['日期','用户']).agg({'累计使用时长': 'sum','使用节点数': 'sum' }).reset_index()
    data['日期'] = pd.to_datetime(data['日期'], format='%Y/%m/%d')
    data = data.sort_values(by=['日期']).reset_index(drop=True)
    return data

def gpu_monthly_df(year, month):
    return 历史GPU使用情况().loc[(历史GPU使用情况()['year'] == year) & (历史GPU使用情况()['month'] == month)].reset_index(drop =True)

def gpu_monthly_usage(year, month, cardName):
    try:
        gpu_monthly_per_card = gpu_monthly_df(year, month).groupby(['分区']).agg({'Used': 'sum', 'All': 'sum'}).reset_index()
        for i in range(len(gpu_monthly_per_card)):
            gpu_monthly_per_card.loc[i, '使用率'] = round(
                int(gpu_monthly_per_card.loc[i, 'Used']) / int(gpu_monthly_per_card.loc[i, 'All']) * 100, 2)
        return round(gpu_monthly_per_card[gpu_monthly_per_card['分区'] == cardName].reset_index(drop=True)['使用率'][0],1)
    except:
        return None

def gpu_monthly_usage_time(year, month, cardName, time):
    try:
        gpu_monthly_per_card = gpu_monthly_df(year, month).groupby(['分区','Time']).agg({'Used': 'sum', 'All': 'sum'}).reset_index()
        for i in range(len(gpu_monthly_per_card)):
            gpu_monthly_per_card.loc[i, '使用率'] = round(
                int(gpu_monthly_per_card.loc[i, 'Used']) / int(gpu_monthly_per_card.loc[i, 'All']) * 100, 2)
        return round(gpu_monthly_per_card.loc[(gpu_monthly_per_card['分区'] == cardName) & (gpu_monthly_per_card['Time'] == time)].reset_index(drop=True)['使用率'][0],1)
    except:
        return None

def monthly_bzcj(df, numMon):
    # monthly report
    month_index = []
    df['创建时间'] = pd.to_datetime(df['创建时间'],format = '%Y/%m/%d')
    for i in range(len(df)):
        if df.loc[i, '创建时间'].month == datetime.date.today().month - numMon:
            month_index.append(i)

    NewMon标注Task_df = df.iloc[month_index].reset_index(drop=True)
    if len(NewMon标注Task_df) == 0:
        NewMon标注Task_df = pd.DataFrame()
    else:
        NewMon标注Task_df['数据量（张）'] = NewMon标注Task_df['数据量（张）'].fillna(0)
        NewMon标注Task_df['任务状态'] = NewMon标注Task_df['任务状态'].astype(taskSorterBZ)
        NewMon标注Task_df = NewMon标注Task_df.sort_values(by=['任务状态', '创建时间']).reset_index(drop=True)

    if len(NewMon标注Task_df) < 1:
        NewMon标注Task_df = pd.DataFrame(columns = ['Rate','业务线','任务ID','任务名称','任务状态','创建人',
                                                    '创建时间','实际完成时间','预算单名称','利润中心','账单确认',
                                                    '费用（元）','是否有数据包被打回','任务延期时长/天','预计完成时间'])
        NewMon标注Task_df['业务线'] = 'DX'
        NewMon标注Task_df['任务状态'] = '任务完成'
        NewMon标注Task_df['创建人'] = '无数据'
        NewMon标注Task_df['是否有数据包被打回'] = False
    return NewMon标注Task_df

biaozhuTask = 标注任务()
caijiTask = 采集任务()
budgetDf = 预算单()
monthly_bz_cur = monthly_bzcj(biaozhuTask, 1)
monthly_bz_last = monthly_bzcj(biaozhuTask, 2)
monthly_cj_cur = monthly_bzcj(caijiTask, 1)
monthly_cj_last = monthly_bzcj(caijiTask, 2)

def tryExcept0(data):
    temp = data
    try:
        temp = data
    except KeyError as ke:
        temp = 0
    return temp

def tryExceptNone(data):
    temp = data
    try:
        temp = data
    except KeyError as ke:
        temp = None
    return temp

def try0toNone(data):
    try:
        if data == 0:
            temp = None
        else:
            temp = data
    except KeyError as ke:
        temp = None
    return temp

def tryNoneto0(data):
    try:
        if data == None:
            temp = 0
        else:
            temp = data
    except KeyError as ke:
        temp =0
    return temp

def try0Divi0(data1, data2):
    try:
        temp = data1/data2
    except ZeroDivisionError as ze:
        temp = 0
    return temp




cat_size_order = CategoricalDtype(
    ['不满', '超载', '合理'],
    ordered=True
)

def groupByWBS(data):
    # remove staff not countable
    try:
        actual_per_wbs_groupby = data.groupby(['项目编号','项目名称','PM姓名','利润中心','WBS所属部门', 'WBS类型','WBS所属业务线']).agg(
            {'实际人天': 'sum', '预估人天': 'sum'}).reset_index().copy()
        for i in range(len(actual_per_wbs_groupby)):
            actual_per_wbs_groupby.loc[i, 'WBS年份'] = actual_per_wbs_groupby.loc[i, '项目编号'][4:6]
    except:
        pass

    try:
        for i in range(len(actual_per_wbs_groupby)):
            actual_per_wbs_groupby.loc[i, '预估填报率'] = actual_per_wbs_groupby.loc[i, '实际人天'] / \
                                                          actual_per_wbs_groupby.loc[i, '预估人天'] * 100
    except:
        pass

    try:
        if actual_per_wbs_groupby.loc[i, '预估填报率'] == np.inf:
            actual_per_wbs_groupby.loc[i, '预估填报率'] = 0
    except:
        pass

    for j in range(len(actual_per_wbs_groupby)):
        if actual_per_wbs_groupby.loc[j, '预估填报率'] < estimate_min:
            actual_per_wbs_groupby.loc[j, '预估填报'] = '不满'
        elif actual_per_wbs_groupby.loc[j, '预估填报率'] > estimate_max:
            actual_per_wbs_groupby.loc[j, '预估填报'] = '超载'
        else:
            actual_per_wbs_groupby.loc[j, '预估填报'] = '合理'

    try:
        actual_per_wbs_groupby['预估填报'] = actual_per_wbs_groupby['预估填报'].astype(cat_size_order)
        actual_per_wbs_groupby = actual_per_wbs_groupby.sort_values(['预估填报']).reset_index(drop=True)
    except:
        pass

    actual_per_wbs_groupby = actual_per_wbs_groupby.round(decimals=1)
    actual_per_wbs_groupby = actual_per_wbs_groupby.replace(np.inf, 0)

    for i in range(len(actual_per_wbs_groupby)):
        if actual_per_wbs_groupby.loc[i, 'WBS类型'] == 'Z':
            actual_per_wbs_groupby.loc[i, 'WBS年份'] = str(datetime.date.today().year)[2:4]

    for i in range(len(actual_per_wbs_groupby)):
        if pd.isna(actual_per_wbs_groupby.loc[i, 'WBS所属部门']):
            if actual_per_wbs_groupby.loc[i, '项目编号'][2:4] == 'IB':
                actual_per_wbs_groupby.loc[i, 'WBS所属部门'] = '中东云平台'
            if actual_per_wbs_groupby.loc[i, '项目编号'][2:4] == 'AB':
                actual_per_wbs_groupby.loc[i, 'WBS所属部门'] = '亚太云平台'
            if actual_per_wbs_groupby.loc[i, '项目编号'][2:4] == 'SC':
                actual_per_wbs_groupby.loc[i, 'WBS所属部门'] = '创新业务部'

    for i in range(len(actual_per_wbs_groupby)):
        if pd.isna(actual_per_wbs_groupby.loc[i, 'WBS所属部门']) or pd.isnull(
                actual_per_wbs_groupby.loc[i, 'WBS所属部门']):
            actual_per_wbs_groupby.loc[i, 'WBS所属部门'] = '未知'

    # actual_per_wbs_groupby.insert(8, '利润中心', actual_per_wbs_groupby.pop('利润中心'))
    # actual_per_wbs_groupby.insert(8, '实际人天', actual_per_wbs_groupby.pop('实际人天'))
    # actual_per_wbs_groupby.insert(8, '预估人天', actual_per_wbs_groupby.pop('预估人天'))
    # actual_per_wbs_groupby.insert(8, '预估填报率', actual_per_wbs_groupby.pop('预估填报率'))
    # actual_per_wbs_groupby.insert(8, '预估填报', actual_per_wbs_groupby.pop('预估填报'))
    # actual_per_wbs_groupby.insert(7, 'PM姓名', actual_per_wbs_groupby.pop('PM姓名'))

    try:
        actual_per_wbs_groupby['预估填报'] = actual_per_wbs_groupby['预估填报'].astype(cat_size_order)
        actual_per_wbs_groupby = actual_per_wbs_groupby.sort_values(['预估填报']).reset_index(drop=True)
    except:
        pass

    actual_per_wbs_groupby = actual_per_wbs_groupby.drop_duplicates().reset_index(drop=True)
    actual_per_wbs_groupby = actual_per_wbs_groupby[actual_per_wbs_groupby['实际人天'] > 0].reset_index(drop=True)
    actual_per_wbs_groupby = actual_per_wbs_groupby.sort_values(['实际人天'], ascending=False).reset_index(drop=True)
    return actual_per_wbs_groupby


def renameDf(data):
    for i in range(len(data)):
        data.loc[i,'项目名称'] = data.loc[i,'项目名称'][0:26]
    return data



def addWBSNotAcitve(df, wbsDf, year, month):
    if month == 1:
        monthList = [10,11,12,month]
        yearList = [year-1, year]
    elif month == 2:
        monthList = [11, 12,1,month]
        yearList = [year - 1, year]
    elif month == 3:
        monthList = [12, 1,2,month]
        yearList = [year - 1, year]
    else:
        monthList = [month-3, month-2, month-1,month]
        yearList = [year]
    wbsDf = wbsDf[(wbsDf['工时年份'].isin(yearList)) & (wbsDf['工时月份'].isin(monthList))].reset_index(drop=True)
    for i in range(len(df)):
        for j in range(len(wbsDf)):
            if df.loc[i,'项目名称'] == wbsDf.loc[j,'项目名称']:
                df.loc[i,'WBS未活跃时长'] = wbsDf.loc[j,'WBS未活跃时长']
    return df


def data_back_biaozhu():
    data = monthly_bz_cur[monthly_bz_cur['是否有数据包被打回'] == True].reset_index(drop=True)
    data = data[['业务线','任务ID','任务名称','创建人','预算单名称','利润中心','账单确认','费用（元）']]
    return data

def data_delay_biaozhu():
    data = monthly_bz_cur[monthly_bz_cur['任务延期时长/天'] >= 5].reset_index(drop=True)
    data = data[['业务线','任务ID','任务名称','创建人','创建时间','预计完成时间','实际完成时间','账单确认','费用（元）']]
    return data

def sortWBS(data):
    wbsSorterReverse = CategoricalDtype(
        [ 'Z','M', 'R',  'P','D',],
        ordered=True
    )
    data['WBS类型'] = data['WBS类型'].astype(wbsSorterReverse)
    data = data.sort_values(by=['WBS类型','实际人天'], ascending=False).reset_index(drop=True)
    return data

def filDataApartment(data, bl):
    return data[data['员工所属部门'] == bl].reset_index(drop=True)


def blGroupByTitle(data, tbHeader, title):
    try:
        groupbyData = data.groupby([tbHeader]).agg({'实际人天': 'sum'}).reset_index()
        num = groupbyData[groupbyData[tbHeader] == title].reset_index(drop=True)['实际人天'][0]
        if num == 0:
            num = None
        return num
    except KeyError as ke:
        return None


def blGroupByzhejiu(data, tbHeader, title):
    try:
        groupbyData = data.groupby([tbHeader]).agg({'折旧': 'sum'}).reset_index()
        num = groupbyData[groupbyData[tbHeader] == title].reset_index(drop=True)['折旧'][0]
        if num == 0:
            num = None
        return num
    except KeyError as ke:
        return None

def blGroupByResFee(data, tbHeader, title):
    try:
        groupbyData = data.groupby([tbHeader]).agg({'费用(元)': 'sum'}).reset_index()
        num = groupbyData[groupbyData[tbHeader] == title].reset_index(drop=True)['费用(元)'][0]
        if num == 0:
            num = None
        return num
    except KeyError as ke:
        return None


def blGroupBygeshu(data, tbHeader, title):
    try:
        groupbyData = data.groupby([tbHeader]).agg({'资产代码': 'count'}).reset_index()
        num = groupbyData[groupbyData[tbHeader] == title].reset_index(drop=True)['资产代码'][0]
        if num == 0:
            num = None
        return num
    except KeyError as ke:
        return None



def blGroupByTitle2(data, tbHeader, title):
    data = data[data['利润中心'] == 'PL111'].reset_index(drop=True)
    try:
        groupbyData = data.groupby([tbHeader]).agg({'实际人天': 'sum'}).reset_index()
        num = groupbyData[groupbyData[tbHeader] == title].reset_index(drop=True)['实际人天'][0]
        if num == 0:
            num = None
        return num
    except KeyError as ke:
        return None

def blGroupByFilter(data, filter, tbHeader):
    try:
        groupbyData = data[~data[tbHeader].isin([filter])].reset_index(drop=True)
        num = groupbyData['实际人天'].sum()
        if num == 0:
            num = None
        return num
    except KeyError as ke:
        return None


def returnWBS_Bl_act(df, value):
    try:
        indicator = round(df[df['WBS类型'] == value]['实际人天'].sum(),1)
        if indicator == 0:
            indicator = None
    except:
        indicator = None
    return indicator

def blGroupByTitlePer(GroupData, blData):
    try:
        num = int(GroupData/blData['实际人天'].sum()*100)
        if num == 0:
            num = None
        return num
    except:
        return None

def df0Beautfy(data):
    return data.replace([0], '-')



def dcppie(data, type):
    dcppie = data[["费用(元)", type]]
    data =  dcppie.groupby(type, as_index=False).agg({ '费用(元)': 'sum'}).reset_index(drop=True)
    return data


def dcpTop10(data):
    top10df = data.groupby('用户名', as_index=False).agg({'费用(元)':'sum'}).reset_index(drop=True)
    top10List = top10df.sort_values(by=['费用(元)'], ascending=False).reset_index(drop=True).head(10)['用户名']
    df = data[data['用户名'].isin(top10List)].reset_index(drop=True).sort_values(by=['费用(元)'], ascending=False).reset_index(drop=True)
    return df


def resAllDfGetCol(资产, lustre, ceph, oc, diamond, gpuUser, gpuFee):
    办公资产df = 资产[资产['用途'] == '办公'].reset_index(drop=True)
    办公资产df = 办公资产df[['员工所属部门', '资源池', '员工组', '岗位名称', '实际保管人', '折旧', '资产月份']]
    for i in range(len(办公资产df)):
        办公资产df.loc[i,'类别'] = '固资折旧-办公'
    项目资产df = 资产[资产['用途'] == '项目'].reset_index(drop=True)
    项目资产df = 项目资产df[['员工所属部门', '资源池', '员工组', '岗位名称', '实际保管人', '折旧', '资产月份']]
    for i in range(len(项目资产df)):
        项目资产df.loc[i,'类别'] = '固资折旧-项目'
    资产df = 办公资产df.append(项目资产df, ignore_index = True)
    资产df = 资产df.rename(columns={'折旧':'费用(元)', '资产月份':'month', "实际保管人":"用户名"})


    lustreDf = lustre[['员工所属部门', '资源池', '员工组', '岗位名称', '用户名','费用(元)', '资源月份']]
    for i in range(len(lustreDf)):
        lustreDf.loc[i,'类别'] = 'DCP-lustre'
    cephDf = ceph[['员工所属部门', '资源池', '员工组', '岗位名称', '用户名', '费用(元)', '资源月份']]
    for i in range(len(cephDf)):
        cephDf.loc[i,'类别'] = 'DCP-ceph'
    ocDf = oc[['员工所属部门', '资源池', '员工组', '岗位名称', '用户名','费用(元)', '资源月份']]
    for i in range(len(ocDf)):
        ocDf.loc[i,'类别'] = 'OC'
    diamondDf = diamond[['员工所属部门', '资源池', '员工组', '岗位名称', '用户名', '费用(元)', '资源月份']]
    for i in range(len(diamondDf)):
        diamondDf.loc[i,'类别'] = 'Diamond'
    资源df = lustreDf.append(cephDf, ignore_index=True).append(ocDf, ignore_index=True).append(diamondDf, ignore_index=True)


    a100df = gpuUser[gpuUser['分区'] == "SH1024/IRDC_A100_40G"].reset_index(drop=True)
    v100df = gpuUser[gpuUser['分区'] == "SH1988/IRDC_V100_16G"].reset_index(drop=True)
    ti1080df = gpuUser[gpuUser['分区'] == "SH40/IRDC_1080Ti"].reset_index(drop=True)
    def groupByGpu(data, type, gpuGroup):
        gpuUserA100 = data.groupby(['员工所属部门', '资源池', '员工组', '岗位名称', 'month', "用户"]).agg({"使用节点数": 'sum'}).reset_index()
        for i in range(len(gpuUserA100)):
            month = gpuUserA100.loc[i,'month']
            sumFee = gpuFee[(gpuFee['month'] == month) & (gpuFee['分区'] == gpuGroup)]['总价'].sum()
            gpuUserA100.loc[i,'费用(元)'] = round(int(gpuUserA100.loc[i,'使用节点数'])/int(gpuUserA100['使用节点数'].sum()) * sumFee,2)
        for i in range(len(gpuUserA100)):
            gpuUserA100.loc[i, '类别'] = type
        gpuUserA100 = gpuUserA100.rename(columns={"用户": "用户名"})
        return gpuUserA100
    gpuUserA100 = groupByGpu(a100df, 'GPU-A100', "SH1024/IRDC_A100_40G")
    gpuUserV100 = groupByGpu(v100df, 'GPU-V100', "SH1988/IRDC_V100_16G")
    gpuUser1080Ti = groupByGpu(ti1080df, 'GPU-1080Ti', "SH40/IRDC_1080Ti")
    gpuDf = gpuUserA100.append(gpuUserV100, ignore_index =True).append(gpuUser1080Ti, ignore_index=True)

    sumDf = 资产df.append(资源df, ignore_index =True).append(gpuDf, ignore_index=True).iloc[:, 0:-2]
    sumDf = sumDf.dropna().reset_index(drop=True)
    sumDf = sumDf[sumDf['费用(元)'] > 0].reset_index(drop=True)
    sumDf['month'] = sumDf['month'].astype(int)
    return sumDf