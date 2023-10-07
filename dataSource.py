# modify value below before deploy the web page
import pathlib
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import openpyxl
from pandas.api.types import CategoricalDtype
import openpyxl


# def getCurLastMonDf(df, yearCol, monCol):
#     try:
#         df[monCol] = df[monCol].astype(int)
#         df[yearCol] = df[yearCol].astype(int)
#     except:
#         pass
#     curYear = df[yearCol].max()
#     curMon = df[df['工时年份'] == curYear].reset_index(drop=True)[monCol].max()
#
#     if curMon == 1:
#         lastMon = 12
#         lastYear = curYear - 1
#     else:
#         lastMon = curMon - 1
#         lastYear = curYear
#
#     lastMonDf = df[(df[monCol] == lastMon) & (df[monCol] == lastYear)].reset_index(drop=True)
#     curMonDf = df[(df[monCol] == curMon) & (df[monCol] == curYear)].reset_index(drop=True)
#
#     return lastMonDf, curMonDf


def getCurLastMonDf(df, value, value2):
    curYear = value
    curMon = value2
    if curMon == 1:
        lastMon = 12
        lastYear = curYear - 1
    else:
        lastMon = curMon - 1
        lastYear = curYear
    lastMonDf = df[(df['工时月份'] == lastMon) & (df['工时年份'] == lastYear)].reset_index(drop=True)
    curMonDf = df[(df['工时月份'] == curMon) & (df['工时年份'] == curYear)].reset_index(drop=True)
    return lastMonDf, curMonDf


# 把下面的数字改成更新的日期时间（工时）
def 本月():
    return 8

def 上月():
    return 7

def 本年():
    return 2023

def 上年():
    return 2023

def 国内全勤人天():
    return str(23)
def 新加坡全勤人天():
    return str(22)


def 人员维度更新时间():
    return str("from 2023/7/26 to 2023/8/25")




# 把下面的数字改成更新的日期时间（固定资产）
def 资产本年():
    return 2023

def 资产上年():
    return 2023

def 资产本月():
    return 6

def 资产上月():
    return 5

def 固定资产更新时间():
    return str("2023/6月账单")



# 把下面的数字改成更新的日期时间（gpu同数据采标）
def gpu本年():
    return 2023

def gpu上年():
    return 2023

def gpu本月():
    return 6

def gpu上月():
    return 5

def GPU使用更新时间():
    return str("2023/6月账单")

def 数据采标更新时间():
    return GPU使用更新时间()  # 同gpu更新时间



# 把下面的数字改成更新的日期时间（dcp oc）
def dcp本年():
    return 2023

def dcp上年():
    return 2023

def dcp本月():
    return 6

def dcp上月():
    return 5


def OC存储更新时间():
    return str("2023/6月账单")

def DCP存储更新时间():
    return OC存储更新时间() # 同dcp时间






# 以下不用调整

def openxl(path):
    return openpyxl.load_workbook(path)

def readData(fileName):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("assets/data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(fileName))

def readCBData(fileName):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("assets/data/数据采标").resolve()
    temp = pd.read_csv(DATA_PATH.joinpath(fileName))
    for i in range(len(temp)):
        try:
            temp.loc[i,'创建时间'] = pd.to_datetime(np.array(temp.loc[i,"创建时间"], dtype='datetime64[s]').item()).date()
        except:
            pass
        try:
            temp['预计完成时间'] = pd.to_datetime(np.array(temp.loc[i,"预计完成时间"], dtype='datetime64[s]').item()).date()
        except:
            pass
        try:
            temp['实际完成时间'] = pd.to_datetime(np.array(temp.loc[i,"实际完成时间"], dtype='datetime64[s]').item()).date()
        except:
            pass

    return temp

def readhistroyData(fileName, sheetName):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("assets/data").resolve()
    return pd.read_excel(DATA_PATH.joinpath(fileName), sheet_name=sheetName)
def 工时历史总表汇总():
    return 'IRDC工时历史总表汇总.xlsx'


合并底表 = readhistroyData(工时历史总表汇总(), '合并底表')
人员维度 = readhistroyData(工时历史总表汇总(), '人员维度')
WBS维度 = readhistroyData(工时历史总表汇总(), 'WBS维度')
员工组维度 = readhistroyData(工时历史总表汇总(), '员工组维度')
WBS所属部门维度 = readhistroyData(工时历史总表汇总(), 'WBS所属部门维度')
岗位名称维度 = readhistroyData(工时历史总表汇总(), '岗位名称维度')
历史资源池维度 = readhistroyData(工时历史总表汇总(), '资源池维度')
业务线维度 = readhistroyData(工时历史总表汇总(), '业务线维度')
员工所属部门维度 = readhistroyData(工时历史总表汇总(), '员工所属部门维度')
未填工时名单 = readhistroyData(工时历史总表汇总(), '未填工时名单')
入离职名单 = readhistroyData(工时历史总表汇总(), '入离职名单')





def 本月人员维度():
    data = 人员维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 上月人员维度():
    data = 人员维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data


def 本月人员维度细化(colHead, name):
    data = 人员维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()]
    data = data[data[colHead] ==  name].reset_index(drop=True)
    return data

