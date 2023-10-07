'''
 # @ Create Time: 2022-11-05 16:58:58.526050
 # @ Create by：Zhidian Lin
'''




import pathlib
from dash import Dash
import dash_auth
from datetime import datetime
from dash import Dash, dcc, html, Input, Output, State, dash_table, ALL, MATCH
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from buildChart import *
from dataSource import *
import openpyxl
import dash
import openpyxl
import flask
from dash.exceptions import PreventUpdate
name = '智慧综合体'
nameEn = 'SX'

本月合并底表 = cleanDF员工部门(本月合并底表(),name)
上月合并底表 = cleanDF员工部门(上月合并底表(),name)
历史底表 = cleanDF员工部门(readhistroyData(工时历史总表汇总(), '合并底表'),name)
历史人员维度 = cleanDF员工部门(readhistroyData(工时历史总表汇总(), '人员维度'),name)
历史WBS维度 = groupByWBS(历史底表)
历史未填工时 = cleanDF员工部门(readhistroyData(工时历史总表汇总(), '未填工时名单'),name)


上月WBS维度 = groupByWBS(上月合并底表)
本月WBS维度 = groupByWBS(本月合并底表)
actual上月WBS维度 = actual_wbs_tb(上月WBS维度)
actual本月WBS维度 = actual_wbs_tb(本月WBS维度)
type本月WBS维度 = wbs_type_number(本月WBS维度)
type上月WBS维度 = wbs_type_number(上月WBS维度)
cur_mon_staff = cleanDF员工部门(cleanCurMonStaff(本月人员维度()),name)
last_mon_staff = cleanDF员工部门(cleanCurMonStaff(上月人员维度()),name)

gpu底表 = cleanDF员工部门(历史GPU用户使用情况(),name)
本月gpu底表 = cleanDF员工部门(本月gpu底表(),name)
上月gpu底表 = cleanDF员工部门(上月gpu底表(),name)
gpu费用 = 历史GPU分区总费用()
本月gpu费用 = 本月gpu费用()
上月gpu费用 = 上月gpu费用()

历史固定资产 = cleanDF员工部门(历史固定资产总表(),name)
历史总库存 = 历史总库存()
历史总库存 = 历史总库存[历史总库存['业务线'] == name].reset_index(drop=True)
历史借库 = 历史借库()

本月固定资产 = cleanDF员工部门(本月固定资产(),name)
上月固定资产 = cleanDF员工部门(上月固定资产(),name)

历史dcp = cleanDF员工部门(历史dcp(),name)
本月dcp = cleanDF员工部门(本月dcp(),name)
上月dcp = cleanDF员工部门(上月dcp(),name)

历史oc = cleanDF员工部门(历史oc(),name)
本月oc = cleanDF员工部门(本月oc(),name)
上月oc = cleanDF员工部门(上月oc(),name)

历史ocUser = cleanDF员工部门(历史ocUser(),name)
本月ocUser = cleanDF员工部门(本月ocUser(),name)
上月ocUser = cleanDF员工部门(上月ocUser(),name)

历史diamond = cleanDF员工部门(历史diamond(),name)
本月diamond = cleanDF员工部门(本月diamond(),name)
上月diamond = cleanDF员工部门(上月diamond(),name)

历史diamondUser = cleanDF员工部门(历史diamondUser(),name)
本月diamondUser = cleanDF员工部门(本月diamondUser(),name)
上月diamondUser = cleanDF员工部门(上月diamondUser(),name)


sumResDf = cleanDF员工部门(resAllDfGetCol(历史固定资产, 历史dcpLustre(), 历史dcpCeph(), 历史oc, 历史diamond, gpu底表, gpu费用), name)



external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sandstone/bootstrap.min.css']
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=3, r=3, b=5, t=2),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
)
# server = flask.Flask(__name__)
app = Dash(__name__, title="IRDC - 智慧综合体 - 工时&资源看板", external_stylesheets=[dbc.themes.SANDSTONE],
           update_title='刷新中，请稍等哦...',
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

html.Img(src=app.get_asset_url('img/IRDC_removed_bg.png'), style={'width': '100%'})
VALID_USERNAME_PASSWORD_PAIRS = {
    cyber(
        'Vm0wd2VHUXhUWGRPVldScFVtMW9WRll3WkRSV2JGbDNXa1JTV0ZKdGVEQmFWVll3VmpGS2RHVkdXbFpOYmtKVVZqQmFTMlJIVmtsalJtaG9UV3N3ZUZkV1dsWmxSbGw1Vkd0a2FGSnRVbGhaYkdSdlpWWmFjMVp0UmxkTlZuQlhWRlpXVjJGSFZuRlJWR3M5'): cyber(
        'Vm0wd2QyVkZOVWRXV0doVVYwZG9jRlZ0TVZOV2JGbDNXa2M1VjFadGVIbFhhMXBQVmpGS2RHVkdiR0ZXVjJoeVZqQmFZV015VGtsaVJtUnBWa1phZVZadE1UUlRNbEpIVm01R1UySklRbTlaV0hCWFpWWmFjMVp0UmxkTlZuQlhWRlpXVjJGSFZuRlJWR3M5'),
    cyber(
        'Vm0wd2VHUXhUWGRPVldSWVYwZDRWVll3Wkc5WFZsbDNXa1JTVjFac2JETlhhMk0xWVd4S2MxZHFRbFZXYlUweFZtMTRZV014WkhWaVJtUlhUVEZLVFZac1ZtRldNVnBXVFZWV2FHVnFRVGs9'): cyber(
        'Vm0wd2QyVkhVWGhVV0dST1ZsZG9WRll3Wkc5V1ZsbDNXa1pPVmxKc2JETldNblF3VmpGS2RHVkdXbFpOYWtFeFdWWlZlRmRXUm5OaVJuQk9VbXh3VFZac1ZtRldNVnBXVFZWV2FHVnFRVGs9'),

    cyber(
        'Vm0wd2VHUXhUWGROVldSWVYwZDRWRll3WkRSV2JGbDNXa1JTVjAxWGVIbFhhMXBQWVd4S2MxZHFRbUZTVjJoeVZtMHhTMUl5VGtsaVJtUlhUVEZLVFZac1ZtRldNVnBXVFZWV2FHVnFRVGs9'):cyber(
        'Vm0wd2VHUXhUWGROVldSWFYwZG9WMVl3Wkc5WFZsbDNXa1pPVlUxV2NIcFhhMk0xVmpGS2RHVkliRmhoTWsweFZtMTRTMk15VGtWU2JIQk9VbTVDVFZac1ZtRldNVnBXVFZWV2FHVnFRVGs9')
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.config.suppress_callback_exceptions = True

tabs_styles = {
    'height': '65px',
    'backgroundColor': '#F9F9F9',
    # 'borderBottom': '1px solid #d6d6d6',
    'borderLeft': 'None',
    'borderTop': 'None',
    'borderRight': 'None'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': 'None',
    'borderRight': 'None',
    'borderLeft': 'None',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#d6d6d6',
    'color': 'black',
    'padding': '10px'
}

# indicator summary for irdc



本月未填工时 = cleanDF员工部门(本月未填工时名单(),name)
上月未填工时 = cleanDF员工部门(上月未填工时名单(),name)
本月未填正式num = len(本月未填工时[本月未填工时['员工组'] == '正式员工'])
本月未填外包num = len(本月未填工时[本月未填工时['员工组'] == '外包员工'])
本月未填实习num = len(本月未填工时[本月未填工时['员工组'] == '实习生'])
上月未填正式num = len(上月未填工时[上月未填工时['员工组'] == '正式员工'])
上月未填外包num = len(上月未填工时[上月未填工时['员工组'] == '外包员工'])
上月未填实习num = len(上月未填工时[上月未填工时['员工组'] == '实习生'])

# staff_number_indicator = indicator_large_ppl(len(cur_mon_staff)+len(本月未填工时), len(last_mon_staff)+len(上月未填工时), "员工数")
# staff_in_indicator = indicator_ppl(cur_in_staff_number+本月未填正式num, last_in_staff_number+上月未填正式num, "正式")
# staff_out_indicator = indicator_ppl(cur_out_staff_number+本月未填外包num, last_out_staff_number+上月未填外包num, "外包")
# staff_intern_indicator = indicator_ppl(cur_intern_staff_number+本月未填实习num, last_intern_staff_number+上月未填实习num, "实习")

# staff_number_indicator = indicator_large_ppl(len(list(set(本月合并底表['员工姓名']))),
#                                              len(list(set(上月合并底表['员工姓名']))), "员工数")




# est all day
est_allday = indicator_irdc_sum(cur_mon_staff, last_mon_staff, "预估人天", "预估人天")
est_percentage = indicator_irdc_rate(cur_mon_staff, last_mon_staff, "实际人天", "预估人天", "预估填报率")

# logic all day
logic_allday = indicator_irdc_sum(cur_mon_staff, last_mon_staff, "理论人天", "理论人天")



# gpu usage
gpu_abud_avg_usage = indicator_gpu_percentage_large(gpu_monthly_usage(本年(), 本月(), 'SH1024/IRDC_A100_40G'),
                                                    gpu_monthly_usage(上年(), 上月(), 'SH1024/IRDC_A100_40G'),
                                                    'IRDC_A100_40G<br>平均使用率')
gpu_abud_10_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1024/IRDC_A100_40G', 10),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH1024/IRDC_A100_40G', 10),
                                                   '10点')
gpu_abud_14_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1024/IRDC_A100_40G', 14),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH1024/IRDC_A100_40G', 14),
                                                   '14点')
gpu_abud_18_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1024/IRDC_A100_40G', 18),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH1024/IRDC_A100_40G', 18),
                                                   '18点')
gpu_abud_22_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1024/IRDC_A100_40G', 22),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH1024/IRDC_A100_40G', 22),
                                                   '22点')

gpu_sg2_avg_usage = indicator_gpu_percentage_large(gpu_monthly_usage(本年(), 本月(), 'SH40/IRDC_1080Ti'),
                                                   gpu_monthly_usage(上年(), 上月(), 'SH40/IRDC_1080Ti'),
                                                   'IRDC_1080Ti<br>平均使用率')
gpu_sg2_10_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_1080Ti', 10),
                                                  gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_1080Ti', 10),
                                                  '10点')
gpu_sg2_14_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_1080Ti', 14),
                                                  gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_1080Ti', 14),
                                                  '14点')
gpu_sg2_18_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_1080Ti', 18),
                                                  gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_1080Ti', 18),
                                                  '18点')
gpu_sg2_22_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_1080Ti', 22),
                                                  gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_1080Ti', 22),
                                                  '22点')

gpu_sh40_avg_usage = indicator_gpu_percentage_large(gpu_monthly_usage(本年(), 本月(), 'SH40/IRDC_Share'),
                                                    gpu_monthly_usage(上年(), 上月(), 'SH40/IRDC_Share'),
                                                    'IRDC_Share<br>平均使用率')
gpu_sh40_10_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_Share', 10),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_Share', 10),
                                                   '10点')
gpu_sh40_14_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_Share', 14),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_Share', 14),
                                                   '14点')
gpu_sh40_18_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_Share', 18),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_Share', 18),
                                                   '18点')
gpu_sh40_22_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH40/IRDC_Share', 22),
                                                   gpu_monthly_usage_time(上年(), 上月(), 'SH40/IRDC_Share', 22),
                                                   '22点')

gpu_sh1988_avg_usage = indicator_gpu_percentage_large(gpu_monthly_usage(本年(), 本月(), 'SH1988/IRDC_V100_16G'),
                                                      gpu_monthly_usage(上年(), 上月(), 'SH1988/IRDC_V100_16G'),
                                                      'IRDC_V100_16G<br>平均使用率')
gpu_sh1988_10_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1988/IRDC_V100_16G', 10),
                                                     gpu_monthly_usage_time(上年(), 上月(), 'SH1988/IRDC_V100_16G', 10),
                                                     '10点')
gpu_sh1988_14_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1988/IRDC_V100_16G', 14),
                                                     gpu_monthly_usage_time(上年(), 上月(), 'SH1988/IRDC_V100_16G', 14),
                                                     '14点')
gpu_sh1988_18_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1988/IRDC_V100_16G', 18),
                                                     gpu_monthly_usage_time(上年(), 上月(), 'SH1988/IRDC_V100_16G', 18),
                                                     '18点')
gpu_sh1988_22_usage = indicator_gpu_percentage_small(gpu_monthly_usage_time(本年(), 本月(), 'SH1988/IRDC_V100_16G', 22),
                                                     gpu_monthly_usage_time(上年(), 上月(), 'SH1988/IRDC_V100_16G', 22),
                                                     '22点')

biaozhuTask = 标注任务()
caijiTask = 采集任务()
budgetDf = 预算单()
monthly_bz_cur = monthly_bzcj(biaozhuTask, 1)
monthly_bz_last = monthly_bzcj(biaozhuTask, 2)
monthly_cj_cur = monthly_bzcj(caijiTask, 1)
monthly_cj_last = monthly_bzcj(caijiTask, 2)

# 标注

if len(monthly_bz_cur) != 0 and len(monthly_bz_last) != 0:
    dataBZ_indicator = indicator_large_ppl(len(tryExcept0(monthly_bz_cur)), len(tryExcept0(monthly_bz_last)), "标注数")
    dataBZ_bill_indicator = indicator_databz(tryExcept0(monthly_bz_cur), tryExcept0(monthly_bz_last), '费用（元）',
                                             '标注总账单')
else:
    dataBZ_indicator = indicator_large_forNA(tryExcept0(len(monthly_bz_cur)), tryExcept0(len(monthly_bz_last)),
                                             "标注数")
    dataBZ_bill_indicator = indicator_databz_forNA(tryExcept0(len(monthly_bz_cur)), tryExcept0(len(monthly_bz_last)),
                                                   '标注总账单')

dataBZ_done_indicator = indicator_ppl(tryExcept0(len(monthly_bz_cur[monthly_bz_cur['任务状态'] == '任务完成'])),
                                      tryExcept0(len(monthly_bz_last[monthly_bz_last['任务状态'] == '任务完成'])),
                                      "Done")
dataBZ_ing_indicator = indicator_ppl(tryExcept0(len(monthly_bz_cur[monthly_bz_cur['任务状态'] != '任务完成'])),
                                     tryExcept0(len(monthly_bz_last[monthly_bz_last['任务状态'] != '任务完成'])), "ING")
dataBZ_back_indicator = indicator_logic_percentages(
    tryExcept0(len(monthly_bz_cur[monthly_bz_cur['是否有数据包被打回'] == True])), tryExcept0(len(monthly_bz_cur)),
    tryExcept0(len(monthly_bz_last[monthly_bz_last['是否有数据包被打回'] == True])), tryExcept0(len(monthly_bz_last)),
    "返工比例")

dataBZ_sx_indicator = indicator_ppl(tryExcept0(len(monthly_bz_cur[monthly_bz_cur['业务线'] == 'SX'])),
                                    tryExcept0(len(monthly_bz_last[monthly_bz_last['业务线'] == 'SX'])), "SX")
dataBZ_dx_indicator = indicator_ppl(tryExcept0(len(monthly_bz_cur[monthly_bz_cur['业务线'] == 'DX'])),
                                    tryExcept0(len(monthly_bz_last[monthly_bz_last['业务线'] == 'DX'])), "DX")
dataBZ_ir_indicator = indicator_ppl(tryExcept0(len(monthly_bz_cur[monthly_bz_cur['业务线'] == 'IR'])),
                                    tryExcept0(len(monthly_bz_last[monthly_bz_last['业务线'] == 'IR'])), "IR")

dataBZ_bill_confirm = indicator_ppl(
    tryExcept0(monthly_bz_cur[monthly_bz_cur['账单确认'] == '已确认']['费用（元）'].sum()),
    tryExcept0(monthly_bz_last[monthly_bz_last['账单确认'] == '已确认']['费用（元）'].sum()), "已确认")
dataBZ_bill_onhold = indicator_ppl(tryExcept0(monthly_bz_cur[monthly_bz_cur['账单确认'] == '待确认']['费用（元）'].sum()),
                                   tryExcept0(
                                       monthly_bz_last[monthly_bz_last['账单确认'] == '待确认']['费用（元）'].sum()),
                                   "待确认")

# 采集
if len(monthly_cj_cur) != 0 and len(monthly_cj_last) != 0:
    dataCJ_indicator = indicator_large_ppl(len(tryExcept0(monthly_cj_cur)), len(tryExcept0(monthly_cj_last)), "采集数")
    dataCJ_bill_indicator = indicator_databz(tryExcept0(monthly_cj_cur), tryExcept0(monthly_cj_last), '费用（元）',
                                             '采集总账单')
    dataCJ_done_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['任务状态'] == '任务完成'])),
                                          tryExcept0(len(monthly_cj_last[monthly_cj_last['任务状态'] == '任务完成'])),
                                          "Done")
    dataCJ_ing_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['任务状态'] != '任务完成'])),
                                         tryExcept0(len(monthly_cj_last[monthly_cj_last['任务状态'] != '任务完成'])),
                                         "ING")
    dataCJ_back_indicator = indicator_ppl(0,
                                          tryExcept0(len(monthly_cj_last[monthly_cj_last['任务状态'] != '任务完成'])),
                                          "ING")

    dataCJ_sx_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['业务线'] == 'SX'])),
                                        tryExcept0(len(monthly_cj_last[monthly_cj_last['业务线'] == 'SX'])), "SX")
    dataCJ_dx_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['业务线'] == 'DX'])),
                                        tryExcept0(len(monthly_cj_last[monthly_cj_last['业务线'] == 'DX'])), "DX")
    dataCJ_ir_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['业务线'] == 'IR'])),
                                        tryExcept0(len(monthly_cj_last[monthly_cj_last['业务线'] == 'IR'])), "IR")

    dataCJ_bill_confirm = indicator_ppl(
        tryExcept0(monthly_cj_cur[monthly_cj_cur['账单确认'] == '已确认']['费用（元）'].sum()),
        tryExcept0(monthly_cj_last[monthly_cj_last['账单确认'] == '已确认']['费用（元）'].sum()),
        "已确认")
    dataCJ_bill_onhold = indicator_ppl(
        tryExcept0(monthly_cj_cur[monthly_cj_cur['账单确认'] == '待确认']['费用（元）'].sum()),
        tryExcept0(monthly_cj_last[monthly_cj_last['账单确认'] == '待确认']['费用（元）'].sum()),
        "待确认")

elif len(monthly_cj_cur) != 0:
    dataCJ_indicator = indicator_large_forNA(tryExcept0(len(monthly_cj_cur)), 0, "采集数")
    dataCJ_bill_indicator = indicator_databz_forNA(tryExcept0(monthly_cj_cur['费用（元）'].sum()), 0, '采集总账单')
    dataCJ_done_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['任务状态'] == '任务完成'])), 0,
                                          "Done")
    dataCJ_ing_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['任务状态'] != '任务完成'])), 0,
                                         "ING")
    dataCJ_back_indicator = indicator_ppl(0,
                                          tryExcept0(len(monthly_cj_last[monthly_cj_last['任务状态'] != '任务完成'])),
                                          "ING")

    dataCJ_sx_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['业务线'] == 'SX'])), 0, "SX")
    dataCJ_dx_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['业务线'] == 'DX'])), 0, "DX")
    dataCJ_ir_indicator = indicator_ppl(tryExcept0(len(monthly_cj_cur[monthly_cj_cur['业务线'] == 'IR'])), 0, "IR")

    dataCJ_bill_confirm = indicator_ppl(
        tryExcept0(monthly_cj_cur[monthly_cj_cur['账单确认'] == '已确认']['费用（元）'].sum()), 0,
        "已确认")
    dataCJ_bill_onhold = indicator_ppl(
        tryExcept0(monthly_cj_cur[monthly_cj_cur['账单确认'] == '待确认']['费用（元）'].sum()), 0,
        "待确认")

elif len(monthly_cj_last) != 0:
    dataCJ_indicator = indicator_large_forNA(0, tryExcept0(len(monthly_cj_last)), "采集数")
    dataCJ_bill_indicator = indicator_databz_forNA(0, tryExcept0(monthly_cj_last['费用（元）'].sum()), '采集总账单')
    dataCJ_done_indicator = indicator_ppl(0,
                                          tryExcept0(len(monthly_cj_last[monthly_cj_last['任务状态'] == '任务完成'])),
                                          "Done")
    dataCJ_ing_indicator = indicator_ppl(0,
                                         tryExcept0(len(monthly_cj_last[monthly_cj_last['任务状态'] != '任务完成'])),
                                         "ING")
    dataCJ_back_indicator = indicator_ppl(0,
                                          tryExcept0(len(monthly_cj_last[monthly_cj_last['任务状态'] != '任务完成'])),
                                          "ING")

    dataCJ_sx_indicator = indicator_ppl(0,
                                        tryExcept0(len(monthly_cj_last[monthly_cj_last['业务线'] == 'SX'])), "SX")
    dataCJ_dx_indicator = indicator_ppl(0,
                                        tryExcept0(len(monthly_cj_last[monthly_cj_last['业务线'] == 'DX'])), "DX")
    dataCJ_ir_indicator = indicator_ppl(0,
                                        tryExcept0(len(monthly_cj_last[monthly_cj_last['业务线'] == 'IR'])), "IR")

    dataCJ_bill_confirm = indicator_ppl(0,
                                        tryExcept0(
                                            monthly_cj_last[monthly_cj_last['账单确认'] == '已确认']['费用（元）'].sum()),
                                        "已确认")
    dataCJ_bill_onhold = indicator_ppl(0,
                                       tryExcept0(
                                           monthly_cj_last[monthly_cj_last['账单确认'] == '待确认']['费用（元）'].sum()),
                                       "待确认")

# build data

irdcDcp = 本月dcp['费用(元)'].sum()
irdcDcplast = 上月dcp['费用(元)'].sum()

irdcDcplustre = 本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True)['费用(元)'].sum()
irdcDcplustrelast = 上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True)['费用(元)'].sum()

irdcDcpceph = 本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True)['费用(元)'].sum()
irdcDcpcephlast = 上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True)['费用(元)'].sum()

irdcOCtotal = 本月oc['费用(元)'].sum() + 本月diamond['费用(元)'].sum()
irdcOCtaotallast = 上月oc['费用(元)'].sum() + 上月diamond['费用(元)'].sum()

irdcOC= 本月oc['费用(元)'].sum()
irdcOClast = 上月oc['费用(元)'].sum()

irdcDiamond = 本月diamond['费用(元)'].sum()
irdcDiamondlast = 上月diamond['费用(元)'].sum()

irdcGpuA100 = 本月gpu费用[本月gpu费用['GPU类型'] == "Tesla_A100_SXM4_40GB"]['总价'].sum()
irdcGpuV100 = 本月gpu费用[本月gpu费用['GPU类型'] == "Tesla_V100_PCIE_16GB"]['总价'].sum()
irdcGpu1080T = 本月gpu费用[本月gpu费用['GPU类型'] == "GeForce_GTX_1080_Ti"]['总价'].sum()


irdcGpuA100last = 上月gpu费用[上月gpu费用['GPU类型'] == "Tesla_A100_SXM4_40GB"]['总价'].sum()
irdcGpuV100last = 上月gpu费用[上月gpu费用['GPU类型'] == "Tesla_V100_PCIE_16GB"]['总价'].sum()
irdcGpu1080Tlast = 上月gpu费用[上月gpu费用['GPU类型'] == "GeForce_GTX_1080_Ti"]['总价'].sum()

irdcGpuTotal = irdcGpuA100 + irdcGpuV100 + irdcGpu1080T
irdcGpuTotallast = irdcGpuA100last + irdcGpuV100last + irdcGpu1080Tlast



sxDatalustre = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧综合体')['费用(元)'].sum()
irDatalustre = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧娱乐')['费用(元)'].sum()
dxSkuDatalustre = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-冰箱')['费用(元)'].sum()
dxTyDatalustre = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-体育')['费用(元)'].sum()
mktDatalustre = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '市场拓展部')['费用(元)'].sum()
oacDatalustre = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '运营与赋能中心')['费用(元)'].sum()

sxDataLastlustre = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧综合体')['费用(元)'].sum()
irDataLastlustre = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧娱乐')['费用(元)'].sum()
dxSkuDataLastlustre = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-冰箱')['费用(元)'].sum()
dxTyDataLastlustre = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-体育')['费用(元)'].sum()
mktDataLastlustre = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '市场拓展部')['费用(元)'].sum()
oacDataLastlustre = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '运营与赋能中心')['费用(元)'].sum()


sxDatalustrec = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧综合体')['用户名'])))
irDatalustrec = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧娱乐')['用户名'])))
dxSkuDatalustrec = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-冰箱')['用户名'])))
dxTyDatalustrec = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-体育')['用户名'])))
mktDatalustrec = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '市场拓展部')['用户名'])))
oacDatalustrec = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '运营与赋能中心')['用户名'])))

sxDataLastlustrec = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧综合体')['用户名'])))
irDataLastlustrec = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '智慧娱乐')['用户名'])))
dxSkuDataLastlustrec = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-冰箱')['用户名'])))
dxTyDataLastlustrec = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '创新孵化-体育')['用户名'])))
mktDataLastlustrec = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '市场拓展部')['用户名'])))
oacDataLastlustrec = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Lustre'].reset_index(drop=True), '运营与赋能中心')['用户名'])))



sxDataceph = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧综合体')['费用(元)'].sum()
irDataceph = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧娱乐')['费用(元)'].sum()
dxSkuDataceph = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-冰箱')['费用(元)'].sum()
dxTyDataceph = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-体育')['费用(元)'].sum()
mktDataceph = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '市场拓展部')['费用(元)'].sum()
oacDataceph = filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '运营与赋能中心')['费用(元)'].sum()

sxDataLastceph = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧综合体')['费用(元)'].sum()
irDataLastceph = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧娱乐')['费用(元)'].sum()
dxSkuDataLastceph = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-冰箱')['费用(元)'].sum()
dxTyDataLastceph = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-体育')['费用(元)'].sum()
mktDataLastceph = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '市场拓展部')['费用(元)'].sum()
oacDataLastceph = filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '运营与赋能中心')['费用(元)'].sum()

sxDatacephc = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧综合体')['用户名'])))
irDatacephc = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧娱乐')['用户名'])))
dxSkuDatacephc = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-冰箱')['用户名'])))
dxTyDatacephc = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-体育')['用户名'])))
mktDatacephc = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '市场拓展部')['用户名'])))
oacDatacephc = len(list(set(filDataApartment(本月dcp[本月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '运营与赋能中心')['用户名'])))

sxDataLastcephc = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧综合体')['用户名'])))
irDataLastcephc = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '智慧娱乐')['用户名'])))
dxSkuDataLastcephc = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-冰箱')['用户名'])))
dxTyDataLastcephc = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '创新孵化-体育')['用户名'])))
mktDataLastcephc = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '市场拓展部')['用户名'])))
oacDataLastcephc = len(list(set(filDataApartment(上月dcp[上月dcp['dcp类别'] == 'Ceph'].reset_index(drop=True), '运营与赋能中心')['用户名'])))


sxDataoc = filDataApartment(本月oc, '智慧综合体')['费用(元)'].sum()
irDataoc = filDataApartment(本月oc, '智慧娱乐')['费用(元)'].sum()
dxSkuDataoc = filDataApartment(本月oc, '创新孵化-冰箱')['费用(元)'].sum()
dxTyDataoc = filDataApartment(本月oc, '创新孵化-体育')['费用(元)'].sum()
mktDataoc = filDataApartment(本月oc, '市场拓展部')['费用(元)'].sum()
oacDataoc = filDataApartment(本月oc, '运营与赋能中心')['费用(元)'].sum()

sxDataLastoc = filDataApartment(上月oc, '智慧综合体')['费用(元)'].sum()
irDataLastoc = filDataApartment(上月oc, '智慧娱乐')['费用(元)'].sum()
dxSkuDataLastoc = filDataApartment(上月oc, '创新孵化-冰箱')['费用(元)'].sum()
dxTyDataLastoc = filDataApartment(上月oc, '创新孵化-体育')['费用(元)'].sum()
mktDataLastoc = filDataApartment(上月oc, '市场拓展部')['费用(元)'].sum()
oacDataLastoc = filDataApartment(上月oc, '运营与赋能中心')['费用(元)'].sum()


sxDataocc = len(list(set(filDataApartment(本月oc, '智慧综合体')['用户名'])))
irDataocc = len(list(set(filDataApartment(本月oc, '智慧娱乐')['用户名'])))
dxSkuDataocc = len(list(set(filDataApartment(本月oc, '创新孵化-冰箱')['用户名'])))
dxTyDataocc = len(list(set(filDataApartment(本月oc, '创新孵化-体育')['用户名'])))
mktDataocc = len(list(set(filDataApartment(本月oc, '市场拓展部')['用户名'])))
oacDataocc = len(list(set(filDataApartment(本月oc, '运营与赋能中心')['用户名'])))

sxDataLastocc = len(list(set(filDataApartment(上月oc, '智慧综合体')['用户名'])))
irDataLastocc = len(list(set(filDataApartment(上月oc, '智慧娱乐')['用户名'])))
dxSkuDataLastocc = len(list(set(filDataApartment(上月oc, '创新孵化-冰箱')['用户名'])))
dxTyDataLastocc = len(list(set(filDataApartment(上月oc, '创新孵化-体育')['用户名'])))
mktDataLastocc = len(list(set(filDataApartment(上月oc, '市场拓展部')['用户名'])))
oacDataLastocc = len(list(set(filDataApartment(上月oc, '运营与赋能中心')['用户名'])))


sxDatadiamond = filDataApartment(本月diamond, '智慧综合体')['费用(元)'].sum()
irDatadiamond = filDataApartment(本月diamond, '智慧娱乐')['费用(元)'].sum()
dxSkuDatadiamond = filDataApartment(本月diamond, '创新孵化-冰箱')['费用(元)'].sum()
dxTyDatadiamond = filDataApartment(本月diamond, '创新孵化-体育')['费用(元)'].sum()
mktDatadiamond = filDataApartment(本月diamond, '市场拓展部')['费用(元)'].sum()
oacDatadiamond = filDataApartment(本月diamond, '运营与赋能中心')['费用(元)'].sum()

sxDataLastdiamond = filDataApartment(上月diamond, '智慧综合体')['费用(元)'].sum()
irDataLastdiamond = filDataApartment(上月diamond, '智慧娱乐')['费用(元)'].sum()
dxSkuDataLastdiamond = filDataApartment(上月diamond, '创新孵化-冰箱')['费用(元)'].sum()
dxTyDataLastdiamond = filDataApartment(上月diamond, '创新孵化-体育')['费用(元)'].sum()
mktDataLastdiamond = filDataApartment(上月diamond, '市场拓展部')['费用(元)'].sum()
oacDataLastdiamond = filDataApartment(上月diamond, '运营与赋能中心')['费用(元)'].sum()

sxDatadiamondc = len(list(set(filDataApartment(本月diamond, '智慧综合体')['用户名'])))
irDatadiamondc = len(list(set(filDataApartment(本月diamond, '智慧娱乐')['用户名'])))
dxSkuDatadiamondc = len(list(set(filDataApartment(本月diamond, '创新孵化-冰箱')['用户名'])))
dxTyDatadiamondc = len(list(set(filDataApartment(本月diamond, '创新孵化-体育')['用户名'])))
mktDatadiamondc = len(list(set(filDataApartment(本月diamond, '市场拓展部')['用户名'])))
oacDatadiamondc = len(list(set(filDataApartment(本月diamond, '运营与赋能中心')['用户名'])))

sxDataLastdiamondc = len(list(set(filDataApartment(上月diamond, '智慧综合体')['用户名'])))
irDataLastdiamondc = len(list(set(filDataApartment(上月diamond, '智慧娱乐')['用户名'])))
dxSkuDataLastdiamondc = len(list(set(filDataApartment(上月diamond, '创新孵化-冰箱')['用户名'])))
dxTyDataLastdiamondc = len(list(set(filDataApartment(上月diamond, '创新孵化-体育')['用户名'])))
mktDataLastdiamondc = len(list(set(filDataApartment(上月diamond, '市场拓展部')['用户名'])))
oacDataLastdiamondc = len(list(set(filDataApartment(上月diamond, '运营与赋能中心')['用户名'])))


sxDatagpu = filDataApartment(本月gpu底表, '智慧综合体')
irDatagpu = filDataApartment(本月gpu底表, '智慧娱乐')
dxSkuDatagpu = filDataApartment(本月gpu底表, '创新孵化-冰箱')
dxTyDatagpu = filDataApartment(本月gpu底表, '创新孵化-体育')
mktDatagpu = filDataApartment(本月gpu底表, '市场拓展部')
oacDatagpu = filDataApartment(本月gpu底表, '运营与赋能中心')

sxDataLastgpu = filDataApartment(上月gpu底表, '智慧综合体')
irDataLastgpu = filDataApartment(上月gpu底表, '智慧娱乐')
dxSkuDataLastgpu = filDataApartment(上月gpu底表, '创新孵化-冰箱')
dxTyDataLastgpu = filDataApartment(上月gpu底表, '创新孵化-体育')
mktDataLastgpu = filDataApartment(上月gpu底表, '市场拓展部')
oacDatagLastpu = filDataApartment(上月gpu底表, '运营与赋能中心')


sxDatagpuc = filDataApartment(本月gpu底表, '智慧综合体')
irDatagpuc = filDataApartment(本月gpu底表, '智慧娱乐')
dxSkuDatagpuc = filDataApartment(本月gpu底表, '创新孵化-冰箱')
dxTyDatagpuc = filDataApartment(本月gpu底表, '创新孵化-体育')
mktDatagpuc = filDataApartment(本月gpu底表, '市场拓展部')
oacDatagpuc = filDataApartment(本月gpu底表, '运营与赋能中心')

sxDataLastgpuc = filDataApartment(上月gpu底表, '智慧综合体')
irDataLastgpuc = filDataApartment(上月gpu底表, '智慧娱乐')
dxSkuDataLastgpuc = filDataApartment(上月gpu底表, '创新孵化-冰箱')
dxTyDataLastgpuc = filDataApartment(上月gpu底表, '创新孵化-体育')
mktDataLastgpuc = filDataApartment(上月gpu底表, '市场拓展部')
oacDatagLastpuc = filDataApartment(上月gpu底表, '运营与赋能中心')

本月1080T底表 = 本月gpu底表[本月gpu底表['分区'] == 'SH40/IRDC_1080Ti']
本月A100底表 = 本月gpu底表[本月gpu底表['分区'] == 'SH1024/IRDC_A100_40G']
本月V100底表 = 本月gpu底表[本月gpu底表['分区'] == 'SH1988/IRDC_V100_16G']
上月1080T底表 = 上月gpu底表[上月gpu底表['分区'] == 'SH40/IRDC_1080Ti']
上月A100底表 = 上月gpu底表[上月gpu底表['分区'] == 'SH1024/IRDC_A100_40G']
上月V100底表 = 上月gpu底表[上月gpu底表['分区'] == 'SH1988/IRDC_V100_16G']

sx本月1080T底表 = 本月1080T底表[本月1080T底表['员工所属部门'] == '智慧综合体']
sx本月A100底表 = 本月A100底表[本月A100底表['员工所属部门'] == '智慧综合体']
sx本月V100底表 = 本月V100底表[本月V100底表['员工所属部门'] == '智慧综合体']
sx上月1080T底表 = 上月1080T底表[上月1080T底表['员工所属部门'] == '智慧综合体']
sx上月A100底表 = 上月A100底表[上月A100底表['员工所属部门'] == '智慧综合体']
sx上月V100底表 = 上月V100底表[上月V100底表['员工所属部门'] == '智慧综合体']

ir本月1080T底表 = 本月1080T底表[本月1080T底表['员工所属部门'] == '智慧娱乐']
ir本月A100底表 = 本月A100底表[本月A100底表['员工所属部门'] == '智慧娱乐']
ir本月V100底表 = 本月V100底表[本月V100底表['员工所属部门'] == '智慧娱乐']
ir上月1080T底表 = 上月1080T底表[上月1080T底表['员工所属部门'] == '智慧娱乐']
ir上月A100底表 = 上月A100底表[上月A100底表['员工所属部门'] == '智慧娱乐']
ir上月V100底表 = 上月V100底表[上月V100底表['员工所属部门'] == '智慧娱乐']

dxSku本月1080T底表 = 本月1080T底表[本月1080T底表['员工所属部门'] == '创新孵化-冰箱']
dxSku本月A100底表 = 本月A100底表[本月A100底表['员工所属部门'] == '创新孵化-冰箱']
dxSku本月V100底表 = 本月V100底表[本月V100底表['员工所属部门'] == '创新孵化-冰箱']
dxSku上月1080T底表 = 上月1080T底表[上月1080T底表['员工所属部门'] == '创新孵化-冰箱']
dxSku上月A100底表 = 上月A100底表[上月A100底表['员工所属部门'] == '创新孵化-冰箱']
dxSku上月V100底表 = 上月V100底表[上月V100底表['员工所属部门'] == '创新孵化-冰箱']

dxTy本月1080T底表 = 本月1080T底表[本月1080T底表['员工所属部门'] == '创新孵化-体育']
dxTy本月A100底表 = 本月A100底表[本月A100底表['员工所属部门'] == '创新孵化-体育']
dxTy本月V100底表 = 本月V100底表[本月V100底表['员工所属部门'] == '创新孵化-体育']
dxTy上月1080T底表 = 上月1080T底表[上月1080T底表['员工所属部门'] == '创新孵化-体育']
dxTy上月A100底表 = 上月A100底表[上月A100底表['员工所属部门'] == '创新孵化-体育']
dxTy上月V100底表 = 上月V100底表[上月V100底表['员工所属部门'] == '创新孵化-体育']

sdk本月1080T底表 = 本月1080T底表[本月1080T底表['资源池'] == '算法SDK资源池']
sdk本月A100底表 = 本月A100底表[本月A100底表['资源池'] == '算法SDK资源池']
sdk本月V100底表 = 本月V100底表[本月V100底表['资源池'] == '算法SDK资源池']
sdk上月1080T底表 = 上月1080T底表[上月1080T底表['资源池'] == '算法SDK资源池']
sdk上月A100底表 = 上月A100底表[上月A100底表['资源池'] == '算法SDK资源池']
sdk上月V100底表 = 上月V100底表[上月V100底表['资源池'] == '算法SDK资源池']

innova本月1080T底表 = 本月1080T底表[本月1080T底表['资源池'] == '创新算法资源池']
innova本月A100底表 = 本月A100底表[本月A100底表['资源池'] == '创新算法资源池']
innova本月V100底表 = 本月V100底表[本月V100底表['资源池'] == '创新算法资源池']
innova上月1080T底表 = 上月1080T底表[上月1080T底表['资源池'] == '创新算法资源池']
innova上月A100底表 = 上月A100底表[上月A100底表['资源池'] == '创新算法资源池']
innova上月V100底表 = 上月V100底表[上月V100底表['资源池'] == '创新算法资源池']


sx_fee1080T = int(irdcGpu1080T * sx本月1080T底表['使用节点数'].sum() / 本月1080T底表['使用节点数'].sum())
sx_fee1080Tlast = int(irdcGpu1080Tlast * sx上月1080T底表['使用节点数'].sum() / 上月1080T底表['使用节点数'].sum())
ir_fee1080T = int(irdcGpu1080T * ir本月1080T底表['使用节点数'].sum() / 本月1080T底表['使用节点数'].sum())
ir_fee1080Tlast = int(irdcGpu1080Tlast * ir上月1080T底表['使用节点数'].sum() / 上月1080T底表['使用节点数'].sum())
dxSku_fee1080T = int(irdcGpu1080T * dxSku本月1080T底表['使用节点数'].sum() / 本月1080T底表['使用节点数'].sum())
dxSku_fee1080Tlast = int(irdcGpu1080Tlast * dxSku上月1080T底表['使用节点数'].sum() / 上月1080T底表['使用节点数'].sum())
dxTy_fee1080T = int(irdcGpu1080T * dxTy本月1080T底表['使用节点数'].sum() / 本月1080T底表['使用节点数'].sum())
dxTy_fee1080Tlast = int(irdcGpu1080Tlast * dxTy上月1080T底表['使用节点数'].sum() / 上月1080T底表['使用节点数'].sum())
sdk_fee1080T = int(irdcGpu1080T * sdk本月1080T底表['使用节点数'].sum() / 本月1080T底表['使用节点数'].sum())
sdk_fee1080Tlast = int(irdcGpu1080Tlast * sdk上月1080T底表['使用节点数'].sum() / 上月1080T底表['使用节点数'].sum())
innova_fee1080T = int(irdcGpu1080T * innova本月1080T底表['使用节点数'].sum() / 本月1080T底表['使用节点数'].sum())
innova_fee1080Tlast = int(irdcGpu1080Tlast * innova上月1080T底表['使用节点数'].sum() / 上月1080T底表['使用节点数'].sum())

sx_p1080T = sx本月1080T底表['用户'].nunique()
sx_p1080Tlast = sx上月1080T底表['用户'].nunique()
ir_p1080T = ir本月1080T底表['用户'].nunique()
ir_p1080Tlast = ir上月1080T底表['用户'].nunique()
dxSku_p1080T = dxSku本月1080T底表['用户'].nunique()
dxSku_p1080Tlast = dxSku上月1080T底表['用户'].nunique()
dxTy_p1080T = dxTy本月1080T底表['用户'].nunique()
dxTy_p1080Tlast = dxTy上月1080T底表['用户'].nunique()
sdk_p1080T = sdk本月1080T底表['用户'].nunique()
sdk_p1080Tlast = sdk上月1080T底表['用户'].nunique()
innova_p1080T = innova本月1080T底表['用户'].nunique()
innova_p1080Tlast = innova上月1080T底表['用户'].nunique()

sx_feeA100 = int(irdcGpuA100 * sx本月A100底表['使用节点数'].sum() / 本月A100底表['使用节点数'].sum())
sx_feeA100last = int(irdcGpuA100last * sx上月A100底表['使用节点数'].sum() / 上月A100底表['使用节点数'].sum())
ir_feeA100  = int(irdcGpuA100 * ir本月A100底表['使用节点数'].sum() / 本月A100底表['使用节点数'].sum())
ir_feeA100last = int(irdcGpuA100last * ir上月A100底表['使用节点数'].sum() / 上月A100底表['使用节点数'].sum())
dxSku_feeA100 = int(irdcGpuA100 * dxSku本月A100底表['使用节点数'].sum() / 本月A100底表['使用节点数'].sum())
dxSku_feeA100last = int(irdcGpuA100last * dxSku上月A100底表['使用节点数'].sum() / 上月A100底表['使用节点数'].sum())
dxTy_feeA100 = int(irdcGpuA100 * dxTy本月A100底表['使用节点数'].sum() / 本月A100底表['使用节点数'].sum())
dxTy_feeA100last = int(irdcGpuA100last * dxTy上月A100底表['使用节点数'].sum() / 上月A100底表['使用节点数'].sum())
sdk_feeA100 = int(irdcGpuA100 * sdk本月A100底表['使用节点数'].sum() / 本月A100底表['使用节点数'].sum())
sdk_feeA100last = int(irdcGpuA100last * sdk上月A100底表['使用节点数'].sum() / 上月A100底表['使用节点数'].sum())
innova_feeA100 = int(irdcGpuA100 * innova本月A100底表['使用节点数'].sum() / 本月A100底表['使用节点数'].sum())
innova_feeA100last = int(irdcGpuA100last * innova上月A100底表['使用节点数'].sum() / 上月A100底表['使用节点数'].sum())

sx_pA100 = sx本月A100底表['用户'].nunique()
sx_pA100last = sx上月A100底表['用户'].nunique()
ir_pA100 = ir本月A100底表['用户'].nunique()
ir_pA100last = ir上月A100底表['用户'].nunique()
dxSku_pA100 = dxSku本月A100底表['用户'].nunique()
dxSku_pA100last = dxSku上月A100底表['用户'].nunique()
dxTy_pA100 = dxTy本月A100底表['用户'].nunique()
dxTy_pA100last = dxTy上月A100底表['用户'].nunique()
sdk_pA100 = sdk本月A100底表['用户'].nunique()
sdk_pA100last = sdk上月A100底表['用户'].nunique()
innova_pA100 = innova本月A100底表['用户'].nunique()
innova_pA100last = innova上月A100底表['用户'].nunique()

sx_feeV100 = int(irdcGpuV100 * sx本月V100底表['使用节点数'].sum() / 本月V100底表['使用节点数'].sum())
sx_feeV100last = int(irdcGpuV100last * sx上月V100底表['使用节点数'].sum() / 上月V100底表['使用节点数'].sum())
ir_feeV100 = int(irdcGpuV100 * ir本月1080T底表['使用节点数'].sum() / 本月V100底表['使用节点数'].sum())
ir_feeV100last = int(irdcGpuV100last * ir上月V100底表['使用节点数'].sum() / 上月V100底表['使用节点数'].sum())
dxSku_feeV100 = int(irdcGpuV100 * dxSku本月V100底表['使用节点数'].sum() / 本月V100底表['使用节点数'].sum())
dxSku_feeV100last = int(irdcGpuV100last * dxSku上月V100底表['使用节点数'].sum() / 上月V100底表['使用节点数'].sum())
dxTy_feeV100 = int(irdcGpuV100 * dxTy本月V100底表['使用节点数'].sum() / 本月V100底表['使用节点数'].sum())
dxTy_feeV100last = int(irdcGpuV100last * dxTy上月V100底表['使用节点数'].sum() / 上月V100底表['使用节点数'].sum())
sdk_feeV100 = int(irdcGpuV100 * sdk本月V100底表['使用节点数'].sum() / 本月V100底表['使用节点数'].sum())
sdk_feeV100last = int(irdcGpuV100last * sdk上月V100底表['使用节点数'].sum() / 上月V100底表['使用节点数'].sum())
innova_feeV100 = int(irdcGpuV100 * innova本月V100底表['使用节点数'].sum() / 本月V100底表['使用节点数'].sum())
innova_feeV100last = int(irdcGpuV100last * innova上月V100底表['使用节点数'].sum() / 上月V100底表['使用节点数'].sum())

sx_pV100 = sx本月V100底表['用户'].nunique()
sx_pV100last = sx上月V100底表['用户'].nunique()
ir_pV100 = ir本月V100底表['用户'].nunique()
ir_pV100last = ir上月V100底表['用户'].nunique()
dxSku_pV100 = dxSku本月V100底表['用户'].nunique()
dxSku_pV100last = dxSku上月V100底表['用户'].nunique()
dxTy_pV100 = dxTy本月V100底表['用户'].nunique()
dxTy_pV100last = dxTy上月V100底表['用户'].nunique()
sdk_pV100 = sdk本月V100底表['用户'].nunique()
sdk_pV100last = sdk上月V100底表['用户'].nunique()
innova_pV100 = innova本月V100底表['用户'].nunique()
innova_pV100last = innova上月V100底表['用户'].nunique()


本月gpuGroupBy部门 = 对比分区gpu0(本月gpu底表, '使用节点数', "员工所属部门", 本月gpu费用, "总使用节点数", '费用')
上月gpuGroupBy部门 = 对比分区gpu0(上月gpu底表, '使用节点数', "员工所属部门", 上月gpu费用, "总使用节点数", '费用')

本月gpuGroupBy资源池 = 对比分区gpu0(本月gpu底表, '使用节点数', "资源池", 本月gpu费用, "总使用节点数", '费用')
上月gpuGroupBy资源池 = 对比分区gpu0(上月gpu底表, '使用节点数', "资源池", 上月gpu费用, "总使用节点数", '费用')

sx_totalFee = 本月gpuGroupBy部门[本月gpuGroupBy部门['员工所属部门'] == '智慧综合体']['费用'].sum()
sx_totalFeelast = 上月gpuGroupBy部门[上月gpuGroupBy部门['员工所属部门'] == '智慧综合体']['费用'].sum()

ir_totalFee = 本月gpuGroupBy部门[本月gpuGroupBy部门['员工所属部门'] == '智慧娱乐']['费用'].sum()
ir_totalFeelast = 上月gpuGroupBy部门[上月gpuGroupBy部门['员工所属部门'] == '智慧娱乐']['费用'].sum()

dxSku_totalFee = 本月gpuGroupBy部门[本月gpuGroupBy部门['员工所属部门'] == '创新孵化-冰箱']['费用'].sum()
dxSku_totalFeelast = 上月gpuGroupBy部门[上月gpuGroupBy部门['员工所属部门'] == '创新孵化-冰箱']['费用'].sum()

dxTy_totalFee = 本月gpuGroupBy部门[本月gpuGroupBy部门['员工所属部门'] == '创新孵化-体育']['费用'].sum()
dxTy_totalFeelast = 上月gpuGroupBy部门[上月gpuGroupBy部门['员工所属部门'] == '创新孵化-体育']['费用'].sum()

sdk_totalFee = 本月gpuGroupBy资源池[本月gpuGroupBy资源池['资源池'] == '算法SDK资源池']['费用'].sum()
sdk_totalFeelast = 上月gpuGroupBy资源池[上月gpuGroupBy资源池['资源池'] == '算法SDK资源池']['费用'].sum()

innova_totalFee = 本月gpuGroupBy资源池[本月gpuGroupBy资源池['资源池'] == '创新算法资源池']['费用'].sum()
innova_totalFeelast = 上月gpuGroupBy资源池[上月gpuGroupBy资源池['资源池'] == '创新算法资源池']['费用'].sum()

sx_totalP = 本月gpu底表[本月gpu底表['员工所属部门'] == '智慧综合体']['用户'].nunique()
sx_totalPlast = 上月gpu底表[上月gpu底表['员工所属部门'] == '智慧综合体']['用户'].nunique()

ir_totalP = 本月gpu底表[本月gpu底表['员工所属部门'] == '智慧娱乐']['用户'].nunique()
ir_totalPlast = 上月gpu底表[上月gpu底表['员工所属部门'] == '智慧娱乐']['用户'].nunique()

dxSku_totalP = 本月gpu底表[本月gpu底表['员工所属部门'] == '创新孵化-冰箱']['用户'].nunique()
dxSku_totalPlast = 上月gpu底表[上月gpu底表['员工所属部门'] == '创新孵化-冰箱']['用户'].nunique()

dxTy_totalP = 本月gpu底表[本月gpu底表['员工所属部门'] == '创新孵化-体育']['用户'].nunique()
dxTy_totalPlast = 上月gpu底表[上月gpu底表['员工所属部门'] == '创新孵化-体育']['用户'].nunique()

sdk_totalP = 本月gpu底表[本月gpu底表['资源池'] == '算法SDK资源池']['用户'].nunique()
sdk_totalPlast = 上月gpu底表[上月gpu底表['资源池'] == '算法SDK资源池']['用户'].nunique()

innova_totalP = 本月gpu底表[本月gpu底表['资源池'] == '创新算法资源池']['用户'].nunique()
innova_totalPlast = 上月gpu底表[上月gpu底表['资源池'] == '创新算法资源池']['用户'].nunique()


# build graph

sx_fee = indicator_bl_total_midGpu(sx_totalFee, sx_totalFeelast, 'SX 总费用')
ir_fee = indicator_bl_total_midGpu(ir_totalFee, ir_totalFeelast, 'IR 总费用')
dxSku_fee = indicator_bl_total_midGpu(dxSku_totalFee, dxSku_totalFeelast, 'DX-SKU 总费用')
dxTy_fee = indicator_bl_total_midGpu(dxTy_totalFee, dxTy_totalFeelast, 'DX-TY 总费用')
sdk_fee = indicator_bl_total_midGpu(sdk_totalFee, sdk_totalFeelast, '算法SDK 总费用')
innova_fee = indicator_bl_total_midGpu(innova_totalFee, innova_totalFeelast, '创新算法 总费用')

sx_p = indicator_bl_total_midGpu(sx_totalP, sx_totalPlast, 'SX 总人数')
ir_p = indicator_bl_total_midGpu(ir_totalP, ir_totalPlast, 'IR 总人数')
dxSku_p = indicator_bl_total_midGpu(dxSku_totalP, dxSku_totalPlast, 'DX-SKU 总人数')
dxTy_p = indicator_bl_total_midGpu(dxTy_totalP, dxTy_totalPlast, 'DX-TY 总人数')
sdk_p = indicator_bl_total_midGpu(sdk_totalP, sdk_totalPlast, '算法SDK 总人数')
innova_p = indicator_bl_total_midGpu(innova_totalP, innova_totalPlast, '创新算法 总人数')

sx_1080T_p = indicator_bl_total_midGpu(sx_p1080T, sx_p1080Tlast, 'SX 人数')
ir_1080T_p = indicator_bl_total_midGpu(ir_p1080T, ir_p1080Tlast, 'IR 人数')
dxSku_1080T_p = indicator_bl_total_midGpu(dxSku_p1080T, dxSku_p1080Tlast, 'DX-SKU 人数')
dxTy_1080T_p = indicator_bl_total_midGpu(dxTy_p1080T, dxTy_p1080Tlast, 'DX-TY 人数')
sdk_1080T_p = indicator_bl_total_midGpu(sdk_p1080T, sdk_p1080Tlast, '算法SDK 人数')
innova_1080T_p = indicator_bl_total_midGpu(innova_p1080T, innova_p1080Tlast, '创新算法 人数')

sx_1080T_fee = indicator_bl_total_midGpu(sx_fee1080T, sx_fee1080Tlast, 'SX 费用')
ir_1080T_fee = indicator_bl_total_midGpu(ir_fee1080T, ir_fee1080Tlast, 'IR 费用')
dxSku_1080T_fee = indicator_bl_total_midGpu(dxSku_fee1080T, dxSku_fee1080Tlast, 'DX-SKU 费用')
dxTy_1080T_fee = indicator_bl_total_midGpu(dxTy_fee1080T, dxTy_fee1080Tlast, 'DX-TY 费用')
sdk_1080T_fee = indicator_bl_total_midGpu(sdk_fee1080T, sdk_fee1080Tlast, '算法SDK 费用')
innova_1080T_fee = indicator_bl_total_midGpu(innova_fee1080T, innova_fee1080Tlast, '创新算法 费用')


sx_V100_p = indicator_bl_total_midGpu(sx_pV100, sx_pV100last, 'SX 人数')
ir_V100_p = indicator_bl_total_midGpu(ir_pV100, ir_pV100last, 'IR 人数')
dxSku_V100_p = indicator_bl_total_midGpu(dxSku_pV100, dxSku_pV100last, 'DX-SKU 人数')
dxTy_V100_p = indicator_bl_total_midGpu(dxTy_pV100, dxTy_pV100last, 'DX-TY 人数')
sdk_V100_p = indicator_bl_total_midGpu(sdk_pV100, sdk_pV100last, '算法SDK 人数')
innova_V100_p = indicator_bl_total_midGpu(innova_pV100, innova_pV100last, '创新算法 人数')

sx_V100_fee = indicator_bl_total_midGpu(sx_feeV100, sx_feeV100last, 'SX 费用')
ir_V100_fee = indicator_bl_total_midGpu(ir_feeV100, ir_feeV100last, 'IR 费用')
dxSku_V100_fee = indicator_bl_total_midGpu(dxSku_feeV100, dxSku_feeV100last, 'DX-SKU 费用')
dxTy_V100_fee = indicator_bl_total_midGpu(dxTy_feeV100, dxTy_feeV100last, 'DX-TY 费用')
sdk_V100_fee = indicator_bl_total_midGpu(sdk_feeV100, sdk_feeV100last, '算法SDK 费用')
innova_V100_fee = indicator_bl_total_midGpu(innova_feeV100, innova_feeV100last, '创新算法 费用')


sx_A100_p = indicator_bl_total_midGpu(sx_pA100, sx_pA100last, 'SX 人数')
ir_A100_p = indicator_bl_total_midGpu(ir_pA100, ir_pA100last, 'IR 人数')
dxSku_A100_p = indicator_bl_total_midGpu(dxSku_pA100, dxSku_pA100last, 'DX-SKU 人数')
dxTy_A100_p = indicator_bl_total_midGpu(dxTy_pA100, dxTy_pA100last, 'DX-TY 人数')
sdk_A100_p = indicator_bl_total_midGpu(sdk_pA100, sdk_pA100last, '算法SDK 人数')
innova_A100_p = indicator_bl_total_midGpu(innova_p1080T, innova_pA100last, '创新算法 人数')

sx_A100_fee = indicator_bl_total_midGpu(sx_feeA100, sx_feeA100last, 'SX 费用')
ir_A100_fee = indicator_bl_total_midGpu(ir_feeA100, ir_feeA100last, 'IR 费用')
dxSku_A100_fee = indicator_bl_total_midGpu(dxSku_feeA100, dxSku_feeA100last, 'DX-SKU 费用')
dxTy_A100_fee = indicator_bl_total_midGpu(dxTy_feeA100, dxTy_feeA100last, 'DX-TY 费用')
sdk_A100_fee = indicator_bl_total_midGpu(sdk_feeA100, sdk_feeA100last, '算法SDK 费用')
innova_A100_fee = indicator_bl_total_midGpu(innova_feeA100, innova_feeA100last, '创新算法 费用')





total_dcp = indicator_bl_totalLL(irdcDcp, irdcDcplast, "DCP 总费用（元）")
total_octotal = indicator_bl_totalLL(irdcOCtotal, irdcOCtaotallast, "OC 总费用（元）")
total_gpu = indicator_bl_totalGpu(irdcGpuTotal, irdcGpuTotallast, "GPU 总费用（元）")

total_lustre = indicator_bl_total_midLL(irdcDcplustre, irdcDcplustrelast, "Lustre")
total_ceph = indicator_bl_total_midLL(irdcDcpceph, irdcDcpcephlast, "Ceph")

total_oc = indicator_bl_total_midLL(irdcOC, irdcOClast, "OC")
total_diamond = indicator_bl_total_midLL(irdcDiamond, irdcDiamondlast, "Diamond")

total_gpuA100 = indicator_bl_totalGpu(irdcGpuA100, irdcGpuA100last, "A100 总费用（元）")
total_gpuV100 = indicator_bl_totalGpu(irdcGpuV100, irdcGpuV100last, "V100 总费用（元）")
total_gpu1080T = indicator_bl_totalGpu(irdcGpu1080T, irdcGpu1080Tlast, "1080Ti 总费用（元）")



sx_lustre= indicator_bl_total_mid(sxDatalustre, sxDataLastlustre, 'Lustre')
ir_lustre= indicator_bl_total_mid(irDatalustre, irDataLastlustre, 'Lustre')
dxSku_lustre= indicator_bl_total_mid(dxSkuDatalustre, dxSkuDataLastlustre, 'Lustre')
dxTy_lustre= indicator_bl_total_mid(dxTyDatalustre, dxTyDataLastlustre, 'Lustre')
mkt_lustre= indicator_bl_total_mid(mktDatalustre, mktDataLastlustre, 'Lustre')
oac_lustre= indicator_bl_total_mid(oacDatalustre, oacDataLastlustre, 'Lustre')

sx_ceph= indicator_bl_total_mid(sxDataceph, sxDataLastceph, 'Ceph')
ir_ceph= indicator_bl_total_mid(irDataceph, irDataLastceph, 'Ceph')
dxSku_ceph= indicator_bl_total_mid(dxSkuDataceph, dxSkuDataLastceph, 'Ceph')
dxTy_ceph= indicator_bl_total_mid(dxTyDataceph, dxTyDataLastceph, 'Ceph')
mkt_ceph= indicator_bl_total_mid(mktDataceph, mktDataLastceph, 'Ceph')
oac_ceph= indicator_bl_total_mid(oacDataceph, oacDataLastceph, 'Ceph')

sx_oc= indicator_bl_total_mid(sxDataoc, sxDataLastoc, 'OC')
ir_oc= indicator_bl_total_mid(irDataoc, irDataLastoc, 'OC')
dxSku_oc= indicator_bl_total_mid(dxSkuDataoc, dxSkuDataLastoc, 'OC')
dxTy_oc= indicator_bl_total_mid(dxTyDataoc, dxTyDataLastoc, 'OC')
mkt_oc= indicator_bl_total_mid(mktDataoc, mktDataLastoc, 'OC')
oac_oc= indicator_bl_total_mid(oacDataoc, oacDataLastoc, 'OC')

sx_diamond= indicator_bl_total_mid(sxDatadiamond, sxDataLastdiamond, 'Diamond')
ir_diamond= indicator_bl_total_mid(irDatadiamond, irDataLastdiamond, 'Diamond')
dxSku_diamond= indicator_bl_total_mid(dxSkuDatadiamond, dxSkuDataLastdiamond, 'Diamond')
dxTy_diamond= indicator_bl_total_mid(dxTyDatadiamond, dxTyDataLastdiamond, 'Diamond')
mkt_diamond= indicator_bl_total_mid(mktDatadiamond, mktDataLastdiamond, 'Diamond')
oac_diamond= indicator_bl_total_mid(oacDatadiamond, oacDataLastdiamond, 'Diamond')

sx_totalRes= indicator_bl_total(
    sxDatadiamond + sxDatalustre + sxDataceph + sxDataoc,
    sxDataLastdiamond + sxDataLastlustre + sxDataLastceph + sxDataLastoc, 'SX 资源总费用')
ir_totalRes = indicator_bl_total(
    irDatadiamond + irDatalustre + irDataceph + irDataoc,
    irDataLastdiamond+ irDataLastlustre + irDataLastceph + irDataLastoc, 'IR 资源总费用')
dxSku_totalRes = indicator_bl_total(
    dxSkuDatadiamond + dxSkuDatalustre + dxSkuDataceph + dxSkuDataoc,
    dxSkuDataLastdiamond+ dxSkuDataLastlustre + dxSkuDataLastceph + dxSkuDataLastoc, 'DX-SKU 资源总费用')
dxTy_totalRes = indicator_bl_total(
    dxTyDatadiamond + dxTyDatalustre + dxTyDataceph + dxTyDataoc,
    dxTyDataLastdiamond+ dxTyDataLastlustre + dxTyDataLastceph + dxTyDataLastoc, 'DX-TY 资源总费用')
mkt_totalRes = indicator_bl_total(
    mktDatadiamond + mktDatalustre + mktDataceph + mktDataoc,
    mktDataLastdiamond+ mktDataLastlustre + mktDataLastceph + mktDataLastoc, 'MKT 资源总费用')
oac_totalRes = indicator_bl_total(
    oacDatadiamond + oacDatalustre + oacDataceph + oacDataoc,
    oacDataLastdiamond+ oacDataLastlustre + oacDataLastceph + oacDataLastoc, 'OAC 资源总费用')



# build data

sxData = filDataApartment(本月固定资产, '智慧综合体')
irData = filDataApartment(本月固定资产, '智慧娱乐')
dxSkuData = filDataApartment(本月固定资产, '创新孵化-冰箱')
dxTyData = filDataApartment(本月固定资产, '创新孵化-体育')
mktData = filDataApartment(本月固定资产, '市场拓展部')
oacData = filDataApartment(本月固定资产, '运营与赋能中心')

sxDataLast = filDataApartment(上月固定资产, '智慧综合体')
irDataLast = filDataApartment(上月固定资产, '智慧娱乐')
dxSkuDataLast = filDataApartment(上月固定资产, '创新孵化-冰箱')
dxTyDataLast = filDataApartment(上月固定资产, '创新孵化-体育')
mktDataLast = filDataApartment(上月固定资产, '市场拓展部')
oacDataLast = filDataApartment(上月固定资产, '运营与赋能中心')

sxDataTotal = int(sxData['折旧'].sum())
sxDataTotalLast = int(sxDataLast['折旧'].sum())

sxDataTotalc = int(sxData['资产代码'].count())
sxDataTotalLastc = int(sxDataLast['资产代码'].count())

irDataTotal = int(irData['折旧'].sum())
irDataTotalLast = int(irDataLast['折旧'].sum())

irDataTotalc = int(irData['资产代码'].count())
irDataTotalLastc = int(irDataLast['资产代码'].count())

dxSkuDataTotal = int(dxSkuData['折旧'].sum())
dxSkuDataTotalLast = int(dxSkuDataLast['折旧'].sum())

dxSkuDataTotalc = int(dxSkuData['资产代码'].count())
dxSkuDataTotalLastc = int(dxSkuDataLast['资产代码'].count())

dxTyDataTotal = int(dxTyData['折旧'].sum())
dxTyDataTotalLast = int(dxTyDataLast['折旧'].sum())

dxTyDataTotalc = int(dxSkuData['资产代码'].count())
dxTyDataTotalLastc = int(dxSkuDataLast['资产代码'].count())

mktDataTotal = int(mktData['折旧'].sum())
mktDataTotalLast = int(mktDataLast['折旧'].sum())

mktDataTotalc = int(mktData['资产代码'].count())
mktDataTotalLastc = int(mktDataLast['资产代码'].count())

oacDataTotal = int(oacData['折旧'].sum())
oacDataTotalLast = int(oacDataLast['折旧'].sum())

oacDataTotalc = int(oacData['资产代码'].count())
oacDataTotalLastc = int(oacDataLast['资产代码'].count())

# sx
sxGroup笔记本电脑 = tryExceptNone(blGroupByzhejiu(sxData, '设备类型', '笔记本电脑'))
sxGroup台式电脑 = tryExceptNone(blGroupByzhejiu(sxData, '设备类型', '台式电脑'))
sxGroup服务器 = tryExceptNone(blGroupByzhejiu(sxData, '设备类型', '服务器'))
sxGroup显示屏 = tryExceptNone(blGroupByzhejiu(sxData, '设备类型', '显示屏'))
sxGroup网络设备 = tryExceptNone(blGroupByzhejiu(sxData, '设备类型', '网络设备'))
sxGroup开发套件 = tryExceptNone(blGroupByzhejiu(sxData, '设备类型', '开发套件'))
sxGroup其他 = tryNoneto0(
    sxDataTotal)-tryNoneto0(
    sxGroup笔记本电脑)-tryNoneto0(
    sxGroup台式电脑)-tryNoneto0(
    sxGroup服务器)-tryNoneto0(
    sxGroup显示屏)-tryNoneto0(
    sxGroup网络设备)-tryNoneto0(
    sxGroup开发套件)

sxGroup笔记本电脑c = tryExceptNone(blGroupBygeshu(sxData, '设备类型', '笔记本电脑'))
sxGroup台式电脑c = tryExceptNone(blGroupBygeshu(sxData, '设备类型', '台式电脑'))
sxGroup服务器c = tryExceptNone(blGroupBygeshu(sxData, '设备类型', '服务器'))
sxGroup显示屏c = tryExceptNone(blGroupBygeshu(sxData, '设备类型', '显示屏'))
sxGroup网络设备c = tryExceptNone(blGroupBygeshu(sxData, '设备类型', '网络设备'))
sxGroup开发套件c = tryExceptNone(blGroupBygeshu(sxData, '设备类型', '开发套件'))
sxGroup其他c = tryNoneto0(
    sxDataTotalc)-tryNoneto0(
    sxGroup笔记本电脑c)-tryNoneto0(
    sxGroup台式电脑c)-tryNoneto0(
    sxGroup服务器c)-tryNoneto0(
    sxGroup显示屏c)-tryNoneto0(
    sxGroup网络设备c)-tryNoneto0(
    sxGroup开发套件c)

sxGroup笔记本电脑last = tryExceptNone(blGroupByzhejiu(sxDataLast, '设备类型', '笔记本电脑'))
sxGroup台式电脑last = tryExceptNone(blGroupByzhejiu(sxDataLast, '设备类型', '台式电脑'))
sxGroup服务器last = tryExceptNone(blGroupByzhejiu(sxDataLast, '设备类型', '服务器'))
sxGroup显示屏last = tryExceptNone(blGroupByzhejiu(sxDataLast, '设备类型', '显示屏'))
sxGroup网络设备last = tryExceptNone(blGroupByzhejiu(sxDataLast, '设备类型', '网络设备'))
sxGroup开发套件last = tryExceptNone(blGroupByzhejiu(sxDataLast, '设备类型', '开发套件'))
sxGroup其他last = tryNoneto0(
    sxDataTotalLast)-tryNoneto0(
    sxGroup笔记本电脑last)-tryNoneto0(
    sxGroup台式电脑last)-tryNoneto0(
    sxGroup服务器last)-tryNoneto0(
    sxGroup显示屏last)-tryNoneto0(
    sxGroup网络设备last)-tryNoneto0(
    sxGroup开发套件last)

sxGroup笔记本电脑clast = tryExceptNone(blGroupBygeshu(sxDataLast, '设备类型', '笔记本电脑'))
sxGroup台式电脑clast = tryExceptNone(blGroupBygeshu(sxDataLast, '设备类型', '台式电脑'))
sxGroup服务器clast = tryExceptNone(blGroupBygeshu(sxDataLast, '设备类型', '服务器'))
sxGroup显示屏clast = tryExceptNone(blGroupBygeshu(sxDataLast, '设备类型', '显示屏'))
sxGroup网络设备clast = tryExceptNone(blGroupBygeshu(sxDataLast, '设备类型', '网络设备'))
sxGroup开发套件clast = tryExceptNone(blGroupBygeshu(sxDataLast, '设备类型', '开发套件'))
sxGroup其他clast = tryNoneto0(
    sxDataTotalLastc)-tryNoneto0(
    sxGroup笔记本电脑clast)-tryNoneto0(
    sxGroup台式电脑clast)-tryNoneto0(
    sxGroup服务器clast)-tryNoneto0(
    sxGroup显示屏clast)-tryNoneto0(
    sxGroup网络设备clast)-tryNoneto0(
    sxGroup开发套件clast)


# ir
irGroup笔记本电脑 = tryExceptNone(blGroupByzhejiu(irData, '设备类型', '笔记本电脑'))
irGroup台式电脑 = tryExceptNone(blGroupByzhejiu(irData, '设备类型', '台式电脑'))
irGroup服务器 = tryExceptNone(blGroupByzhejiu(irData, '设备类型', '服务器'))
irGroup显示屏 = tryExceptNone(blGroupByzhejiu(irData, '设备类型', '显示屏'))
irGroup网络设备 = tryExceptNone(blGroupByzhejiu(irData, '设备类型', '网络设备'))
irGroup开发套件 = tryExceptNone(blGroupByzhejiu(irData, '设备类型', '开发套件'))
irGroup其他 = tryNoneto0(
    irDataTotal)-tryNoneto0(
    irGroup笔记本电脑)-tryNoneto0(
    irGroup台式电脑)-tryNoneto0(
    irGroup服务器)-tryNoneto0(
    irGroup显示屏)-tryNoneto0(
    irGroup网络设备)-tryNoneto0(
    irGroup开发套件)

irGroup笔记本电脑c = tryExceptNone(blGroupBygeshu(irData, '设备类型', '笔记本电脑'))
irGroup台式电脑c = tryExceptNone(blGroupBygeshu(irData, '设备类型', '台式电脑'))
irGroup服务器c = tryExceptNone(blGroupBygeshu(irData, '设备类型', '服务器'))
irGroup显示屏c = tryExceptNone(blGroupBygeshu(irData, '设备类型', '显示屏'))
irGroup网络设备c = tryExceptNone(blGroupBygeshu(irData, '设备类型', '网络设备'))
irGroup开发套件c = tryExceptNone(blGroupBygeshu(irData, '设备类型', '开发套件'))
irGroup其他c = tryNoneto0(
    irDataTotalc)-tryNoneto0(
    irGroup笔记本电脑c)-tryNoneto0(
    irGroup台式电脑c)-tryNoneto0(
    irGroup服务器c)-tryNoneto0(
    irGroup显示屏c)-tryNoneto0(
    irGroup网络设备c)-tryNoneto0(
    irGroup开发套件c)

irGroup笔记本电脑last = tryExceptNone(blGroupByzhejiu(irDataLast, '设备类型', '笔记本电脑'))
irGroup台式电脑last = tryExceptNone(blGroupByzhejiu(irDataLast, '设备类型', '台式电脑'))
irGroup服务器last = tryExceptNone(blGroupByzhejiu(irDataLast, '设备类型', '服务器'))
irGroup显示屏last = tryExceptNone(blGroupByzhejiu(irDataLast, '设备类型', '显示屏'))
irGroup网络设备last = tryExceptNone(blGroupByzhejiu(irDataLast, '设备类型', '网络设备'))
irGroup开发套件last = tryExceptNone(blGroupByzhejiu(irDataLast, '设备类型', '开发套件'))
irGroup其他last = tryNoneto0(
    irDataTotalLast)-tryNoneto0(
    irGroup笔记本电脑last)-tryNoneto0(
    irGroup台式电脑last)-tryNoneto0(
    irGroup服务器last)-tryNoneto0(
    irGroup显示屏last)-tryNoneto0(
    irGroup网络设备last)-tryNoneto0(
    irGroup开发套件last)

irGroup笔记本电脑clast = tryExceptNone(blGroupBygeshu(irDataLast, '设备类型', '笔记本电脑'))
irGroup台式电脑clast = tryExceptNone(blGroupBygeshu(irDataLast, '设备类型', '台式电脑'))
irGroup服务器clast = tryExceptNone(blGroupBygeshu(irDataLast, '设备类型', '服务器'))
irGroup显示屏clast = tryExceptNone(blGroupBygeshu(irDataLast, '设备类型', '显示屏'))
irGroup网络设备clast = tryExceptNone(blGroupBygeshu(irDataLast, '设备类型', '网络设备'))
irGroup开发套件clast = tryExceptNone(blGroupBygeshu(irDataLast, '设备类型', '开发套件'))
irGroup其他clast = tryNoneto0(
    irDataTotalLastc)-tryNoneto0(
    irGroup笔记本电脑clast)-tryNoneto0(
    irGroup台式电脑clast)-tryNoneto0(
    irGroup服务器clast)-tryNoneto0(
    irGroup显示屏clast)-tryNoneto0(
    irGroup网络设备clast)-tryNoneto0(
    irGroup开发套件clast)


# dx-sku

dxSkuGroup笔记本电脑 = tryExceptNone(blGroupByzhejiu(dxSkuData, '设备类型', '笔记本电脑'))
dxSkuGroup台式电脑 = tryExceptNone(blGroupByzhejiu(dxSkuData, '设备类型', '台式电脑'))
dxSkuGroup服务器 = tryExceptNone(blGroupByzhejiu(dxSkuData, '设备类型', '服务器'))
dxSkuGroup显示屏 = tryExceptNone(blGroupByzhejiu(dxSkuData, '设备类型', '显示屏'))
dxSkuGroup网络设备 = tryExceptNone(blGroupByzhejiu(dxSkuData, '设备类型', '网络设备'))
dxSkuGroup开发套件 = tryExceptNone(blGroupByzhejiu(dxSkuData, '设备类型', '开发套件'))
dxSkuGroup其他 = tryNoneto0(
    dxSkuDataTotal)-tryNoneto0(
    dxSkuGroup笔记本电脑)-tryNoneto0(
    dxSkuGroup台式电脑)-tryNoneto0(
    dxSkuGroup服务器)-tryNoneto0(
    dxSkuGroup显示屏)-tryNoneto0(
    dxSkuGroup网络设备)-tryNoneto0(
    dxSkuGroup开发套件)

dxSkuGroup笔记本电脑c = tryExceptNone(blGroupBygeshu(dxSkuData, '设备类型', '笔记本电脑'))
dxSkuGroup台式电脑c = tryExceptNone(blGroupBygeshu(dxSkuData, '设备类型', '台式电脑'))
dxSkuGroup服务器c = tryExceptNone(blGroupBygeshu(dxSkuData, '设备类型', '服务器'))
dxSkuGroup显示屏c = tryExceptNone(blGroupBygeshu(dxSkuData, '设备类型', '显示屏'))
dxSkuGroup网络设备c = tryExceptNone(blGroupBygeshu(dxSkuData, '设备类型', '网络设备'))
dxSkuGroup开发套件c = tryExceptNone(blGroupBygeshu(dxSkuData, '设备类型', '开发套件'))
dxSkuGroup其他c = tryNoneto0(
    dxSkuDataTotalc)-tryNoneto0(
    dxSkuGroup笔记本电脑c)-tryNoneto0(
    dxSkuGroup台式电脑c)-tryNoneto0(
    dxSkuGroup服务器c)-tryNoneto0(
    dxSkuGroup显示屏c)-tryNoneto0(
    dxSkuGroup网络设备c)-tryNoneto0(
    dxSkuGroup开发套件c)

dxSkuGroup笔记本电脑last = tryExceptNone(blGroupByzhejiu(dxSkuDataLast, '设备类型', '笔记本电脑'))
dxSkuGroup台式电脑last = tryExceptNone(blGroupByzhejiu(dxSkuDataLast, '设备类型', '台式电脑'))
dxSkuGroup服务器last = tryExceptNone(blGroupByzhejiu(dxSkuDataLast, '设备类型', '服务器'))
dxSkuGroup显示屏last = tryExceptNone(blGroupByzhejiu(dxSkuDataLast, '设备类型', '显示屏'))
dxSkuGroup网络设备last = tryExceptNone(blGroupByzhejiu(dxSkuDataLast, '设备类型', '网络设备'))
dxSkuGroup开发套件last = tryExceptNone(blGroupByzhejiu(dxSkuDataLast, '设备类型', '开发套件'))
dxSkuGroup其他last = tryNoneto0(
    dxSkuDataTotalLast)-tryNoneto0(
    dxSkuGroup笔记本电脑last)-tryNoneto0(
    dxSkuGroup台式电脑last)-tryNoneto0(
    dxSkuGroup服务器last)-tryNoneto0(
    dxSkuGroup显示屏last)-tryNoneto0(
    dxSkuGroup网络设备last)-tryNoneto0(
    dxSkuGroup开发套件last)

dxSkuGroup笔记本电脑clast = tryExceptNone(blGroupBygeshu(dxSkuDataLast, '设备类型', '笔记本电脑'))
dxSkuGroup台式电脑clast = tryExceptNone(blGroupBygeshu(dxSkuDataLast, '设备类型', '台式电脑'))
dxSkuGroup服务器clast = tryExceptNone(blGroupBygeshu(dxSkuDataLast, '设备类型', '服务器'))
dxSkuGroup显示屏clast = tryExceptNone(blGroupBygeshu(dxSkuDataLast, '设备类型', '显示屏'))
dxSkuGroup网络设备clast = tryExceptNone(blGroupBygeshu(dxSkuDataLast, '设备类型', '网络设备'))
dxSkuGroup开发套件clast = tryExceptNone(blGroupBygeshu(dxSkuDataLast, '设备类型', '开发套件'))
dxSkuGroup其他clast = tryNoneto0(
    dxSkuDataTotalLastc)-tryNoneto0(
    dxSkuGroup笔记本电脑clast)-tryNoneto0(
    dxSkuGroup台式电脑clast)-tryNoneto0(
    dxSkuGroup服务器clast)-tryNoneto0(
    dxSkuGroup显示屏clast)-tryNoneto0(
    dxSkuGroup网络设备clast)-tryNoneto0(
    dxSkuGroup开发套件clast)


# dx-ty

dxTyGroup笔记本电脑 = tryExceptNone(blGroupByzhejiu(dxTyData, '设备类型', '笔记本电脑'))
dxTyGroup台式电脑 = tryExceptNone(blGroupByzhejiu(dxTyData, '设备类型', '台式电脑'))
dxTyGroup服务器 = tryExceptNone(blGroupByzhejiu(dxTyData, '设备类型', '服务器'))
dxTyGroup显示屏 = tryExceptNone(blGroupByzhejiu(dxTyData, '设备类型', '显示屏'))
dxTyGroup网络设备 = tryExceptNone(blGroupByzhejiu(dxTyData, '设备类型', '网络设备'))
dxTyGroup开发套件 = tryExceptNone(blGroupByzhejiu(dxTyData, '设备类型', '开发套件'))
dxTyGroup其他 = tryNoneto0(
    dxTyDataTotal)-tryNoneto0(
    dxTyGroup笔记本电脑)-tryNoneto0(
    dxTyGroup台式电脑)-tryNoneto0(
    dxTyGroup服务器)-tryNoneto0(
    dxTyGroup显示屏)-tryNoneto0(
    dxTyGroup网络设备)-tryNoneto0(
    dxTyGroup开发套件)

dxTyGroup笔记本电脑c = tryExceptNone(blGroupBygeshu(dxTyData, '设备类型', '笔记本电脑'))
dxTyGroup台式电脑c = tryExceptNone(blGroupBygeshu(dxTyData, '设备类型', '台式电脑'))
dxTyGroup服务器c = tryExceptNone(blGroupBygeshu(dxTyData, '设备类型', '服务器'))
dxTyGroup显示屏c = tryExceptNone(blGroupBygeshu(dxTyData, '设备类型', '显示屏'))
dxTyGroup网络设备c = tryExceptNone(blGroupBygeshu(dxTyData, '设备类型', '网络设备'))
dxTyGroup开发套件c = tryExceptNone(blGroupBygeshu(dxTyData, '设备类型', '开发套件'))
dxTyGroup其他c = tryNoneto0(
    dxTyDataTotalc)-tryNoneto0(
    dxTyGroup笔记本电脑c)-tryNoneto0(
    dxTyGroup台式电脑c)-tryNoneto0(
    dxTyGroup服务器c)-tryNoneto0(
    dxTyGroup显示屏c)-tryNoneto0(
    dxTyGroup网络设备c)-tryNoneto0(
    dxTyGroup开发套件c)

dxTyGroup笔记本电脑last = tryExceptNone(blGroupByzhejiu(dxTyDataLast, '设备类型', '笔记本电脑'))
dxTyGroup台式电脑last = tryExceptNone(blGroupByzhejiu(dxTyDataLast, '设备类型', '台式电脑'))
dxTyGroup服务器last = tryExceptNone(blGroupByzhejiu(dxTyDataLast, '设备类型', '服务器'))
dxTyGroup显示屏last = tryExceptNone(blGroupByzhejiu(dxTyDataLast, '设备类型', '显示屏'))
dxTyGroup网络设备last = tryExceptNone(blGroupByzhejiu(dxTyDataLast, '设备类型', '网络设备'))
dxTyGroup开发套件last = tryExceptNone(blGroupByzhejiu(dxTyDataLast, '设备类型', '开发套件'))
dxTyGroup其他last = tryNoneto0(
    dxTyDataTotalLast)-tryNoneto0(
    dxTyGroup笔记本电脑last)-tryNoneto0(
    dxTyGroup台式电脑last)-tryNoneto0(
    dxTyGroup服务器last)-tryNoneto0(
    dxTyGroup显示屏last)-tryNoneto0(
    dxTyGroup网络设备last)-tryNoneto0(
    dxTyGroup开发套件last)

dxTyGroup笔记本电脑clast = tryExceptNone(blGroupBygeshu(dxTyDataLast, '设备类型', '笔记本电脑'))
dxTyGroup台式电脑clast = tryExceptNone(blGroupBygeshu(dxTyDataLast, '设备类型', '台式电脑'))
dxTyGroup服务器clast = tryExceptNone(blGroupBygeshu(dxTyDataLast, '设备类型', '服务器'))
dxTyGroup显示屏clast = tryExceptNone(blGroupBygeshu(dxTyDataLast, '设备类型', '显示屏'))
dxTyGroup网络设备clast = tryExceptNone(blGroupBygeshu(dxTyDataLast, '设备类型', '网络设备'))
dxTyGroup开发套件clast = tryExceptNone(blGroupBygeshu(dxTyDataLast, '设备类型', '开发套件'))
dxTyGroup其他clast = tryNoneto0(
    dxTyDataTotalLastc)-tryNoneto0(
    dxTyGroup笔记本电脑clast)-tryNoneto0(
    dxTyGroup台式电脑clast)-tryNoneto0(
    dxTyGroup服务器clast)-tryNoneto0(
    dxTyGroup显示屏clast)-tryNoneto0(
    dxTyGroup网络设备clast)-tryNoneto0(
    dxTyGroup开发套件clast)


#mkt

mktGroup笔记本电脑 = tryExceptNone(blGroupByzhejiu(mktData, '设备类型', '笔记本电脑'))
mktGroup台式电脑 = tryExceptNone(blGroupByzhejiu(mktData, '设备类型', '台式电脑'))
mktGroup服务器 = tryExceptNone(blGroupByzhejiu(mktData, '设备类型', '服务器'))
mktGroup显示屏 = tryExceptNone(blGroupByzhejiu(mktData, '设备类型', '显示屏'))
mktGroup网络设备 = tryExceptNone(blGroupByzhejiu(mktData, '设备类型', '网络设备'))
mktGroup开发套件 = tryExceptNone(blGroupByzhejiu(mktData, '设备类型', '开发套件'))
mktGroup其他 = tryNoneto0(
    mktDataTotal)-tryNoneto0(
    mktGroup笔记本电脑)-tryNoneto0(
    mktGroup台式电脑)-tryNoneto0(
    mktGroup服务器)-tryNoneto0(
    mktGroup显示屏)-tryNoneto0(
    mktGroup网络设备)-tryNoneto0(
    mktGroup开发套件)

mktGroup笔记本电脑c = tryExceptNone(blGroupBygeshu(mktData, '设备类型', '笔记本电脑'))
mktGroup台式电脑c = tryExceptNone(blGroupBygeshu(mktData, '设备类型', '台式电脑'))
mktGroup服务器c = tryExceptNone(blGroupBygeshu(mktData, '设备类型', '服务器'))
mktGroup显示屏c = tryExceptNone(blGroupBygeshu(mktData, '设备类型', '显示屏'))
mktGroup网络设备c = tryExceptNone(blGroupBygeshu(mktData, '设备类型', '网络设备'))
mktGroup开发套件c = tryExceptNone(blGroupBygeshu(mktData, '设备类型', '开发套件'))
mktGroup其他c = tryNoneto0(
    mktDataTotalc)-tryNoneto0(
    mktGroup笔记本电脑c)-tryNoneto0(
    mktGroup台式电脑c)-tryNoneto0(
    mktGroup服务器c)-tryNoneto0(
    mktGroup显示屏c)-tryNoneto0(
    mktGroup网络设备c)-tryNoneto0(
    mktGroup开发套件c)

mktGroup笔记本电脑last = tryExceptNone(blGroupByzhejiu(mktDataLast, '设备类型', '笔记本电脑'))
mktGroup台式电脑last = tryExceptNone(blGroupByzhejiu(mktDataLast, '设备类型', '台式电脑'))
mktGroup服务器last = tryExceptNone(blGroupByzhejiu(mktDataLast, '设备类型', '服务器'))
mktGroup显示屏last = tryExceptNone(blGroupByzhejiu(mktDataLast, '设备类型', '显示屏'))
mktGroup网络设备last = tryExceptNone(blGroupByzhejiu(mktDataLast, '设备类型', '网络设备'))
mktGroup开发套件last = tryExceptNone(blGroupByzhejiu(mktDataLast, '设备类型', '开发套件'))
mktGroup其他last = tryNoneto0(
    mktDataTotalLast)-tryNoneto0(
    mktGroup笔记本电脑last)-tryNoneto0(
    mktGroup台式电脑last)-tryNoneto0(
    mktGroup服务器last)-tryNoneto0(
    mktGroup显示屏last)-tryNoneto0(
    mktGroup网络设备last)-tryNoneto0(
    mktGroup开发套件last)

mktGroup笔记本电脑clast = tryExceptNone(blGroupBygeshu(mktDataLast, '设备类型', '笔记本电脑'))
mktGroup台式电脑clast = tryExceptNone(blGroupBygeshu(mktDataLast, '设备类型', '台式电脑'))
mktGroup服务器clast = tryExceptNone(blGroupBygeshu(mktDataLast, '设备类型', '服务器'))
mktGroup显示屏clast = tryExceptNone(blGroupBygeshu(mktDataLast, '设备类型', '显示屏'))
mktGroup网络设备clast = tryExceptNone(blGroupBygeshu(mktDataLast, '设备类型', '网络设备'))
mktGroup开发套件clast = tryExceptNone(blGroupBygeshu(mktDataLast, '设备类型', '开发套件'))
mktGroup其他clast = tryNoneto0(
    mktDataTotalLastc)-tryNoneto0(
    mktGroup笔记本电脑clast)-tryNoneto0(
    mktGroup台式电脑clast)-tryNoneto0(
    mktGroup服务器clast)-tryNoneto0(
    mktGroup显示屏clast)-tryNoneto0(
    mktGroup网络设备clast)-tryNoneto0(
    mktGroup开发套件clast)


# oac

oacGroup笔记本电脑 = tryExceptNone(blGroupByzhejiu(oacData, '设备类型', '笔记本电脑'))
oacGroup台式电脑 = tryExceptNone(blGroupByzhejiu(oacData, '设备类型', '台式电脑'))
oacGroup服务器 = tryExceptNone(blGroupByzhejiu(oacData, '设备类型', '服务器'))
oacGroup显示屏 = tryExceptNone(blGroupByzhejiu(oacData, '设备类型', '显示屏'))
oacGroup网络设备 = tryExceptNone(blGroupByzhejiu(oacData, '设备类型', '网络设备'))
oacGroup开发套件 = tryExceptNone(blGroupByzhejiu(oacData, '设备类型', '开发套件'))
oacGroup其他 = tryNoneto0(
    oacDataTotal)-tryNoneto0(
    oacGroup笔记本电脑)-tryNoneto0(
    oacGroup台式电脑)-tryNoneto0(
    oacGroup服务器)-tryNoneto0(
    oacGroup显示屏)-tryNoneto0(
    oacGroup网络设备)-tryNoneto0(
    oacGroup开发套件)

oacGroup笔记本电脑c = tryExceptNone(blGroupBygeshu(oacData, '设备类型', '笔记本电脑'))
oacGroup台式电脑c = tryExceptNone(blGroupBygeshu(oacData, '设备类型', '台式电脑'))
oacGroup服务器c = tryExceptNone(blGroupBygeshu(oacData, '设备类型', '服务器'))
oacGroup显示屏c = tryExceptNone(blGroupBygeshu(oacData, '设备类型', '显示屏'))
oacGroup网络设备c = tryExceptNone(blGroupBygeshu(oacData, '设备类型', '网络设备'))
oacGroup开发套件c = tryExceptNone(blGroupBygeshu(oacData, '设备类型', '开发套件'))
oacGroup其他c = tryNoneto0(
    oacDataTotalc)-tryNoneto0(
    oacGroup笔记本电脑c)-tryNoneto0(
    oacGroup台式电脑c)-tryNoneto0(
    oacGroup服务器c)-tryNoneto0(
    oacGroup显示屏c)-tryNoneto0(
    oacGroup网络设备c)-tryNoneto0(
    oacGroup开发套件c)


oacGroup笔记本电脑last = tryExceptNone(blGroupByzhejiu(oacDataLast, '设备类型', '笔记本电脑'))
oacGroup台式电脑last = tryExceptNone(blGroupByzhejiu(oacDataLast, '设备类型', '台式电脑'))
oacGroup服务器last = tryExceptNone(blGroupByzhejiu(oacDataLast, '设备类型', '服务器'))
oacGroup显示屏last = tryExceptNone(blGroupByzhejiu(oacDataLast, '设备类型', '显示屏'))
oacGroup网络设备last = tryExceptNone(blGroupByzhejiu(oacDataLast, '设备类型', '网络设备'))
oacGroup开发套件last = tryExceptNone(blGroupByzhejiu(oacDataLast, '设备类型', '开发套件'))
oacGroup其他last = tryNoneto0(
    oacDataTotalLast)-tryNoneto0(
    oacGroup笔记本电脑last)-tryNoneto0(
    oacGroup台式电脑last)-tryNoneto0(
    oacGroup服务器last)-tryNoneto0(
    oacGroup显示屏last)-tryNoneto0(
    oacGroup网络设备last)-tryNoneto0(
    oacGroup开发套件last)

oacGroup笔记本电脑clast = tryExceptNone(blGroupBygeshu(oacDataLast, '设备类型', '笔记本电脑'))
oacGroup台式电脑clast = tryExceptNone(blGroupBygeshu(oacDataLast, '设备类型', '台式电脑'))
oacGroup服务器clast = tryExceptNone(blGroupBygeshu(oacDataLast, '设备类型', '服务器'))
oacGroup显示屏clast = tryExceptNone(blGroupBygeshu(oacDataLast, '设备类型', '显示屏'))
oacGroup网络设备clast = tryExceptNone(blGroupBygeshu(oacDataLast, '设备类型', '网络设备'))
oacGroup开发套件clast = tryExceptNone(blGroupBygeshu(oacDataLast, '设备类型', '开发套件'))
oacGroup其他clast = tryNoneto0(
    oacDataTotalLastc)-tryNoneto0(
    oacGroup笔记本电脑clast)-tryNoneto0(
    oacGroup台式电脑clast)-tryNoneto0(
    oacGroup服务器clast)-tryNoneto0(
    oacGroup显示屏clast)-tryNoneto0(
    oacGroup网络设备clast)-tryNoneto0(
    oacGroup开发套件clast)



# build graph

sx_wh_total = indicator_bl_total(sxDataTotal, sxDataTotalLast, "SX 总折旧")
ir_wh_total = indicator_bl_total(irDataTotal, irDataTotalLast, "IR 总折旧")
dxSku_wh_total = indicator_bl_total(dxSkuDataTotal, dxSkuDataTotalLast, "DX-SKU 总折旧")
dxTy_wh_total = indicator_bl_total(dxTyDataTotal, dxTyDataTotalLast, "DX-TY 总折旧")
mkt_wh_total = indicator_bl_total(mktDataTotal, mktDataTotalLast, "MKT 总折旧")
oac_wh_total = indicator_bl_total(oacDataTotal, oacDataTotalLast, "运赋 总折旧")

# 笔记本
sx_笔记本电脑= indicator_bl_total_mid(sxGroup笔记本电脑, sxGroup笔记本电脑last, '笔记本折旧')
ir_笔记本电脑 = indicator_bl_total_mid(irGroup笔记本电脑, irGroup笔记本电脑last, '笔记本折旧')
dxSku_笔记本电脑 = indicator_bl_total_mid(dxSkuGroup笔记本电脑, dxSkuGroup笔记本电脑last, '笔记本折旧')
dxTy_笔记本电脑 = indicator_bl_total_mid(dxTyGroup笔记本电脑, dxTyGroup笔记本电脑last, '笔记本折旧')
mkt_笔记本电脑 = indicator_bl_total_mid(mktGroup笔记本电脑, mktGroup笔记本电脑last, '笔记本折旧')
oac_笔记本电脑 = indicator_bl_total_mid(oacGroup笔记本电脑, oacGroup笔记本电脑last, '笔记本折旧')

sx_笔记本电脑c = indicator_bl_total_mid(sxGroup笔记本电脑c, sxGroup笔记本电脑clast, '笔记本数量')
ir_笔记本电脑c = indicator_bl_total_mid(irGroup笔记本电脑c, irGroup笔记本电脑clast, '笔记本数量')
dxSku_笔记本电脑c = indicator_bl_total_mid(dxSkuGroup笔记本电脑c, dxSkuGroup笔记本电脑clast, '笔记本数量')
dxTy_笔记本电脑c = indicator_bl_total_mid(dxTyGroup笔记本电脑c, dxTyGroup笔记本电脑clast, '笔记本数量')
mkt_笔记本电脑c = indicator_bl_total_mid(mktGroup笔记本电脑c, mktGroup笔记本电脑clast, '笔记本数量')
oac_笔记本电脑c = indicator_bl_total_mid(oacGroup笔记本电脑c, oacGroup笔记本电脑clast, '笔记本数量')


# 台式电脑
sx_台式电脑= indicator_bl_total_mid(sxGroup台式电脑, sxGroup台式电脑last, '台式折旧')
ir_台式电脑 = indicator_bl_total_mid(irGroup台式电脑, irGroup台式电脑last, '台式折旧')
dxSku_台式电脑 = indicator_bl_total_mid(dxSkuGroup台式电脑, dxSkuGroup台式电脑last, '台式折旧')
dxTy_台式电脑= indicator_bl_total_mid(dxTyGroup台式电脑, dxTyGroup台式电脑last, '台式折旧')
mkt_台式电脑 = indicator_bl_total_mid(mktGroup台式电脑, mktGroup台式电脑last, '台式折旧')
oac_台式电脑 = indicator_bl_total_mid(oacGroup台式电脑, oacGroup台式电脑last, '台式折旧')

sx_台式电脑c = indicator_bl_total_mid(sxGroup台式电脑c, sxGroup台式电脑clast, '台式数量')
ir_台式电脑c = indicator_bl_total_mid(irGroup台式电脑c, irGroup台式电脑clast, '台式数量')
dxSku_台式电脑c = indicator_bl_total_mid(dxSkuGroup台式电脑c, dxSkuGroup台式电脑clast, '台式数量')
dxTy_台式电脑c = indicator_bl_total_mid(dxTyGroup台式电脑c, dxTyGroup台式电脑clast, '台式数量')
mkt_台式电脑c = indicator_bl_total_mid(mktGroup台式电脑c, mktGroup台式电脑clast, '台式数量')
oac_台式电脑c = indicator_bl_total_mid(oacGroup台式电脑c, oacGroup台式电脑clast, '台式数量')


# 服务器
sx_服务器= indicator_bl_total_mid(sxGroup服务器, sxGroup服务器last, '服务器折旧')
ir_服务器 = indicator_bl_total_mid(irGroup服务器, irGroup服务器last, '服务器折旧')
dxSku_服务器 = indicator_bl_total_mid(dxSkuGroup服务器, dxSkuGroup服务器last, '服务器折旧')
dxTy_服务器= indicator_bl_total_mid(dxTyGroup服务器, dxTyGroup服务器last, '服务器折旧')
mkt_服务器 = indicator_bl_total_mid(mktGroup服务器, mktGroup服务器last, '服务器折旧')
oac_服务器 = indicator_bl_total_mid(oacGroup服务器, oacGroup服务器last, '服务器折旧')

sx_服务器c = indicator_bl_total_mid(sxGroup服务器c, sxGroup服务器clast, '服务器数量')
ir_服务器c = indicator_bl_total_mid(irGroup服务器c, irGroup服务器clast, '服务器数量')
dxSku_服务器c = indicator_bl_total_mid(dxSkuGroup服务器c, dxSkuGroup服务器clast, '服务器数量')
dxTy_服务器c = indicator_bl_total_mid(dxTyGroup服务器c, dxTyGroup服务器clast, '服务器数量')
mkt_服务器c = indicator_bl_total_mid(mktGroup服务器c, mktGroup服务器clast, '服务器数量')
oac_服务器c = indicator_bl_total_mid(oacGroup服务器c, oacGroup服务器clast, '服务器数量')


# 显示屏
sx_显示屏= indicator_bl_total_mid(sxGroup显示屏, sxGroup显示屏last, '显示屏折旧')
ir_显示屏 = indicator_bl_total_mid(irGroup显示屏, irGroup显示屏last, '显示屏折旧')
dxSku_显示屏 = indicator_bl_total_mid(dxSkuGroup显示屏, dxSkuGroup显示屏last, '显示屏折旧')
dxTy_显示屏= indicator_bl_total_mid(dxTyGroup显示屏, dxTyGroup显示屏last, '显示屏折旧')
mkt_显示屏 = indicator_bl_total_mid(mktGroup显示屏, mktGroup显示屏last, '显示屏折旧')
oac_显示屏 = indicator_bl_total_mid(oacGroup显示屏, oacGroup显示屏last, '显示屏折旧')

sx_显示屏c = indicator_bl_total_mid(sxGroup显示屏c, sxGroup显示屏clast, '显示屏数量')
ir_显示屏c = indicator_bl_total_mid(irGroup显示屏c, irGroup显示屏clast, '显示屏数量')
dxSku_显示屏c = indicator_bl_total_mid(dxSkuGroup显示屏c, dxSkuGroup显示屏clast, '显示屏数量')
dxTy_显示屏c = indicator_bl_total_mid(dxTyGroup显示屏c, dxTyGroup显示屏clast, '显示屏数量')
mkt_显示屏c = indicator_bl_total_mid(mktGroup显示屏c, mktGroup显示屏clast, '显示屏数量')
oac_显示屏c = indicator_bl_total_mid(oacGroup显示屏c, oacGroup显示屏clast, '显示屏数量')

# 网络设备
sx_网络设备= indicator_bl_total_mid(sxGroup网络设备, sxGroup网络设备last, '网络设备折旧')
ir_网络设备 = indicator_bl_total_mid(irGroup网络设备, irGroup网络设备last, '网络设备折旧')
dxSku_网络设备 = indicator_bl_total_mid(dxSkuGroup网络设备, dxSkuGroup网络设备last, '网络设备折旧')
dxTy_网络设备= indicator_bl_total_mid(dxTyGroup网络设备, dxTyGroup网络设备last, '网络设备折旧')
mkt_网络设备 = indicator_bl_total_mid(mktGroup网络设备, mktGroup网络设备last, '网络设备折旧')
oac_网络设备 = indicator_bl_total_mid(oacGroup网络设备, oacGroup网络设备last, '网络设备折旧')

sx_网络设备c = indicator_bl_total_mid(sxGroup网络设备c, sxGroup网络设备clast, '网络设备数量')
ir_网络设备c = indicator_bl_total_mid(irGroup网络设备c, irGroup网络设备clast, '网络设备数量')
dxSku_网络设备c = indicator_bl_total_mid(dxSkuGroup网络设备c, dxSkuGroup网络设备clast, '网络设备数量')
dxTy_网络设备c = indicator_bl_total_mid(dxTyGroup网络设备c, dxTyGroup网络设备clast, '网络设备数量')
mkt_网络设备c = indicator_bl_total_mid(mktGroup网络设备c, mktGroup网络设备clast, '网络设备数量')
oac_网络设备c = indicator_bl_total_mid(oacGroup网络设备c, oacGroup网络设备clast, '网络设备数量')


# 开发套件
sx_开发套件= indicator_bl_total_mid(sxGroup开发套件, sxGroup开发套件last, '开发套件折旧')
ir_开发套件 = indicator_bl_total_mid(irGroup开发套件, irGroup开发套件last, '开发套件折旧')
dxSku_开发套件 = indicator_bl_total_mid(dxSkuGroup开发套件, dxSkuGroup开发套件last, '开发套件折旧')
dxTy_开发套件= indicator_bl_total_mid(dxTyGroup开发套件, dxTyGroup开发套件last, '开发套件折旧')
mkt_开发套件 = indicator_bl_total_mid(mktGroup开发套件, mktGroup开发套件last, '开发套件折旧')
oac_开发套件 = indicator_bl_total_mid(oacGroup开发套件, oacGroup开发套件last, '开发套件折旧')

sx_开发套件c = indicator_bl_total_mid(sxGroup开发套件c, sxGroup开发套件clast, '开发套件数量')
ir_开发套件c = indicator_bl_total_mid(irGroup开发套件c, irGroup开发套件clast, '开发套件数量')
dxSku_开发套件c = indicator_bl_total_mid(dxSkuGroup开发套件c, dxSkuGroup开发套件clast, '开发套件数量')
dxTy_开发套件c = indicator_bl_total_mid(dxTyGroup开发套件c, dxTyGroup开发套件clast, '开发套件数量')
mkt_开发套件c = indicator_bl_total_mid(mktGroup开发套件c, mktGroup开发套件clast, '开发套件数量')
oac_开发套件c = indicator_bl_total_mid(oacGroup开发套件c, oacGroup开发套件clast, '开发套件数量')


# 其他
sx_其他= indicator_bl_total_mid(sxGroup其他, sxGroup其他last, '其他折旧')
ir_其他 = indicator_bl_total_mid(irGroup其他, irGroup其他last, '其他折旧')
dxSku_其他 = indicator_bl_total_mid(dxSkuGroup其他, dxSkuGroup其他last, '其他折旧')
dxTy_其他= indicator_bl_total_mid(dxTyGroup其他, dxTyGroup其他last, '其他折旧')
mkt_其他 = indicator_bl_total_mid(mktGroup其他, mktGroup其他last, '其他折旧')
oac_其他 = indicator_bl_total_mid(oacGroup其他, oacGroup其他last, '其他折旧')

sx_其他c = indicator_bl_total_mid(sxGroup其他c, sxGroup其他clast, '其他数量')
ir_其他c = indicator_bl_total_mid(irGroup其他c, irGroup其他clast, '其他数量')
dxSku_其他c = indicator_bl_total_mid(dxSkuGroup其他c, dxSkuGroup其他clast, '其他数量')
dxTy_其他c = indicator_bl_total_mid(dxTyGroup其他c, dxTyGroup其他clast, '其他数量')
mkt_其他c = indicator_bl_total_mid(mktGroup其他c, mktGroup其他clast, '其他数量')
oac_其他c = indicator_bl_total_mid(oacGroup其他c, oacGroup其他clast, '其他数量')



# 总折旧
irdc折旧 = 本月固定资产['折旧'].sum()
irdc折旧last = 上月固定资产['折旧'].sum()

irdc办公折旧 = 本月固定资产[本月固定资产['用途'] == '办公']['折旧'].sum()
irdc办公折旧last = 上月固定资产[上月固定资产['用途'] == '办公']['折旧'].sum()

irdc项目折旧 = 本月固定资产[本月固定资产['用途'] == '项目']['折旧'].sum()
irdc项目折旧last = 上月固定资产[上月固定资产['用途'] == '项目']['折旧'].sum()


irdc折旧c = 本月固定资产['资产代码'].count()
irdc折旧lastc = 上月固定资产['资产代码'].count()

irdc办公折旧c = 本月固定资产[(本月固定资产['用途'] == '办公') & (本月固定资产['折旧'] > 0)]['资产代码'].count()
irdc办公折旧lastc = 上月固定资产[(上月固定资产['用途'] == '办公') & (上月固定资产['折旧'] > 0)]['资产代码'].count()

irdc项目折旧c = 本月固定资产[(本月固定资产['用途'] == '项目') & (本月固定资产['折旧'] > 0)]['资产代码'].count()
irdc项目折旧lastc = 上月固定资产[(上月固定资产['用途'] == '项目') & (上月固定资产['折旧'] > 0)]['资产代码'].count()

# 净值
irdc净值 = 本月固定资产['净值'].sum()
irdc净值last = 上月固定资产['净值'].sum()

irdc办公净值 = 本月固定资产[本月固定资产['用途'] == '办公']['净值'].sum()
irdc办公净值last = 上月固定资产[上月固定资产['用途'] == '办公']['净值'].sum()

irdc项目净值 = 本月固定资产[本月固定资产['用途'] == '项目']['净值'].sum()
irdc项目净值last = 上月固定资产[上月固定资产['用途'] == '项目']['净值'].sum()

irdc净值c = 本月固定资产['资产代码'].count()
irdc净值lastc = 上月固定资产['资产代码'].count()

irdc办公净值c = 本月固定资产[本月固定资产['用途'] == '办公']['资产代码'].count()
irdc办公净值lastc = 上月固定资产[上月固定资产['用途'] == '办公']['资产代码'].count()

irdc项目净值c = 本月固定资产[本月固定资产['用途'] == '项目']['资产代码'].count()
irdc项目净值lastc = 上月固定资产[上月固定资产['用途'] == '项目']['资产代码'].count()


# 总值
irdc总值 = 本月固定资产['总值'].sum()
irdc总值last = 上月固定资产['总值'].sum()

irdc办公总值 = 本月固定资产[本月固定资产['用途'] == '办公']['总值'].sum()
irdc办公总值last = 上月固定资产[上月固定资产['用途'] == '办公']['总值'].sum()

irdc项目总值 = 本月固定资产[本月固定资产['用途'] == '项目']['总值'].sum()
irdc项目总值last = 上月固定资产[上月固定资产['用途'] == '项目']['总值'].sum()

irdc总值c = 本月固定资产['资产代码'].count()
irdc总值lastc = 上月固定资产['资产代码'].count()

irdc办公总值c = 本月固定资产[本月固定资产['用途'] == '办公']['资产代码'].count()
irdc办公总值lastc = 上月固定资产[上月固定资产['用途'] == '办公']['资产代码'].count()

irdc项目总值c = 本月固定资产[本月固定资产['用途'] == '项目']['资产代码'].count()
irdc项目总值lastc = 上月固定资产[上月固定资产['用途'] == '项目']['资产代码'].count()


# build graph
total_折旧 = indicator_bl_totalL(irdc折旧, irdc折旧last, "总折旧")
total_净值 = indicator_bl_totalL(irdc净值, irdc净值last, "总净值")
total_总值 = indicator_bl_totalL(irdc总值, irdc总值last, "总值")

total_办公折旧 = indicator_bl_total_midL(irdc办公折旧, irdc办公折旧last, "办公折旧")
total_办公净值 = indicator_bl_total_midL(irdc办公净值, irdc办公净值last, "办公净值")
total_办公总值 = indicator_bl_total_midL(irdc办公总值, irdc办公总值last, "办公总值")

total_项目折旧 = indicator_bl_total_midL(irdc项目折旧, irdc项目折旧last, "项目折旧")
total_项目净值 = indicator_bl_total_midL(irdc项目净值, irdc项目净值last, "项目净值")
total_项目总值 = indicator_bl_total_midL(irdc项目总值, irdc项目总值last, "项目总值")


total_折旧c = indicator_bl_totalL(irdc折旧, irdc折旧last, "折旧数")
total_净值c = indicator_bl_totalL(irdc净值, irdc净值last, "净值数")
total_总值c = indicator_bl_totalL(irdc总值, irdc总值last, "总值数")

total_办公折旧c = indicator_bl_total_midL(irdc办公折旧c, irdc办公折旧lastc, "办公折旧数")
total_办公净值c = indicator_bl_total_midL(irdc办公净值c, irdc办公净值lastc, "办公净值数")
total_办公总值c = indicator_bl_total_midL(irdc办公总值c, irdc办公总值lastc, "办公总值数")

total_项目折旧c = indicator_bl_total_midL(irdc项目折旧c, irdc项目折旧lastc, "项目折旧数")
total_项目净值c = indicator_bl_total_midL(irdc项目净值c, irdc项目净值lastc, "项目净值数")
total_项目总值c = indicator_bl_total_midL(irdc项目总值c, irdc项目总值lastc, "项目总值数")







sx_wh_total = indicator_bl_total(sxDataTotal, sxDataTotalLast, "SX 总人天")




sxWbsD = tryExceptNone(blGroupByTitle(sxData, 'WBS类型', 'D'))
sxWbsDLast = tryExceptNone(blGroupByTitle(sxDataLast, 'WBS类型', 'D'))
irWbsD = tryExceptNone(blGroupByTitle(irData, 'WBS类型', 'D'))
irWbsDLast = tryExceptNone(blGroupByTitle(irDataLast, 'WBS类型', 'D'))
dxSkuWbsD = tryExceptNone(blGroupByTitle(dxSkuData, 'WBS类型', 'D'))
dxSkuWbsDLast = tryExceptNone(blGroupByTitle(dxSkuDataLast, 'WBS类型', 'D'))
dxTyWbsD = tryExceptNone(blGroupByTitle(dxTyData, 'WBS类型', 'D'))
dxTyWbsDLast = tryExceptNone(blGroupByTitle(dxTyDataLast, 'WBS类型', 'D'))
mktWbsD = tryExceptNone(blGroupByTitle(mktData, 'WBS类型', 'D'))
mktWbsDLast = tryExceptNone(blGroupByTitle(mktDataLast, 'WBS类型', 'D'))
oacWbsD = tryExceptNone(blGroupByTitle(oacData, 'WBS类型', 'D'))
oacWbsDLast = tryExceptNone(blGroupByTitle(oacDataLast, 'WBS类型', 'D'))

sxWbsDper = tryExceptNone(blGroupByTitlePer(sxWbsD, sxData))
sxWbsDperLast = tryExceptNone(blGroupByTitlePer(sxWbsDLast, sxDataLast))
irWbsDper = tryExceptNone(blGroupByTitlePer(irWbsD, irData))
irWbsDperLast = tryExceptNone(blGroupByTitlePer(irWbsDLast, irDataLast))
dxSkuWbsDper = tryExceptNone(blGroupByTitlePer(dxSkuWbsD, dxSkuData))
dxSkuWbsDperLast = tryExceptNone(blGroupByTitlePer(dxSkuWbsDLast, dxSkuDataLast))
dxTyWbsDper = tryExceptNone(blGroupByTitlePer(dxTyWbsD, dxTyData))
dxTyWbsDperLast = tryExceptNone(blGroupByTitlePer(dxTyWbsDLast, dxTyDataLast))
mktWbsDper = tryExceptNone(blGroupByTitlePer(mktWbsD, mktData))
mktWbsDperLast = tryExceptNone(blGroupByTitlePer(mktWbsDLast, mktDataLast))
oacWbsDper = tryExceptNone(blGroupByTitlePer(oacWbsD, oacData))
oacWbsDperLast = tryExceptNone(blGroupByTitlePer(oacWbsDLast, oacDataLast))

sx_wbsD = indicator_bl_total_mid(sxWbsD, sxWbsDLast, 'D类')
ir_wbsD = indicator_bl_total_mid(irWbsD, irWbsDLast, 'D类')
dxSku_wbsD = indicator_bl_total_mid(dxSkuWbsD, dxSkuWbsDLast, 'D类')
dxTy_wbsD = indicator_bl_total_mid(dxTyWbsD, dxTyWbsDLast, 'D类')
mkt_wbsD = indicator_bl_total_mid(mktWbsD, mktWbsDLast, 'D类')
oac_wbsD = indicator_bl_total_mid(oacWbsD, oacWbsDLast, 'D类')

sx_wbsDper = indicator_bl_total_mid_rate(sxWbsDper, sxWbsDperLast, '占比')
ir_wbsDper = indicator_bl_total_mid_rate(irWbsDper, irWbsDperLast, '占比')
dxSku_wbsDper = indicator_bl_total_mid_rate(dxSkuWbsDper, dxSkuWbsDperLast, '占比')
dxTy_wbsDper = indicator_bl_total_mid_rate(dxTyWbsDper, dxTyWbsDperLast, '占比')
mkt_wbsDper = indicator_bl_total_mid_rate(mktWbsDper, mktWbsDperLast, '占比')
oac_wbsDper = indicator_bl_total_mid_rate(oacWbsDper, oacWbsDperLast, '占比')

sxWbsX = tryExceptNone(blGroupByFilter(sxData, 'PL111', '利润中心'))
sxWbsXLast = tryExceptNone(blGroupByFilter(sxDataLast, 'PL111', '利润中心'))
irWbsX = tryExceptNone(blGroupByFilter(irData, 'PL111', '利润中心'))
irWbsXLast = tryExceptNone(blGroupByFilter(irDataLast, 'PL111', '利润中心'))
dxSkuWbsX = tryExceptNone(blGroupByFilter(dxSkuData, 'PL111', '利润中心'))
dxSkuWbsXLast = tryExceptNone(blGroupByFilter(dxSkuDataLast, 'PL111', '利润中心'))
dxTyWbsX = tryExceptNone(blGroupByFilter(dxTyData, 'PL111', '利润中心'))
dxTyWbsXLast = tryExceptNone(blGroupByFilter(dxTyDataLast, 'PL111', '利润中心'))
mktWbsX = tryExceptNone(blGroupByFilter(mktData, 'PL111', '利润中心'))
mktWbsXLast = tryExceptNone(blGroupByFilter(mktDataLast, 'PL111', '利润中心'))
oacWbsX = tryExceptNone(blGroupByFilter(oacData, 'PL111', '利润中心'))
oacWbsXLast = tryExceptNone(blGroupByFilter(oacDataLast, 'PL111', '利润中心'))

sxWbsXper = tryExceptNone(blGroupByTitlePer(sxWbsX, sxData))
sxWbsXperLast = tryExceptNone(blGroupByTitlePer(sxWbsXLast, sxDataLast))
irWbsXper = tryExceptNone(blGroupByTitlePer(irWbsX, irData))
irWbsXperLast = tryExceptNone(blGroupByTitlePer(irWbsXLast, irDataLast))
dxSkuWbsXper = tryExceptNone(blGroupByTitlePer(dxSkuWbsX, dxSkuData))
dxSkuWbsXperLast = tryExceptNone(blGroupByTitlePer(dxSkuWbsXLast, dxSkuDataLast))
dxTyWbsXper = tryExceptNone(blGroupByTitlePer(dxTyWbsX, dxTyData))
dxTyWbsXperLast = tryExceptNone(blGroupByTitlePer(dxTyWbsXLast, dxTyDataLast))
mktWbsXper = tryExceptNone(blGroupByTitlePer(mktWbsX, mktData))
mktWbsXperLast = tryExceptNone(blGroupByTitlePer(mktWbsXLast, mktDataLast))
oacWbsXper = tryExceptNone(blGroupByTitlePer(oacWbsX, oacData))
oacWbsXperLast = tryExceptNone(blGroupByTitlePer(oacWbsXLast, oacDataLast))

sx_wbsX = indicator_bl_total_mid(sxWbsX, sxWbsXLast, '其他部门')
ir_wbsX = indicator_bl_total_mid(irWbsX, irWbsXLast, '其他部门')
dxSku_wbsX = indicator_bl_total_mid(dxSkuWbsX, dxSkuWbsXLast, '其他部门')
dxTy_wbsX = indicator_bl_total_mid(dxTyWbsX, dxTyWbsXLast, '其他部门')
mkt_wbsX = indicator_bl_total_mid(mktWbsX, mktWbsXLast, '其他部门')
oac_wbsX = indicator_bl_total_mid(oacWbsX, oacWbsXLast, '其他部门')

sx_wbsXper = indicator_bl_total_mid_rate(sxWbsXper, sxWbsXperLast, '占比')
ir_wbsXper = indicator_bl_total_mid_rate(irWbsXper, irWbsXperLast, '占比')
dxSku_wbsXper = indicator_bl_total_mid_rate(dxSkuWbsXper, dxSkuWbsXperLast, '占比')
dxTy_wbsXper = indicator_bl_total_mid_rate(dxTyWbsXper, dxTyWbsXperLast, '占比')
mkt_wbsXper = indicator_bl_total_mid_rate(mktWbsXper, mktWbsXperLast, '占比')
oac_wbsXper = indicator_bl_total_mid_rate(oacWbsXper, oacWbsXperLast, '占比')

modal = html.Div(
    [
        dbc.Button("Open modal", id="open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0,
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Row([
                html.Img(src=app.get_asset_url("img/dash-logo.png"), id="plotly-image",
                         style={"height": "60px", "width": "auto"}),
            ]),
        ),
        dbc.Col([
            # dbc.Row([
            #         dbc.Col([html.P(更新时间() + ' updated')]),
            # ]),
            dbc.Row([html.Div([
                dbc.Button("数据说明", id="open", n_clicks=0, color="transparent", ),
                dbc.Modal([
                    dbc.ModalBody(
                        html.Div(
                            className="markdown-text",
                            children=dcc.Markdown(
                                children=(
                                    """
                            ###### 【 ⏰ 工时数据说明】 
                            ###### 1、数据来源
                            上月26日-本月25日内OA工时填报已报送工时;
                            ###### 2、人员构成
                            部门正式员工、人力外包、实习生（不含外部门人员、项目外包成员、当月入离职员工）;
                            ###### 3、数据定义
                            理论工时：部门填写工时人数*当月工作日天数；
                            实际工时：OA工时填报中的已报送工时；
                            预计工时：PM对项目当月做出的[工时预估](https://docs.qq.com/sheet/DVkVZRUNseGJ4Q0tl?tab=7bdo9o)。
                            合理预估填报率：80% < 实际人天/预估人天 < 120%；
                            合理理论填报率：90% < 实际人天/理论人天 < 120%。
                            ###### 
                            ###### 【 💎 资源数据说明】 
                            ###### 1、GPU
                            数据来源于脚本自动抓取各集群每日整点GPU卡使用情况，可关注企微群 ` IRDC内部GPU资源调度群`  每日推送；
                            ###### 2、数据采标
                            数据爬取自Sensebee各采集标注任务，可关注企微群 ` IRDC数据采标任务群`  每日推送；
                            ###### 3、Open Cloud、DCP存储
                            数据来源每月财务账单
                            ###### 4、固定资产
                            数据来源每月财务账单

                        """
                                )), ), ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                    id="modal",
                    size="lg",
                    is_open=False,
                ),
            ])]),
        ]),
        dbc.Col([
            dcc.Tabs(id="tabs-title", value='工时', children=[
                dcc.Tab(label='工时', value='工时', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='资源', value='资源', style=tab_style, selected_style=tab_selected_style),
            ]),
        ], width=9)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='tabs-content')
        ])
    ])
], fluid=True)


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('pandas-output-container-1', 'value'),
    Input('产品线详细', 'value')
)
def select_bl(value):
    return value


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
@app.callback(
    Output("collapse2", "is_open"),
    [Input("collapse-button2", "n_clicks")],
    [State("collapse2", "is_open")],
)
@app.callback(
    Output("collapse3", "is_open"),
    [Input("collapse-button3", "n_clicks")],
    [State("collapse3", "is_open")],
)
@app.callback(
    Output("collapse4", "is_open"),
    [Input("collapse-button4", "n_clicks")],
    [State("collapse4", "is_open")],
)
@app.callback(
    Output("collapse6", "is_open"),
    [Input("collapse-button6", "n_clicks")],
    [State("collapse6", "is_open")],
)
@app.callback(
    Output("collapse7", "is_open"),
    [Input("collapse-button7", "n_clicks")],
    [State("collapse7", "is_open")],
)
@app.callback(
    Output("collapse8", "is_open"),
    [Input("collapse-button8", "n_clicks")],
    [State("collapse8", "is_open")],
)
@app.callback(
    Output("collapse9", "is_open"),
    [Input("collapse-button9", "n_clicks")],
    [State("collapse9", "is_open")],
)
@app.callback(
    Output("collapse10", "is_open"),
    [Input("collapse-button10", "n_clicks")],
    [State("collapse10", "is_open")],
)
@app.callback(
    Output("collapse11", "is_open"),
    [Input("collapse-button11", "n_clicks")],
    [State("collapse11", "is_open")],
)
@app.callback(
    Output("collapse12", "is_open"),
    [Input("collapse-button12", "n_clicks")],
    [State("collapse12", "is_open")],
)
@app.callback(
    Output("collapse13", "is_open"),
    [Input("collapse-button13", "n_clicks")],
    [State("collapse13", "is_open")],
)
@app.callback(
    Output("collapse14", "is_open"),
    [Input("collapse-button14", "n_clicks")],
    [State("collapse14", "is_open")],
)
@app.callback(
    Output("collapse15", "is_open"),
    [Input("collapse-button15", "n_clicks")],
    [State("collapse15", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open





def dfExist(df, dfNoStr, collbtn, coll):
    if len(df) > 1:
        return dbc.Row([collapse_btn_table(collbtn, "df", df,
                                           coll), ])
    else:
        return html.P(dfNoStr, style={"fontSize": 25, "color": "red"})


def dfExistDfStr(df, dfStr):
    if len(df) > 0:
        return dbc.Row([
            html.P(dfStr + str(len(df)),
                   style={"fontSize": 25}),
        ])
    else:
        return dbc.Row([])


def dfExistDf(df, dfStr):
    try:
        data = df
        if len(data) > 0:
            return dbc.Row([
                dbc.Col([
                    dash_table_not_collapse(dfStr, data)
                ]),
            ])
        else:
            return dbc.Row([])
    except:
        return dbc.Row([])

def dfExistDfLeftAlign(df, dfStr):
    try:
        data = df
        if len(data) > 0:
            return dbc.Row([
                dbc.Col([
                    dash_table_not_collapseLeftAlign(dfStr, data)
                ]),
            ])
        else:
            return dbc.Row([])
    except:
        return dbc.Row([])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs-title', 'value'))
def render_content(tab):
    if tab == '工时':
        return dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.P('工时年月-全局筛选', style={'fontSize': 20, 'color': 'blue'}),
                ], xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col([
                    dcc.Dropdown(
                        id='dropDown_工时year',
                        options=list(set(list(历史人员维度['工时年份']))),
                        value=max(历史人员维度['工时年份']),
                        clearable=False,
                        style={"width": "100%"},
                        placeholder='工时年份'
                    ),
                ], xs=5, sm=5, md=5, lg=5, xl=5),
                dbc.Col([
                    dcc.Dropdown(
                        id='dropDown_工时month',
                        options=list(set(list(历史人员维度['工时月份']))),
                        value=max(历史人员维度['工时月份']),
                        clearable=False,
                        style={"width": "100%"},
                        placeholder='工时月份'
                    ),
                ], xs=5, sm=5, md=5, lg=5, xl=5),
            ]),
            html.Br(),
            html.P('工时看板-快速查看', style={'fontSize': 20, 'color': 'blue'}),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('WBS类型'),
                    ], xs=2, sm=2, md=2, lg=2, xl=2),
                    dbc.Col([
                        dcc.Dropdown(
                            id='dropDown_wbs_type',
                            options=list(set(list(历史底表['WBS类型']))),
                            value=list(set(list(历史底表['WBS类型']))),
                            clearable=False,
                            multi=True,
                            style={"width": "100%"},
                            placeholder='WBS类型'
                        ),
                    ], xs=10, sm=10, md=10, lg=10, xl=10),
                ]),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            dcc.RadioItems(
                                id='radio_wh员工组vsWBS类型vs资源池',
                                options=[
                                    {'label': 'WBS类型', 'value': 'WBS类型'},
                                    {'label': '资源池', 'value': '资源池'},
                                    {'label': '员工组', 'value': '员工组'},
                                ],
                                value='WBS类型',
                                style={"width": "100%"},
                                inline=True),
                        ]),
                        html.Div([
                            dcc.RadioItems(
                                id='radio_wh利润中心vsWBS部门',
                                options=[
                                    {'label': '利润中心', 'value': '利润中心'},
                                    {'label': 'WBS所属部门', 'value': 'WBS所属部门'},
                                ],
                                value='利润中心',
                                style={"width": "100%"},
                                inline=True),
                        ]),
                        html.Div(
                            dcc.Graph(id='graph_wh利润中心vsWBS部门',
                                      style={'height': 500,
                                             "border-radius": "5px",
                                             "background-color": "#f9f9f9",
                                             "box-shadow": "2px 2px 2px lightgrey",
                                             "position": "relative",
                                             "margin-bottom": "15px"
                                             },
                                      config={'displayModeBar': False},
                                      ),
                        ),

                    ])
                ], xs=12, sm=12, md=6, lg=6, xl=6),
                dbc.Col([
                    html.Div([
                        html.Div([
                            dcc.RadioItems(
                                id='radio_wbsTop10',
                                options=[
                                    {'label': 'Bar', 'value': 'Bar'},
                                ],
                                value='Bar',
                                style={"width": "100%"},
                                inline=True),
                        ]),
                        html.Div([
                            dcc.RadioItems(
                                id='radio_wbsTop10_filter',
                                options=[
                                    {'label': '项目名称', 'value': '项目名称'},
                                ],
                                value='项目名称',
                                style={"width": "100%"},
                                inline=True),
                        ]),
                        html.Div([
                            dcc.Graph(id='graph_wbsTop10',
                                      style={'height': 500,
                                             "border-radius": "5px",
                                             "background-color": "#f9f9f9",
                                             "box-shadow": "2px 2px 2px lightgrey",
                                             "position": "relative",
                                             "margin-bottom": "15px"
                                             },
                                      config={'displayModeBar': False},
                                      ),
                        ]),
                    ])
                ], xs=12, sm=12, md=6, lg=6, xl=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            dcc.RadioItems(
                                id='radio_wh员工组vs资源池',
                                options=[
                                    {'label': 'WBS类型', 'value': 'WBS类型'},
                                    {'label': '员工组', 'value': '员工组'},
                                    {'label': '资源池', 'value': '资源池'},
                                    {'label': 'WBS状态', 'value': '未活跃WBS'},
                                ],
                                value='WBS类型',
                                style={"width": "100%"},
                                inline=True),
                        ]),
                        html.Div(
                            dcc.Graph(id='graph_wh员工组vs资源池',
                                      style={'height': 500,
                                             "border-radius": "5px",
                                             "background-color": "#f9f9f9",
                                             "box-shadow": "2px 2px 2px lightgrey",
                                             "position": "relative",
                                             "margin-bottom": "15px"
                                             },
                                      config={'displayModeBar': False},
                                      ),
                        ),

                    ])
                ],xs=12, sm=12, md=6, lg=6, xl=6),
                dbc.Col([
                    html.Div([
                        html.Div([
                            dcc.RadioItems(
                                id='radio_wh非业务线',
                                options=[
                                    {'label': 'WBS类型', 'value': 'WBS类型'},
                                    {'label': '员工组', 'value': '员工组'},
                                    {'label': '资源池', 'value': '资源池'},
                                ],
                                value='WBS类型',
                                style={"width": "100%"},
                                inline=True),
                        ]),
                        html.Div(
                            dcc.Graph(id='graph_wh非业务线',
                                      style={'height': 500,
                                             "border-radius": "5px",
                                             "background-color": "#f9f9f9",
                                             "box-shadow": "2px 2px 2px lightgrey",
                                             "position": "relative",
                                             "margin-bottom": "15px"
                                             },
                                      config={'displayModeBar': False},
                                      ),
                        ),

                    ])
                ],xs=12, sm=12, md=6, lg=6, xl=6),
            ]),
            html.Br(),
            html.Br(),
            html.P('工时看板-人员维度',style={'fontSize':20, 'color':'blue'}),
            html.P(id='renyuanweidu'),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="staff_number_indicator", config={'displayModeBar': False},
                              style={
                                  "background-color": "#f9f9f9",
                                  "box-shadow": "1px 1px 1px lightgrey",
                                  "position": "relative",
                                  "margin-bottom": "1px",
                                  "width": '120px'
                              }),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="staff_in_indicator",  config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="staff_out_indicator", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="staff_intern_indicator", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                    ])
                ]),
                dbc.Col([
                    dcc.Graph(id="logic_percentage", config={'displayModeBar': False},
                              style={
                                  "background-color": "#f9f9f9",
                                  "box-shadow": "1px 1px 1px lightgrey",
                                  "position": "relative",
                                  "margin-bottom": "1px",
                                  "width": '120px'
                              }),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="logic_in_percentage", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="logic_out_percentage", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="logic_intern_percentage", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                    ])
                ]),
                dbc.Col([
                    dcc.Graph(id="act_allday", config={'displayModeBar': False},
                              style={
                                  "background-color": "#f9f9f9",
                                  "box-shadow": "1px 1px 1px lightgrey",
                                  "position": "relative",
                                  "margin-bottom": "1px",
                                  "width": '120px'
                              }),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="act_in_day", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="act_out_day", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="act_intern_day", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                    ])
                ]),
                dbc.Col([
                    dcc.Graph(id="act_perday", config={'displayModeBar': False},
                              style={
                                  "background-color": "#f9f9f9",
                                  "box-shadow": "1px 1px 1px lightgrey",
                                  "position": "relative",
                                  "margin-bottom": "1px",
                                  "width": '120px'
                              }),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="act_in_perday", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="act_out_perday", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="act_intern_perday", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                    ])
                ]),
                dbc.Col([
                    dcc.Graph(id="attend_allday", config={'displayModeBar': False},
                              style={
                                  "background-color": "#f9f9f9",
                                  "box-shadow": "1px 1px 1px lightgrey",
                                  "position": "relative",
                                  "margin-bottom": "1px",
                                  "width": '120px'
                              }),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="attend_in_day", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="attend_out_day", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                        dcc.Graph(id="attend_intern_day", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "margin-left": "-12px",
                                      "width": '88px'
                                  }),
                    ])
                ]),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="sx_研究",  config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  }),
                        dcc.Graph(id="sx_研究per", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  })
                    ]),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="sx_开发", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  }),
                        dcc.Graph(id="sx_开发per", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  })
                    ]),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="sx_平台", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  }),
                        dcc.Graph(id="sx_平台per", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  })
                    ]),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="sx_测试", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  }),
                        dcc.Graph(id="sx_测试per", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  })
                    ]),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="sx_非", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  }),
                        dcc.Graph(id="sx_非per", config={'displayModeBar': False},
                                  style={
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '120px'
                                  })
                    ]),
                ]),

            ]),
            html.Br(),
            html.Div(
                dbc.Accordion([
                    dbc.AccordionItem([
                        dbc.Row([
                            dbc.Col([
                                irdc_graph('历史WBS类型-line', fig历史实际人均人天细分(历史部门实际人均人天()[['月份',name,'海外研发中心']]))
                            ]),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='员工所属部门汇总-summary',
                                          style={'height': 500,
                                                 'width': '100%',
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          ),
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                            dbc.Col([
                                dcc.Graph(id='员工所属部门汇总-bar',
                                          style={'height': 500,
                                                 'width': '100%',
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          ),
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                            html.Br(),
                            # dbc.Row([
                            #     dash_table.DataTable(
                            #         id='apartment_wh', ),
                            #     dash_table_not_collapse("apartment_wh", staff_资源池_table(cleanDF员工部门(cur_mon_staff,name))),
                            # ]),
                            # html.Br(),
                            html.Br(),
                            dbc.Row([
                                dcc.RadioItems(
                                    id='radio_历史WBS类型',
                                    options=[
                                        {'label': '资源池', 'value': '资源池'},
                                        {'label': '员工组', 'value': '员工组'},
                                        {'label': '岗位名称', 'value': '岗位名称'},
                                    ],
                                    value='资源池',
                                    style={"width": "60%"},
                                    inline=True),
                                ]),
                            dbc.Row([
                                dcc.Graph(id='业务线汇总-pie',
                                          style={'height': 500,
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          )]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            dcc.RadioItems(
                                                id='radio_产品线工时投入',
                                                options=[
                                                    {'label': '员工组', 'value': 'graph_员工组人天'},
                                                    {'label': '岗位名称', 'value': 'graph_岗位名称人天'},
                                                ],
                                                value='graph_员工组人天',
                                                style={"width": "60%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_产品线工时投入',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                        html.Br(),
                                        html.Div([
                                            dash_table.DataTable(
                                                id='table_产品线工时投入', )
                                        ]),
                                        html.Br(),
                                    ])
                                ]),
                            ]),
                            html.Br(),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.P(id="入离职名单", style={"fontSize": 25}),
                                dash_table.DataTable(id='入离职名单table'),
                            ]),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.P(id="未工时填报", style={"fontSize": 25}),
                                dash_table.DataTable(id='未工时填报table'),
                            ]),
                        ]),
                        html.Br(),
                        dbc.Col([
                            html.P(id="非正常工作日填报", style={"fontSize":25}),
                            dash_table.DataTable(id='非正常工作日填报table',
                                                 style_data_conditional=tbl_style(),
                                                 ),
                        ]),
                        html.Br(),
                        dbc.Row([
                            html.P(id="填报工时人员明细", style={"fontSize": 25}),
                        ]),
                        dbc.Row([
                            dash_table.DataTable(
                                id='cur_mon_staff_detailed',
                                style_data_conditional=tbl_style(),
                            )
                        ]),
                        html.Br(),
                        html.Br(),
                        html.P(
                            "查看员工历史工时填报（可用'填报率'筛选员工散点图，点击该散点查看历史工时；可输入员工姓名快速查看）",
                            style={"fontSize": 25}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.P("预估填报率:"),
                                    ], xs=4, sm=4, md=3, lg=3, xl=3),
                                    dbc.Col([
                                        dcc.RangeSlider(
                                            id='range-slider实际vs预估',
                                            step=1,
                                            allowCross=False, tooltip={"placement": "bottom", "always_visible": True}
                                        ),
                                    ], xs=8, sm=8, md=9, lg=9, xl=9),
                                ]),
                                dbc.Row([
                                    dcc.Graph(id='fig全量实际vs预估人天-scatter',
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "15px"
                                                     },
                                              config={'displayModeBar': False},
                                              ),
                                ]),
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.P("理论填报率:"),
                                    ], xs=4, sm=4, md=3, lg=3, xl=3),
                                    dbc.Col([
                                        dcc.RangeSlider(
                                            id='range-slider实际vs理论',
                                            step=1,
                                            allowCross=False, tooltip={"placement": "bottom", "always_visible": True}
                                        ),
                                    ], xs=8, sm=8, md=9, lg=9, xl=9),
                                ]),
                                dbc.Row([
                                    dcc.Graph(id='fig全量实际vs理论人天-scatter',
                                              config={'displayModeBar': False},
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "15px"
                                                     }
                                              ),
                                ]),
                            ], xs=12, sm=12, md=6, lg=6, xl=6)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.P(id="sameDaysWithStaff"),
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                            dbc.Col([
                                html.P(id="sameDaysWithStaff2"),
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.P('员工姓名'),
                            ], xs=12, sm=12, md=2, lg=2, xl=2),
                            dbc.Col([
                                dcc.Input(
                                    id="input_userName",
                                    type="text",
                                    style={'width': '100%'},
                                    placeholder="输入【员工姓名】查看历史工时",
                                ),

                            ], xs=12, sm=12, md=10, lg=10, xl=10),
                        ]),
                        html.Div(id="staffNameRemind"),
                        dbc.Row([
                            dcc.Graph(id='historical_days',
                                      style={'height': 400,
                                             "border-radius": "5px",
                                             "background-color": "#f9f9f9",
                                             "box-shadow": "2px 2px 2px lightgrey",
                                             "position": "relative",
                                             "margin-bottom": "15px"
                                             },
                                      config={'displayModeBar': False},
                                      )]),
                        dbc.Row([
                            dcc.Graph(id='historical_wbs_days',
                                      style={'height': 600,
                                             "border-radius": "5px",
                                             "background-color": "#f9f9f9",
                                             "box-shadow": "2px 2px 2px lightgrey",
                                             "position": "relative",
                                             "margin-bottom": "15px"
                                             },
                                      config={'displayModeBar': False},
                                      )]),
                    ], title='点击查看人员维度详细', )
                ], flush=True, start_collapsed=True, id="accordtion-staff")),
            html.Br(),
            html.Br(),
            html.P('工时看板-项目维度', style={'fontSize': 20, 'color': 'blue'}),
            html.P(id='wbsweidu'),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="wbs_all_number",  config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "2px 2px 2px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '620px'
                                  })
                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_d_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                         "background-color": "#f9f9f9",
                                         "box-shadow": "1px 1px 1px lightgrey",
                                         "position": "relative",
                                         "margin-bottom": "1px",
                                      "width":"110px",
                                         }),
                        dcc.Graph(id="sx_d_number",  config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_d_number",  config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_d_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_d_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_d_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_d_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_p_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "110px",
                                  }),
                        dcc.Graph(id="sx_p_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_p_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_p_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_p_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_p_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_p_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),

                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_r_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "110px",
                                  }),
                        dcc.Graph(id="sx_r_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_r_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_r_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_r_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_r_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_r_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_m_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "110px",
                                  }),
                        dcc.Graph(id="sx_m_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_m_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_m_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_m_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_m_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_m_number", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),

                    ]),
                ]),
                dbc.Col([
                    dbc.Row([
                        dcc.Graph(id="wbs_actual_hrs", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "2px 2px 2px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": '620px'
                                  })
                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_d_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "110px",
                                  }),
                        dcc.Graph(id="sx_d_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_d_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_d_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_d_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_d_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_d_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_p_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "110px",
                                  }),
                        dcc.Graph(id="sx_p_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_p_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_p_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_p_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_p_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_p_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_r_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "110px",
                                  }),
                        dcc.Graph(id="sx_r_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_r_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_r_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_r_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_r_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_r_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                    ]),
                    dbc.Row([
                        dcc.Graph(id="wbs_m_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "110px",
                                  }),
                        dcc.Graph(id="sx_m_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="ir_m_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="dx_m_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="innova_m_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="mkt_m_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                        dcc.Graph(id="oac_m_act", config={'displayModeBar': False},
                                  style={
                                      # "border-radius": "5px",
                                      "background-color": "#f9f9f9",
                                      "box-shadow": "1px 1px 1px lightgrey",
                                      "position": "relative",
                                      "margin-bottom": "1px",
                                      "width": "85px",
                                  }),
                    ]),
                ]),
            ]),
            html.Br(),
            html.Div(
                dbc.Accordion([
                    dbc.AccordionItem([
                        dbc.Row([
                            dbc.Col([
                                irdc_graph('历史WBS类型-line', fig历史WBS类型(历史WBS类型人天(历史底表)))
                            ]),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dcc.Graph(id='历史WBS类型-pie',
                                      style={'height': 500,
                                             "border-radius": "5px",
                                             "background-color": "#f9f9f9",
                                             "box-shadow": "2px 2px 2px lightgrey",
                                             "position": "relative",
                                             "margin-bottom": "15px"
                                             },
                                      config={'displayModeBar': False},
                                      )]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='WBS部门Top5-bar',
                                          style={'height': 500,
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          )
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                            dbc.Col([
                                dcc.Graph(id='WBS实际人天Top5-pie',
                                          style={'height': 500,
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          )
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                        ]),
                        html.Br(),
                        dbc.Col([
                            html.P(id="本月填报全部WBS", style={"fontSize": 25}),
                            dash_table.DataTable(id='本月填报全部WBStable',
                                                 style_data_conditional=tbl_style(), ),
                        ]),
                        # dbc.Row([
                        #     html.P('本月填报全部WBS（按实际人天倒序排序）: '+str(len(actual_wbs_tb(本月WBS维度))))
                        # ]),
                        # dbc.Col([
                        #     dash_table_not_collapse("WBS部门Top5_id",
                        #                             本月WBS维度.iloc[:, 0:-2]),
                        # ]),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.P('WBS类型'),
                                    ], xs=6, sm=6, md=2, lg=2, xl=2),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='dropDown_wbs类型',
                                            options=list(set(本月WBS维度['WBS类型'])),
                                            value='D',
                                            clearable=False,
                                            style={"width": "100%"},
                                            placeholder='WBS类型'
                                        ),
                                    ], xs=6, sm=6, md=4, lg=4, xl=4),
                                ]),
                                html.Div([
                                    html.Div([
                                        dcc.RadioItems(
                                            id='radio_产品线wbsD工时投入',
                                            options=[
                                                {'label': '员工组', 'value': 'graph_wbs员工组人天'},
                                                {'label': '岗位名称', 'value': 'graph_wbs岗位名称人天'},
                                                {'label': '员工姓名', 'value': 'graph_wbs员工姓名人天'},
                                                {'label': 'WBS部门', 'value': 'graph_wbsWBS部门人天'},
                                            ],
                                            value='graph_wbs员工组人天',
                                            style={"width": "60%"},
                                            inline=True),
                                    ]),
                                    html.Div([
                                        dcc.Graph(id='graph_产品线wbsD工时投入',
                                                  style={'height': 500,
                                                         "border-radius": "5px",
                                                         "background-color": "#f9f9f9",
                                                         "box-shadow": "2px 2px 2px lightgrey",
                                                         "position": "relative",
                                                         "margin-bottom": "15px"
                                                         },
                                                  config={'displayModeBar': False},
                                                  ),
                                    ]),
                                ])
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                            dbc.Col([
                                dbc.Row([
                                    html.P('员工投入到非IRDC利润中心的实际人天')
                                ]),
                                html.Div([
                                    html.Div([
                                        dcc.RadioItems(
                                            id='radio_产品线wbsX工时投入',
                                            options=[
                                                {'label': '员工组', 'value': 'graph_wbsX员工组人天'},
                                                {'label': '岗位名称', 'value': 'graph_wbsX岗位名称人天'},
                                                {'label': '员工姓名', 'value': 'graph_wbsX员工姓名人天'},
                                                {'label': 'WBS部门', 'value': 'graph_wbsXWBS部门人天'},
                                            ],
                                            value='graph_wbsX员工组人天',
                                            style={"width": "60%"},
                                            inline=True),
                                    ]),
                                    html.Div(
                                        dcc.Graph(id='graph_产品线wbsX工时投入',
                                                  style={'height': 500,
                                                         "border-radius": "5px",
                                                         "background-color": "#f9f9f9",
                                                         "box-shadow": "2px 2px 2px lightgrey",
                                                         "position": "relative",
                                                         "margin-bottom": "15px"
                                                         },
                                                  config={'displayModeBar': False},
                                                  ),
                                    ),

                                ])
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                        ]),
                        html.Br(),
                        dbc.Row([
                            html.Div([
                                html.Div([
                                    dcc.RadioItems(
                                        id='radio_wh非业务线项目名称vswbs部门',
                                        options=[
                                            {'label': '项目名称', 'value': '项目名称'},
                                            {'label': 'WBS所属部门', 'value': 'WBS所属部门'},
                                        ],
                                        value='项目名称',
                                        style={"width": "100%"},
                                        inline=True),
                                    dcc.RadioItems(
                                        id='radio_wh非业务线项目名称vswbs部门2',
                                        options=[
                                            {'label': 'WBS类型', 'value': 'WBS类型'},
                                            {'label': '员工组', 'value': '员工组'},
                                            {'label': '资源池', 'value': '资源池'},
                                            {'label': '员工姓名', 'value': '员工姓名'},
                                        ],
                                        value='资源池',
                                        style={"width": "100%"},
                                        inline=True),
                                ]),
                                html.Div(
                                    dcc.Graph(id='graph_wh非业务线项目名称vswbs部门',
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "5px"
                                                     },
                                              config={'displayModeBar': False},
                                              ),
                                ),
                            ])
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.P(id="未PL111工时", style={"fontSize": 25}),
                                dash_table.DataTable(id='未PL111工时table',
                                                 style_data_conditional=tbl_style(),),
                            ]),
                        ]),
                        html.Br(),
                        # dbc.Row([
                        #     html.P('本月填报的全部WBS：' + str(len(actual_wbs_tb(本月WBS维度))), style={"fontSize": 25})
                        # ]),
                        # dbc.Row([
                        #     dash_table_not_collapse_showAll("all_tb_WBS_id",
                        #                                     sortWBS(actual_wbs_tb(本月WBS维度).sort_values(
                        #                                         by=['实际人天', 'WBS所属部门'],
                        #                                         ascending=False).reset_index(drop=True)))
                        #
                        # ]),
                        # html.Br(),
                        html.Br(),
                        html.P("查看历史WBS工时填报记录（先选'部门'再选其下'项目名称'，可切换'岗位名称/员工组/员工姓名'查看历史分布）", style={"fontSize": 25}),
                        dbc.Row([
                            dbc.Col([
                                html.P('WBS类型'),
                            ], xs=12, sm=12, md=2, lg=2, xl=2),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='dropDown_wbs_type_wbsFilter',
                                    options=list(set(list(历史底表['WBS类型']))),
                                    value=list(set(list(历史底表['WBS类型']))),
                                    clearable=False,
                                    multi=True,
                                    style={"width": "100%"},
                                    placeholder='WBS类型'
                                ),
                            ], xs=12, sm=12, md=10, lg=10, xl=10),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.P('WBS所属部门'),
                            ], xs=12, sm=12, md=2, lg=2, xl=2),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='dropDown_利润中心wbs部门',
                                    options=[{'label': opt, 'value': opt} for opt in
                                             list(set(list(历史底表['WBS所属部门'])))],
                                    value=list(set(list(历史底表['WBS所属部门'])))[0],
                                    placeholder="选择WBS所属部门",
                                    clearable=False,
                                    style={"width": "100%"},
                                    # multi=True
                                ),
                            ], xs=12, sm=12, md=10, lg=10, xl=10),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.P('项目名称'),
                            ], xs=12, sm=12, md=2, lg=2, xl=2),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='dropDown_wbs名称',
                                    # options=[{'label': opt, 'value': opt} for opt in
                                    #          list(set(list(getAllWBS()['项目名称'])))],
                                    # value=list(set(list(getAllWBS()['项目名称'])))[0],
                                    clearable=False,
                                    placeholder="选择项目名称",
                                    style={"width": "100%"},
                                    # multi=True
                                ),
                            ], xs=12, sm=12, md=10, lg=10, xl=10),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dcc.RadioItems(
                                id='radio_资源池岗位名称员工姓名',
                                options=[
                                    {'label': '岗位名称', 'value': '岗位名称'},
                                    {'label': '员工组', 'value': '员工组'},
                                    {'label': '资源池', 'value': '资源池'},
                                    {'label': '员工姓名', 'value': '员工姓名'},
                                ],
                                value='岗位名称',
                                style={"width": "60%"},
                                inline=True),
                        ]),
                        dbc.Row([
                            dcc.Graph(id='wbsHistorical_days', config={'displayModeBar': False}, )
                        ]),
                        html.Div([
                            dash_table.DataTable(
                                id='table_历史wbs工时投入', )
                        ]),
                        html.Br(),
                    ], title='点击查看WBS维度详细'),
                ], flush=True, start_collapsed=True, id="accordtion-wbs")),
            html.Br(),
        ], fluid=True, id="accordtion-wh")

    elif tab == '资源':
        return dbc.Container([
            html.P("GPU使用情况 ( Update at " + GPU使用更新时间() + ' )'),
            dbc.Row([
                dbc.Col([
                    irdc_summary_large("gpu_sh40_avg_usage", gpu_sh40_avg_usage)
                ]),
                dbc.Col([
                    dbc.Row([
                        irdc_summary_smWider("gpu_sh40_10_usage", gpu_sh40_10_usage),
                        irdc_summary_smWider("gpu_sh40_14_usage", gpu_sh40_14_usage),
                        irdc_summary_smWider("gpu_sh40_18_usage", gpu_sh40_18_usage),
                        irdc_summary_smWider("gpu_sh40_22_usage", gpu_sh40_22_usage),
                    ])]),

                dbc.Col([
                    irdc_summary_large("gpu_sg2_avg_usage", gpu_sg2_avg_usage)
                ]),
                dbc.Col([
                    dbc.Row([
                        irdc_summary_smWider("gpu_sg2_10_usage", gpu_sg2_10_usage),
                        irdc_summary_smWider("gpu_sg2_14_usage", gpu_sg2_14_usage),
                        irdc_summary_smWider("gpu_sg2_18_usage", gpu_sg2_18_usage),
                        irdc_summary_smWider("gpu_sg2_22_usage", gpu_sg2_22_usage),
                    ])]),

                dbc.Col([
                    irdc_summary_large("gpu_sh1988_avg_usage", gpu_sh1988_avg_usage)
                ]),
                dbc.Col([
                    dbc.Row([
                        irdc_summary_smWider("gpu_sh1988_10_usage", gpu_sh1988_10_usage),
                        irdc_summary_smWider("gpu_sh1988_14_usage", gpu_sh1988_14_usage),
                        irdc_summary_smWider("gpu_sh1988_18_usage", gpu_sh1988_18_usage),
                        irdc_summary_smWider("gpu_sh1988_22_usage", gpu_sh1988_22_usage),
                    ])]),

                dbc.Col([
                    irdc_summary_large("gpu_abud_avg_usage", gpu_abud_avg_usage)
                ]),
                dbc.Col([
                    dbc.Row([
                        irdc_summary_smWider("gpu_abud_10_usage", gpu_abud_10_usage),
                        irdc_summary_smWider("gpu_abud_14_usage", gpu_abud_14_usage),
                        irdc_summary_smWider("gpu_abud_18_usage", gpu_abud_18_usage),
                        irdc_summary_smWider("gpu_abud_22_usage", gpu_abud_22_usage),
                    ])]),

            ]),
            html.Br(),
            # dbc.Row([
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_middleGpu("sx_fee_indicator", sx_fee),
            #             irdc_wh_middleGpu("sx_p_indicator", sx_p)
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_middleGpu("sx_1080T_fee_indicator", sx_1080T_fee),
            #             irdc_wh_middleGpu("sx_1080T_p_indicator", sx_1080T_p)
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_middleGpu("sx_V100_fee_indicator", sx_V100_fee),
            #             irdc_wh_middleGpu("sx_V100_p_indicator", sx_V100_p)
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_middleGpu("sx_A100_fee_indicator", sx_A100_fee),
            #             irdc_wh_middleGpu("sx_A100_p_indicator", sx_A100_p)
            #         ]),
            #     ]),
            # ]),
            # html.Br(),
            html.Div(
                dbc.Accordion(
                    [
                        dbc.AccordionItem([
                            # html.Div([
                            #     dcc.RadioItems(
                            #         id='radio_历史gpu费用',
                            #         options=[
                            #             {'label': '总费用', 'value': '总费用'},
                            #             {'label': '总卡数', 'value': '总卡数'},
                            #         ],
                            #         value='总费用',
                            #         style={"width": "80%"},
                            #         inline=True),
                            # ]),
                            # html.Div([
                            #     dcc.Graph(id='graph_历史gpu费用',
                            #               style={'height': 500,
                            #                      "border-radius": "5px",
                            #                      "background-color": "#f9f9f9",
                            #                      "box-shadow": "2px 2px 2px lightgrey",
                            #                      "position": "relative",
                            #                      "margin-bottom": "15px"
                            #                      },
                            #               config={'displayModeBar': False},
                            #               ),
                            # ]),
                            html.Div([
                                html.Div([
                                    dcc.RadioItems(
                                        id='radio_gpu_filter',
                                        options=[
                                            {'label': '使用率', 'value': '使用率'},
                                            # {'label': '累计使用节点', 'value': '累计使用节点'},
                                            # {'label': '累计使用时长', 'value': '累计使用时长'},
                                        ],
                                        value='使用率',
                                        style={"width": "60%"},
                                        inline=True),

                                ]),
                                html.Div([
                                    dcc.RadioItems(
                                        id='radio_gpu_use',
                                        options=[
                                            {'label': 'Avg', 'value': 'graph_gpu_avg'},
                                            # {'label': '10点', 'value': 'graph_gpu_10'},
                                            # {'label': '14点', 'value': 'graph_gpu_14'},
                                            # {'label': '18点', 'value': 'graph_gpu_18'},
                                            # {'label': '22点', 'value': 'graph_gpu_22'},
                                        ],
                                        value='graph_gpu_avg',
                                        style={"width": "60%"},
                                        inline=True),
                                ]),
                                html.Div(
                                    dcc.Graph(id='graph_gpu_use',
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "15px"
                                                     },
                                              config={'displayModeBar': False},
                                              ),
                                ),
                                html.Br(),
                                html.Div([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('员工所属部门'),
                                        ], xs=6, sm=6, md=3, lg=3, xl=3),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='dropDown_gpu_user_filter',
                                                options=[name],
                                                value=[name],
                                                clearable=False,
                                                multi=True,
                                                style={"width": "100%"},
                                                placeholder='员工所属部门'
                                            ),
                                        ], xs=6, sm=6, md=9, lg=9, xl=9),
                                    ]),
                                ]),
                                html.Div([
                                    dcc.RadioItems(
                                        id='radio_gpu_user_filter',
                                        options=[
                                            {'label': '累计使用节点', 'value': '累计使用节点'},
                                            {'label': '累计使用时长（小时）', 'value': '累计使用时长'},
                                        ],
                                        value='累计使用节点',
                                        style={"width": "60%"},
                                        inline=True),
                                ]),
                                html.Div(
                                    dcc.Graph(id='graph_gpu_user_use',
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "15px"
                                                     },
                                              config={'displayModeBar': False},
                                              ),
                                ),

                            ]),
                            html.Br(),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('使用率月'),
                                        ], xs=6, sm=6, md=4, lg=4, xl=4),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='dropDown_gpu_util',
                                                options=list(set(gpu费用['month'])),
                                                value=max(list(set(gpu费用['month']))),
                                                clearable=False,
                                                style={"width": "100%"},
                                                placeholder='使用率'
                                            ),
                                        ], xs=6, sm=6, md=3, lg=3, xl=3),
                                    ]),
                                ]),
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('总费用月'),
                                        ], xs=6, sm=6, md=4, lg=4, xl=4),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='dropDown_gpu_fee',
                                                options=list(set(gpu费用['month'])),
                                                value=max(list(set(gpu费用['month']))),
                                                clearable=False,
                                                style={"width": "100%"},
                                                placeholder='总费用'
                                            ),
                                        ], xs=6, sm=6, md=3, lg=3, xl=3),
                                    ]),

                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            dcc.RadioItems(
                                                id='radio_使用率月份',
                                                options=[
                                                    {'label': '员工组', 'value': 'graph_gpu员工组util'},
                                                    {'label': '岗位名称', 'value': 'graph_gpu岗位名称util'},
                                                    {'label': '员工姓名', 'value': 'graph_gpu员工姓名util'},

                                                ],
                                                value='graph_gpu员工姓名util',
                                                style={"width": "80%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_使用率月份',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      ),
                                        ]),
                                    ])
                                ]
                                    , xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            dcc.RadioItems(
                                                id='radio_总费用月份',
                                                options=[
                                                    {'label': '员工组', 'value': 'graph_gpu员工组fee'},
                                                    {'label': '岗位名称', 'value': 'graph_gpu岗位名称fee'},
                                                    {'label': '员工姓名', 'value': 'graph_gpu员工姓名fee'},
                                                ],
                                                value='graph_gpu员工姓名fee',
                                                style={"width": "80%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_总费用月份',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      ),
                                        ]),
                                    ])
                                ]
                                    , xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('使用节点月'),
                                        ], xs=6, sm=6, md=4, lg=4, xl=4),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='dropDown_gpu_month',
                                                options=list(set(gpu底表['month'])),
                                                value=max(list(set(gpu底表['month']))),
                                                clearable=False,
                                                style={"width": "100%"},
                                                placeholder='使用节点'
                                            ),
                                        ], xs=6, sm=6, md=3, lg=3, xl=3),
                                    ]),
                                ]),
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('累计时长月'),
                                        ], xs=6, sm=6, md=4, lg=4, xl=4),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='dropDown_gpu_month2',
                                                options=list(set(gpu底表['month'])),
                                                value=max(list(set(gpu底表['month']))),
                                                clearable=False,
                                                style={"width": "100%"},
                                                placeholder='累计时长'
                                            ),
                                        ], xs=6, sm=6, md=3, lg=3, xl=3),
                                    ]),

                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            dcc.RadioItems(
                                                id='radio_使用节点月份',
                                                options=[
                                                    {'label': '员工组', 'value': 'graph_gpu员工组'},
                                                    {'label': '岗位名称', 'value': 'graph_gpu岗位名称'},
                                                    {'label': '员工姓名', 'value': 'graph_gpu员工姓名'},

                                                ],
                                                value='graph_gpu员工姓名',
                                                style={"width": "80%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_使用节点月份',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      ),
                                        ]),
                                    ])
                                ]
                                    , xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            dcc.RadioItems(
                                                id='radio_累计时长月份',
                                                options=[
                                                    {'label': '员工组', 'value': 'graph_gpu员工组2'},
                                                    {'label': '岗位名称', 'value': 'graph_gpu岗位名称2'},
                                                    {'label': '员工姓名', 'value': 'graph_gpu员工姓名2'},
                                                ],
                                                value='graph_gpu员工姓名2',
                                                style={"width": "80%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_累计时长月份',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      ),
                                        ]),
                                    ])
                                ]
                                    , xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    irdc_graph('gpuTop10userNodes-bar', figGpuUserTimeTop10资源池(monthly_gpu资源池(gpu底表)))
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    irdc_graph('gpuTop10userTime-bar', figGpuUserTimeTop10资源池(monthly_gpu资源池(gpu底表)))
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            dbc.Col([
                                dash_table_not_collapse("gpuTop10userNodes_id", monthly_gpu资源池(gpu底表)),
                            ]),
                            html.Br(),
                            html.Br(),
                        ],
                            title='点击查看GPU使用详细',
                        )
                    ],

                    flush=True, start_collapsed=True, id="accordtion-gpu"
                ),
            ),

            html.Br(),
            html.P("DCP与OC存储  ( Update at " + OC存储更新时间() + ' )'),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        irdc_wh_largeLL("total_dcp_indicator", total_dcp)
                    ]),
                    dbc.Row([
                        irdc_wh_middleLL("total_lustre_indicator", total_lustre),
                        irdc_wh_middleLL("total_ceph_indicator", total_ceph)
                    ]),
                ]),
                dbc.Col([
                    dbc.Row([
                        irdc_wh_largeLL("total_octotal_indicator", total_octotal)
                    ]),
                    dbc.Row([
                        irdc_wh_middleLL("total_oc_indicator", total_oc),
                        irdc_wh_middleLL("total_diamond_indicator", total_diamond)
                    ]),

                ]),
            ]),
            html.Br(),
            # dbc.Row([
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("sx_total_indicator", sx_totalRes)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_笔记本电脑_indicator", sx_lustre),
            #             irdc_wh_middle("sx_笔记本电脑c_indicator", sx_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_台式电脑_indicator", sx_ceph),
            #             irdc_wh_middle("sx_台式电脑c_indicator", sx_台式电脑c)
            #         ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("sx_服务器_indicator", sx_oc),
            #         #     irdc_wh_middle("sx_服务器c_indicator", sx_服务器c)
            #         # ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("sx_显示屏_indicator", sx_diamond),
            #         #     irdc_wh_middle("sx_显示屏c_indicator", sx_显示屏c)
            #         # ]),
            #
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("ir_total_indicator", ir_totalRes)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_笔记本电脑_indicator", ir_lustre),
            #             irdc_wh_middle("ir_笔记本电脑c_indicator", ir_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_台式电脑_indicator", ir_ceph),
            #             irdc_wh_middle("ir_台式电脑c_indicator", ir_台式电脑c)
            #         ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("ir_服务器_indicator", ir_oc),
            #         #     irdc_wh_middle("ir_服务器c_indicator", ir_服务器c)
            #         # ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("ir_显示屏_indicator", ir_diamond),
            #         #     irdc_wh_middle("ir_显示屏c_indicator", ir_显示屏c)
            #         # ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("dxSku_total_indicator", dxSku_totalRes)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_笔记本电脑_indicator", dxSku_lustre),
            #             irdc_wh_middle("dxSku_笔记本电脑c_indicator", dxSku_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_台式电脑_indicator", dxSku_ceph),
            #             irdc_wh_middle("dxSku_台式电脑c_indicator", dxSku_台式电脑c)
            #         ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("dxSku_服务器_indicator", dxSku_oc),
            #         #     irdc_wh_middle("dxSku_服务器c_indicator", dxSku_服务器c)
            #         # ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("dxSku_显示屏_indicator", dxSku_diamond),
            #         #     irdc_wh_middle("dxSku_显示屏c_indicator", dxSku_显示屏c)
            #         # ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("dxTy_total_indicator", dxTy_totalRes)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_笔记本电脑_indicator", dxTy_lustre),
            #             irdc_wh_middle("dxTy_笔记本电脑c_indicator", dxTy_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_台式电脑_indicator", dxTy_ceph),
            #             irdc_wh_middle("dxTy_台式电脑c_indicator", dxTy_台式电脑c)
            #         ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("dxTy_服务器_indicator", dxTy_oc),
            #         #     irdc_wh_middle("dxTy_服务器c_indicator", dxTy_服务器c)
            #         # ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("dxTy_显示屏_indicator", dxTy_diamond),
            #         #     irdc_wh_middle("dxTy_显示屏c_indicator", dxTy_显示屏c)
            #         # ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("mkt_total_indicator", mkt_totalRes)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_笔记本电脑_indicator", mkt_lustre),
            #             irdc_wh_middle("mkt_笔记本电脑c_indicator", mkt_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_台式电脑_indicator", mkt_ceph),
            #             irdc_wh_middle("mkt_台式电脑c_indicator", mkt_台式电脑c)
            #         ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("mkt_服务器_indicator", mkt_oc),
            #         #     irdc_wh_middle("mkt_服务器c_indicator", mkt_服务器c)
            #         # ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("mkt_显示屏_indicator", mkt_diamond),
            #         #     irdc_wh_middle("mkt_显示屏c_indicator", mkt_显示屏c)
            #         # ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("oac_total_indicator", oac_totalRes)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_笔记本电脑_indicator", oac_lustre),
            #             irdc_wh_middle("oac_笔记本电脑c_indicator", oac_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_台式电脑_indicator", oac_ceph),
            #             irdc_wh_middle("oac_台式电脑c_indicator", oac_台式电脑c)
            #         ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("oac_服务器_indicator", oac_oc),
            #         #     irdc_wh_middle("oac_服务器c_indicator", oac_服务器c)
            #         # ]),
            #         # dbc.Row([
            #         #     irdc_wh_middle("oac_显示屏_indicator", oac_diamond),
            #         #     irdc_wh_middle("oac_显示屏c_indicator", oac_显示屏c)
            #         # ]),
            #     ]),
            # ]),
            # html.Br(),
            html.Div([
                dbc.Accordion(
                    [
                        dbc.AccordionItem([
                            html.Div(
                                irdc_graph('graph_历史资源费用-line', fig历史资源费用(历史资源总费用细分(历史dcp, sumResDf)))
                            ),
                            html.Br(),
                            html.Div([
                                dcc.RadioItems(
                                    id='radio_oc月环比',
                                    options=[
                                        {'label': '资源池', 'value': '资源池'},
                                        {'label': '单项资源类型', 'value': '单项资源类型'},
                                        {'label': '员工组', 'value': '员工组'},
                                        {'label': '岗位名称', 'value': '岗位名称'},
                                        {'label': '用户名', 'value': '用户名'},
                                    ],
                                    value='用户名',
                                    style={"width": "60%"},
                                    inline=True),
                            ]),
                            html.Div([
                                dcc.Graph(id='oc月环比-pie',
                                          style={'height': 500,
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          )]),
                            html.Br(),
                            html.Div([
                                dcc.RadioItems(
                                    id='radio_diamond月环比',
                                    options=[
                                        {'label': '资源池', 'value': '资源池'},
                                        {'label': '单项资源类型', 'value': '单项资源类型'},
                                        {'label': '员工组', 'value': '员工组'},
                                        {'label': '岗位名称', 'value': '岗位名称'},
                                        {'label': '用户名', 'value': '用户名'},
                                    ],
                                    value='用户名',
                                    style={"width": "60%"},
                                    inline=True),
                            ]),
                            html.Div([
                                dcc.Graph(id='diamond月环比-pie',
                                          style={'height': 500,
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          )]),
                            html.Br(),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.P('费用月'),
                                                ], xs=6, sm=6, md=4, lg=4, xl=4),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='dropDown_oc_month',
                                                        options=list(set(历史ocUser['资源月份'])),
                                                        value=max(list(set(历史ocUser['资源月份']))),
                                                        clearable=False,
                                                        style={"width": "100%"},
                                                        placeholder='费用月'
                                                    ),
                                                ], xs=6, sm=6, md=3, lg=3, xl=3),
                                            ]),

                                            dcc.RadioItems(
                                                id='radio_oc使用量费用',
                                                options=[
                                                    {'label': '已使用量', 'value': '已使用量'},
                                                    {'label': '费用(元)', 'value': '费用(元)'},
                                                ],
                                                value='费用(元)',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_oc使用量费用全选项',
                                                options=[
                                                    {'label': '资源池', 'value': '资源池'},
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '单项资源类型', 'value': '单项资源类型'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '用户名', 'value': '用户名'},
                                                ],
                                                value='用户名',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_oc使用量费用',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.P('费用月'),
                                                ], xs=6, sm=6, md=4, lg=4, xl=4),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='dropDown_oc_month2',
                                                        options=list(set(历史ocUser['资源月份'])),
                                                        value=max(list(set(历史ocUser['资源月份']))),
                                                        clearable=False,
                                                        style={"width": "100%"},
                                                        placeholder='费用月'
                                                    ),
                                                ], xs=6, sm=6, md=3, lg=3, xl=3),
                                            ]),

                                            dcc.RadioItems(
                                                id='radio_oc使用量费用2',
                                                options=[
                                                    {'label': '已使用量', 'value': '已使用量'},
                                                    {'label': '费用(元)', 'value': '费用(元)'},
                                                ],
                                                value='费用(元)',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_oc使用量费用全选项2',
                                                options=[
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '单项资源类型', 'value': '单项资源类型'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '用户名', 'value': '用户名'},
                                                ],
                                                value='用户名',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_oc使用量费用2',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.P('费用月'),
                                                ], xs=6, sm=6, md=4, lg=4, xl=4),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='dropDown_diamond_month',
                                                        options=list(set(历史diamondUser['资源月份'])),
                                                        value=max(list(set(历史diamondUser['资源月份']))),
                                                        clearable=False,
                                                        style={"width": "100%"},
                                                        placeholder='费用月'
                                                    ),
                                                ], xs=6, sm=6, md=3, lg=3, xl=3),
                                            ]),

                                            dcc.RadioItems(
                                                id='radio_diamond使用量费用',
                                                options=[
                                                    {'label': '已使用量', 'value': '已使用量'},
                                                    {'label': '费用(元)', 'value': '费用(元)'},
                                                ],
                                                value='费用(元)',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_diamond使用量费用全选项',
                                                options=[
                                                    {'label': '资源池', 'value': '资源池'},
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '单项资源类型', 'value': '单项资源类型'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '用户名', 'value': '用户名'},
                                                ],
                                                value='用户名',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_diamond使用量费用',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.P('费用月'),
                                                ], xs=6, sm=6, md=4, lg=4, xl=4),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='dropDown_diamond_month2',
                                                        options=list(set(历史diamondUser['资源月份'])),
                                                        value=max(list(set(历史diamondUser['资源月份']))),
                                                        clearable=False,
                                                        style={"width": "100%"},
                                                        placeholder='费用月'
                                                    ),
                                                ], xs=6, sm=6, md=3, lg=3, xl=3),
                                            ]),

                                            dcc.RadioItems(
                                                id='radio_diamond使用量费用2',
                                                options=[
                                                    {'label': '已使用量', 'value': '已使用量'},
                                                    {'label': '费用(元)', 'value': '费用(元)'},
                                                ],
                                                value='费用(元)',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_diamond使用量费用全选项2',
                                                options=[
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '单项资源类型', 'value': '单项资源类型'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '用户名', 'value': '用户名'},
                                                ],
                                                value='用户名',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_diamond使用量费用2',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),

                            dfExistDfStr(新增Tb(cleanUser(本月ocUser, "OCID", '单项资源使用量'),
                                                cleanUser(上月ocUser, "OCID", '单项资源使用量'), "OCID",
                                                '单项资源使用量'),
                                         '环比新增OC资源(本月OC明细, 按照费用倒序排序)：'),
                            dfExistDf(新增Tb(cleanUser(本月ocUser, "OCID", '单项资源使用量'),
                                             cleanUser(上月ocUser, "OCID", '单项资源使用量'), "OCID",
                                             "单项资源使用量"), 'oc新增table'),
                            html.Br(),
                            dfExistDfStr(减少Tb(cleanUser(本月ocUser, "OCID", '单项资源使用量'),
                                                cleanUser(上月ocUser, "OCID", '单项资源使用量'), "OCID",
                                                '单项资源使用量'),
                                         '环比减少OC资源(上月OC明细, 按照费用倒序排序)：'),
                            dfExistDf(减少Tb(cleanUser(本月ocUser, "OCID", '单项资源使用量'),
                                             cleanUser(上月ocUser, "OCID", '单项资源使用量'), "OCID",
                                             "单项资源使用量"), 'oc减少table'),

                            html.Br(),
                            dfExistDfStr(新增Tb(cleanUser(本月diamondUser, "diamondID", '单项资源使用量'),
                                                cleanUser(上月diamondUser, "diamondID", '单项资源使用量'), "diamondID",
                                                '单项资源使用量'),
                                         '环比新增diamond资源(本月diamond明细, 按照费用倒序排序)：'),
                            dfExistDf(新增Tb(cleanUser(本月diamondUser, "diamondID", '单项资源使用量'),
                                             cleanUser(上月diamondUser, "diamondID", '单项资源使用量'), "diamondID",
                                             "单项资源使用量"), 'diamond新增table'),
                            html.Br(),
                            dfExistDfStr(减少Tb(cleanUser(本月diamondUser, "diamondID", '单项资源使用量'),
                                                cleanUser(上月diamondUser, "diamondID", '单项资源使用量'), "diamondID",
                                                '单项资源使用量'),
                                         '环比减少diamond资源(上月diamond明细, 按照费用倒序排序)：'),
                            dfExistDf(减少Tb(cleanUser(本月diamondUser, "diamondID", '单项资源使用量'),
                                             cleanUser(上月diamondUser, "diamondID", '单项资源使用量'), "diamondID",
                                             "单项资源使用量"), 'diamond减少table'),

                            html.Br(),
                            html.P('本月OC明细'),
                            html.Div([
                                dfExistDf(本月oc.iloc[:, :-2], 'table_本月OC明细')
                            ]),
                            html.Br(),
                            html.P('本月Diamond明细'),
                            html.Div([
                                dfExistDf(本月diamond.iloc[:, :-2], 'table_本月Diamond明细')
                            ]),

                        ],
                            title='点击查看OC存储详细',
                        )
                    ],
                    flush=True, start_collapsed=True, id="accordtion-oc"
                ),
                html.Br(),
                dbc.Accordion(
                    [
                        dbc.AccordionItem([
                            # html.Div(
                            #     irdc_graph('graph_历史dcp-line', fig历史dcp())
                            # ),
                            html.Br(),
                            html.Div([
                                dcc.RadioItems(
                                    id='radio_dcp月环比',
                                    options=[
                                        {'label': '集群名称', 'value': '集群名称'},
                                        {'label': '存储类型(SSD/HDD)', 'value': '存储类型(SSD/HDD)'},
                                        {'label': '员工组', 'value': '员工组'},
                                        {'label': '岗位名称', 'value': '岗位名称'},
                                        {'label': '用户名', 'value': '用户名'},
                                    ],
                                    value='集群名称',
                                    style={"width": "60%"},
                                    inline=True),
                            ]),
                            html.Div([
                                dcc.Graph(id='dcp月环比-pie',
                                          style={'height': 500,
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          )]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.P('费用月'),
                                                ], xs=6, sm=6, md=4, lg=4, xl=4),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='dropDown_dcp_month',
                                                        options=list(set(历史dcp['资源月份'])),
                                                        value=max(list(set(历史dcp['资源月份']))),
                                                        clearable=False,
                                                        style={"width": "100%"},
                                                        placeholder='费用月'
                                                    ),
                                                ], xs=6, sm=6, md=3, lg=3, xl=3),
                                            ]),

                                            dcc.RadioItems(
                                                id='radio_dcp使用量费用',
                                                options=[
                                                    {'label': '已使用量(TB)', 'value': '已使用量(TB)'},
                                                    {'label': '费用(元)', 'value': '费用(元)'},
                                                ],
                                                value='费用(元)',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_dcp使用量费用全选项',
                                                options=[
                                                    {'label': '资源池', 'value': '资源池'},
                                                    {'label': '集群名称', 'value': '集群名称'},
                                                    {'label': '存储类型(SSD/HDD)', 'value': '存储类型(SSD/HDD)'},
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '用户名', 'value': '用户名'},
                                                ],
                                                value='资源池',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_dcp使用量费用',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.P('费用月'),
                                                ], xs=6, sm=6, md=4, lg=4, xl=4),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='dropDown_dcp_month2',
                                                        options=list(set(历史dcp['资源月份'])),
                                                        value=max(list(set(历史dcp['资源月份']))),
                                                        clearable=False,
                                                        style={"width": "100%"},
                                                        placeholder='费用月'
                                                    ),
                                                ], xs=6, sm=6, md=3, lg=3, xl=3),
                                            ]),

                                            dcc.RadioItems(
                                                id='radio_dcp使用量费用2',
                                                options=[
                                                    {'label': '已使用量(TB)', 'value': '已使用量(TB)'},
                                                    {'label': '费用(元)', 'value': '费用(元)'},
                                                ],
                                                value='费用(元)',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_dcp使用量费用全选项2',
                                                options=[
                                                    {'label': '员工部门', 'value': '员工部门'},
                                                    {'label': '集群名称', 'value': '集群名称'},
                                                    {'label': '存储类型(SSD/HDD)', 'value': '存储类型(SSD/HDD)'},
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '用户名', 'value': '用户名'},
                                                ],
                                                value='员工部门',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_dcp使用量费用2',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    irdc_graph('graph_Top10dcp-bar', figDcpTop10(本月dcp))
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    html.P('本月Dcp费用(元)Top10'),
                                    html.Div([
                                        dfExistDf(dcpTop10(本月dcp).iloc[:, 0:-7], 'table_Top10dcp')
                                    ]),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            dfExistDfStr(新增Tb(本月dcp, 上月dcp, 'dcpID', '用户已使用(TB)'),
                                         '环比新增DCP资源(本月DCP明细, 按照费用倒序排序)：'),
                            dfExistDf(新增Tb(本月dcp, 上月dcp, "dcpID",
                                             "用户已使用(TB)"), 'DCP新增table'),
                            html.Br(),
                            dfExistDfStr(减少Tb(本月dcp, 上月dcp, 'dcpID', '用户已使用(TB)'),
                                         '环比减少DCP资源(上月DCP明细, 按照费用倒序排序)：'),
                            dfExistDf(减少Tb(本月dcp, 上月dcp, "dcpID",
                                             "用户已使用(TB)"), 'DCP减少table'),

                            html.Br(),

                        ],
                            title='点击查看DCP存储详细',
                        )
                    ],
                    flush=True, start_collapsed=True, id="accordtion-dcp"
                ),
            ]),

            # html.Br(),
            # html.P("数据采标 ( Update at " + 数据采标更新时间() + ' )'),
            # dbc.Row([
            #     dbc.Col([
            #         irdc_summary_large_ppls("dataBZ_indicator", dataBZ_indicator)
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_summary_smWider_ppls("dataBZ_done_indicator", dataBZ_done_indicator),
            #             irdc_summary_smWider_ppls("dataBZ_ing_indicator", dataBZ_ing_indicator),
            #             irdc_summary_smWider_ppls("dataBZ_back_indicator", dataBZ_back_indicator),
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_summary_smWider_ppls("dataBZ_sx_indicator", dataBZ_sx_indicator),
            #             irdc_summary_smWider_ppls("dataBZ_dx_indicator", dataBZ_dx_indicator),
            #             irdc_summary_smWider_ppls("dataBZ_ir_indicator", dataBZ_ir_indicator),
            #         ]),
            #     ]),
            #     dbc.Col([
            #         irdc_summary_large_ppls("dataBZ_bill_indicator", dataBZ_bill_indicator)
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_summary_smWider_ppls("dataBZ_bill_confirm", dataBZ_bill_confirm),
            #             irdc_summary_smWider_ppls("dataBZ_bill_onhold", dataBZ_bill_onhold),
            #         ]),
            #     ]),
            #     dbc.Col([
            #         irdc_summary_large_ppls("dataCJ_indicator", dataCJ_indicator)
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_summary_smWider_ppls("dataCJ_done_indicator", dataCJ_done_indicator),
            #             irdc_summary_smWider_ppls("dataCJ_ing_indicator", dataCJ_ing_indicator),
            #             irdc_summary_smWider_ppls("dataCJ_back_indicator", dataCJ_back_indicator),
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_summary_smWider_ppls("dataCJ_sx_indicator", dataCJ_sx_indicator),
            #             irdc_summary_smWider_ppls("dataCJ_dx_indicator", dataCJ_dx_indicator),
            #             irdc_summary_smWider_ppls("dataCJ_ir_indicator", dataCJ_ir_indicator),
            #         ]),
            #     ]),
            #     dbc.Col([
            #         irdc_summary_large_ppls("dataCJ_bill_indicator", dataCJ_bill_indicator)
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_summary_smWider_ppls("dataCJ_bill_confirm", dataCJ_bill_confirm),
            #             irdc_summary_smWider_ppls("dataCJ_bill_onhold", dataCJ_bill_onhold),
            #         ]),
            #     ]),
            # ]),
            # html.Br(),
            # html.Div(
            #     dbc.Accordion(
            #         [
            #             dbc.AccordionItem([
            #                 dbc.Row([
            #                     irdc_graph('fig历史业务线标注费-id',
            #                                fig历史业务线采标费用(历史标注费用(), '业务线历史标注费用'))
            #                 ]),
            #                 html.Br(),
            #                 dbc.Row([
            #                     dbc.Col([
            #                         irdc_graph('figBZBillTop5-bar', figBZBillTop5())
            #                     ], xs=12, sm=12, md=6, lg=6, xl=6),
            #                     dbc.Col([
            #                         irdc_graph('figBZBillTop5-pie', figBZBilltop5分布())
            #                     ], xs=12, sm=12, md=6, lg=6, xl=6),
            #                 ]),
            #                 # dbc.Col([
            #                 #     dash_table_not_collapse("bzBill_top5_id",
            #                 #                             bzBill_top5()),
            #                 # ]),
            #                 html.Br(),
            #                 dbc.Row([
            #                     dfExist(monthly_bz_cur, "上月无标注任务", "collapse-button9", 'collapse9'),
            #                     html.Br(),
            #                 ]),
            #
            #                 dbc.Row([
            #                     dbc.Col([
            #                         dbc.Row([
            #                             html.P('验收数据包打回任务数：' + str(
            #                                 len(data_back_biaozhu())),
            #                                    style={"fontSize": 25}),
            #                         ]),
            #                         dbc.Row([
            #                             irdc_graph('数据包打回任务-pie', fig标注数据包打回())
            #                         ]),
            #
            #                     ], xs=12, sm=12, md=6, lg=6, xl=6),
            #                     dbc.Col([
            #                         dbc.Row([
            #                             html.P('标注延期超过5天任务数：' + str(
            #                                 len(data_delay_biaozhu())),
            #                                    style={"fontSize": 25}),
            #                         ]),
            #                         dbc.Row([
            #                             irdc_graph('标注任务延期超过5天-pie', fig标注任务延期())
            #                         ])
            #                     ], xs=12, sm=12, md=6, lg=6, xl=6),
            #                 ]),
            #
            #                 dbc.Row([
            #                     dbc.Col([
            #                         collapse_btn_table("collapse-button11", "验收数据包打回任务_id",
            #                                            data_back_biaozhu(),
            #                                            'collapse11'),
            #                     ], xs=12, sm=12, md=6, lg=6, xl=6),
            #                     dbc.Col([
            #                         collapse_btn_table("collapse-button12", "标注任务延期超过5天_id",
            #                                            data_delay_biaozhu(),
            #                                            'collapse12'),
            #                     ], xs=12, sm=12, md=6, lg=6, xl=6),
            #                 ]),
            #
            #                 dbc.Row([
            #                     irdc_graph('fig历史业务线采集费-id',
            #                                fig历史业务线采标费用(历史采集费用(), '业务线历史采集费用'))
            #                 ]),
            #                 dbc.Row([
            #                     dfExist(monthly_cj_cur, "上月无采集任务", "collapse-button10", 'collapse10'),
            #                     html.Br(),
            #                 ]),
            #             ],
            #                 title='点击查看数据采标任务详细'
            #             )
            #         ],
            #         flush=True, start_collapsed=True, id="accordtion-data"
            #     ),
            # ),

            html.Br(),
            html.P("固定资产 ( Update at " + 固定资产更新时间() + ' )'),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        irdc_wh_largeL("sx_total_indicator", total_折旧)
                    ]),
                    dbc.Row([
                        irdc_wh_middleL("sx_wbsD_indicator", total_办公折旧),
                        irdc_wh_middleL("sx_wbsDper_indicator", total_办公折旧c)
                    ]),
                    dbc.Row([
                        irdc_wh_middleL("sx_wbsX_indicator", total_项目折旧),
                        irdc_wh_middleL("sx_wbsXper_indicator", total_项目折旧c)
                    ]),

                ]),
                dbc.Col([
                    dbc.Row([
                        irdc_wh_largeL("ir_total_indicator", total_净值)
                    ]),
                    dbc.Row([
                        irdc_wh_middleL("ir_算法资源池_indicator", total_办公净值),
                        irdc_wh_middleL("ir_算法资源池per_indicator", total_办公净值c)
                    ]),
                    dbc.Row([
                        irdc_wh_middleL("ir_开发资源池_indicator", total_项目净值),
                        irdc_wh_middleL("ir_开发资源池per_indicator", total_项目净值c)
                    ]),

                ]),
                dbc.Col([
                    dbc.Row([
                        irdc_wh_largeL("dxSku_total_indicator", total_总值)
                    ]),
                    dbc.Row([
                        irdc_wh_middleL("dxSku_算法资源池_indicator", total_办公总值),
                        irdc_wh_middleL("dxSku_算法资源池per_indicator", total_办公总值c)
                    ]),
                    dbc.Row([
                        irdc_wh_middleL("dxSku_开发资源池_indicator", total_项目总值),
                        irdc_wh_middleL("dxSku_开发资源池per_indicator", total_项目总值c)
                    ]),

                ]),
            ]),
            # dbc.Row([
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("sx_total_indicator", sx_wh_total)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_笔记本电脑_indicator", sx_笔记本电脑),
            #             irdc_wh_middle("sx_笔记本电脑c_indicator", sx_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_台式电脑_indicator", sx_台式电脑),
            #             irdc_wh_middle("sx_台式电脑c_indicator", sx_台式电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_服务器_indicator", sx_服务器),
            #             irdc_wh_middle("sx_服务器c_indicator", sx_服务器c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_显示屏_indicator", sx_显示屏),
            #             irdc_wh_middle("sx_显示屏c_indicator", sx_显示屏c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_网络设备_indicator", sx_网络设备),
            #             irdc_wh_middle("sx_网络设备c_indicator", sx_网络设备c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_开发套件_indicator", sx_开发套件),
            #             irdc_wh_middle("sx_开发套件c_indicator", sx_开发套件c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("sx_其他_indicator", sx_其他),
            #             irdc_wh_middle("sx_其他c_indicator", sx_其他c)
            #         ]),
            #
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("ir_total_indicator", ir_wh_total)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_笔记本电脑_indicator", ir_笔记本电脑),
            #             irdc_wh_middle("ir_笔记本电脑c_indicator", ir_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_台式电脑_indicator", ir_台式电脑),
            #             irdc_wh_middle("ir_台式电脑c_indicator", ir_台式电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_服务器_indicator", ir_服务器),
            #             irdc_wh_middle("ir_服务器c_indicator", ir_服务器c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_显示屏_indicator", ir_显示屏),
            #             irdc_wh_middle("ir_显示屏c_indicator", ir_显示屏c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_网络设备_indicator", ir_网络设备),
            #             irdc_wh_middle("ir_网络设备c_indicator", ir_网络设备c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_开发套件_indicator", ir_开发套件),
            #             irdc_wh_middle("ir_开发套件c_indicator", ir_开发套件c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("ir_其他_indicator", ir_其他),
            #             irdc_wh_middle("ir_其他c_indicator", ir_其他c)
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("dxSku_total_indicator", dxSku_wh_total)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_笔记本电脑_indicator", dxSku_笔记本电脑),
            #             irdc_wh_middle("dxSku_笔记本电脑c_indicator", dxSku_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_台式电脑_indicator", dxSku_台式电脑),
            #             irdc_wh_middle("dxSku_台式电脑c_indicator", dxSku_台式电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_服务器_indicator", dxSku_服务器),
            #             irdc_wh_middle("dxSku_服务器c_indicator", dxSku_服务器c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_显示屏_indicator", dxSku_显示屏),
            #             irdc_wh_middle("dxSku_显示屏c_indicator", dxSku_显示屏c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_网络设备_indicator", dxSku_网络设备),
            #             irdc_wh_middle("dxSku_网络设备c_indicator", dxSku_网络设备c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_开发套件_indicator", dxSku_开发套件),
            #             irdc_wh_middle("dxSku_开发套件c_indicator", dxSku_开发套件c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxSku_其他_indicator", dxSku_其他),
            #             irdc_wh_middle("dxSku_其他c_indicator", dxSku_其他c)
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("dxTy_total_indicator", dxTy_wh_total)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_笔记本电脑_indicator", dxTy_笔记本电脑),
            #             irdc_wh_middle("dxTy_笔记本电脑c_indicator", dxTy_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_台式电脑_indicator", dxTy_台式电脑),
            #             irdc_wh_middle("dxTy_台式电脑c_indicator", dxTy_台式电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_服务器_indicator", dxTy_服务器),
            #             irdc_wh_middle("dxTy_服务器c_indicator", dxTy_服务器c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_显示屏_indicator", dxTy_显示屏),
            #             irdc_wh_middle("dxTy_显示屏c_indicator", dxTy_显示屏c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_网络设备_indicator", dxTy_网络设备),
            #             irdc_wh_middle("dxTy_网络设备c_indicator", dxTy_网络设备c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_开发套件_indicator", dxTy_开发套件),
            #             irdc_wh_middle("dxTy_开发套件c_indicator", dxTy_开发套件c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("dxTy_其他_indicator", dxTy_其他),
            #             irdc_wh_middle("dxTy_其他c_indicator", dxTy_其他c)
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("mkt_total_indicator", mkt_wh_total)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_笔记本电脑_indicator", mkt_笔记本电脑),
            #             irdc_wh_middle("mkt_笔记本电脑c_indicator", mkt_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_台式电脑_indicator", mkt_台式电脑),
            #             irdc_wh_middle("mkt_台式电脑c_indicator", mkt_台式电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_服务器_indicator", mkt_服务器),
            #             irdc_wh_middle("mkt_服务器c_indicator", mkt_服务器c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_显示屏_indicator", mkt_显示屏),
            #             irdc_wh_middle("mkt_显示屏c_indicator", mkt_显示屏c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_网络设备_indicator", mkt_网络设备),
            #             irdc_wh_middle("mkt_网络设备c_indicator", mkt_网络设备c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_开发套件_indicator", mkt_开发套件),
            #             irdc_wh_middle("mkt_开发套件c_indicator", mkt_开发套件c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("mkt_其他_indicator", mkt_其他),
            #             irdc_wh_middle("mkt_其他c_indicator", mkt_其他c)
            #         ]),
            #     ]),
            #     dbc.Col([
            #         dbc.Row([
            #             irdc_wh_large("oac_total_indicator", oac_wh_total)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_笔记本电脑_indicator", oac_笔记本电脑),
            #             irdc_wh_middle("oac_笔记本电脑c_indicator", oac_笔记本电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_台式电脑_indicator", oac_台式电脑),
            #             irdc_wh_middle("oac_台式电脑c_indicator", oac_台式电脑c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_服务器_indicator", oac_服务器),
            #             irdc_wh_middle("oac_服务器c_indicator", oac_服务器c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_显示屏_indicator", oac_显示屏),
            #             irdc_wh_middle("oac_显示屏c_indicator", oac_显示屏c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_网络设备_indicator", oac_网络设备),
            #             irdc_wh_middle("oac_网络设备c_indicator", oac_网络设备c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_开发套件_indicator", oac_开发套件),
            #             irdc_wh_middle("oac_开发套件c_indicator", oac_开发套件c)
            #         ]),
            #         dbc.Row([
            #             irdc_wh_middle("oac_其他_indicator", oac_其他),
            #             irdc_wh_middle("oac_其他c_indicator", oac_其他c)
            #         ]),
            #     ]),
            # ]),
            html.Br(),
            html.Div(
                dbc.Accordion(
                    [
                        dbc.AccordionItem([
                            # html.Div([
                            #     dcc.RadioItems(
                            #         id='radio_历史固定资产',
                            #         options=[
                            #             {'label': '办公', 'value': 'graph_历史固定资产办公'},
                            #             {'label': '项目', 'value': 'graph_历史固定资产项目'},
                            #         ],
                            #         value='graph_历史固定资产办公',
                            #         style={"width": "60%"},
                            #         inline=True),
                            #
                            # ]),
                            # html.Div([
                            #     dcc.RadioItems(
                            #         id='radio_历史固定资产人均',
                            #         options=[
                            #             {'label': 'Total', 'value': 'graph_历史固定资产Total'},
                            #             {'label': 'Avg', 'value': 'graph_历史固定资产Avg'},
                            #         ],
                            #         value='graph_历史固定资产Total',
                            #         style={"width": "60%"},
                            #         inline=True),
                            # ]),
                            # html.Div(
                            #     dcc.Graph(id='graph_历史固定资产',
                            #               style={'height': 500,
                            #                      "border-radius": "5px",
                            #                      "background-color": "#f9f9f9",
                            #                      "box-shadow": "2px 2px 2px lightgrey",
                            #                      "position": "relative",
                            #                      "margin-bottom": "15px"
                            #                      },
                            #               config={'displayModeBar': False},
                            #               ),
                            # ),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dcc.RadioItems(
                                            id='radio_固定资产汇总员工部门',
                                            options=[
                                                {'label': '办公', 'value': '办公'},
                                                {'label': '项目', 'value': '项目'},
                                            ],
                                            value='办公',
                                            style={"width": "60%"},
                                            inline=True),
                                    ]),
                                    html.Div([
                                        dcc.Graph(id='固定资产汇总员工部门-bar',
                                                  style={'height': 500,
                                                         "border-radius": "5px",
                                                         "background-color": "#f9f9f9",
                                                         "box-shadow": "2px 2px 2px lightgrey",
                                                         "position": "relative",
                                                         "margin-bottom": "15px"
                                                         },
                                                  config={'displayModeBar': False},
                                                  )]),
                                    # irdc_graph('固定资产汇总员工部门-bar', fig员工所属门固定资产总值(本月固定资产, '折旧', '折旧','净值','总值','部门折旧部门平均' , '总')),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    html.Div([
                                        dcc.RadioItems(
                                            id='radio_固定资产汇总员工部门人均',
                                            options=[
                                                {'label': '办公', 'value': '办公'},
                                                {'label': '项目', 'value': '项目'},
                                            ],
                                            value='办公',
                                            style={"width": "60%"},
                                            inline=True),
                                    ]),
                                    html.Div([
                                        dcc.Graph(id='固定资产汇总员工部门人均-bar',
                                                  style={'height': 500,
                                                         "border-radius": "5px",
                                                         "background-color": "#f9f9f9",
                                                         "box-shadow": "2px 2px 2px lightgrey",
                                                         "position": "relative",
                                                         "margin-bottom": "15px"
                                                         },
                                                  config={'displayModeBar': False},
                                                  )]),
                                    # irdc_graph('固定资产汇总员工部门人均-bar', fig员工所属门固定资产总值(本月固定资产, '折旧人均', '折旧人均','净值人均','总值人均','部门折旧人均' ,'人均')),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            # html.Br(),
                            # dbc.Row([
                            #     dbc.Col([
                            #         html.Div([
                            #             dcc.RadioItems(
                            #                 id='radio_固定资产汇总资源池',
                            #                 options=[
                            #                     {'label': '办公', 'value': '办公'},
                            #                     {'label': '项目', 'value': '项目'},
                            #                 ],
                            #                 value='办公',
                            #                 style={"width": "60%"},
                            #                 inline=True),
                            #         ]),
                            #         html.Div([
                            #             dcc.Graph(id='固定资产汇总资源池-bar',
                            #                       style={'height': 500,
                            #                              "border-radius": "5px",
                            #                              "background-color": "#f9f9f9",
                            #                              "box-shadow": "2px 2px 2px lightgrey",
                            #                              "position": "relative",
                            #                              "margin-bottom": "15px"
                            #                              },
                            #                       config={'displayModeBar': False},
                            #                       )]),
                            #         # irdc_graph('固定资产汇总员工部门-bar', fig员工所属门固定资产总值(本月固定资产, '折旧', '折旧','净值','总值','部门折旧部门平均' , '总')),
                            #     ], xs=12, sm=12, md=6, lg=6, xl=6),
                            #     dbc.Col([
                            #         html.Div([
                            #             dcc.RadioItems(
                            #                 id='radio_固定资产汇总资源池人均',
                            #                 options=[
                            #                     {'label': '办公', 'value': '办公'},
                            #                     {'label': '项目', 'value': '项目'},
                            #                 ],
                            #                 value='办公',
                            #                 style={"width": "60%"},
                            #                 inline=True),
                            #         ]),
                            #         html.Div([
                            #             dcc.Graph(id='固定资产汇总资源池人均-bar',
                            #                       style={'height': 500,
                            #                              "border-radius": "5px",
                            #                              "background-color": "#f9f9f9",
                            #                              "box-shadow": "2px 2px 2px lightgrey",
                            #                              "position": "relative",
                            #                              "margin-bottom": "15px"
                            #                              },
                            #                       config={'displayModeBar': False},
                            #                       )]),
                            #         # irdc_graph('固定资产汇总员工部门人均-bar', fig员工所属门固定资产总值(本月固定资产, '折旧人均', '折旧人均','净值人均','总值人均','部门折旧人均' ,'人均')),
                            #     ], xs=12, sm=12, md=6, lg=6, xl=6),
                            # ]),
                            html.Br(),
                            html.Div([
                                dcc.RadioItems(
                                    id='radio_固定资产汇总',
                                    options=[
                                        {'label': '资源池', 'value': '资源池'},
                                    ],
                                    value='资源池',
                                    style={"width": "60%"},
                                    inline=True),
                            ]),
                            html.Div([
                                dcc.Graph(id='固定资产汇总-pie',
                                          style={'height': 500,
                                                 "border-radius": "5px",
                                                 "background-color": "#f9f9f9",
                                                 "box-shadow": "2px 2px 2px lightgrey",
                                                 "position": "relative",
                                                 "margin-bottom": "15px"
                                                 },
                                          config={'displayModeBar': False},
                                          )]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.P('总费用月'),
                                                ], xs=6, sm=6, md=4, lg=4, xl=4),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='dropDown_固定资产_fee2',
                                                        options=list(set(历史固定资产['资产月份'])),
                                                        value=max(list(set(历史固定资产['资产月份']))),
                                                        clearable=False,
                                                        style={"width": "100%"},
                                                        placeholder='资产月份'
                                                    ),
                                                ], xs=6, sm=6, md=3, lg=3, xl=3),
                                            ]),
                                            dcc.RadioItems(
                                                id='radio_固定资产金额类型2',
                                                options=[
                                                    {'label': '折旧', 'value': '折旧'},
                                                    {'label': '净值', 'value': '净值'},
                                                    {'label': '总值', 'value': '总值'},
                                                ],
                                                value='折旧',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_折旧固定资产type2',
                                                options=[
                                                    {'label': '办公', 'value': '办公'},
                                                    {'label': '项目', 'value': '项目'},
                                                ],
                                                value='办公',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_折旧固定资产全选项2',
                                                options=[
                                                    {'label': '设备类型', 'value': '设备类型'},
                                                    {'label': '资产状态', 'value': '资产状态'},
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '员工所属部门', 'value': '员工所属部门'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '员工姓名', 'value': '员工姓名'},
                                                ],
                                                value='设备类型',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_折旧固定资产员工部门2',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),

                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            html.Br(),
                                            dcc.RadioItems(
                                                id='radio_固定资产数量2',
                                                options=[
                                                    {'label': '折旧中', 'value': '折旧中'},
                                                    {'label': '折旧中&折旧完', 'value': '折旧中&折旧完'},
                                                    {'label': '折旧完', 'value': '折旧完'},
                                                ],
                                                value='折旧中',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_折旧固定资产type数量2',
                                                options=[
                                                    {'label': '办公', 'value': '办公'},
                                                    {'label': '项目', 'value': '项目'},
                                                ],
                                                value='办公',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_折旧固定资产全选项数量2',
                                                options=[
                                                    {'label': '设备类型', 'value': '设备类型'},
                                                    {'label': '资产状态', 'value': '资产状态'},
                                                    {'label': '员工组', 'value': '员工组'},
                                                    {'label': '员工所属部门', 'value': '员工所属部门'},
                                                    {'label': '岗位名称', 'value': '岗位名称'},
                                                    {'label': '员工姓名', 'value': '员工姓名'},
                                                ],
                                                value='设备类型',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_折旧固定资产员工部门数量2',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            # html.Br(),
                            # dbc.Row([
                            #     dbc.Col([
                            #         dbc.Row([
                            #             html.Div([
                            #                 dcc.RadioItems(
                            #                     id='radio_固定资产数量',
                            #                     options=[
                            #                         {'label': '折旧中', 'value': '折旧中'},
                            #                         {'label': '折旧中&折旧完', 'value': '折旧中&折旧完'},
                            #                         {'label': '折旧完', 'value': '折旧完'},
                            #                     ],
                            #                     value='折旧中',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #
                            #                 dcc.RadioItems(
                            #                     id='radio_折旧固定资产type数量',
                            #                     options=[
                            #                         {'label': '办公', 'value': '办公'},
                            #                         {'label': '项目', 'value': '项目'},
                            #                     ],
                            #                     value='办公',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #
                            #                 dcc.RadioItems(
                            #                     id='radio_折旧固定资产全选项数量',
                            #                     options=[
                            #                         {'label': '设备类型', 'value': '设备类型'},
                            #                         {'label': '资产状态', 'value': '资产状态'},
                            #                         {'label': '员工组', 'value': '员工组'},
                            #                         {'label': '资源池', 'value': '资源池'},
                            #                         {'label': '岗位名称', 'value': '岗位名称'},
                            #                         {'label': '员工姓名', 'value': '员工姓名'},
                            #                     ],
                            #                     value='设备类型',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #             ]),
                            #             html.Div([
                            #                 dcc.Graph(id='graph_折旧固定资产员工部门数量',
                            #                           style={'height': 500,
                            #                                  "border-radius": "5px",
                            #                                  "background-color": "#f9f9f9",
                            #                                  "box-shadow": "2px 2px 2px lightgrey",
                            #                                  "position": "relative",
                            #                                  "margin-bottom": "15px"
                            #                                  },
                            #                           config={'displayModeBar': False},
                            #                           )]),
                            #         ]),
                            #
                            #     ], xs=12, sm=12, md=6, lg=6, xl=6),
                            #     dbc.Col([
                            #         dbc.Row([
                            #             html.Div([
                            #                 dcc.RadioItems(
                            #                     id='radio_固定资产数量2',
                            #                     options=[
                            #                         {'label': '折旧中', 'value': '折旧中'},
                            #                         {'label': '折旧中&折旧完', 'value': '折旧中&折旧完'},
                            #                         {'label': '折旧完', 'value': '折旧完'},
                            #                     ],
                            #                     value='折旧中',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #
                            #                 dcc.RadioItems(
                            #                     id='radio_折旧固定资产type数量2',
                            #                     options=[
                            #                         {'label': '办公', 'value': '办公'},
                            #                         {'label': '项目', 'value': '项目'},
                            #                     ],
                            #                     value='办公',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #
                            #                 dcc.RadioItems(
                            #                     id='radio_折旧固定资产全选项数量2',
                            #                     options=[
                            #                         {'label': '设备类型', 'value': '设备类型'},
                            #                         {'label': '资产状态', 'value': '资产状态'},
                            #                         {'label': '员工组', 'value': '员工组'},
                            #                         {'label': '员工所属部门', 'value': '员工所属部门'},
                            #                         {'label': '岗位名称', 'value': '岗位名称'},
                            #                         {'label': '员工姓名', 'value': '员工姓名'},
                            #                     ],
                            #                     value='设备类型',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #             ]),
                            #             html.Div([
                            #                 dcc.Graph(id='graph_折旧固定资产员工部门数量2',
                            #                           style={'height': 500,
                            #                                  "border-radius": "5px",
                            #                                  "background-color": "#f9f9f9",
                            #                                  "box-shadow": "2px 2px 2px lightgrey",
                            #                                  "position": "relative",
                            #                                  "margin-bottom": "15px"
                            #                                  },
                            #                           config={'displayModeBar': False},
                            #                           )]),
                            #         ]),
                            #
                            #     ], xs=12, sm=12, md=6, lg=6, xl=6),
                            # ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dcc.RadioItems(
                                        id='radio_resTop10折旧',
                                        options=[
                                            {'label': '办公', 'value': 'graph_resTop10折旧办公'},
                                            {'label': '项目', 'value': 'graph_resTop10折旧项目'},
                                        ],
                                        value='graph_resTop10折旧办公',
                                        style={"width": "80%"},
                                        inline=True),
                                    dcc.Graph(id='graph_resTop10折旧',
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "15px"
                                                     },
                                              config={'displayModeBar': False},
                                              ),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    html.P('本月资产折旧Top10'),
                                    html.Div([

                                        dash_table.DataTable(
                                            id='table_resTop10折旧', page_size=10, ),
                                    ]),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dcc.RadioItems(
                                        id='radio_resTop10净值',
                                        options=[
                                            {'label': '办公', 'value': 'graph_resTop10净值办公'},
                                            {'label': '项目', 'value': 'graph_resTop10净值项目'},
                                        ],
                                        value='graph_resTop10净值办公',
                                        style={"width": "80%"},
                                        inline=True),
                                    dcc.Graph(id='graph_resTop10净值',
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "15px"
                                                     },
                                              config={'displayModeBar': False},
                                              ),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    html.P('本月资产净值Top10'),
                                    html.Div([
                                        dash_table.DataTable(
                                            id='table_resTop10净值', page_size=10, ),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dcc.RadioItems(
                                        id='radio_resTop10总值',
                                        options=[
                                            {'label': '办公', 'value': 'graph_resTop10总值办公'},
                                            {'label': '项目', 'value': 'graph_resTop10总值项目'},
                                        ],
                                        value='graph_resTop10总值办公',
                                        style={"width": "80%"},
                                        inline=True),
                                    dcc.Graph(id='graph_resTop10总值',
                                              style={'height': 500,
                                                     "border-radius": "5px",
                                                     "background-color": "#f9f9f9",
                                                     "box-shadow": "2px 2px 2px lightgrey",
                                                     "position": "relative",
                                                     "margin-bottom": "15px"
                                                     },
                                              config={'displayModeBar': False},
                                              ),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    html.P('本月资产总值Top10'),
                                    html.Div([
                                        dash_table.DataTable(
                                            id='table_resTop10总值', page_size=10, ),
                                    ]),

                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            dfExistDfStr(本月固定资产[本月固定资产['折旧'] >= 1000].sort_values(
                                                                by=['折旧'], ascending=False).reset_index(
                                                                drop=True),"折旧超过1K的资产: "),
                            dfExistDf(本月固定资产[本月固定资产['折旧'] >= 1000].sort_values(
                                                                by=['折旧'], ascending=False).reset_index(
                                                                drop=True)[
                                                                ['实际保管人', '员工所属部门', '员工组', '资源池',
                                                                 '岗位名称', '用途', '设备类型', '资产状态', '资产代码',
                                                                 '保管人姓名', '折旧', '净值', '总值']], "折旧超过1K的资产table"),
                            html.Br(),
                            dfExistDfStr(本月固定资产[本月固定资产['资产状态'] == '报废'].sort_values(
                                                                by=['折旧'], ascending=False).reset_index(
                                                                drop=True), "本月报废的资产: "),
                            dfExistDf(本月固定资产[本月固定资产['资产状态'] == '报废'].sort_values(
                                                                by=['折旧'], ascending=False).reset_index(
                                                                drop=True)[
                                                                ['实际保管人', '员工所属部门', '员工组', '资源池',
                                                                 '岗位名称', '用途', '设备类型', '资产状态', '资产代码',
                                                                 '保管人姓名', '折旧', '净值', '总值']], "本月报废的资产table"),
                            html.Br(),
                            dfExistDfStr(新增固定资产(本月固定资产, 上月固定资产),
                                         '环比新增固定资产个数(本月固定资产明细, 按照折旧倒序排序)：'),
                            dfExistDf(新增固定资产_tb(本月固定资产, 上月固定资产, "资产代码",
                                                      "折旧")[
                                          ['实际保管人', '员工所属部门', '员工组', '资源池', '岗位名称', '用途',
                                           '设备类型', '资产状态', '资产代码', '保管人姓名',
                                           '折旧', '净值', '总值']], '固定资产新增table'),
                            html.Br(),
                            dfExistDfStr(减少固定资产(本月固定资产, 上月固定资产),
                                         '环比减少固定资产个数(上月固定资产明细, 按照折旧倒序排序)：'),
                            dfExistDf(减少固定资产_tb(本月固定资产, 上月固定资产, "资产代码",
                                                      "折旧")[
                                          ['实际保管人', '员工所属部门', '员工组', '资源池', '岗位名称', '用途',
                                           '设备类型', '资产状态', '资产代码', '保管人姓名',
                                           '折旧', '净值', '总值']], '固定资产减少table'),

                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dcc.RadioItems(
                                                id='radio_总库存金额',
                                                options=[
                                                    {'label': '借库', 'value': '借库'},
                                                    {'label': '在库', 'value': '在库'},
                                                ],
                                                value='借库',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_总库存金额全选项',
                                                options=[
                                                    {'label': '业务线', 'value': '业务线'},
                                                    {'label': '类别', 'value': '类别'},
                                                    {'label': '物料名称', 'value': '物料名称'},
                                                    {'label': '库存天数区间', 'value': '库存天数区间'},
                                                    {'label': '年末预估逾期业绩核算金额（万）',
                                                     'value': '年末预估逾期业绩核算金额（万）'},
                                                ],
                                                value='类别',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_总库存金额',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                                dbc.Col([
                                    dbc.Row([
                                        html.Div([
                                            dcc.RadioItems(
                                                id='radio_总库存个数',
                                                options=[
                                                    {'label': '借库', 'value': '借库'},
                                                    {'label': '在库', 'value': '在库'},
                                                ],
                                                value='借库',
                                                style={"width": "100%"},
                                                inline=True),

                                            dcc.RadioItems(
                                                id='radio_总库存个数全选项',
                                                options=[
                                                    {'label': '业务线', 'value': '业务线'},
                                                    {'label': '类别', 'value': '类别'},
                                                    {'label': '物料名称', 'value': '物料名称'},
                                                    {'label': '库存天数区间', 'value': '库存天数区间'},
                                                ],
                                                value='类别',
                                                style={"width": "100%"},
                                                inline=True),
                                        ]),
                                        html.Div([
                                            dcc.Graph(id='graph_总库存个数',
                                                      style={'height': 500,
                                                             "border-radius": "5px",
                                                             "background-color": "#f9f9f9",
                                                             "box-shadow": "2px 2px 2px lightgrey",
                                                             "position": "relative",
                                                             "margin-bottom": "15px"
                                                             },
                                                      config={'displayModeBar': False},
                                                      )]),
                                    ]),
                                ], xs=12, sm=12, md=6, lg=6, xl=6),
                            ]),
                            html.Br(),
                            # dbc.Row([
                            #     dbc.Col([
                            #         dbc.Row([
                            #             html.Div([
                            #                 dcc.RadioItems(
                            #                     id='radio_借库金额',
                            #                     options=[
                            #                         {'label': '借库人BG', 'value': '借库人BG'},
                            #                         {'label': '物料描述', 'value': '物料描述'},
                            #                         {'label': '逾期状态', 'value': '逾期状态'},
                            #                         {'label': '业务类型', 'value': '业务类型'},
                            #                         {'label': '物料名称', 'value': '物料名称'},
                            #                         {'label': '借库人二级部门', 'value': '借库人二级部门'},
                            #                     ],
                            #                     value='借库人BG',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #             ]),
                            #             html.Div([
                            #                 dcc.Graph(id='graph_借库金额',
                            #                           style={'height': 500,
                            #                                  "border-radius": "5px",
                            #                                  "background-color": "#f9f9f9",
                            #                                  "box-shadow": "2px 2px 2px lightgrey",
                            #                                  "position": "relative",
                            #                                  "margin-bottom": "15px"
                            #                                  },
                            #                           config={'displayModeBar': False},
                            #                           )]),
                            #         ]),
                            #     ], xs=12, sm=12, md=6, lg=6, xl=6),
                            #     dbc.Col([
                            #         dbc.Row([
                            #             html.Div([
                            #                 dcc.RadioItems(
                            #                     id='radio_借库个数',
                            #                     options=[
                            #                         {'label': '借库人BG', 'value': '借库人BG'},
                            #                         {'label': '物料描述', 'value': '物料描述'},
                            #                         {'label': '逾期状态', 'value': '逾期状态'},
                            #                         {'label': '业务类型', 'value': '业务类型'},
                            #                         {'label': '物料名称', 'value': '物料名称'},
                            #                         {'label': '借库人二级部门', 'value': '借库人二级部门'},
                            #                     ],
                            #                     value='借库人BG',
                            #                     style={"width": "100%"},
                            #                     inline=True),
                            #
                            #             ]),
                            #             html.Div([
                            #                 dcc.Graph(id='graph_借库个数',
                            #                           style={'height': 500,
                            #                                  "border-radius": "5px",
                            #                                  "background-color": "#f9f9f9",
                            #                                  "box-shadow": "2px 2px 2px lightgrey",
                            #                                  "position": "relative",
                            #                                  "margin-bottom": "15px"
                            #                                  },
                            #                           config={'displayModeBar': False},
                            #                           )]),
                            #         ]),
                            #     ], xs=12, sm=12, md=6, lg=6, xl=6),
                            # ]),
                            html.Br(),
                            html.P("本月总库存"),
                            dash_table_not_collapse_showAll("本月总库存table",
                                                            历史总库存[(历史总库存['资产年份'] == 资产本年()) & (
                                                                    历史总库存['资产月份'] == 资产本月())].drop(
                                                                ['总存货(万元)', '存货金额（元）'], axis=1).iloc[:,
                                                            0:-2]),

                            html.Br(),
                            html.P("本月借库"),
                            dash_table_not_collapse_showAll("本月借库table", 历史借库[
                                                                                 (历史借库[
                                                                                      '资产年份'] == 资产本年()) & (
                                                                                             历史借库[
                                                                                                 '资产月份'] == 资产本月())].drop(
                                [
                                    'OA流程编号', '行号', '子行号', '借库人工号', '客户号', 'Pipeline'], axis=1).iloc[:,
                                                                             0:-2]),

                        ],
                            title='点击查看固定资产详细',
                        )
                    ],
                    flush=True, start_collapsed=True, id="accordtion-computers"
                ),
            ),

            html.Br(),
            html.Br(),
            html.P(
                "查看员工历史资源总费用（先选'员工部门/资源池'列表 再选其下'人名'）",
                style={"fontSize": 25}),
            dbc.Row([
                dbc.Col([
                    dcc.RadioItems(
                        id='radio_员工历史资源费用',
                        options=[
                            {'label': '资源池', 'value': '资源池'},
                        ],
                        value='资源池',
                        style={"width": "60%"},
                        inline=True),
                ], xs=12, sm=12, md=2, lg=2, xl=2),
                dbc.Col([
                    dcc.Dropdown(
                        id='dropDown_员工历史资源费用',
                        options=[{'label': opt, 'value': opt} for opt in list(set(sumResDf['资源池']))],
                        value=list(set(sumResDf['资源池']))[0],
                        placeholder="选择资源池",
                        clearable=False,
                        style={"width": "100%"},
                    ),
                ], xs=12, sm=12, md=10, lg=10, xl=10),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.P('员工姓名'),
                ], xs=12, sm=12, md=2, lg=2, xl=2),
                dbc.Col([
                    dcc.Dropdown(
                        id='dropDown_员工姓名',
                        clearable=False,
                        placeholder="选择员工姓名",
                        style={"width": "100%"},
                        # multi=True
                    ),
                ], xs=12, sm=12, md=10, lg=10, xl=10),
            ]),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='staffHistoricalRes_days', config={'displayModeBar': False}, )
                ])
            ]),
            html.Br(),
            html.Br(),
            html.P('上诉员工历史资源费用'),
            html.Div([
                dash_table.DataTable(
                    id='table_历史员工资源费用', )
            ]),
            html.Br(),

        ], fluid=True, id="accordtion-res")


@app.callback(
    [Output("staff_number_indicator", "figure"),
     Output("logic_percentage", "figure"),
     Output("act_allday", "figure"),
     Output("act_perday", "figure"),
     Output("attend_allday", "figure"),
     Output("staff_in_indicator", "figure"),
     Output("staff_out_indicator", "figure"),
     Output("staff_intern_indicator", "figure"),
     Output("logic_in_percentage", "figure"),
     Output("logic_out_percentage", "figure"),
     Output("logic_intern_percentage", "figure"),
     Output("act_in_day", "figure"),
     Output("act_out_day", "figure"),
     Output("act_intern_day", "figure"),
     Output("attend_in_day", "figure"),
     Output("attend_out_day", "figure"),
     Output("attend_intern_day", "figure"),
     Output("act_in_perday", "figure"),
     Output("act_out_perday", "figure"),
     Output("act_intern_perday", "figure"),
     Output("sx_研究", "figure"),
     Output("sx_研究per", "figure"),
     Output("sx_开发", "figure"),
     Output("sx_开发per", "figure"),
     Output("sx_平台", "figure"),
     Output("sx_平台per", "figure"),
     Output("sx_测试", "figure"),
     Output("sx_测试per", "figure"),
     Output("sx_非", "figure"),
     Output("sx_非per", "figure"),
     ],
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def indicator_staff_summary(year, month):
    lastMonDf, curMonDf = getCurLastMonDf(历史底表, year, month)
    lastStaffDf, curStaffDf = getCurLastMonDf(历史人员维度, year, month)
    lastWBSDf, curWBSDf = groupByWBS(lastMonDf), groupByWBS(curMonDf)

    cur_in_staff_number = len(list(set(filterData(curMonDf, "员工组", "正式员工")['员工姓名'])))
    last_in_staff_number = len(list(set(filterData(lastMonDf, "员工组", "正式员工")['员工姓名'])))
    cur_out_staff_number = len(list(set(filterData(curMonDf, "员工组", "外包员工")['员工姓名'])))
    last_out_staff_number = len(list(set(filterData(lastMonDf, "员工组", "外包员工")['员工姓名'])))
    cur_intern_staff_number = len(list(set(filterData(curMonDf, "员工组", "实习生")['员工姓名'])))
    last_intern_staff_number = len(list(set(filterData(lastMonDf, "员工组", "实习生")['员工姓名'])))
    last_in_actual_day = filterData(lastMonDf, "员工组", "正式员工")['实际人天'].sum()
    cur_in_actual_day = filterData(curMonDf, "员工组", "正式员工")['实际人天'].sum()
    last_out_actual_day = filterData(lastMonDf, "员工组", "外包员工")['实际人天'].sum()
    cur_out_actual_day = filterData(curMonDf, "员工组", "外包员工")['实际人天'].sum()
    last_intern_actual_day = filterData(lastMonDf, "员工组", "实习生")['实际人天'].sum()
    cur_intern_actual_day = filterData(curMonDf, "员工组", "实习生")['实际人天'].sum()
    last_in_lo_day = filterCurMonStaff(lastStaffDf, "员工组", "正式员工")['理论人天'].sum()
    cur_in_lo_day = filterCurMonStaff(curStaffDf, "员工组", "正式员工")['理论人天'].sum()
    last_out_lo_day = filterCurMonStaff(lastStaffDf, "员工组", "外包员工")['理论人天'].sum()
    cur_out_lo_day = filterCurMonStaff(curStaffDf, "员工组", "外包员工")['理论人天'].sum()
    last_intern_lo_day = filterCurMonStaff(lastStaffDf, "员工组", "实习生")['理论人天'].sum()
    cur_intern_lo_day = filterCurMonStaff(curStaffDf, "员工组", "实习生")['理论人天'].sum()
    act_in_day = indicator_ppl(cur_in_actual_day, last_in_actual_day, "正式")
    act_out_day = indicator_ppl(cur_out_actual_day, last_out_actual_day, "外包")
    act_intern_day = indicator_ppl(cur_intern_actual_day, cur_intern_actual_day, "实习")
    attend_in_day = indicator_ppl(cur_in_actual_day, last_in_actual_day, "正式")
    attend_out_day = indicator_ppl(cur_out_actual_day, last_out_actual_day, "外包")
    attend_intern_day = indicator_ppl(cur_intern_actual_day, cur_intern_actual_day, "实习")
    act_in_perday = indicator_irdc_type_per(cur_in_actual_day, cur_in_staff_number, last_in_actual_day,
                                            last_in_staff_number, "正式")
    act_out_perday = indicator_irdc_type_per(cur_out_actual_day, cur_out_staff_number, last_out_actual_day,
                                             last_out_staff_number, "外包")
    act_intern_perday = indicator_irdc_type_per(cur_intern_actual_day, cur_intern_staff_number, last_intern_actual_day,
                                                last_intern_staff_number, "实习")
    sxData = filDataApartment(curMonDf, name)
    sxDataLast = filDataApartment(lastMonDf, name)
    sxDataTotal = try0toNone(int(sxData['实际人天'].sum()))
    sxDataTotalLast = try0toNone(int(sxDataLast['实际人天'].sum()))
    sxGroup研究 = tryExceptNone(blGroupByTitle(sxData, '资源池', '算法SDK资源池'))
    sxGroup开发 = tryExceptNone(blGroupByTitle(sxData, '资源池', '业务开发资源池'))
    sxGroup平台 = tryExceptNone(blGroupByTitle(sxData, '资源池', '架构平台资源池'))
    sxGroup测试 = tryExceptNone(blGroupByTitle(sxData, '资源池', '测试运维资源池'))
    sxGroup非 = tryExceptNone(blGroupByTitle(sxData, '资源池', '非资源池'))
    sxGroup研究last = tryExceptNone(blGroupByTitle(sxDataLast, '资源池', '算法SDK资源池'))
    sxGroup开发last = tryExceptNone(blGroupByTitle(sxDataLast, '资源池', '业务开发资源池'))
    sxGroup平台last = tryExceptNone(blGroupByTitle(sxDataLast, '资源池', '架构平台资源池'))
    sxGroup测试last = tryExceptNone(blGroupByTitle(sxDataLast, '资源池', '测试运维资源池'))
    sxGroup非last = tryExceptNone(blGroupByTitle(sxDataLast, '资源池', '非资源池'))
    sxGroup研究per = tryExceptNone(blGroupByTitlePer(sxGroup研究, sxData))
    sxGroup开发per = tryExceptNone(blGroupByTitlePer(sxGroup开发, sxData))
    sxGroup平台per = tryExceptNone(blGroupByTitlePer(sxGroup平台, sxData))
    sxGroup测试per = tryExceptNone(blGroupByTitlePer(sxGroup测试, sxData))
    sxGroup非per = tryExceptNone(blGroupByTitlePer(sxGroup非, sxData))
    sxGroup研究perlast = tryExceptNone(blGroupByTitlePer(sxGroup研究last, sxDataLast))
    sxGroup开发perlast = tryExceptNone(blGroupByTitlePer(sxGroup开发last, sxDataLast))
    sxGroup平台perlast = tryExceptNone(blGroupByTitlePer(sxGroup平台last, sxDataLast))
    sxGroup测试perlast = tryExceptNone(blGroupByTitlePer(sxGroup测试last, sxDataLast))
    sxGroup非perlast = tryExceptNone(blGroupByTitlePer(sxGroup非last, sxDataLast))

    staff_number_indicator = indicator_large_ppl(len(list(set(curMonDf['员工姓名']))), len(list(set(lastMonDf['员工姓名']))), "员工数")
    logic_percentage = indicator_irdc_rate(curStaffDf, lastStaffDf, "实际人天", "理论人天", "填报率")
    act_allday = indicator_irdc_sum(curMonDf, lastMonDf, "实际人天", "实际人天")
    act_perday = indicator_irdc_per(curMonDf, lastMonDf, "实际人天", "员工姓名", "实际人均")
    attend_allday = indicator_irdc_sum(cur_mon_staff, last_mon_staff, "实际人天", "考勤人天")
    staff_in_indicator = indicator_ppl(cur_in_staff_number, last_in_staff_number, "正式")
    staff_out_indicator = indicator_ppl(cur_out_staff_number, last_out_staff_number, "外包")
    staff_intern_indicator = indicator_ppl(cur_intern_staff_number, last_intern_staff_number, "实习")
    logic_in_percentage = indicator_logic_percentage(cur_in_actual_day, cur_in_lo_day, last_in_actual_day,
                                                     last_in_lo_day,
                                                     "正式")
    logic_out_percentage = indicator_logic_percentage(cur_out_actual_day, cur_out_lo_day, last_out_actual_day,
                                                      last_out_lo_day, "外包")
    logic_intern_percentage = indicator_logic_percentage(cur_intern_actual_day, cur_intern_lo_day,
                                                         last_intern_actual_day,
                                                         last_intern_lo_day, "实习")
    sx_研究 = indicator_bl_total_midBL(sxGroup研究, sxGroup研究last, '算法总人天')
    sx_研究per = indicator_bl_total_mid_rateBL(sxGroup研究per, sxGroup研究perlast, '占比')
    sx_开发 = indicator_bl_total_midBL(sxGroup开发, sxGroup开发last, '开发总人天')
    sx_开发per = indicator_bl_total_mid_rateBL(sxGroup开发per, sxGroup开发perlast, '占比')
    sx_平台 = indicator_bl_total_midBL(sxGroup平台, sxGroup平台last, '平台总人天')
    sx_平台per = indicator_bl_total_mid_rateBL(sxGroup平台per, sxGroup平台perlast, '占比')
    sx_测试 = indicator_bl_total_midBL(sxGroup测试, sxGroup测试last, '测试总人天')
    sx_测试per = indicator_bl_total_mid_rateBL(sxGroup测试per, sxGroup测试perlast, '占比')
    sx_非 = indicator_bl_total_midBL(sxGroup非, sxGroup非last, '非资源总人天')
    sx_非per = indicator_bl_total_mid_rateBL(sxGroup非per, sxGroup非perlast, '占比')

    return staff_number_indicator, logic_percentage, act_allday, act_perday, attend_allday, \
           staff_in_indicator, staff_out_indicator, staff_intern_indicator, logic_in_percentage, logic_out_percentage, \
           logic_intern_percentage, act_in_day, act_out_day, act_intern_day, attend_in_day, attend_out_day, attend_intern_day, \
           act_in_perday, act_out_perday, act_intern_perday, sx_研究, sx_研究per, sx_开发, sx_开发per, sx_平台, sx_平台per,\
           sx_测试, sx_测试per, sx_非, sx_非per


@app.callback([
     Output("wbs_all_number", "figure"),
     Output("wbs_d_number", "figure"),
     Output("sx_d_number", "figure"),
     Output("ir_d_number", "figure"),
     Output("dx_d_number", "figure"),
     Output("innova_d_number", "figure"),
     Output("mkt_d_number", "figure"),
     Output("oac_d_number", "figure"),
     Output("wbs_p_number", "figure"),
     Output("sx_p_number", "figure"),
     Output("ir_p_number", "figure"),
     Output("dx_p_number", "figure"),
     Output("innova_p_number", "figure"),
     Output("mkt_p_number", "figure"),
     Output("oac_p_number", "figure"),
     Output("wbs_r_number", "figure"),
     Output("sx_r_number", "figure"),
     Output("ir_r_number", "figure"),
     Output("dx_r_number", "figure"),
     Output("innova_r_number", "figure"),
     Output("mkt_r_number", "figure"),
     Output("oac_r_number", "figure"),
     Output("wbs_m_number", "figure"),
     Output("sx_m_number", "figure"),
     Output("ir_m_number", "figure"),
     Output("dx_m_number", "figure"),
     Output("innova_m_number", "figure"),
     Output("mkt_m_number", "figure"),
     Output("oac_m_number", "figure"),
     Output("wbs_actual_hrs", "figure"),
     Output("wbs_d_act", "figure"),
     Output("sx_d_act", "figure"),
     Output("ir_d_act", "figure"),
     Output("dx_d_act", "figure"),
     Output("innova_d_act", "figure"),
     Output("mkt_d_act", "figure"),
     Output("oac_d_act", "figure"),
     Output("wbs_p_act", "figure"),
     Output("sx_p_act", "figure"),
     Output("ir_p_act", "figure"),
     Output("dx_p_act", "figure"),
     Output("innova_p_act", "figure"),
     Output("mkt_p_act", "figure"),
     Output("oac_p_act", "figure"),
     Output("wbs_r_act", "figure"),
     Output("sx_r_act", "figure"),
     Output("ir_r_act", "figure"),
     Output("dx_r_act", "figure"),
     Output("innova_r_act", "figure"),
     Output("mkt_r_act", "figure"),
     Output("oac_r_act", "figure"),
     Output("wbs_m_act", "figure"),
     Output("sx_m_act", "figure"),
     Output("ir_m_act", "figure"),
     Output("dx_m_act", "figure"),
     Output("innova_m_act", "figure"),
     Output("mkt_m_act", "figure"),
     Output("oac_m_act", "figure"),],
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def indicator_summary_wbs(year, month):
    lastMonDf, curMonDf = getCurLastMonDf(历史底表, year, month)
    lastStaffDf, curStaffDf = getCurLastMonDf(历史人员维度, year, month)
    lastWBSDf, curWBSDf = groupByWBS(lastMonDf), groupByWBS(curMonDf)

    # wbs
    indicator_sxibg_num_last = lastMonDf[lastMonDf['WBS所属业务线'].isin(['SX'])].reset_index(drop=True)
    indicator_sxibg_num_cur = curMonDf[curMonDf['WBS所属业务线'].isin(['SX'])].reset_index(drop=True)

    indicator_sx_d_num_last = filterWBSLen(indicator_sxibg_num_last,'D')
    indicator_sx_d_num_cur = filterWBSLen(indicator_sxibg_num_cur, 'D')
    sx_d_number = indicator_wbs_number2(indicator_sx_d_num_cur, indicator_sx_d_num_last, 'SX')

    indicator_sx_p_num_last = filterWBSLen(indicator_sxibg_num_last,'P')
    indicator_sx_p_num_cur = filterWBSLen(indicator_sxibg_num_cur,'P')
    sx_p_number = indicator_wbs_number2(indicator_sx_p_num_cur, indicator_sx_p_num_last, 'SX')

    indicator_sx_r_num_last = filterWBSLen(indicator_sxibg_num_last,'R')
    indicator_sx_r_num_cur = filterWBSLen(indicator_sxibg_num_cur,  'R')
    sx_r_number = indicator_wbs_number2(indicator_sx_r_num_cur, indicator_sx_r_num_last, 'SX')

    indicator_sx_m_num_last = filterWBSLen(indicator_sxibg_num_last, 'M')
    indicator_sx_m_num_cur = filterWBSLen(indicator_sxibg_num_cur, 'M')
    sx_m_number = indicator_wbs_number2(indicator_sx_m_num_cur, indicator_sx_m_num_last, 'SX')

    indicator_sx_d_act_last = returnWBS_Bl_act(indicator_sxibg_num_last, 'D')
    indicator_sx_d_act_cur = returnWBS_Bl_act(indicator_sxibg_num_cur, 'D')
    sx_d_act = indicator_wbs_number2(indicator_sx_d_act_cur, indicator_sx_d_act_last, 'SX')

    indicator_sx_p_act_last = returnWBS_Bl_act(indicator_sxibg_num_last, 'P')
    indicator_sx_p_act_cur = returnWBS_Bl_act(indicator_sxibg_num_cur, 'P')
    sx_p_act = indicator_wbs_number2(indicator_sx_p_act_cur, indicator_sx_p_act_last, 'SX')

    indicator_sx_r_act_last = returnWBS_Bl_act(indicator_sxibg_num_last, 'R')
    indicator_sx_r_act_cur = returnWBS_Bl_act(indicator_sxibg_num_cur, 'R')
    sx_r_act = indicator_wbs_number2(indicator_sx_r_act_cur, indicator_sx_r_act_last, 'SX')

    indicator_sx_m_act_last = returnWBS_Bl_act(indicator_sxibg_num_last, 'M')
    indicator_sx_m_act_cur = returnWBS_Bl_act(indicator_sxibg_num_cur, 'M')
    sx_m_act = indicator_wbs_number2(indicator_sx_m_act_cur, indicator_sx_m_act_last, 'SX')

    # indicator_ssxibg_act_last = actual本月WBS维度[actual本月WBS维度['WBS所属部门'].isin(['中东云平台','亚太云平台'])]['实际人天'].sum()
    # indicator_sxibg_act_cur = actual本月WBS维度[actual本月WBS维度['WBS所属部门'].isin(['中东云平台','亚太云平台'])]['实际人天'].sum()
    # sx_act = indicator_wbs_number2(indicator_sxibg_act_cur, indicator_ssxibg_act_last,'SX')

    indicator_ir_num_last = lastMonDf[lastMonDf['WBS所属业务线'].isin(['IR'])].reset_index(drop=True)
    indicator_ir_num_cur = curMonDf[curMonDf['WBS所属业务线'].isin(['IR'])].reset_index(drop=True)

    indicator_ir_d_num_last = filterWBSLen(indicator_ir_num_last, 'D')
    indicator_ir_d_num_cur = filterWBSLen(indicator_ir_num_cur, 'D')
    ir_d_number = indicator_wbs_number2(indicator_ir_d_num_cur, indicator_ir_d_num_last, 'IR')

    indicator_ir_p_num_last = filterWBSLen(indicator_ir_num_last, 'P')
    indicator_ir_p_num_cur = filterWBSLen(indicator_ir_num_cur, 'P')
    ir_p_number = indicator_wbs_number2(indicator_ir_p_num_cur, indicator_ir_p_num_last, 'IR')

    indicator_ir_r_num_last = filterWBSLen(indicator_ir_num_last, 'R')
    indicator_ir_r_num_cur = filterWBSLen(indicator_ir_num_cur, 'R')
    ir_r_number = indicator_wbs_number2(indicator_ir_r_num_cur, indicator_ir_r_num_last, 'IR')

    indicator_ir_m_num_last = filterWBSLen(indicator_ir_num_last, 'M')
    indicator_ir_m_num_cur = filterWBSLen(indicator_ir_num_cur, 'M')
    ir_m_number = indicator_wbs_number2(indicator_ir_m_num_cur, indicator_ir_m_num_last, 'IR')

    indicator_ir_d_act_last = returnWBS_Bl_act(indicator_ir_num_last, 'D')
    indicator_ir_d_act_cur = returnWBS_Bl_act(indicator_ir_num_cur, 'D')
    ir_d_act = indicator_wbs_number2(indicator_ir_d_act_cur, indicator_ir_d_act_last, 'IR')

    indicator_ir_p_act_last = returnWBS_Bl_act(indicator_ir_num_last, 'P')
    indicator_ir_p_act_cur = returnWBS_Bl_act(indicator_ir_num_cur, 'P')
    ir_p_act = indicator_wbs_number2(indicator_ir_p_act_cur, indicator_ir_p_act_last, 'IR')

    indicator_ir_r_act_last = returnWBS_Bl_act(indicator_ir_num_last, 'R')
    indicator_ir_r_act_cur = returnWBS_Bl_act(indicator_ir_num_cur, 'R')
    ir_r_act = indicator_wbs_number2(indicator_ir_r_act_cur, indicator_ir_r_act_last, 'IR')

    indicator_ir_m_act_last = returnWBS_Bl_act(indicator_ir_num_last, 'M')
    indicator_ir_m_act_cur = returnWBS_Bl_act(indicator_ir_num_cur, 'M')
    ir_m_act = indicator_wbs_number2(indicator_ir_m_act_cur, indicator_ir_m_act_last, 'IR')


    indicator_dx_num_last = lastMonDf[lastMonDf['WBS所属业务线'].isin(['DX-TY'])].reset_index(drop=True)
    indicator_dx_num_cur = curMonDf[curMonDf['WBS所属业务线'].isin(['DX-TY'])].reset_index(drop=True)

    indicator_dx_d_num_last = filterWBSLen(indicator_dx_num_last, 'D')
    indicator_dx_d_num_cur = filterWBSLen(indicator_dx_num_cur, 'D')
    dx_d_number = indicator_wbs_number2(indicator_dx_d_num_cur, indicator_dx_d_num_last, 'DX-TY')

    indicator_dx_p_num_last = filterWBSLen(indicator_dx_num_last, 'P')
    indicator_dx_p_num_cur = filterWBSLen(indicator_dx_num_cur, 'P')
    dx_p_number = indicator_wbs_number2(indicator_dx_p_num_cur, indicator_dx_p_num_last, 'DX-TY')

    indicator_dx_r_num_last = filterWBSLen(indicator_dx_num_last, 'R')
    indicator_dx_r_num_cur = filterWBSLen(indicator_dx_num_cur, 'R')
    dx_r_number = indicator_wbs_number2(indicator_dx_r_num_cur, indicator_dx_r_num_last, 'DX-TY')

    indicator_dx_m_num_last = filterWBSLen(indicator_dx_num_last, 'M')
    indicator_dx_m_num_cur = filterWBSLen(indicator_dx_num_cur, 'M')
    dx_m_number = indicator_wbs_number2(indicator_dx_m_num_cur, indicator_dx_m_num_last, 'DX-TY')

    indicator_dx_d_act_last = returnWBS_Bl_act(indicator_dx_num_last, 'D')
    indicator_dx_d_act_cur = returnWBS_Bl_act(indicator_dx_num_cur, 'D')
    dx_d_act = indicator_wbs_number2(indicator_dx_d_act_cur, indicator_dx_d_act_last, 'DX-TY')

    indicator_dx_p_act_last = returnWBS_Bl_act(indicator_dx_num_last, 'P')
    indicator_dx_p_act_cur = returnWBS_Bl_act(indicator_dx_num_cur, 'P')
    dx_p_act = indicator_wbs_number2(indicator_dx_p_act_cur, indicator_dx_p_act_last, 'DX-TY')

    indicator_dx_r_act_last = returnWBS_Bl_act(indicator_dx_num_last, 'R')
    indicator_dx_r_act_cur = returnWBS_Bl_act(indicator_dx_num_cur, 'R')
    dx_r_act = indicator_wbs_number2(indicator_dx_r_act_cur, indicator_dx_r_act_last, 'DX-TY')

    indicator_dx_m_act_last = returnWBS_Bl_act(indicator_dx_num_last, 'M')
    indicator_dx_m_act_cur = returnWBS_Bl_act(indicator_dx_num_cur, 'M')
    dx_m_act = indicator_wbs_number2(indicator_dx_m_act_cur, indicator_dx_m_act_last, 'DX-TY')


    indicator_innova_num_last = lastMonDf[lastMonDf['WBS所属业务线'].isin(['DX-SKU'])].reset_index(drop=True)
    indicator_innova_num_cur = curMonDf[curMonDf['WBS所属业务线'].isin(['DX-SKU'])].reset_index(drop=True)

    indicator_innova_d_num_last = filterWBSLen(indicator_innova_num_last, 'D')
    indicator_innova_d_num_cur = filterWBSLen(indicator_innova_num_cur, 'D')
    innova_d_number = indicator_wbs_number2(indicator_innova_d_num_cur, indicator_innova_d_num_last, 'DX-SKU')

    indicator_innova_p_num_last = filterWBSLen(indicator_innova_num_last, 'P')
    indicator_innova_p_num_cur = filterWBSLen(indicator_innova_num_cur, 'P')
    innova_p_number = indicator_wbs_number2(indicator_innova_p_num_cur, indicator_innova_p_num_last, 'DX-SKU')

    indicator_innova_r_num_last = filterWBSLen(indicator_innova_num_last, 'R')
    indicator_innova_r_num_cur = filterWBSLen(indicator_innova_num_cur, 'R')
    innova_r_number = indicator_wbs_number2(indicator_innova_r_num_cur, indicator_innova_r_num_last, 'DX-SKU')

    indicator_innova_m_num_last = filterWBSLen(indicator_innova_num_last, 'M')
    indicator_innova_m_num_cur = filterWBSLen(indicator_innova_num_cur, 'M')
    innova_m_number = indicator_wbs_number2(indicator_innova_m_num_cur, indicator_innova_m_num_last, 'DX-SKU')

    indicator_innova_d_act_last = returnWBS_Bl_act(indicator_innova_num_last, 'D')
    indicator_innova_d_act_cur = returnWBS_Bl_act(indicator_innova_num_cur, 'D')
    innova_d_act = indicator_wbs_number2(indicator_innova_d_act_cur, indicator_innova_d_act_last, 'DX-SKU')

    indicator_innova_p_act_last = returnWBS_Bl_act(indicator_innova_num_last, 'P')
    indicator_innova_p_act_cur = returnWBS_Bl_act(indicator_innova_num_cur, 'P')
    innova_p_act = indicator_wbs_number2(indicator_innova_p_act_cur, indicator_innova_p_act_last, 'DX-SKU')

    indicator_innova_r_act_last = returnWBS_Bl_act(indicator_innova_num_last, 'R')
    indicator_innova_r_act_cur = returnWBS_Bl_act(indicator_innova_num_cur, 'R')
    innova_r_act = indicator_wbs_number2(indicator_innova_r_act_cur, indicator_innova_r_act_last, 'DX-SKU')

    indicator_innova_m_act_last = returnWBS_Bl_act(indicator_innova_num_last, 'M')
    indicator_innova_m_act_cur = returnWBS_Bl_act(indicator_innova_num_cur, 'M')
    innova_m_act = indicator_wbs_number2(indicator_innova_m_act_cur, indicator_innova_m_act_last, 'DX-SKU')


    indicator_oac_num_last = lastMonDf[lastMonDf['WBS所属业务线'].isin(['OAC'])].reset_index(drop=True)
    indicator_oac_num_cur = curMonDf[curMonDf['WBS所属业务线'].isin(['OAC'])].reset_index(drop=True)

    indicator_oac_d_num_last = filterWBSLen(indicator_oac_num_last, 'D')
    indicator_oac_d_num_cur = filterWBSLen(indicator_oac_num_cur, 'D')
    oac_d_number = indicator_wbs_number2(indicator_oac_d_num_cur, indicator_oac_d_num_last, '运赋')

    indicator_oac_p_num_last = filterWBSLen(indicator_oac_num_last, 'P')
    indicator_oac_p_num_cur = filterWBSLen(indicator_oac_num_cur, 'P')
    oac_p_number = indicator_wbs_number2(indicator_oac_p_num_cur, indicator_oac_p_num_last, '运赋')

    indicator_oac_r_num_last = filterWBSLen(indicator_oac_num_last, 'R')
    indicator_oac_r_num_cur = filterWBSLen(indicator_oac_num_cur, 'R')
    oac_r_number = indicator_wbs_number2(indicator_oac_r_num_cur, indicator_oac_r_num_last, '运赋')

    indicator_oac_m_num_last = filterWBSLen(indicator_oac_num_last, 'M')
    indicator_oac_m_num_cur = filterWBSLen(indicator_oac_num_cur, 'M')
    oac_m_number = indicator_wbs_number2(indicator_oac_m_num_cur, indicator_oac_m_num_last, '运赋')

    indicator_oac_d_act_last = returnWBS_Bl_act(indicator_oac_num_last, 'D')
    indicator_oac_d_act_cur = returnWBS_Bl_act(indicator_oac_num_cur, 'D')
    oac_d_act = indicator_wbs_number2(indicator_oac_d_act_cur, indicator_oac_d_act_last, '运赋')

    indicator_oac_p_act_last = returnWBS_Bl_act(indicator_oac_num_last, 'P')
    indicator_oac_p_act_cur = returnWBS_Bl_act(indicator_oac_num_cur, 'P')
    oac_p_act = indicator_wbs_number2(indicator_oac_p_act_cur, indicator_oac_p_act_last, '运赋')

    indicator_oac_r_act_last = returnWBS_Bl_act(indicator_oac_num_last, 'R')
    indicator_oac_r_act_cur = returnWBS_Bl_act(indicator_oac_num_cur, 'R')
    oac_r_act = indicator_wbs_number2(indicator_oac_r_act_cur, indicator_oac_r_act_last, '运赋')

    indicator_oac_m_act_last = returnWBS_Bl_act(indicator_oac_num_last, 'M')
    indicator_oac_m_act_cur = returnWBS_Bl_act(indicator_oac_num_cur, 'M')
    oac_m_act = indicator_wbs_number2(indicator_oac_m_act_cur, indicator_oac_m_act_last, '运赋')


    indicator_mkt_num_last = lastMonDf[lastMonDf['WBS所属业务线'].isin(['MKT'])].reset_index(drop=True)
    indicator_mkt_num_cur = curMonDf[curMonDf['WBS所属业务线'].isin(['MKT'])].reset_index(drop=True)

    indicator_mkt_d_num_last = filterWBSLen(indicator_mkt_num_last, 'D')
    indicator_mkt_d_num_cur = filterWBSLen(indicator_mkt_num_cur, 'D')
    mkt_d_number = indicator_wbs_number2(indicator_mkt_d_num_cur, indicator_mkt_d_num_last, 'MKT')

    indicator_mkt_p_num_last = filterWBSLen(indicator_mkt_num_last, 'P')
    indicator_mkt_p_num_cur = filterWBSLen(indicator_mkt_num_cur, 'P')
    mkt_p_number = indicator_wbs_number2(indicator_mkt_p_num_cur, indicator_mkt_p_num_last, 'MKT')

    indicator_mkt_r_num_last = filterWBSLen(indicator_mkt_num_last, 'R')
    indicator_mkt_r_num_cur = filterWBSLen(indicator_mkt_num_cur, 'R')
    mkt_r_number = indicator_wbs_number2(indicator_mkt_r_num_cur, indicator_mkt_r_num_last, 'MKT')

    indicator_mkt_m_num_last = filterWBSLen(indicator_mkt_num_last, 'M')
    indicator_mkt_m_num_cur = filterWBSLen(indicator_mkt_num_cur, 'M')
    mkt_m_number = indicator_wbs_number2(indicator_mkt_m_num_cur, indicator_mkt_m_num_last, 'MKT')

    indicator_mkt_d_act_last = returnWBS_Bl_act(indicator_mkt_num_last, 'D')
    indicator_mkt_d_act_cur = returnWBS_Bl_act(indicator_mkt_num_cur, 'D')
    mkt_d_act = indicator_wbs_number2(indicator_mkt_d_act_cur, indicator_mkt_d_act_last, 'MKT')

    indicator_mkt_p_act_last = returnWBS_Bl_act(indicator_mkt_num_last, 'P')
    indicator_mkt_p_act_cur = returnWBS_Bl_act(indicator_mkt_num_cur, 'P')
    mkt_p_act = indicator_wbs_number2(indicator_mkt_p_act_cur, indicator_mkt_p_act_last, 'MKT')

    indicator_mkt_r_act_last = returnWBS_Bl_act(indicator_mkt_num_last, 'R')
    indicator_mkt_r_act_cur = returnWBS_Bl_act(indicator_mkt_num_cur, 'R')
    mkt_r_act = indicator_wbs_number2(indicator_mkt_r_act_cur, indicator_mkt_r_act_last, 'MKT')

    indicator_mkt_m_act_last = returnWBS_Bl_act(indicator_mkt_num_last, 'M')
    indicator_mkt_m_act_cur = returnWBS_Bl_act(indicator_mkt_num_cur, 'M')
    mkt_m_act = indicator_wbs_number2(indicator_mkt_m_act_cur, indicator_mkt_m_act_last, 'MKT')

    wbs_all_number = indicator_wbs_sum_wide(actual_wbs_tb(curWBSDf), actual_wbs_tb(lastWBSDf), '项目编号', "WBS个数")
    wbs_p_number = indicator_wbs_number(wbs_type_number(curWBSDf), wbs_type_number(lastWBSDf), 'P', 'P类总个数')
    wbs_m_number = indicator_wbs_number(wbs_type_number(curWBSDf), wbs_type_number(lastWBSDf), 'M', 'M类总个数')
    wbs_r_number = indicator_wbs_number(wbs_type_number(curWBSDf), wbs_type_number(lastWBSDf), 'R', 'R类总个数')
    wbs_d_number = indicator_wbs_number(wbs_type_number(curWBSDf), wbs_type_number(lastWBSDf), 'D', 'D类总个数')
    # wbs_p_numebr_sx = indicator_wbs_number_sm(type本月WBS维度, type上月WBS维度,'P','P类总数')
    # wbs_m_numebr_sx = indicator_wbs_number_sm(type本月WBS维度, type上月WBS维度,'M','M类总数')
    # wbs_r_numebr_sx = indicator_wbs_number_sm(type本月WBS维度, type上月WBS维度,'R','R类总数')
    # wbs_d_numebr_sx = indicator_wbs_number_sm(type本月WBS维度, type上月WBS维度,'D','D类总数')
    wbs_more_number = indicator_wbs_number2(len(curWBSDf), len(lastWBSDf), '增加')
    wbs_less_number = indicator_wbs_number2(len(lastWBSDf), len(curWBSDf), '减少')
    wbs_actual_hrs = indicator_wbs_act_wide(curMonDf, lastMonDf, '实际人天', '实际人天')
    # wbs_p_act_percentage = indicator_wbs_type(actual本月WBS维度, actual上月WBS维度, 'P','WBS类型','实际人天','P占比')
    # wbs_m_act_percentage = indicator_wbs_type(actual本月WBS维度, actual上月WBS维度, 'M','WBS类型','实际人天','M占比')
    # wbs_r_act_percentage = indicator_wbs_type(actual本月WBS维度, actual上月WBS维度, 'R','WBS类型','实际人天','R占比')
    # wbs_d_act_percentage = indicator_wbs_type(actual本月WBS维度, actual上月WBS维度, 'D','WBS类型','实际人天','D占比')
    wbs_p_act = indicator_wbs_type_sum(curMonDf, lastMonDf, 'P', 'WBS类型', '实际人天', 'P类总人天')
    wbs_m_act = indicator_wbs_type_sum(curMonDf, lastMonDf, 'M', 'WBS类型', '实际人天', 'M类总人天')
    wbs_r_act = indicator_wbs_type_sum(curMonDf, lastMonDf, 'R', 'WBS类型', '实际人天', 'R类总人天')
    wbs_d_act = indicator_wbs_type_sum(curMonDf, lastMonDf, 'D', 'WBS类型', '实际人天', 'D类总人天')
    return  wbs_all_number, wbs_d_number, sx_d_number, ir_d_number, dx_d_number, \
           innova_d_number, mkt_d_number, oac_d_number, wbs_p_number, sx_p_number, ir_p_number, dx_p_number, innova_p_number, \
           mkt_p_number, oac_p_number, wbs_r_number, sx_r_number, ir_r_number, dx_r_number, innova_r_number, mkt_r_number, \
           oac_r_number, wbs_m_number, sx_m_number, ir_m_number, dx_m_number, innova_m_number, mkt_m_number, oac_m_number, \
           wbs_actual_hrs, wbs_d_act, sx_d_act, ir_d_act, dx_d_act, innova_d_act, mkt_d_act, oac_d_act, wbs_p_act, sx_p_act, \
           ir_p_act, dx_p_act, innova_p_act, mkt_p_act, oac_p_act, wbs_r_act, sx_r_act, ir_r_act, dx_r_act, innova_r_act, \
           mkt_r_act, oac_r_act, wbs_m_act, sx_m_act, ir_m_act, dx_m_act, innova_m_act, mkt_m_act, oac_m_act



@app.callback(
    Output("graph_notActiveWBS", "figure"),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value'),
     Input('dropDown_wbs_type','value'),
     Input('radio_notActiveWBS','value')]
)
def update_notActiveWbs_pie(year, month, wbsType, radioChoice):
    data = 历史底表[历史底表['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    data = data[data['WBS类型'].isin(wbsType)].reset_index(drop=True)
    data = groupByWBS(data)
    df = addWBSNotAcitve(groupByWBS(data), readhistroyData(工时历史总表汇总(), 'WBS维度'), year, month)
    if radioChoice == 'Pie':
        return figNotActiveWBSpie(df, 'WBS未活跃时长', month)



@app.callback(
    Output("graph_wh员工组vs资源池", "figure"),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value'),
     Input('dropDown_wbs_type','value'),
     Input('radio_wh员工组vs资源池','value')]
)
def update_wbsType_pie(year, month, wbsType, radioChoice):
    data = 历史底表[历史底表['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    data = data[data['WBS类型'].isin(wbsType)].reset_index(drop=True)
    if radioChoice == 'WBS类型':
        return figWBSTypepie细分2(data, '实际人天', month)
    elif radioChoice == '员工组':
        return figWBSpie员工组(data, '员工组', month)
    elif radioChoice == '资源池':
        return figWBSpie员工组(data, '资源池', month)
    elif radioChoice == '未活跃WBS':
        data = groupByWBS(data)
        df = addWBSNotAcitve(groupByWBS(data), readhistroyData(工时历史总表汇总(), 'WBS维度'), year, month)
        return figNotActiveWBSpie(df, 'WBS未活跃时长', month)



@app.callback(
    Output('graph_wh利润中心vsWBS部门', 'figure'),
    [Input('dropDown_wbs_type', 'value'),
    Input(component_id='radio_wh员工组vsWBS类型vs资源池', component_property='value'),
     Input(component_id='radio_wh利润中心vsWBS部门', component_property='value'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_WBSgraph_profitCenter_WBSApartment(wbsType, fitler, attri, year, month):
    data = wbsTypeFilterBL(历史底表, wbsType, name, year, month)
    if fitler == 'WBS类型':
        if attri == '利润中心':
            return fig员工部门不同维度wbs22(groupByProfit(data, "WBS类型"), '合并利润中心', "WBS类型",
                                          str(month)+'月WBS类型工时投入')
        elif attri == 'WBS所属部门':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data,'WBS所属部门', '实际人天', "WBS类型"),'WBS所属部门', "WBS类型",
                                          str(month)+'月WBS类型工时投入')
    elif fitler == '资源池':
        if attri == '利润中心':
            return fig员工部门不同维度wbs22(groupByProfit(data, "资源池"), '合并利润中心', "资源池",
                                            str(month) + '月资源池工时投入')
        elif attri == 'WBS所属部门':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, 'WBS所属部门', '实际人天', "资源池"), 'WBS所属部门',
                                            "资源池",
                                            str(month) + '月资源池工时投入')
    elif fitler == "员工组":
        if attri == '利润中心':
            return fig员工部门不同维度wbs22(groupByProfit(data,  "员工组"), '合并利润中心', "员工组",
                                            str(month) + '月员工组工时投入')
        elif attri == 'WBS所属部门':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, 'WBS所属部门', '实际人天', "员工组"), 'WBS所属部门',
                                            "员工组",
                                            str(month) + '月员工组工时投入')


#
# @app.callback(
#     Output('graph_wh员工组_利润中心vsWBS部门', 'figure'),
#     [Input('dropDown_wbs_type', 'value'),
#      Input(component_id='radio_wh员工组_利润中心vsWBS部门', component_property='value'),
#      Input('dropDown_工时year', 'value'),
#      Input('dropDown_工时month', 'value')]
# )
# def build_WBSgraph_profitCenter_WBSApartment2(wbsType, attri, year, month):
#     data = wbsTypeFilterBL(历史底表, wbsType, name, year, month)
#     if attri == '利润中心':
#         return fig员工部门不同维度wbs22(wbsQuickCheck(data, '利润中心','实际人天', "员工组"), '利润中心', "员工组",
#                                       str(month)+'月员工组工时投入')
#     elif attri == 'WBS所属部门':
#         return fig员工部门不同维度wbs22(wbsQuickCheck(data,'WBS所属部门', '实际人天', "员工组"),'WBS所属部门', "员工组",
#                                       str(month)+'月员工组工时投入')
#
#
# @app.callback(
#     Output('graph_wh资源池_利润中心vsWBS部门', 'figure'),
#     [Input('dropDown_wbs_type', 'value'),
#      Input(component_id='radio_wh资源池_利润中心vsWBS部门', component_property='value'),
#      Input('dropDown_工时year', 'value'),
#      Input('dropDown_工时month', 'value')]
# )
# def build_WBSgraph_profitCenter_WBSApartment3(wbsType, attri, year, month):
#     data = wbsTypeFilterBL(历史底表, wbsType, name, year, month)
#     if attri == '利润中心':
#         return fig员工部门不同维度wbs22(wbsQuickCheck(data, '利润中心','实际人天', "资源池"), '利润中心', "资源池",
#                                       str(month)+'月资源池工时投入')
#     elif attri == 'WBS所属部门':
#         return fig员工部门不同维度wbs22(wbsQuickCheck(data,'WBS所属部门', '实际人天', "资源池"),'WBS所属部门', "资源池",
#                                       str(month)+'月资源池工时投入')


@app.callback(
    Output('graph_wh非业务线', 'figure'),
    [Input('dropDown_wbs_type', 'value'),
     Input(component_id='radio_wh非业务线', component_property='value'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_WBSgraph_notBL(wbsType, attri, year, month):
    历史底表DF = readhistroyData(工时历史总表汇总(), '合并底表')
    历史底表DF = 历史底表DF[历史底表DF['WBS所属业务线'] == nameEn]
    历史底表DF = 历史底表DF[历史底表DF['员工所属部门'] != name].reset_index(drop=True)
    data = wbsTypeFilterBL2(历史底表DF, wbsType,  year, month)
    if attri == 'WBS类型':
        return fig员工部门不同维度wbs22(wbsQuickCheck(data, 'WBS所属部门','实际人天', "WBS类型"), 'WBS所属部门', "WBS类型",
                                      str(month)+'月非'+str(nameEn)+'员工在WBS类型的工时投入')
    elif attri == '员工组':
        return fig员工部门不同维度wbs22(wbsQuickCheck(data,'WBS所属部门', '实际人天', "员工组"),'WBS所属部门', "员工组",
                                      str(month)+'月非'+str(nameEn)+'员工在员工组的工时投入')
    elif attri == '资源池':
        return fig员工部门不同维度wbs22(wbsQuickCheck(data,'WBS所属部门', '实际人天', "资源池"),'WBS所属部门', "资源池",
                                      str(month)+'月非'+str(nameEn)+'员工在资源池的工时投入')


@app.callback(
    Output('graph_wh非业务线项目名称vswbs部门', 'figure'),
    [Input(component_id='radio_wh非业务线项目名称vswbs部门', component_property='value'),
    Input(component_id='radio_wh非业务线项目名称vswbs部门2', component_property='value'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_WBSgraph_notBL(attri, attri2, year, month):
    历史底表DF = readhistroyData(工时历史总表汇总(), '合并底表')
    历史底表DF = 历史底表DF[历史底表DF['WBS所属业务线'] == nameEn]
    历史底表DF = 历史底表DF[历史底表DF['员工所属部门'] != name].reset_index(drop=True)
    data = wbsTypeFilterBL3(历史底表DF, year, month)
    if attri == "WBS所属部门":
        if attri2 == 'WBS类型':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, 'WBS所属部门', '实际人天', "WBS类型"), 'WBS所属部门',"WBS类型",
                                            str(month) + '月非' + str(nameEn) + '员工在WBS类型的工时投入')
        elif attri2 == '员工组':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, 'WBS所属部门', '实际人天', "员工组"), 'WBS所属部门',"员工组",
                                            str(month) + '月非' + str(nameEn) + '员工在员工组的工时投入')
        elif attri2 == '资源池':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, 'WBS所属部门', '实际人天', "资源池"), 'WBS所属部门', "资源池",
                                            str(month) + '月非' + str(nameEn) + '员工在资源池的工时投入')
        elif attri2 == '员工姓名':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, 'WBS所属部门', '实际人天', "员工姓名"), 'WBS所属部门', "员工姓名",
                                            str(month) + '月非' + str(nameEn) + '员工投入到本部门的工时')
    elif attri == '项目名称':
        if attri2 == 'WBS类型':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, '项目名称', '实际人天', "WBS类型"), '项目名称', "WBS类型",
                                            str(month) + '月非' + str(nameEn) + '员工在WBS类型的工时投入')
        elif attri2 == '员工组':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, '项目名称', '实际人天', "员工组"), '项目名称', "员工组",
                                            str(month) + '月非' + str(nameEn) + '员工在员工组的工时投入')
        elif attri2 == '资源池':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, '项目名称', '实际人天', "资源池"), '项目名称', "资源池",
                                            str(month) + '月非' + str(nameEn) + '员工在资源池的工时投入')
        elif attri2 == '员工姓名':
            return fig员工部门不同维度wbs22(wbsQuickCheck(data, '项目名称', '实际人天', "员工姓名"), '项目名称', "员工姓名",
                                            str(month) + '月非' + str(nameEn) + '员工投入到本部门的工时')





# @app.callback(
#     Output("graph_wbsTypePercentage", "figure"),
#     [Input('dropDown_工时year', 'value'),
#      Input('dropDown_工时month', 'value'),
#      Input('dropDown_wbs_type','value'),
#      Input('radio_wbsTypePercentage','value')]
# )
# def update_wbsType_pie(year, month, wbsType, actEst):
#     data = 历史底表[历史底表['工时年份'] == year].reset_index(drop=True)
#     data = data[data['工时月份'] == month].reset_index(drop=True)
#     data = data[data['WBS类型'].isin(wbsType)].reset_index(drop=True)
#     return figWBSTypepie细分2(data, actEst, month)



@app.callback(
    Output("graph_wbsTop10", "figure"),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value'),
     Input('dropDown_wbs_type','value'),
     Input('radio_wbsTop10','value'),
    Input('radio_wbsTop10_filter','value'),
     ]
)
def update_wbsType_top10(year, month, wbsType, barPie, wbsName):
    data = cleanMY(历史底表, year, month)
    data = data[data['WBS类型'].isin(wbsType)].reset_index(drop=True)
    if barPie == 'Bar':
        if wbsName == '项目名称':
            return figWBS部门Top(groupByWBS(data), month)
    # elif barPie == "Pie":
    #     return figWBStop填报分布Filter(wbs_top_distributionFilter(groupByWBS(data)), month)




@app.callback(
    Output("员工所属部门汇总-summary", "figure"),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def update_summary_bar(year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    return fig资源池byFilterP(staff_groupBy_table(cleanDF员工部门(data, name), "资源池"),month)



@app.callback(
    Output("员工所属部门汇总-bar", "figure"),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def update_summary_bar(year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    return fig资源池人均人天byFilterP(staff_groupBy_table(cleanDF员工部门(data, name), "资源池"), month)


@app.callback(
    Output("业务线汇总-pie", "figure"),
    [Input('radio_历史WBS类型','value'),
    Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def update_summary_bar(radioChoice, year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    if radioChoice == "员工组":
        return fig业务线pieBL(wbs员工组pie细分Quick(staff_groupBy_table(data, "员工组"), "员工组"), month, "员工组")
    elif radioChoice == "资源池":
        return fig业务线pieBL(wbs员工组pie细分Quick(staff_groupBy_table(data, "资源池"), "资源池"), month, "资源池")
    elif radioChoice == "岗位名称":
        return fig业务线pieBL(wbs员工组pie细分Quick(staff_groupBy_table(data, "岗位名称"), "岗位名称"), month, "岗位名称")




@app.callback([Output('range-slider实际vs预估',  'min'),
               Output('range-slider实际vs预估',  'max'),
               Output('range-slider实际vs预估',  'marks'),
               Output('range-slider实际vs预估', 'value'),],
              [Input('dropDown_工时year', 'value'),
               Input('dropDown_工时month', 'value')])
def update_slider_est(year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    min, max = data.预估填报率.min(), data.预估填报率.max()
    marks = {
        min: {
            'label': str(min)+'%',
            'style': {'color': 'orange'}},
        80: {'label': '80%', 'style': {'color': 'green'}},
        120: {'label': '120%', 'style': {'color': 'green'}},
        max: {
            'label': str(max)+'%',
            'style': {'color': 'red'}}
    }
    new_value = [min, max]
    return min, max, marks, new_value


@app.callback([Output('range-slider实际vs理论',  'min'),
               Output('range-slider实际vs理论',  'max'),
               Output('range-slider实际vs理论',  'marks'),
               Output('range-slider实际vs理论', 'value')],
              [Input('dropDown_工时year', 'value'),
               Input('dropDown_工时month', 'value')])
def update_slider_act(year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    min, max = data.理论填报率.min(), data.理论填报率.max()
    marks = {
        min: {
            'label': str(min)+'%',
            'style': {'color': 'orange'}},
        80: {'label': '80%', 'style': {'color': 'green'}},
        120: {'label': '120%', 'style': {'color': 'green'}},
        max: {
            'label': str(max)+'%',
            'style': {'color': 'red'}}
    }
    new_value = [min, max]
    return min, max, marks, new_value



@app.callback(
    Output("fig全量实际vs预估人天-scatter", "figure"),
    [Input("range-slider实际vs预估", "value"),
    Input('dropDown_工时year', 'value'),
    Input('dropDown_工时month', 'value')])
def update_bar_chart2(slider_range, year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    low, high = slider_range
    mask = (data.预估填报率 >= low) & (data.预估填报率 <= high)
    fig = px.scatter(data[mask],
                     title=str(month)+'月员工"实际人天"v."预估人天"',
                     x="实际人天", y="预估人天",
                     color="资源池", size="实际人天", hover_data=['员工姓名', '员工组', '资源池', '岗位名称'])
    return fig



@app.callback(
    Output("fig全量实际vs理论人天-scatter", "figure"),
    [Input("range-slider实际vs理论", "value"),
    Input('dropDown_工时year', 'value'),
    Input('dropDown_工时month', 'value')])
def update_bar_chart4(slider_range, year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    low, high = slider_range
    mask = (data.理论填报率 >= low) & (data.理论填报率 <= high)
    fig = px.scatter(data[mask],
                     title=str(month)+'月员工"实际人天"v."理论人天"',
                     x="实际人天", y="理论人天",
                     color="资源池", size="实际人天", hover_data=['员工姓名', '员工组', '资源池', '岗位名称'])
    return fig





@app.callback(
    [Output("historical_days", "figure"),
     Output("historical_wbs_days", "figure"),
     Output('staffNameRemind', 'children'),
     Output('sameDaysWithStaff', 'children'),
     Output('sameDaysWithStaff2', 'children')],
    [Input('input_userName', 'value'),
     Input('fig全量实际vs理论人天-scatter', 'clickData'),
     Input('fig全量实际vs预估人天-scatter', 'clickData'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def update_outputLogic(input_userName, clickDatalogic, clickDataestim, year, month):
    ctx = dash.callback_context
    click_id = ctx.triggered[0]['prop_id'].split('.')[0]
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    try:
        if click_id == 'fig全量实际vs预估人天-scatter':
            user = clickDataestim['points'][0]['customdata'][0]
            actDays = clickDataestim['points'][0]['x']
            estDays = clickDataestim['points'][0]['y']
            temp = data[data['实际人天'] == actDays]
            temp = temp[temp['预估人天'] == estDays].copy().reset_index(drop=True)
            sameDaysStaff = list(set(temp['员工姓名']))
            if len(sameDaysStaff) > 1:
                sameDaysStaff.remove(user)
                sameDaysStaff = str(month)+'"月工时的实际人天"和"预估人天" 与【{}】 一致的员工有： '.format(user) + str(sameDaysStaff)
                sameDaysStaff2 = ""
            else:
                sameDaysStaff = str(month)+"月工时没有其他员工与 【{}】 一致".format(user)
                sameDaysStaff2 = ""

        elif click_id == 'fig全量实际vs理论人天-scatter':
            user = clickDatalogic['points'][0]['customdata'][0]
            actDays = clickDatalogic['points'][0]['x']
            logicDays = clickDatalogic['points'][0]['y']
            temp = data[data['实际人天'] == int(actDays)]
            temp = temp[temp['理论人天'] == int(logicDays)].copy().reset_index(drop=True)
            sameDaysStaff2 = list(set(temp['员工姓名']))
            if len(sameDaysStaff2) > 1:
                sameDaysStaff2.remove(user)
                sameDaysStaff2 = str(month)+'"月工时的实际人天"和"理论人天" 与【{}】一致的员工有： '.format(user) + str(sameDaysStaff2)
                sameDaysStaff = ""
            else:
                sameDaysStaff2 = str(month)+"月工时没有其他员工与 【{}】 一致".format(user)
                sameDaysStaff = ""

        elif len(input_userName) > 0:
            user = input_userName
            sameDaysStaff = ""
            sameDaysStaff2 = ""

        data1 = getCertainUserDays(历史人员维度, user).reset_index(drop=True)
        for i in range(len(data1)):
            data1.loc[i, '工时月份'] = str(data1.loc[i, '工时年份']) + '年' + str(data1.loc[i, '工时月份']) + '月'
        figure = fig员工历史人天(data1)
        staff_apartment = data1['员工所属部门'][0]
        staff_title = data1['岗位名称'][0]
        staff_res = data1['资源池'][0]
        staff_type = data1['员工组'][0]

        data2 = getCertainUserWBS(历史底表, user).reset_index(drop=True)
        for i in range(len(data2)):
            data2.loc[i, '工时月份'] = str(data2.loc[i, '工时年份']) + '年' + str(data2.loc[i, '工时月份']) + '月'
        figure2 = fig员工历史wbs人天(data2)
        return figure, figure2, '{} ( 部门：{}-{}，岗位：{}-{} ) 的历史工时如下'.format(user, staff_apartment, staff_type,
                                                                                     staff_res,
                                                                                     staff_title), sameDaysStaff, sameDaysStaff2
    except:
        user = None
        figure = go.Figure()
        figure2 = go.Figure()
        return figure, figure2, '{} 员工不存在 or 姓名输入错误 or 该员工没有数据！'.format(user), "", ""



@app.callback(
    Output('历史WBS类型-pie', 'figure'),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_graph_pie_wbs(year, month):
    data = 历史底表[历史底表['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    return figWBSTypepie细分(groupByWBS(data), month)


@app.callback(
    Output('WBS部门Top5-bar', 'figure'),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_graph_bar_top10wbs(year, month):
    data = 历史底表[历史底表['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    return figWBS部门Top(groupByWBS(data), month)



@app.callback(
    Output('WBS实际人天Top5-pie', 'figure'),
    [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_graph_pie_wbs(year, month):
    data = 历史底表[历史底表['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    return figWBStop填报分布Filter(wbs_top_distributionFilter(groupByWBS(data)), month)



@app.callback(
    Output('graph_产品线工时投入', 'figure'),
    [Input(component_id='radio_产品线工时投入', component_property='value'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_graph_bl_wl(attri, year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)

    if attri == 'graph_员工组人天':
        return fig员工部门员工组资源池细分BL(data, name, month)
    elif attri == 'graph_岗位名称人天':
        return fig员工部门岗位名称资源池细分BL(data, name, month)



@app.callback(
    [Output('填报工时人员明细', 'children'),
    Output('cur_mon_staff_detailed', 'data')],
     [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def table_all_staff(year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    strP = str(month)+'月工时填报人员明细（按实际人天倒序排序）'
    data = data.iloc[:, 0:-4].sort_values(by=['实际人天']).reset_index(drop=True)
    return strP, data.to_dict('records')


@app.callback(
    [Output('非正常工作日填报', 'children'),
    Output('非正常工作日填报table', 'data')],
     [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def table_not_fill_staff(year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    strP = str(month) + '月非正常工作日填报工时人数 (以"员工工作地点"与"行政放假安排"判定是否为当地工作日): ' + str(len(cleanDF员工部门(not_fill_wh(data, year, month), name)))
    df = cleanDF员工部门(not_fill_wh(data, year, month), name)
    return strP, df.to_dict('records')


@app.callback(
    [Output('未工时填报', 'children'),
    Output('未工时填报table', 'data')],
     [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def table_not_fill_staff(year, month):
    data = 历史未填工时[历史未填工时['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    strP = str(month) + '月未填报工时人数 : ' + str(len(data))
    return strP, data.to_dict('records')

@app.callback(
    [Output('入离职名单', 'children'),
    Output('入离职名单table', 'data')],
     [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def table_staff_in_out(year, month):
    staff_in_out = cleanDF员工部门(readhistroyData(工时历史总表汇总(), '入离职名单'), name)
    data = staff_in_out[staff_in_out['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    data['时间'] = pd.to_datetime(data['时间']).dt.date
    strP = str(month) + '月入离职人数 : ' + str(len(data))
    return strP, data.iloc[:, 0:-2].to_dict('records')


@app.callback(
    [Output('本月填报全部WBS', 'children'),
    Output('本月填报全部WBStable', 'data')],
     [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def table_not_PL11_wbs(year, month):
    data = 历史底表[历史底表['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)
    data = data[data['WBS类型'] != "Z"].reset_index(drop=True)
    data = groupByWBS(data)
    strP = str(month) + '月本月填报全部WBS（按照实际人天倒序排序) : ' + str(len(list(set(list(data['项目名称']))))) +'个项目'
    return strP, data.to_dict('records')





@app.callback(
    [Output('未PL111工时', 'children'),
    Output('未PL111工时table', 'data')],
     [Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def table_not_PL11_wbs(year, month):
    data = cleanDF员工部门(notPL111wbsTypeFilterBL(name, year, month).iloc[:, 0:-4].sort_values(by=['实际人天'],ascending=False).reset_index(drop=True),name)
    data = data[data['WBS类型'] != "Z"].reset_index(drop=True)
    strP = str(month) + '月非PL111WBS的工时投入明细（按照实际人天倒序排序) : ' + str(len(list(set(list(data['员工姓名']))))) +'人，'+ str(len(list(set(list(data['项目名称']))))) +'个项目'
    return strP, data.to_dict('records')



@app.callback(
    Output('table_产品线工时投入', 'data'),
    [Input(component_id='radio_产品线工时投入', component_property='value'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_table_bl_wl2(attri, year, month):
    data = 历史人员维度[历史人员维度['工时年份'] == year].reset_index(drop=True)
    data = data[data['工时月份'] == month].reset_index(drop=True)

    if attri == 'graph_员工组人天':
        return df0Beautfy(groupByWl(data,
                                    {'业务开发资源池': [],
                                     '架构平台资源池': [],
                                     '测试运维资源池': [],
                                     '算法SDK资源池': [],
                                     '非资源池': []},
                                    ['正式员工', '外包员工', '实习生'],
                                    '资源池', '员工组')).to_dict('records')
    elif attri == 'graph_岗位名称人天':
        return df0Beautfy(groupByWl(data,
                                    {'业务开发资源池': [],
                                     '架构平台资源池': [],
                                     '测试运维资源池': [],
                                     '算法SDK资源池': [],
                                     '非资源池': []},
                                    ['前端开发','后端开发','平台开发','架构师','DevOps' ,'测试',
                                     '算法开发','算法研究','产品管理','项目管理','UI设计','RPL','产品方案'],
                                    '资源池', '岗位名称')).to_dict('records')




@app.callback(
    Output('table_历史wbs工时投入', 'data'),
    Input('dropDown_wbs名称', 'value')
)
def build_table_wbs_historical_days(value):
    data = 历史底表
    data = data[data['资源池'] != 0]
    data = data[data['实际人天'] > 0]
    data = data[data['员工所属部门'] == name]
    return data[data['项目名称'] == value].reset_index(drop=True).to_dict('records')


@app.callback(
    Output('graph_产品线wbsD工时投入', 'figure'),
    [Input('dropDown_wbs类型', 'value'),
     Input(component_id='radio_产品线wbsD工时投入', component_property='value'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_WBSgraph_bl_wl(WBStype, attri, year, month):
    data = 历史底表
    if attri == 'graph_wbs员工组人天':
        data = wbsTypeFilterBL(data, list(WBStype),name, year, month)
        return fig员工部门不同维度wbs2(对比部门汇总2BL(data, '实际人天', "员工组"), "员工组",
                                      str(month)+'月资源池员工组投入' + WBStype + '类WBS实际人天', '资源池')
    elif attri == 'graph_wbs岗位名称人天':
        data = wbsTypeFilterBL(data, list(WBStype),name, year, month)
        return fig员工部门不同维度wbs2(对比部门汇总2BL(data, '实际人天', "岗位名称"), "岗位名称",
                                      str(month)+'月资源池岗位名称投入' + WBStype + '类WBS实际人天', '资源池')
    elif attri == 'graph_wbs员工姓名人天':
        data = wbsTypeFilterBL(data, list(WBStype),name, year, month)
        return fig员工部门不同维度wbs2(对比部门汇总2BL(data, '实际人天', "员工姓名"), "员工姓名",
                                      str(month)+'月资源池员工姓名投入' + WBStype + '类WBS实际人天', '资源池')
    elif attri == 'graph_wbsWBS部门人天':
        data = wbsTypeFilterBL(data, list(WBStype),name, year, month)
        return fig员工部门不同维度wbs2(对比部门汇总2BL(data, '实际人天', "WBS所属部门"), "WBS所属部门",
                                      str(month)+'月资源池WBS部门投入' + WBStype + '类WBS实际人天', '资源池')


@app.callback(
    Output('graph_产品线wbsX工时投入', 'figure'),
    [Input(component_id='radio_产品线wbsX工时投入', component_property='value'),
     Input('dropDown_工时year', 'value'),
     Input('dropDown_工时month', 'value')]
)
def build_WBSgraphX_bl_wl(attri,year, month):
    if attri == 'graph_wbsX员工组人天':
        return fig员工部门不同维度wbs2(对比部门汇总2BL(notPL111wbsTypeFilterBL(name,year, month), '实际人天', "员工组"), "员工组",
                                      str(month)+'月资源池员工组投入非PL111WBS实际人天', '资源池')
    elif attri == 'graph_wbsX岗位名称人天':
        return fig员工部门不同维度wbs2(对比部门汇总2BL(notPL111wbsTypeFilterBL(name,year, month), '实际人天', "岗位名称"), "岗位名称",
                                      str(month)+'月资源池岗位名称投入非PL111WBS实际人天', '资源池')
    elif attri == 'graph_wbsX员工姓名人天':
        return fig员工部门不同维度wbs2(对比部门汇总2BL(notPL111wbsTypeFilterBL(name,year, month), '实际人天', "员工姓名"), "员工姓名",
                                      str(month)+'月资源池员工姓名投入非PL111WBS实际人天', '资源池')
    elif attri == 'graph_wbsXWBS部门人天':
        return fig员工部门不同维度wbs2(对比部门汇总2BL(notPL111wbsTypeFilterBL(name,year, month), '实际人天', "WBS所属部门"), "WBS所属部门",
                                      str(month)+'月资源池WBS部门投入非PL111WBS实际人天', '资源池')


@app.callback(
    [Output('dropDown_利润中心wbs部门', 'options'),
     Output('dropDown_利润中心wbs部门', 'value')],
    [Input('dropDown_wbs_type_wbsFilter', 'value')]
)
def buildWbsNameListFirst(wbsType):
    data = 历史底表
    data= data[data['WBS类型'].isin(wbsType)].reset_index(drop=True)
    data = data[data['员工所属部门'] == name].reset_index(drop=True)
    opts = list(set(data['WBS所属部门']))
    options = [{'label': opt, 'value': opt} for opt in opts]
    value = opts[0]
    return options, value



@app.callback(
    [Output('dropDown_wbs名称', 'options'),
     Output('dropDown_wbs名称', 'value')],
    [Input('dropDown_wbs_type_wbsFilter', 'value'),
     Input('dropDown_利润中心wbs部门', 'value')]
)
def buildWbsNameListSecond(wbsType, value):
    data = 历史底表
    data= data[data['WBS类型'].isin(wbsType)].reset_index(drop=True)
    data = data[data['WBS所属部门'] == value].reset_index(drop=True)
    data = data[data['员工所属部门'] == name].reset_index(drop=True)
    opts = list(set(data['项目名称']))
    options = [{'label': opt, 'value': opt} for opt in opts]
    value = opts[0]
    return options, value

#
# @app.callback(
#     Output('wbsHistorical_days', 'figure'),
#     [Input('dropDown_wbs名称', 'value'),
#      Input(component_id='radio_资源池岗位名称员工姓名', component_property='value')]
# )
# def build_wbsGraph(wbsName, groupByValue):
#     data = getCertainWBSFilter(历史底表, wbsName).reset_index(drop=True)
#     data = data[data['资源池'] == name]
#     groupBy = groupByValue
#     for i in range(len(data)):
#         data.loc[i, '工时月份'] = str(data.loc[i, '工时年份']) + '年' + str(data.loc[i, '工时月份']) + '月'
#     figure = fig历史wbs人天(data, groupBy)
#     return figure


@app.callback(
    Output('wbsHistorical_days', 'figure'),
    [Input('dropDown_wbs名称', 'value'),
     Input(component_id='radio_资源池岗位名称员工姓名', component_property='value')]
)
def build_wbsGraphWBS(wbsName, groupByValue):
    data = getCertainWBS(历史底表, wbsName).reset_index(drop=True)
    groupBy = groupByValue
    for i in range(len(data)):
        data.loc[i, '工时月份'] = str(data.loc[i, '工时年份']) + '年' + str(data.loc[i, '工时月份']) + '月'
    return fig历史wbs人天(data, groupBy)



@app.callback(
    Output('graph_gpu_use', 'figure'),
    [Input(component_id='radio_gpu_filter', component_property='value'),
     Input(component_id='radio_gpu_use', component_property='value')]
)
def build_graph_gpu_use(radio_gpu_filter, value_gpu_use):
    if radio_gpu_filter == '使用率':
        if value_gpu_use == 'graph_gpu_avg':
            return fig历史gpu使用(clean_gpu_avg_usage(), "日期", '使用率', 'GPU历史使用率', '分区')
        if value_gpu_use == 'graph_gpu_10':
            return fig历史gpu使用具体时间点(历史GPU使用情况(), 10, "日期", '使用率', 'GPU历史使用率')
        if value_gpu_use == 'graph_gpu_14':
            return fig历史gpu使用具体时间点(历史GPU使用情况(), 14, "日期", '使用率', 'GPU历史使用率')
        if value_gpu_use == 'graph_gpu_18':
            return fig历史gpu使用具体时间点(历史GPU使用情况(), 18, "日期", '使用率', 'GPU历史使用率')
        if value_gpu_use == 'graph_gpu_22':
            return fig历史gpu使用具体时间点(历史GPU使用情况(), 22, "日期", '使用率', 'GPU历史使用率')

    elif radio_gpu_filter == '累计使用节点':
        if value_gpu_use == 'graph_gpu_avg':
            return fig历史gpu使用(gpu_avg_sum_nodes(历史GPU用户使用情况()), '日期', '使用节点数', 'GPU累计使用节点数',
                                  '分区')
        if value_gpu_use == 'graph_gpu_10':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 10, '日期', '使用节点数', 'GPU累计使用节点数')
        if value_gpu_use == 'graph_gpu_14':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 14, '日期', '使用节点数', 'GPU累计使用节点数')
        if value_gpu_use == 'graph_gpu_18':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 18, '日期', '使用节点数', 'GPU累计使用节点数')
        if value_gpu_use == 'graph_gpu_22':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 22, '日期', '使用节点数', 'GPU累计使用节点数')

    elif radio_gpu_filter == '累计使用时长':
        if value_gpu_use == 'graph_gpu_avg':
            return fig历史gpu使用(gpu_avg_sum_time(历史GPU用户使用情况()), '日期', '累计使用时长',
                                  'GPU累计使用时长(小时)', '分区')
        if value_gpu_use == 'graph_gpu_10':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 10, '日期', '累计使用时长', 'GPU累计使用时长(小时)')
        if value_gpu_use == 'graph_gpu_14':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 14, '日期', '累计使用时长', 'GPU累计使用时长(小时)')
        if value_gpu_use == 'graph_gpu_18':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 18, '日期', '累计使用时长', 'GPU累计使用时长(小时)')
        if value_gpu_use == 'graph_gpu_22':
            return fig历史gpu使用具体时间点(历史GPU用户使用情况(), 22, '日期', '累计使用时长', 'GPU累计使用时长(小时)')


@app.callback(
    Output('graph_使用率月份', 'figure'),
    [Input('dropDown_gpu_util', 'value'),
     Input(component_id='radio_使用率月份', component_property='value')]
)
def build_WBSgraph_bl_wl3(type, attri):
    if attri == 'graph_gpu员工所属部门util':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpuRelative(对比分区gpu0(data, '使用节点数', "员工所属部门", fee, "总使用节点数", '使用率'), "员工所属部门",
                                      str(type) + '月gpu使用率',"使用率")
    elif attri == 'graph_gpu员工组util':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpuRelative(对比分区gpu0(data, '使用节点数', "员工组", fee, "总使用节点数", '使用率'), "员工组",
                                      str(type) + '月gpu使用率',"使用率")
    elif attri == 'graph_gpu岗位名称util':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpuRelative(对比分区gpu0(data, '使用节点数', "岗位名称", fee, "总使用节点数", '使用率'), "岗位名称",
                                      str(type) + '月gpu使用率',"使用率")
    elif attri == 'graph_gpu员工姓名util':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpuRelative(对比分区gpu0(data, '使用节点数', "用户", fee, "总使用节点数", '使用率'), "用户",
                                      str(type) + '月gpu使用率',"使用率")


@app.callback(
    Output('graph_总费用月份', 'figure'),
    [Input('dropDown_gpu_fee', 'value'),
     Input(component_id='radio_总费用月份', component_property='value')]
)
def build_WBSgraph_bl_wl4(type, attri):
    if attri == 'graph_gpu员工所属部门fee':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu0(data, '使用节点数', "员工所属部门", fee, "总使用节点数", '费用'), "员工所属部门",
                                      str(type) + '月gpu总费用',"费用")
    elif attri == 'graph_gpu员工组fee':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu0(data, '使用节点数', "员工组", fee, "总使用节点数", '费用'), "员工组",
                                      str(type) + '月gpu总费用',"费用")
    elif attri == 'graph_gpu岗位名称fee':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu0(data, '使用节点数', "岗位名称", fee, "总使用节点数", '费用'), "岗位名称",
                                      str(type) + '月gpu总费用',"费用")
    elif attri == 'graph_gpu员工姓名fee':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        fee = gpu费用[gpu费用['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu0(data, '使用节点数', "用户", fee, "总使用节点数", '费用'), "用户",
                                      str(type) + '月gpu总费用',"费用")


@app.callback(
    Output('graph_使用节点月份', 'figure'),
    [Input('dropDown_gpu_month', 'value'),
     Input(component_id='radio_使用节点月份', component_property='value')]
)
def build_WBSgraph_bl_wl_gpu(type, attri):
    if attri == 'graph_gpu员工所属部门':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu(data, '使用节点数', "员工所属部门", "总使用节点数"), "员工所属部门",
                                      str(type) + '月gpu总使用节点',"总使用节点数")
    elif attri == 'graph_gpu员工组':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu(data, '使用节点数', "员工组",  "总使用节点数"), "员工组",
                                      str(type) + '月gpu总使用节点',"总使用节点数")
    elif attri == 'graph_gpu岗位名称':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu(data, '使用节点数', "岗位名称", "总使用节点数"), "岗位名称",
                                      str(type) + '月gpu总使用节点',"总使用节点数")
    elif attri == 'graph_gpu员工姓名':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu(data, '使用节点数', "用户",  "总使用节点数"), "用户",
                                      str(type) + '月gpu总使用节点',"总使用节点数")


@app.callback(
    Output('graph_累计时长月份', 'figure'),
    [Input('dropDown_gpu_month2', 'value'),
     Input(component_id='radio_累计时长月份', component_property='value')]
)
def build_WBSgraph_bl_wl2_gpu(type, attri):
    if attri == 'graph_gpu员工所属部门2':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu2(data, '累计使用时长', "员工所属部门","总累计时长"), "员工所属部门",
                                       str(type) + '月gpu总累计时长',"总累计时长")
    elif attri == 'graph_gpu员工组2':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu2(data, '累计使用时长', "员工组", "总累计时长"), "员工组",
                                       str(type) + '月gpu总累计时长',"总累计时长")
    elif attri == 'graph_gpu岗位名称2':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu2(data, '累计使用时长', "岗位名称", "总累计时长"), "岗位名称",
                                       str(type) + '月gpu总累计时长',"总累计时长")
    elif attri == 'graph_gpu员工姓名2':
        data = gpu底表[gpu底表['month'] == type].reset_index(drop=True)
        return fig集群分区不同维度gpu(对比分区gpu2(data, '累计使用时长', "用户", "总累计时长"), "用户",
                                       str(type) + '月gpu总累计时长',"总累计时长")


@app.callback(
    Output('graph_gpu_user_use', 'figure'),
    [Input('dropDown_gpu_user_filter', 'value'),
    Input(component_id='radio_gpu_user_filter', component_property='value')]
)
def build_graph_gpu_user_user(dropdown, value):
    if value == '累计使用节点':
        return fig历史gpu使用(clean_gpu_user(dropdown), "日期", '使用节点数', '历史用户累计使用节点', '用户')
    elif value == '累计使用时长':
        return fig历史gpu使用(clean_gpu_user(dropdown), "日期", '累计使用时长', '历史用户累计使用时长', '用户')


# @app.callback(
#     Output('graph_历史gpu费用', 'figure'),
#     Input(component_id='radio_历史gpu费用', component_property='value')
# )
# def build_gpu_fee(type):
#     if type == '总费用':
#         return fig历史gpu(历史GPU费用(), '费用(元)')
#     elif type == '总卡数':
#         return fig历史gpu(历史GPU卡数(), '卡数')



@app.callback(
    Output('graph_折旧固定资产员工部门', 'figure'),
    [Input('dropDown_固定资产_fee','value'),
    Input(component_id='radio_固定资产金额类型', component_property='value'),
    Input(component_id='radio_折旧固定资产type', component_property='value'),
     Input(component_id='radio_折旧固定资产全选项', component_property='value'),]
)
def build_gpu_detailedBar折旧(month, valueType, type, allChoice):
    data = 历史固定资产[历史固定资产['资产月份'] == month].reset_index(drop=True)
    if valueType == '折旧':
        if type == '办公':
            data = data[data['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资源池'), '资源池', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月员工部门办公资产'+valueType, '总金额')
        elif type == '项目':
            data = data[data['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资源池'), '资源池', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月员工部门项目资产'+valueType, '总金额')

    elif valueType == '净值':
        if type == '办公':
            data = data[data['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资源池'), '资源池', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月员工部门办公资产'+valueType, '总金额')
        elif type == '项目':
            data = data[data['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资源池'), '资源池', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月员工部门项目资产'+valueType, '总金额')

    elif valueType == '总值':
        if type == '办公':
            data = data[data['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资源池'), '资源池', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月员工部门办公资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月员工部门办公资产'+valueType, '总金额')
        elif type == '项目':
            data = data[data['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '资源池'), '资源池', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月员工部门项目资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门(对比部门汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月员工部门项目资产'+valueType, '总金额')


@app.callback(
    Output('graph_折旧固定资产员工部门2', 'figure'),
    [Input('dropDown_固定资产_fee2', 'value'),
    Input(component_id='radio_固定资产金额类型2', component_property='value'),
    Input(component_id='radio_折旧固定资产type2', component_property='value'),
     Input(component_id='radio_折旧固定资产全选项2', component_property='value'),]
)
def build_gpu_detailedBar折旧2(month, valueType, type, allChoice):
    data = 历史固定资产[历史固定资产['资产月份'] == month].reset_index(drop=True)
    if valueType == '折旧':
        if type == '办公':
            data = data[data['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工所属部门'), '员工所属部门', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月资源池办公资产'+valueType, '总金额')
        elif type == '项目':
            data = data[data['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工所属部门'), '员工所属部门', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月资源池项目资产'+valueType, '总金额')

    elif valueType == '净值':
        if type == '办公':
            data = data[data['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工所属部门'), '员工所属部门', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月资源池办公资产'+valueType, '总金额')
        elif type == '项目':
            data = data[data['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工所属部门'), '员工所属部门', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月资源池项目资产'+valueType, '总金额')

    elif valueType == '总值':
        if type == '办公':
            data = data[data['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工所属部门'), '员工所属部门', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月资源池办公资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月资源池办公资产'+valueType, '总金额')
        elif type == '项目':
            data = data[data['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '设备类型'), '设备类型', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '资产状态'), '资产状态', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工组'), '员工组', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '员工所属部门'), '员工所属部门', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '岗位名称'), '岗位名称', str(month)+'月资源池项目资产'+valueType, '总金额')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, valueType, '实际保管人'), '实际保管人', str(month)+'月资源池项目资产'+valueType, '总金额')





@app.callback(
    Output('graph_折旧固定资产员工部门数量', 'figure'),
    [Input(component_id='radio_固定资产数量', component_property='value'),
    Input(component_id='radio_折旧固定资产type数量', component_property='value'),
     Input(component_id='radio_折旧固定资产全选项数量', component_property='value'),]
)
def build_gpu_detailedBar折旧数量(valueType, type, allChoice):
    if valueType == '折旧中':
        if type == '办公':
            data = 本月固定资产[(本月固定资产['用途'] == '办公') & (本月固定资产['折旧'] > 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月折旧中员工部门办公资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧中员工部门办公资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月折旧中员工部门办公资产个数', '总个数')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资源池'), '资源池', '本月折旧中员工部门办公资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月折旧中员工部门办公资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月折旧中员工部门办公资产个数', '总个数')
        elif type == '项目':
            data = 本月固定资产[(本月固定资产['用途'] == '项目') & (本月固定资产['折旧'] > 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月折旧中员工部门项目资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧中员工部门项目资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月折旧中员工部门项目资产个数', '总个数')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资源池'), '资源池', '本月折旧中员工部门项目资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月折旧中员工部门项目资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月折旧中员工部门项目资产个数', '总个数')

    elif valueType == '折旧完':
        if type == '办公':
            data = 本月固定资产[(本月固定资产['用途'] == '办公') & (本月固定资产['折旧'] == 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月折旧完员工部门办公资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧完员工部门办公资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月折旧完员工部门办公资产个数', '总个数')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资源池'), '资源池', '本月折旧完员工部门办公资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月折旧完员工部门办公资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月折旧完员工部门办公资产个数', '总个数')
        elif type == '项目':
            data = 本月固定资产[(本月固定资产['用途'] == '项目') & (本月固定资产['折旧'] == 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月折旧完员工部门项目资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧完员工部门项目资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月折旧完员工部门项目资产个数', '总个数')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资源池'), '资源池', '本月折旧完员工部门项目资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月折旧完员工部门项目资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月折旧完员工部门项目资产个数', '总个数')

    elif valueType == '折旧中&折旧完':
        if type == '办公':
            data = 本月固定资产[本月固定资产['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月员工部门办公总资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月员工部门办公总资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月员工部门办公总资产个数', '总个数')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资源池'), '资源池', '本月员工部门办公总资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月员工部门办公总资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月员工部门办公总资产个数', '总个数')
        elif type == '项目':
            data = 本月固定资产[本月固定资产['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月员工部门项目总资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月员工部门项目总资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月员工部门项目总资产个数', '总个数')
            if allChoice == '资源池':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '资源池'), '资源池', '本月员工部门项目总资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月员工部门项目总资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同员工部门数量(对比部门汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月员工部门项目总资产个数', '总个数')


@app.callback(
    Output('graph_折旧固定资产员工部门数量2', 'figure'),
    [Input(component_id='radio_固定资产数量2', component_property='value'),
    Input(component_id='radio_折旧固定资产type数量2', component_property='value'),
     Input(component_id='radio_折旧固定资产全选项数量2', component_property='value'),]
)
def build_gpu_detailedBar折旧2数量(valueType, type, allChoice):
    if valueType == '折旧中':
        if type == '办公':
            data = 本月固定资产[(本月固定资产['用途'] == '办公') & (本月固定资产['折旧'] > 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月折旧中资源池办公资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧中资源池办公资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月折旧中资源池办公资产个数', '总个数')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工所属部门'), '员工所属部门','本月折旧中资源池办公资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月折旧中资源池办公资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月折旧中资源池办公资产个数', '总个数')
        elif type == '项目':
            data = 本月固定资产[(本月固定资产['用途'] == '项目') & (本月固定资产['折旧'] > 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月折旧中资源池项目资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧中资源池项目资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月折旧中资源池项目资产个数', '总个数')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工所属部门'), '员工所属部门',  '本月折旧中资源池项目资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月折旧中资源池项目资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月折旧中资源池项目资产个数', '总个数')

    elif valueType == '折旧中&折旧完':
        if type == '办公':
            data = 本月固定资产[本月固定资产['用途'] == '办公'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月资源池办公总资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月资源池办公总资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月资源池办公总资产个数', '总个数')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工所属部门'), '员工所属部门', '本月资源池办公总资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月资源池办公总资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月资源池办公总资产个数', '总个数')
        elif type == '项目':
            data = 本月固定资产[本月固定资产['用途'] == '项目'].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型','本月资源池项目总资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月资源池项目总资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工组'), '员工组', '本月资源池项目总资产个数', '总个数')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工所属部门'), '员工所属部门', '本月资源池项目总资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月资源池项目总资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月资源池项目总资产个数', '总个数')

    elif valueType == '折旧完':
        if type == '办公':
            data = 本月固定资产[(本月固定资产['用途'] == '办公') & (本月固定资产['折旧'] == 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型', '本月折旧完资源池办公资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧完资源池办公资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工组'), '员工组','本月折旧完资源池办公资产个数', '总个数')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工所属部门'), '员工所属部门', '本月折旧完资源池办公资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称','本月折旧完资源池办公资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人','本月折旧完资源池办公资产个数', '总个数')
        elif type == '项目':
            data = 本月固定资产[(本月固定资产['用途'] == '项目') & (本月固定资产['折旧'] == 0)].reset_index(drop=True)
            if allChoice == '设备类型':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '设备类型'), '设备类型','本月折旧完资源池项目资产个数', '总个数')
            if allChoice == '资产状态':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '资产状态'), '资产状态', '本月折旧完资源池项目资产个数', '总个数')
            if allChoice == '员工组':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工组'), '员工组','本月折旧完资源池项目资产个数', '总个数')
            if allChoice == '员工所属部门':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '员工所属部门'), '员工所属部门', '本月折旧完资源池项目资产个数', '总个数')
            if allChoice == '岗位名称':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '岗位名称'), '岗位名称', '本月折旧完资源池项目资产个数', '总个数')
            if allChoice == '员工姓名':
                return fig固定资产detail不同资源池数量(对比资源池汇总固定资产数量(data, '资产代码', '实际保管人'), '实际保管人', '本月折旧完资源池项目资产个数', '总个数')



@app.callback(
    Output('graph_历史固定资产', 'figure'),
    [Input(component_id='radio_历史固定资产', component_property='value'),
     Input(component_id='radio_历史固定资产人均', component_property='value')]
)
def build_graph_固定资产(type, totalAvg):
    data = 历史固定资产总值()
    if type == 'graph_历史固定资产办公':
        if totalAvg == 'graph_历史固定资产Total':
            return fig历史固定资产金额(data, "办公", 'Total')
        if totalAvg == 'graph_历史固定资产Avg':
            return fig历史固定资产金额(data, "办公", 'Avg')

    elif type == 'graph_历史固定资产项目':
        if totalAvg == 'graph_历史固定资产Total':
            return fig历史固定资产金额(data, "项目", 'Total')
        if totalAvg == 'graph_历史固定资产Avg':
            return fig历史固定资产金额(data, "项目", 'Avg')




@app.callback(
    Output('固定资产汇总员工部门-bar', 'figure'),
    Input(component_id='radio_固定资产汇总员工部门', component_property='value'),
)
def build_graph_固定资产2(type):
    if type == '办公':
        data = 本月固定资产[本月固定资产['用途'] == '办公']
        return fig资源池固定资产总值(data, '折旧', '折旧','净值','总值','资源池折旧平均' , '总')
    elif type == '项目':
        data = 本月固定资产[本月固定资产['用途'] == '项目']
        return fig资源池固定资产总值(data, '折旧', '折旧','净值','总值','资源池折旧平均' , '总')
    # if type == '办公':
    #     data = 本月固定资产[本月固定资产['用途'] == '办公']
    #     return fig员工所属门固定资产总值(data, '折旧', '折旧','净值','总值','部门折旧部门平均' , '总')
    # elif type == '项目':
    #     data = 本月固定资产[本月固定资产['用途'] == '项目']
    #     return fig员工所属门固定资产总值(data, '折旧', '折旧','净值','总值','部门折旧部门平均' , '总')



@app.callback(
    Output('固定资产汇总员工部门人均-bar', 'figure'),
    Input(component_id='radio_固定资产汇总员工部门人均', component_property='value'),
)
def build_graph_固定资产3(type):
    # if type == '办公':
    #     data = 本月固定资产[本月固定资产['用途'] == '办公']
    #     return fig员工所属门固定资产总值(data, '折旧人均', '折旧人均','净值人均','总值人均','部门折旧人均' ,'人均')
    # elif type == '项目':
    #     data = 本月固定资产[本月固定资产['用途'] == '项目']
    #     return fig员工所属门固定资产总值(data, '折旧人均', '折旧人均','净值人均','总值人均','部门折旧人均' ,'人均')
    if type == '办公':
        data = 本月固定资产[本月固定资产['用途'] == '办公']
        return fig资源池固定资产总值(data, '折旧人均', '折旧人均','净值人均','总值人均','资源池折旧人均' ,'人均')
    elif type == '项目':
        data = 本月固定资产[本月固定资产['用途'] == '项目']
        return fig资源池固定资产总值(data, '折旧人均', '折旧人均','净值人均','总值人均','资源池折旧人均' ,'人均')




@app.callback(
    Output('固定资产汇总资源池-bar', 'figure'),
    Input(component_id='radio_固定资产汇总资源池', component_property='value'),
)
def build_graph_固定资产资源池(type):
    if type == '办公':
        data = 本月固定资产[本月固定资产['用途'] == '办公']
        return fig资源池固定资产总值(data, '折旧', '折旧','净值','总值','资源池折旧平均' , '总')
    elif type == '项目':
        data = 本月固定资产[本月固定资产['用途'] == '项目']
        return fig资源池固定资产总值(data, '折旧', '折旧','净值','总值','资源池折旧平均' , '总')



@app.callback(
    Output('固定资产汇总资源池人均-bar', 'figure'),
    Input(component_id='radio_固定资产汇总资源池人均', component_property='value'),
)
def build_graph_固定资产资源池人均(type):
    if type == '办公':
        data = 本月固定资产[本月固定资产['用途'] == '办公']
        return fig资源池固定资产总值(data, '折旧人均', '折旧人均','净值人均','总值人均','资源池折旧人均' ,'人均')
    elif type == '项目':
        data = 本月固定资产[本月固定资产['用途'] == '项目']
        return fig资源池固定资产总值(data, '折旧人均', '折旧人均','净值人均','总值人均','资源池折旧人均' ,'人均')




@app.callback(
    Output('固定资产汇总-pie', 'figure'),
    Input(component_id='radio_固定资产汇总', component_property='value'),
)
def build_graph_固定资产资源池2(type):
    if type == '资源池':
        return fig固定资产资源池pie(本月固定资产)
    # elif type == '资源池':
    #     return fig固定资产资源池pie(本月固定资产)



@app.callback(
    [Output('graph_resTop10折旧', 'figure'),
    Output('table_resTop10折旧', 'data'),],
    Input(component_id='radio_resTop10折旧', component_property='value'),
)
def build_top10_折旧固定资产(type):
    if type =='graph_resTop10折旧办公':
        try:
            data = filterData(本月固定资产, '用途', '办公')
            data = data[data['折旧'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '折旧')
        except:
            data = filterData(本月固定资产, '用途', '办公')
            data = data[data['折旧'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '折旧')
        return fig资产Top10(data, '办公', '折旧'), data[['实际保管人','员工组','员工所属部门','资源池','岗位名称','设备类型','资产状态','用途','总值','净值','折旧']].to_dict('records')
    elif type == 'graph_resTop10折旧项目':
        try:
            data = filterData(本月固定资产, '用途', '项目')
            data = data[data['折旧'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '折旧')
        except:
            data = filterData(本月固定资产, '用途', '项目')
            data = data[data['折旧'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '折旧')
        return fig资产Top10(data, '项目', '折旧'), data[['实际保管人','员工组','员工所属部门','资源池','岗位名称','设备类型','资产状态','用途','总值','净值','折旧']].to_dict('records')



@app.callback(
    [Output('graph_resTop10净值', 'figure'),
    Output('table_resTop10净值', 'data'),],
    Input(component_id='radio_resTop10净值', component_property='value'),
)
def build_top10_净值固定资产(type):
    if type =='graph_resTop10净值办公':
        try:
            data = filterData(本月固定资产, '用途', '办公')
            data = data[data['净值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '净值')
        except:
            data = filterData(本月固定资产, '用途', '办公')
            data = data[data['净值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '净值')
        return fig资产Top10(data, '办公', '净值'), data[['实际保管人','员工组','员工所属部门','资源池','岗位名称','设备类型','资产状态','用途','总值','净值','折旧']].to_dict('records')
    elif type == 'graph_resTop10净值项目':
        try:
            data = filterData(本月固定资产, '用途', '项目')
            data = data[data['净值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '净值')
        except:
            data = filterData(本月固定资产, '用途', '项目')
            data = data[data['净值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '净值')
        return fig资产Top10(data, '项目', '净值'), data[['实际保管人','员工组','员工所属部门','资源池','岗位名称','设备类型','资产状态','用途','总值','净值','折旧']].to_dict('records')



@app.callback(
    [Output('graph_resTop10总值', 'figure'),
    Output('table_resTop10总值', 'data'),],
    Input(component_id='radio_resTop10总值', component_property='value'),
)
def build_top10_总值固定资产(type):
    if type =='graph_resTop10总值办公':
        try:
            data = filterData(本月固定资产, '用途', '办公')
            data = data[data['总值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '总值')
        except:
            data = filterData(本月固定资产, '用途', '办公')
            data = data[data['总值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '总值')
        return fig资产Top10(data, '办公', '总值'), data[['实际保管人','员工组','员工所属部门','资源池','岗位名称','设备类型','资产状态','用途','总值','净值','折旧']].to_dict('records')
    elif type == 'graph_resTop10总值项目':
        try:
            data = filterData(本月固定资产, '用途', '项目')
            data = data[data['总值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '总值')
        except:
            data = filterData(本月固定资产, '用途', '项目')
            data = data[data['总值'] > 0].reset_index(drop=True)
            data = 固定资产top10(data, '总值')
        return fig资产Top10(data, '项目', '总值'), data[['实际保管人','员工组','员工所属部门','资源池','岗位名称','设备类型','资产状态','用途','总值','净值','折旧']].to_dict('records')



@app.callback(
    Output('graph_总库存金额', 'figure'),
    [Input(component_id='radio_总库存金额', component_property='value'),
    Input(component_id='radio_总库存金额全选项', component_property='value'),]
)
def build_总库存金额(type, allChoice):
    if type == '借库':
        data = 历史总库存[历史总库存['借库数量'] >0].reset_index(drop=True)
        if allChoice == '业务线':
            return fig固定资产detail不同月(对比总库存固定资产(data, '借库余额（万）', '业务线'), '业务线', '历史总库存借库金额', '总金额', '金额占比', '资产月份')
        if allChoice == '类别':
            return fig固定资产detail不同月(对比总库存固定资产(data, '借库余额（万）', '类别'), '类别', '历史总库存借库金额', '总金额', '金额占比', '资产月份')
        if allChoice == '物料名称':
            return fig固定资产detail不同月(对比总库存固定资产(data, '借库余额（万）', '物料名称'), '物料名称', '历史总库存借库金额', '总金额', '金额占比', '资产月份')
        if allChoice == '库存天数区间':
            return fig固定资产detail不同月(对比总库存固定资产(data, '借库余额（万）', '库存天数区间'), '库存天数区间', '历史总库存借库金额', '总金额', '金额占比', '资产月份')

    elif type == '在库':
        data = 历史总库存[历史总库存['在库数量'] >0].reset_index(drop=True)
        if allChoice == '业务线':
            return fig固定资产detail不同月(对比总库存固定资产(data, '在库余额（万）', '业务线'), '业务线', '历史总库存在库金额', '总金额', '金额占比', '资产月份')
        if allChoice == '类别':
            return fig固定资产detail不同月(对比总库存固定资产(data, '在库余额（万）', '类别'), '类别', '历史总库存在库金额', '总金额', '金额占比', '资产月份')
        if allChoice == '物料名称':
            return fig固定资产detail不同月(对比总库存固定资产(data, '在库余额（万）', '物料名称'), '物料名称', '历史总库存在库金额', '总金额', '金额占比', '资产月份')
        if allChoice == '库存天数区间':
            return fig固定资产detail不同月(对比总库存固定资产(data, '在库余额（万）', '库存天数区间'), '库存天数区间', '历史总库存在库金额', '总金额', '金额占比', '资产月份')
        if allChoice == '年末预估逾期业绩核算金额（万）':
            return fig固定资产detail不同月(对比总库存固定资产(data, '年末预估逾期业绩核算金额（万）', '业务线'), '业务线',
                                           '在库年末预估逾期业绩核算金额', '总金额', '金额占比', '资产月份')





@app.callback(
    Output('graph_总库存个数', 'figure'),
    [Input(component_id='radio_总库存个数', component_property='value'),
    Input(component_id='radio_总库存个数全选项', component_property='value'),]
)
def build_总库存个数(type, allChoice):
    if type == '借库':
        data = 历史总库存[历史总库存['借库数量'] >0].reset_index(drop=True)
        if allChoice == '业务线':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '借库数量', '业务线'), '业务线', '历史总库存借库个数', '总个数', '个数占比', '资产月份')
        if allChoice == '类别':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '借库数量', '类别'), '类别', '历史总库存借库个数', '总个数', '个数占比', '资产月份')
        if allChoice == '物料名称':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '借库数量', '物料名称'), '物料名称', '历史总库存借库个数', '总个数', '个数占比', '资产月份')
        if allChoice == '库存天数区间':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '借库数量', '库存天数区间'), '库存天数区间', '历史总库存借库个数', '总个数', '个数占比', '资产月份')

    elif type == '在库':
        data = 历史总库存[历史总库存['在库数量'] >0].reset_index(drop=True)
        if allChoice == '业务线':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '在库数量', '业务线'), '业务线', '历史总库存在库个数', '总个数', '个数占比', '资产月份')
        if allChoice == '类别':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '在库数量', '类别'), '类别', '历史总库存在库个数', '总个数', '个数占比', '资产月份')
        if allChoice == '物料名称':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '在库数量', '物料名称'), '物料名称', '历史总库存在库个数', '总个数', '个数占比', '资产月份')
        if allChoice == '库存天数区间':
            return fig固定资产detail不同月(对比总库存固定资产数量(data, '在库数量', '库存天数区间'), '库存天数区间', '历史总库存在库个数', '总个数', '个数占比', '资产月份')








@app.callback(
    Output('dcp月环比-pie', 'figure'),
    Input(component_id='radio_dcp月环比', component_property='value'),
)
def build_graph_dcpPie(allchoice):
    dataLast = 上月dcp
    dataNew = 本月dcp
    if allchoice == '集群名称':
        return figDcppie(dataLast, '集群名称', dataNew, "部门DCP总费用占比-月度环比")
    if allchoice == '存储类型(SSD/HDD)':
        return figDcppie(dataLast, '存储类型(SSD/HDD)', dataNew, "部门DCP总费用占比-月度环比")
    if allchoice == '员工组':
        return figDcppie(dataLast, '员工组', dataNew, "部门DCP总费用占比-月度环比")
    if allchoice == '岗位名称':
        return figDcppie(dataLast, '岗位名称', dataNew, "部门DCP总费用占比-月度环比")
    if allchoice == '用户名':
        return figDcppie(dataLast, '用户名', dataNew, "部门DCP总费用占比-月度环比")





@app.callback(
    Output('graph_dcp使用量费用', 'figure'),
    [Input('dropDown_dcp_month', 'value'),
     Input(component_id='radio_dcp使用量费用', component_property='value'),
     Input(component_id='radio_dcp使用量费用全选项', component_property='value')]
)
def build_graph_dcp使用量费用(month, type, allchoice):
    data = 历史dcp
    data = data[data['资源月份'] == month].reset_index(drop=True)
    if type == '已使用量(TB)':
        if allchoice == '资源池':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '用户已使用(TB)', '资源池', '总使用量', '用量占比', '员工所属部门'), '资源池','本月员工部门DCP已使用量(TB)占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '集群名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '用户已使用(TB)', '集群名称', '总使用量', '用量占比', '员工所属部门'), '集群名称','本月员工部门DCP已使用量(TB)占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '存储类型(SSD/HDD)':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '用户已使用(TB)', '存储类型(SSD/HDD)', '总使用量', '用量占比', '员工所属部门'), '存储类型(SSD/HDD)','本月员工部门DCP已使用量(TB)占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '用户已使用(TB)', '员工组', '总使用量', '用量占比', '员工所属部门'), '员工组','本月员工部门DCP已使用量(TB)占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '用户已使用(TB)', '岗位名称', '总使用量', '用量占比', '员工所属部门'), '岗位名称','本月员工部门DCP已使用量(TB)占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '用户已使用(TB)', '用户名', '总使用量', '用量占比', '员工所属部门'), '用户名','本月员工部门DCP已使用量(TB)占比', '总使用量', '用量占比', '员工所属部门')
    elif type == '费用(元)':
        if allchoice == '资源池':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '资源池', '总金额', '金额占比', '员工所属部门'), '资源池','本月员工部门DCP费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '集群名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '集群名称', '总金额', '金额占比', '员工所属部门'), '集群名称','本月员工部门DCP费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '存储类型(SSD/HDD)':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '存储类型(SSD/HDD)', '总金额', '金额占比', '员工所属部门'), '存储类型(SSD/HDD)','本月员工部门DCP费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '员工组', '总金额', '金额占比', '员工所属部门'), '员工组','本月员工部门DCP费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '岗位名称', '总金额', '金额占比', '员工所属部门'), '岗位名称','本月员工部门DCP费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '用户名', '总金额', '金额占比', '员工所属部门'), '用户名','本月员工部门DCP费用(元)占比', '总金额', '金额占比', '员工所属部门')



@app.callback(
    Output('graph_dcp使用量费用2', 'figure'),
    [Input('dropDown_dcp_month2', 'value'),
     Input(component_id='radio_dcp使用量费用2', component_property='value'),
     Input(component_id='radio_dcp使用量费用全选项2', component_property='value')]
)
def build_graph_dcp使用量费用2(month, type, allchoice):
    data = 历史dcp
    data = data[data['资源月份'] == month].reset_index(drop=True)
    if type == '已使用量(TB)':
        if allchoice == '员工部门':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '用户已使用(TB)', '员工所属部门'),
                                               '员工所属部门', '本月资源池DCP已使用量(TB)占比', '总金额')
        if allchoice == '集群名称':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '用户已使用(TB)', '集群名称'), '集群名称',
                                               '本月资源池DCP已使用量(TB)占比', '总金额')
        if allchoice == '存储类型(SSD/HDD)':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '用户已使用(TB)', '存储类型(SSD/HDD)'),
                                               '存储类型(SSD/HDD)', '本月资源池DCP已使用量(TB)占比', '总金额')
        if allchoice == '员工组':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '用户已使用(TB)', '员工组'), '员工组',
                                               '本月资源池DCP已使用量(TB)占比', '总金额')
        if allchoice == '岗位名称':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '用户已使用(TB)', '岗位名称'), '岗位名称',
                                               '本月资源池DCP已使用量(TB)占比', '总金额')
        if allchoice == '用户名':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '用户已使用(TB)', '用户名'), '用户名',
                                               '本月资源池DCP已使用量(TB)占比', '总金额')
    elif type == '费用(元)':
        if allchoice == '员工部门':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '费用(元)', '员工所属部门'), '员工所属部门',
                                               '本月资源池DCP费用(元)占比', '总金额')
        if allchoice == '集群名称':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '费用(元)', '集群名称'), '集群名称',
                                               '本月资源池DCP费用(元)占比', '总金额')
        if allchoice == '存储类型(SSD/HDD)':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '费用(元)', '存储类型(SSD/HDD)'),
                                               '存储类型(SSD/HDD)', '本月资源池DCP费用(元)占比', '总金额')
        if allchoice == '员工组':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '费用(元)', '员工组'), '员工组',
                                               '本月资源池DCP费用(元)占比', '总金额')
        if allchoice == '岗位名称':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '费用(元)', '岗位名称'), '岗位名称',
                                               '本月资源池DCP费用(元)占比', '总金额')
        if allchoice == '用户名':
            return fig固定资产detail不同资源池(对比资源池汇总固定资产(data, '费用(元)', '用户名'), '用户名',
                                               '本月资源池DCP费用(元)占比', '总金额')





@app.callback(
    Output('oc月环比-pie', 'figure'),
    Input(component_id='radio_oc月环比', component_property='value'),
)
def build_graph_ocPie(allchoice):
    dataLast = 上月ocUser
    dataNew = 本月ocUser
    if allchoice == '员工部门':
        return figDcppie(dataLast, '员工所属部门', dataNew, "部门OC总费用占比-月度环比")
    if allchoice == '资源池':
        return figDcppie(dataLast, '资源池', dataNew, "部门OC总费用占比-月度环比")
    if allchoice == '单项资源类型':
        return figDcppie(dataLast, '单项资源类型', dataNew, "部门OC总费用占比-月度环比")
    if allchoice == '员工组':
        return figDcppie(dataLast, '员工组', dataNew, "部门OC总费用占比-月度环比")
    if allchoice == '岗位名称':
        return figDcppie(dataLast, '岗位名称', dataNew, "部门OC总费用占比-月度环比")
    if allchoice == '用户名':
        return figDcppie(dataLast, '用户名', dataNew, "部门OC总费用占比-月度环比")



@app.callback(
    Output('diamond月环比-pie', 'figure'),
    Input(component_id='radio_diamond月环比', component_property='value'),
)
def build_graph_diamondPie(allchoice):
    dataLast = 上月diamondUser
    dataNew = 本月diamondUser
    if allchoice == '员工部门':
        return figDcppie(dataLast, '员工所属部门', dataNew, "部门Diamond总费用占比-月度环比")
    if allchoice == '资源池':
        return figDcppie(dataLast, '资源池', dataNew, "部门Diamond总费用占比-月度环比")
    if allchoice == '单项资源类型':
        return figDcppie(dataLast, '单项资源类型', dataNew, "部门Diamond总费用占比-月度环比")
    if allchoice == '员工组':
        return figDcppie(dataLast, '员工组', dataNew, "部门Diamond总费用占比-月度环比")
    if allchoice == '岗位名称':
        return figDcppie(dataLast, '岗位名称', dataNew, "部门Diamond总费用占比-月度环比")
    if allchoice == '用户名':
        return figDcppie(dataLast, '用户名', dataNew, "部门Diamond总费用占比-月度环比")





@app.callback(
    Output('graph_oc使用量费用', 'figure'),
    [Input('dropDown_oc_month', 'value'),
     Input(component_id='radio_oc使用量费用', component_property='value'),
     Input(component_id='radio_oc使用量费用全选项', component_property='value')]
)
def build_graph_oc使用量费用(month, type, allchoice):
    data = 历史ocUser
    data = data[data['资源月份'] == month].reset_index(drop=True)
    if type == '费用(元)':
        if allchoice == '资源池':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '资源池', '总金额', '金额占比', '员工所属部门'), '资源池','本月员工部门OC费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '员工组', '总金额', '金额占比', '员工所属部门'), '员工组','本月员工部门OC费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '单项资源类型', '总金额', '金额占比', '员工所属部门'), '单项资源类型','本月员工部门OC费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '岗位名称', '总金额', '金额占比', '员工所属部门'), '岗位名称','本月员工部门OC费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '用户名', '总金额', '金额占比', '员工所属部门'), '用户名','本月员工部门OC费用(元)占比', '总金额', '金额占比', '员工所属部门')

    elif type == '已使用量':
        if allchoice == '资源池':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '资源池', '总使用量', '用量占比', '员工所属部门'), '资源池','本月员工部门OC使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '员工组', '总使用量', '用量占比', '员工所属部门'), '员工组','本月员工部门OC使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '单项资源类型', '总使用量', '用量占比', '员工所属部门'), '单项资源类型','本月员工部门OC使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '岗位名称', '总使用量', '用量占比', '员工所属部门'), '岗位名称','本月员工部门OC使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '用户名', '总使用量', '用量占比', '员工所属部门'), '用户名','本月员工部门OC使用量占比', '总使用量', '用量占比', '员工所属部门')



@app.callback(
    Output('graph_oc使用量费用2', 'figure'),
    [Input('dropDown_oc_month2', 'value'),
     Input(component_id='radio_oc使用量费用2', component_property='value'),
     Input(component_id='radio_oc使用量费用全选项2', component_property='value')]
)
def build_graph_oc使用量费用2(month, type, allchoice):
    data = 历史ocUser
    data = data[data['资源月份'] == month].reset_index(drop=True)
    if type == '费用(元)':
        if allchoice == '员工部门':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '员工所属部门', '总金额', '金额占比', '资源池'), '员工所属部门','本月资源池OC费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '员工组', '总金额', '金额占比', '资源池'), '员工组','本月资源池OC费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '单项资源类型', '总金额', '金额占比', '资源池'), '单项资源类型','本月资源池OC费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '岗位名称', '总金额', '金额占比', '资源池'), '岗位名称','本月资源池OC费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '用户名', '总金额', '金额占比', '资源池'), '用户名','本月资源池OC费用(元)占比', '总金额', '金额占比', '资源池')

    elif type == '已使用量':
        if allchoice == '员工部门':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '员工所属部门', '总使用量', '用量占比', '资源池'), '员工所属部门','本月员工部门OC使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '员工组', '总使用量', '用量占比', '资源池'), '员工组','本月员工部门OC使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '单项资源类型', '总使用量', '用量占比', '资源池'), '单项资源类型','本月员工部门OC使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '岗位名称', '总使用量', '用量占比', '资源池'), '岗位名称','本月员工部门OC使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '用户名', '总使用量', '用量占比', '资源池'), '用户名','本月员工部门OC使用量占比', '总使用量', '用量占比', '资源池')




@app.callback(
    Output('graph_diamond使用量费用', 'figure'),
    [Input('dropDown_diamond_month', 'value'),
     Input(component_id='radio_diamond使用量费用', component_property='value'),
     Input(component_id='radio_diamond使用量费用全选项', component_property='value')]
)
def build_graph_diamond使用量费用(month, type, allchoice):
    data = 历史diamondUser
    data = data[data['资源月份'] == month].reset_index(drop=True)
    if type == '费用(元)':
        if allchoice == '资源池':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '资源池', '总金额', '金额占比', '员工所属部门'), '资源池','本月员工部门diamond费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '员工组', '总金额', '金额占比', '员工所属部门'), '员工组','本月员工部门diamond费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '单项资源类型', '总金额', '金额占比', '员工所属部门'), '单项资源类型','本月员工部门diamond费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '岗位名称', '总金额', '金额占比', '员工所属部门'), '岗位名称','本月员工部门diamond费用(元)占比', '总金额', '金额占比', '员工所属部门')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '用户名', '总金额', '金额占比', '员工所属部门'), '用户名','本月员工部门diamond费用(元)占比', '总金额', '金额占比', '员工所属部门')

    elif type == '已使用量':
        if allchoice == '资源池':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '资源池', '总使用量', '用量占比', '员工所属部门'), '资源池','本月员工部门diamond使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '员工组', '总使用量', '用量占比', '员工所属部门'), '员工组','本月员工部门diamond使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '单项资源类型', '总使用量', '用量占比', '员工所属部门'), '单项资源类型','本月员工部门diamond使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '岗位名称', '总使用量', '用量占比', '员工所属部门'), '岗位名称','本月员工部门diamond使用量占比', '总使用量', '用量占比', '员工所属部门')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '用户名', '总使用量', '用量占比', '员工所属部门'), '用户名','本月员工部门diamond使用量占比', '总使用量', '用量占比', '员工所属部门')


@app.callback(
    Output('graph_diamond使用量费用2', 'figure'),
    [Input('dropDown_diamond_month2', 'value'),
     Input(component_id='radio_diamond使用量费用2', component_property='value'),
     Input(component_id='radio_diamond使用量费用全选项2', component_property='value')]
)
def build_graph_diamond使用量费用2(month, type, allchoice):
    data = 历史diamondUser
    data = data[data['资源月份'] == month].reset_index(drop=True)
    if type == '费用(元)':
        if allchoice == '员工部门':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '员工所属部门', '总金额', '金额占比', '资源池'), '员工所属部门','本月资源池diamond费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '员工组', '总金额', '金额占比', '资源池'), '员工组','本月资源池diamond费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '单项资源类型', '总金额', '金额占比', '资源池'), '单项资源类型','本月资源池diamond费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '岗位名称', '总金额', '金额占比', '资源池'), '岗位名称','本月资源池diamond费用(元)占比', '总金额', '金额占比', '资源池')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '费用(元)', '用户名', '总金额', '金额占比', '资源池'), '用户名','本月资源池diamond费用(元)占比', '总金额', '金额占比', '资源池')

    elif type == '已使用量':
        if allchoice == '员工部门':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '员工所属部门', '总使用量', '用量占比', '资源池'), '员工所属部门','本月员工部门diamond使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '员工组':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '员工组', '总使用量', '用量占比', '资源池'), '员工组','本月员工部门diamond使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '单项资源类型':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '单项资源类型', '总使用量', '用量占比', '资源池'), '单项资源类型','本月员工部门diamond使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '岗位名称':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '岗位名称', '总使用量', '用量占比', '资源池'), '岗位名称','本月员工部门diamond使用量占比', '总使用量', '用量占比', '资源池')
        if allchoice == '用户名':
            return fig固定资产detail不同Attri(对比汇总dcp(data, '单项资源使用量', '用户名', '总使用量', '用量占比', '资源池'), '用户名','本月员工部门diamond使用量占比', '总使用量', '用量占比', '资源池')


@app.callback(
    [Output('dropDown_员工历史资源费用', 'options'),
     Output('dropDown_员工历史资源费用', 'value')],
    Input('radio_员工历史资源费用', 'value')
)
def staffHistoricalRes(value):
    if value == '资源池':
        options = list(set(sumResDf['资源池']))
        value = options[0]
    # if value == '资源池':
    #     options = list(set(sumResDf['资源池']))
    #     value = options[0]
    return options,value



@app.callback(
    [Output('dropDown_员工姓名', 'options'),
     Output('dropDown_员工姓名', 'value'),],
    [Input('radio_员工历史资源费用', 'value'),
     Input('dropDown_员工历史资源费用', 'value')]
)
def staffHistoricalRes2(radio, value):
    # if radio == '员工所属部门':
    #     options = list(set(sumResDf[sumResDf['资源池'] == value]['用户名']))
    #     value = options[0]
    if radio == '资源池':
        options = list(set(sumResDf[sumResDf['资源池'] == value]['用户名']))
        value = options[0]
    return options, value


@app.callback(
    Output('staffHistoricalRes_days', 'figure'),
    Input('dropDown_员工姓名', 'value'),
)
def staffHistoricalResGraph(value):
    data = sumResDf[sumResDf['用户名'] == value].reset_index(drop=True).iloc[:, -4:]
    return fig固定资产detail不同月(data, '类别', '员工历史资源总费用', '费用(元)', '用户名', 'month')



@app.callback(
    Output('table_历史员工资源费用', 'data'),
    Input('dropDown_员工姓名', 'value')
)
def staffHistoricalResTable(value):
    data = sumResDf[sumResDf['用户名'] == value].reset_index(drop=True)
    return data.to_dict('records')



@app.callback(
    [Output('dropDown_工时month', 'options'),
    Output('dropDown_工时month', 'value')],
    Input('dropDown_工时year', 'value')
)
def buildWHlist(value):
    data = 历史人员维度[历史人员维度['工时年份'] == value].reset_index(drop=True)
    opts = sorted(list(set(data['工时月份'])), reverse=True)
    options = [{'label': opt, 'value': opt} for opt in opts]
    value = opts[0]
    return options, value


@app.callback(
    Output('renyuanweidu', 'children'),
    [Input('dropDown_工时year', 'value'),
    Input('dropDown_工时month', 'value')]
)
def buildWH(value, value2):
    data = readhistroyData(工时历史总表汇总(), '人员维度')
    data = data[data['工时年份'] == value].reset_index(drop=True)
    data = data[data['工时月份'] == value2].reset_index(drop=True)
    人员维度更新时间 = str(value2) + '月工时'
    国内全勤人天 = max(data[~data['工作地点'].isin(['阿布扎比','新加坡'])]['理论人天'])
    新加坡全勤人天 = max(data[data['工作地点'].isin(['新加坡'])]['理论人天'])
    阿布扎比全勤人天 = max(data[data['工作地点'].isin(['阿布扎比'])]['理论人天'])
    return "人员维度数据自 {}; 国内全勤 {} 人天, 新加坡全勤 {} 人天, 阿布扎比全勤 {} 人天。".format(人员维度更新时间, 国内全勤人天, 新加坡全勤人天, 阿布扎比全勤人天)


@app.callback(
    Output('wbsweidu', 'children'),
    Input('dropDown_工时month', 'value')
)
def buildWH(value2):
    人员维度更新时间 = str(value2) + '月工时'
    return "WBS维度数据自 {}。".format(人员维度更新时间)



@app.callback(
    Output('切换人员维度底表', 'data'),
    [Input('dropDown_工时year', 'value'),
    Input('dropDown_工时month', 'value')]
)
def return切换底表(value, value2):
    curYear = value
    curMon = value2

    if curMon == 1:
        lastMon = 12
        lastYear = curYear - 1
    else:
        lastMon = curMon - 1
        lastYear = curYear

    lastMonDf = 历史人员维度[(历史人员维度['工时月份'] == lastMon) & (历史人员维度['工时年份'] == lastYear)].reset_index(drop=True)
    curMonDf = 历史人员维度[(历史人员维度['工时月份'] == curMon) & (历史人员维度['工时年份'] == curYear)].reset_index(drop=True)

    return lastMonDf.to_dict('records'), curMonDf.to_dict('records')


# if __name__ == "__main__":
#     app.run_server(debug=True, port=8090)
#
# app.callback 里加上prevent_initial_callback=True,为了不要一开始就call back
# 用判断条件来看是是否要trigger，用state，然后def里的参数需要input 和state 几个
# return 记得用component_property 来放在def里return
# 用df作图，永远先copy 成新df来做！！！
# PreventUpdate 用来避免output update
# 有很多output，但有些不想update 用Dash.no_update