def 上月人员维度细化(colHead, name):
    data = 人员维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data



def 本月WBS维度():
    data = WBS维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 上月WBS维度():
    data = WBS维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data

def 本月WBS维度细化(colHead, name):
    data = WBS维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data

def 上月WBS维度细化(colHead, name):
    data = WBS维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data


def 本月未填工时名单():
    data = 未填工时名单
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 上月未填工时名单():
    data = 未填工时名单
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data

def 本月未填工时名单细化(colHead, name):
    data = 未填工时名单
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data

def 上月未填工时名单细化(colHead, name):
    data = 未填工时名单
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data


def 本月业务线维度():
    data = 业务线维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 上月业务线维度():
    data = 业务线维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data

def 资源池维度():
    data = 历史资源池维度
    return data


def 本月资源池维度():
    data = 历史资源池维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data
def 上月资源池维度():
    data = 历史资源池维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data

def 岗位维度():
    data = 岗位名称维度
    return data

def 本月岗位名称维度():
    data = 岗位名称维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data
#
def 上月岗位名称维度():
    data = 岗位名称维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data

def 员工部门维度():
    data = 员工所属部门维度
    return data

def 本月员工所属部门维度():
    data = 员工所属部门维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 上月员工所属部门维度():
    data = 员工所属部门维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data


def 本月业务线员工组():
    data = 员工组维度
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 上月业务线员工组():
    data = 员工组维度
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data


def 本月入离职名单():
    data = 入离职名单
    data['时间'] = pd.to_datetime(data['时间']).apply(lambda x: x.date())
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 本月合并底表():
    data = 合并底表
    data = data[data['资源池'] != 0]
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()].reset_index(drop=True)
    return data

def 上月合并底表():
    data = 合并底表
    data = data[data['资源池'] != 0]
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()].reset_index(drop=True)
    return data


def 本月入离职名单细化(colHead, name):
    data = 入离职名单
    data['时间'] = pd.to_datetime(data['时间']).apply(lambda x: x.date())
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data

def 本月合并底表细化(colHead, name):
    data = 合并底表
    data = data[data['资源池'] != 0]
    data = data[data['工时年份'] == 本年()]
    data = data[data['工时月份'] == 本月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data

def 上月合并底表细化(colHead, name):
    data = 合并底表
    data = data[data['资源池'] != 0]
    data = data[data['工时年份'] == 上年()]
    data = data[data['工时月份'] == 上月()]
    data = data[data[colHead] == name].reset_index(drop=True)
    return data

def 本月固定资产():
    df = 历史固定资产总表()
    data = df[df['资产月份'] == 资产本月()]
    data = data[data['资产年份'] == 资产本年()].reset_index(drop=True)
    data['总值'] = data['总值'].astype(int)
    data['净值'] = data['净值'].astype(int)
    data['折旧'] = data['折旧'].astype(int)
    return data

def 上月固定资产():
    df = 历史固定资产总表()
    data = df[df['资产月份'] == 资产上月()]
    data = data[data['资产年份'] == 资产上年()].reset_index(drop=True)
    data['总值'] = data['总值'].astype(int)
    data['净值'] = data['净值'].astype(int)
    data['折旧'] = data['折旧'].astype(int)
    return data


def 本月dcp():
    data = 历史dcp()
    data = data[data['资源年份'] == dcp本年()]
    data = data[data['资源月份'] == dcp本月()].reset_index(drop=True)
    return data

def 上月dcp():
    data = 历史dcp()
    data = data[data['资源年份'] == dcp上年()]
    data = data[data['资源月份'] == dcp上月()].reset_index(drop=True)
    return data


def 历史dcp():
    dfLustre = 历史dcpLustre()[['用户名','集群名称','存储类型(SSD/HDD)','用户已使用(TB)','业务线','员工所属部门',
                          '资源池','岗位名称','员工组','费用(元)','费用占比(个人/部门)','费用占比(个人/集群)',
                          '费用占比(个人/存储类型)','资源年份','资源月份','dcp类别','dcpID']]
    dfCeph = 历史dcpCeph()[['用户名','集群名称','存储类型(SSD/HDD)','用户已使用(TB)','业务线','员工所属部门',
                          '资源池','岗位名称','员工组','费用(元)','费用占比(个人/部门)','费用占比(个人/集群)',
                          '费用占比(个人/存储类型)','资源年份','资源月份','dcp类别','dcpID']]
    data = dfLustre.append(dfCeph)
    data['资源月份'] = data['资源月份'].astype('int')
    data['资源年份'] = data['资源年份'].astype('int')
    return data.reset_index(drop=True)





def 历史部门实际人均人天():
    return readData('历史部门实际人均人天.csv')

def 历史部门理论填报率():
    return readData('历史部门理论填报率.csv')


def 历史WBS类型实际人天():
    return readData('历史WBS类型实际人天.csv')

def 历史GPU使用情况():
    return readData('历史gpu使用率.csv')


def 历史GPU用户使用情况():
    return readData('历史gpu用户使用率.csv')

def 历史GPU分区总费用():
    return readData('历史gpu分区总费用.csv')


def 历史GPU费用():
    return readData('历史gpu费用.csv')


def 历史GPU卡数():
    return readData('历史gpu卡数.csv')


def 预算单():
    return readCBData('预算单.csv')

def 标注任务():
    return readCBData('标注任务.csv')

def 采集任务():
    return readCBData('采集任务.csv')

def 历史标注费用():
    return readCBData('历史业务线数据标注费用.csv')

def 历史采集费用():
    return readCBData('历史业务线数据采集费用.csv')


def 历史固定资产总表():
    return readhistroyData('IRDC资产历史总表汇总.xlsx','固定资产')

def 员工部门资产金额():
    return readhistroyData('IRDC资产历史总表汇总.xlsx','员工部门资产金额')


def 历史总库存():
    data = readhistroyData('IRDC资产历史总表汇总.xlsx','总存库')
    data['在库余额（万）'] = data['在库余额（万）'].round(decimals=3)
    data['借库余额（万）'] = data['借库余额（万）'].round(decimals=3)
    data['年末预估逾期业绩核算金额（万）'] = data['年末预估逾期业绩核算金额（万）'].round(decimals=3)
    data = data.sort_values(by=['年末预估逾期业绩核算金额（万）'],ascending=False).reset_index()
    return data



def 历史借库():
    data = readhistroyData('IRDC资产历史总表汇总.xlsx','借库')
    data.drop(columns=['Pipeline描述', '借库人三级部门','实际发货日期', '工厂', 'BG',
                     'BU名称', 'PL', 'PL名称', '产品系列','借库人BG','商机有效性','WBS ID','客户名称',
                              'BG head审批单价', 'BG head审批总价', 'BU名称'], inplace=True)
    data['成本单价'] = data['成本单价'].round(decimals=3)
    data['成本总价'] = data['成本总价'].round(decimals=3)
    for i in range(len(data)):
        data.loc[i,'需求日期'] = pd.to_datetime(np.array(data.loc[i,"需求日期"], dtype='datetime64[s]').item()).date()
        data.loc[i,'预计归还日期'] = pd.to_datetime(np.array(data.loc[i, "预计归还日期"], dtype='datetime64[s]').item()).date()
        data.loc[i, '借库罚金起算日'] = pd.to_datetime(np.array(data.loc[i, "借库罚金起算日"], dtype='datetime64[s]').item()).date()
        data.loc[i, '应归还日期'] = pd.to_datetime(np.array(data.loc[i, "应归还日期"], dtype='datetime64[s]').item()).date()
    return data


def 历史固定资产总值():
    return readData('历史固定资产总值.csv')


def 历史资源费用():
    return readData('历史资源费用.csv')

def 历史dcpLustre():
    return readhistroyData('IRDC资源总表汇总.xlsx','Lustre')

def 历史dcpCeph():
    return readhistroyData('IRDC资源总表汇总.xlsx','Ceph')

def 历史oc():
    df = readhistroyData('IRDC资源总表汇总.xlsx','OC')
    df = df.loc[:, (df != 0).any(axis=0)]
    df = df[df['费用(元)'] > 0].reset_index(drop=True)
    df.drop(columns=['利润中心编码', 'BG/部门', 'N-1部门','N-2部门', '负责人AD'], inplace=True)
    return df

def 本月oc():
    data = 历史oc()
    data = data[data['资源年份'] == dcp本年()]
    data = data[data['资源月份'] == dcp本月()].reset_index(drop=True)
    return data

def 上月oc():
    data = 历史oc()
    data = data[data['资源年份'] == dcp上年()]
    data = data[data['资源月份'] == dcp上月()].reset_index(drop=True)
    return data


def 历史ocUser():
    df = readhistroyData('IRDC资源总表汇总.xlsx','ocUser')
    return df

def 本月ocUser():
    data = 历史ocUser()
    data = data[data['资源年份'] == dcp本年()]
    data = data[data['资源月份'] == dcp本月()].reset_index(drop=True)
    return data

def 上月ocUser():
    data = 历史ocUser()
    data = data[data['资源年份'] == dcp上年()]
    data = data[data['资源月份'] == dcp上月()].reset_index(drop=True)
    return data



def 历史diamond():
    df = readhistroyData('IRDC资源总表汇总.xlsx','Diamond')
    df = df.loc[:, (df != 0).any(axis=0)]
    df = df[df['费用(元)'] > 0].reset_index(drop=True)
    df.drop(columns=['利润中心编码', 'BG/部门', 'N-1部门', 'N-2部门', '用户AD'], inplace=True)
    return df


def 本月diamond():
    data = 历史diamond()
    data = data[data['资源年份'] == dcp本年()]
    data = data[data['资源月份'] == dcp本月()].reset_index(drop=True)
    return data

def 上月diamond():
    data = 历史diamond()
    data = data[data['资源年份'] == dcp上年()]
    data = data[data['资源月份'] == dcp上月()].reset_index(drop=True)
    return data



def 历史diamondUser():
    df = readhistroyData('IRDC资源总表汇总.xlsx','diamondUser')
    return df

def 本月diamondUser():
    data = 历史diamondUser()
    data = data[data['资源年份'] == dcp本年()]
    data = data[data['资源月份'] == dcp本月()].reset_index(drop=True)
    return data

def 上月diamondUser():
    data = 历史diamondUser()
    data = data[data['资源年份'] == dcp上年()]
    data = data[data['资源月份'] == dcp上月()].reset_index(drop=True)
    return data


def 本月gpu底表():
    data = 历史GPU用户使用情况()
    data = data[data['year'] == gpu本年()]
    data = data[data['month'] == gpu本月()].reset_index(drop=True)
    return data


def 上月gpu底表():
    data = 历史GPU用户使用情况()
    data = data[data['year'] == gpu上年()]
    data = data[data['month'] == gpu上月()].reset_index(drop=True)
    return data


def 本月gpu费用():
    data = 历史GPU分区总费用()
    data = data[data['year'] == gpu本年()]
    data = data[data['month'] == gpu本月()].reset_index(drop=True)
    return data


def 上月gpu费用():
    data = 历史GPU分区总费用()
    data = data[data['year'] == gpu上年()]
    data = data[data['month'] == gpu上月()].reset_index(drop=True)
    return data