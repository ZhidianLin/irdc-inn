from cleanData import *
from dataSource import *
import pathlib
from dash import Dash
import dash_auth
from datetime import datetime
from dash import Dash, dcc, html, Input, Output, State, dash_table, ALL, MATCH
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64
from dash.exceptions import PreventUpdate
import openpyxl



本月人员维度 = 本月人员维度()
上月人员维度 = 上月人员维度()
all_actual_days = 历史部门实际人均人天()
all_logic_percentage = 历史部门理论填报率()
# cur_bus_line_summary = 本月业务线维度()
# # last_bus_line_summary = 上月业务线维度()
# cur_staff_apartment = 本月员工所属部门维度()
# business_line_staff_type = 本月业务线员工组()
cur_mon_staff = cleanCurMonStaff(本月人员维度)
last_mon_staff = cleanCurMonStaff(上月人员维度)
staff_apartment_tb = cleanstaff_apartment_table()
business_line_tb = cleanbusiness_line_table()
员工所属部门汇总1 = cleanstaff_apartment_table()

资源池汇总 = cleanstaff_ziyuanchi_table()
岗位名称 = cleanstaff_title_table()
资源池 = cleanstaff_ziyuanchi_table()
# 预估业务线pie = 业务线pie("预估人天")
实际业务线pie = 业务线pie("实际人天", cleanbusiness_line_table())
理论业务线pie = 业务线pie("理论人天", cleanbusiness_line_table())

实际岗位pie = 岗位pie('实际人天')
理论岗位pie = 岗位pie('理论人天')
实际资源池pie = 资源池pie('实际人天')
理论资源池pie = 资源池pie('理论人天')
理论业务线汇总 = 业务线汇总('理论人天')
实际业务线汇总 = 业务线汇总('实际人天')
理论实际业务线汇总 = 对比部门汇总(cur_mon_staff , '理论人天','实际人天',"员工组")
理论实际资源池汇总 = 对比部门汇总(cur_mon_staff, '理论人天','实际人天', '资源池')
理论实际岗位名称汇总 = 对比部门汇总(cur_mon_staff, '理论人天','实际人天','岗位名称')

def 理论实际业务线汇总资源池细分(name):
    data = cur_mon_staff[cur_mon_staff['资源池'] == name]
    return 对比部门汇总资源池细分(data , '理论人天','实际人天','预估人天',"员工组")

def 理论实际岗位名称汇总资源池细分(name):
    data = cur_mon_staff[cur_mon_staff['资源池'] == name]
    return 对比部门汇总资源池细分(data , '理论人天','实际人天','预估人天',"岗位名称")

def 理论实际业务线汇总资源池细分BL(data, name):
    data = data[data['员工所属部门'] == name]
    return 对比部门汇总资源池细分BL(data , '理论人天','实际人天','预估人天',"员工组")

def 理论实际岗位名称汇总资源池细分BL(data, name):
    data = data[data['员工所属部门'] == name]
    return 对比部门汇总资源池细分BL(data , '理论人天','实际人天','预估人天',"岗位名称")


理论实际资源池员工组汇总 = 对比资源池汇总(cur_mon_staff , '理论人天','实际人天',"员工组")
理论实际资源池员工所属部门汇总 = 对比资源池汇总(cur_mon_staff, '理论人天','实际人天', '员工所属部门')
理论实际资源池岗位名称汇总 = 对比资源池汇总(cur_mon_staff, '理论人天','实际人天','岗位名称')

实际部门wbspie = wbs部门pie(本月WBS维度(), "实际人天")
预估部门wbspie = wbs部门pie(本月WBS维度(), "预估人天")
实际类型wbspie = wbs类型pie(本月WBS维度(), "实际人天")
预估类型wbspie = wbs类型pie(本月WBS维度(), "预估人天")
# 实际利润中心wbspie = wbs利润中心pie("实际人天")
# 预估利润中心wbspie = wbs利润中心pie("预估人天")

# indicator summary for sx
cur_mon_staff_sx = monStaff_businessLine(本月人员维度,'SX')
last_mon_staff_sx = monStaff_businessLine(上月人员维度,'SX')
cur_mon_staff_sx_ibg = monStaff_businessLine(本月人员维度,'SX-IBG')
last_mon_staff_sx_ibg = monStaff_businessLine(上月人员维度,'SX-IBG')
cur_mon_staff_sx_abg = monStaff_businessLine(本月人员维度,'SX-ABG')
last_mon_staff_sx_abg = monStaff_businessLine(上月人员维度,'SX-ABG')

# indicator summary for ir
cur_mon_staff_ir = monStaff_businessLine(本月人员维度,'IR')
last_mon_staff_ir = monStaff_businessLine(上月人员维度,'IR')

# indicator summary for aiot
cur_mon_staff_aiot = monStaff_businessLine(本月人员维度,'AIOT')
last_mon_staff_aiot = monStaff_businessLine(上月人员维度,'AIOT')

# indicator summary for dx
cur_mon_staff_dx = monStaff_businessLine(本月人员维度,'DX')
last_mon_staff_dx = monStaff_businessLine(上月人员维度,'DX')
cur_mon_staff_dx_ty = monStaff_businessLine(本月人员维度,'DX-TY')
last_mon_staff_dx_ty = monStaff_businessLine(上月人员维度,'DX-TY')
cur_mon_staff_dx_sku = monStaff_businessLine(本月人员维度,'DX-SKU')
last_mon_staff_dx_sku = monStaff_businessLine(上月人员维度,'DX-SKU')


def cyber(ciphertext):
    result=''
    ciphertext=ciphertext.encode('utf-8')
    basedecode={
          '64':lambda x:base64.b64decode(x)
            }
    for j in range(10):
        try:
            ciphertext=basedecode['64'](ciphertext)
        except:
            print('cybersecurity failed')
    result=ciphertext.decode('utf-8')
    return result


def indicator_logic_percentage(cur_in_actual_day, cur_in_lo_day,last_in_actual_day, last_in_lo_day,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = tryExceptNone(round(cur_in_actual_day/cur_in_lo_day*100,1)),
        number={"suffix": "%"},
        delta = {"reference": round(last_in_actual_day/last_in_lo_day*100,1), "valueformat": ".0f",},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2,delta_font_size=12,number_font_size=18,title_font_size=13
    )
    indicator.update_layout(
        height=80,width=88,
    )
    return indicator


def indicator_irdc_rate(cur_data, last_data, tableValue1, tableValue2, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[tableValue1].sum()/cur_data[tableValue2].sum() *100,1),
        number={"suffix": "%"},
        title = {"text": reName},
        align="center",
        delta={"reference": round(last_data[tableValue1].sum() / last_data[tableValue2].sum() * 100, 1),
               "valueformat": ".0f"},

    ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=122,
    )
    return indicator

def indicator_logic_percentages(cur_in_actual_day, cur_in_lo_day,last_in_actual_day, last_in_lo_day,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(try0Divi0(cur_in_actual_day, cur_in_lo_day),1),
        number={"suffix": "%"},
        delta = {"reference": round(try0Divi0(last_in_actual_day,last_in_lo_day),1), "valueformat": ".0f",},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2,delta_font_size=12,number_font_size=18,title_font_size=13
    )
    indicator.update_layout(
        height=80,width=80,
    )
    return indicator

# indicator summary
def indicator_bg(cur_data, last_data, tableValue, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = len(cur_data[tableValue]),
        delta = {"reference": len(last_data[tableValue]), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=12,number_font_size=28,title_font_size=15
    )
    indicator.update_layout(
        height=120,width=135,
    )
    return indicator

def indicator_large(cur_data, last_data, tableValue, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = len(cur_data[tableValue]),
        delta = {"reference": len(last_data[tableValue]), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=30,title_font_size=18
    )
    indicator.update_layout(
        height=240,width=150,
    )
    return indicator

def indicator_large_ppl(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=122,
    )
    return indicator


def indicator_large_ppls(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=100,
    )
    return indicator

def indicator_bl_total(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=12,number_font_size=20,title_font_size=15
    )
    indicator.update_layout(
        height=80,width=180,
    )
    return indicator

def indicator_bl_totalL(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=12,number_font_size=20,title_font_size=15
    )
    indicator.update_layout(
        height=80,width=400,
    )
    return indicator

def indicator_bl_total_midL(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=200,
    )
    return indicator


def indicator_bl_total_midGpu(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=150,
    )
    return indicator


def indicator_bl_totalLL(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=12,number_font_size=20,title_font_size=15
    )
    indicator.update_layout(
        height=80,width=620,
    )
    return indicator

def indicator_bl_totalGpu(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=12,number_font_size=20,title_font_size=15
    )
    indicator.update_layout(
        height=80,width=300,
    )
    return indicator


def indicator_bl_total_midLL(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=310,
    )
    return indicator


def indicator_bl_total_midLS(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=120,
    )
    return indicator

def indicator_bl_total_mid(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=90,
    )
    return indicator

def indicator_bl_total_midBL(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=120,
    )
    return indicator

def indicator_bl_total_mid_rate(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        number={"suffix": "%"},
        title = {"text": reName},
        align="center",
        delta={"reference": last_data,
               "valueformat": ".0f"},

    ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=90,
    )
    return indicator

def indicator_bl_total_mid_rateBL(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        number={"suffix": "%"},
        title = {"text": reName},
        align="center",
        delta={"reference": last_data,
               "valueformat": ".0f"},

    ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=10,number_font_size=12,title_font_size=11
    )
    indicator.update_layout(
        height=60,width=120,
    )
    return indicator

def indicator_bl_total_sm(cur_data, last_data,  reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=4,number_font_size=8,title_font_size=6
    )
    indicator.update_layout(
        height=40,width=90,
    )
    return indicator

def indicator_large_forNA(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=133,
    )
    return indicator

def indicator_large_forNAs(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=100,
    )
    return indicator

def indicator_wbs_sum(cur_data, last_data, tableValue, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = len(cur_data[tableValue]),
        delta = {"reference": len(last_data[tableValue]), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=30,title_font_size=18
    )
    indicator.update_layout(
        height=320,width=150,
    )
    return indicator

def indicator_wbs_sum_wide(cur_data, last_data, tableValue, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = len(cur_data[tableValue]),
        delta = {"reference": len(last_data[tableValue]), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=15,number_font_size=23,title_font_size=18
    )
    indicator.update_layout(
        height=95,width=620,
    )
    return indicator

def indicator_wbs_number(cur_data, last_data, tableValue, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data[tableValue],
        delta = {"reference": last_data[tableValue], "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2, delta_font_size=12, number_font_size=20, title_font_size=15
    )
    indicator.update_layout(
        height=80, width=110,
    )
    return indicator

def indicator_wbs_number_sm(cur_data, last_data, tableValue, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data[tableValue],
        delta = {"reference": last_data[tableValue], "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2, delta_font_size=11, number_font_size=18, title_font_size=13
    )
    indicator.update_layout(
        height=80, width=85,
    )
    return indicator

def indicator_wbs_number2(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2, delta_font_size=11, number_font_size=18, title_font_size=13
    )
    indicator.update_layout(
        height=80, width=85,
    )
    return indicator

def indicator_wbs_act(cur_data, last_data, tableValue,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[tableValue].sum(),1),
        delta = {"reference": round(last_data[tableValue].sum(),1), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=30,title_font_size=18
    )
    indicator.update_layout(
        height=320,width=150,
    )
    return indicator

def indicator_wbs_act_wide(cur_data, last_data, tableValue,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[tableValue].sum(),1),
        delta = {"reference": round(last_data[tableValue].sum(),1), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=15,number_font_size=23,title_font_size=18
    )
    indicator.update_layout(
        height=95,width=620,
    )
    return indicator

def indicator_databz(cur_data, last_data, tableValue,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[tableValue].sum(),1),
        delta = {"reference": round(last_data[tableValue].sum(),1), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=133,
    )
    return indicator

def indicator_databzs(cur_data, last_data, tableValue,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[tableValue].sum(),1),
        delta = {"reference": round(last_data[tableValue].sum(),1), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=100,
    )
    return indicator

def indicator_databz_forNA(cur_data, last_data,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=133,
    )
    return indicator

def indicator_databz_forNAs(cur_data, last_data,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=100,
    )
    return indicator


def indicator_wbs_type(cur_data, last_data, type, tableValue1, tableValue2, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[cur_data[tableValue1] == type][tableValue2].sum()/cur_data[tableValue2].sum()*100,1),
        number={"suffix": "%"},
        title = {"text": reName},
        align="center",
        delta={"reference": round(
            last_data[last_data[tableValue1] == type][tableValue2].sum() / last_data[tableValue2].sum() * 100, 1),
               "valueformat": ".0f"},
    ))
    indicator.update_traces(
        domain_column=2, domain_row=2, delta_font_size=12, number_font_size=20, title_font_size=15
    )
    indicator.update_layout(
        height=80, width=100,
    )
    return indicator


def indicator_wbs_type_sum(cur_data, last_data, type, tableValue1, tableValue2, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data[cur_data[tableValue1] == type][tableValue2].sum(),
        title = {"text": reName},
        align="center",
        delta={"reference": last_data[last_data[tableValue1] == type][tableValue2].sum(),
               "valueformat": ".0f"},
    ))
    indicator.update_traces(
        domain_column=2, domain_row=2, delta_font_size=12, number_font_size=20, title_font_size=15
    )
    indicator.update_layout(
        height=80, width=110,
    )
    return indicator


def indicator_wbs_percentage(cur_data, last_data, type, wbsApartment, tableValue1, tableValue2, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[cur_data[wbsApartment] == type][tableValue2].sum()/cur_data[cur_data[wbsApartment] == type][tableValue1].sum()*100,1),
        number={"suffix": "%"},
        title = {"text": reName},
        align="center",
        delta={"reference": round(last_data[last_data[wbsApartment] == type][tableValue2].sum()/last_data[last_data[wbsApartment] == type][tableValue1].sum()*100,1),
               "valueformat": ".0f"},

    ))
    indicator.update_traces(
        domain_column=2, domain_row=2, delta_font_size=12, number_font_size=20, title_font_size=15
    )
    indicator.update_layout(
        height=80, width=100,
    )
    return indicator

def indicator_irdc_sum(cur_data, last_data, tableValue,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[tableValue].sum(),1),
        delta = {"reference": round(last_data[tableValue].sum(),1), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=122,
    )
    return indicator

def indicator_irdc_per(cur_data, last_data, tableValue1, tableValue2,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[tableValue1].sum()/len(list(set(cur_data[tableValue2]))),1),
        delta = {"reference": round(last_data[tableValue1].sum()/len(list(set(last_data[tableValue2]))),1), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=26,title_font_size=18
    )
    indicator.update_layout(
        height=242,width=122,
    )
    return indicator


def indicator_irdc_type_per(cur_in_actual_day, cur_in_staff_number, last_in_actual_day, last_in_staff_number, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_in_actual_day/cur_in_staff_number,1),
        delta = {"reference": round(last_in_actual_day/last_in_staff_number,1), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2,delta_font_size=12,number_font_size=18,title_font_size=13
    )
    indicator.update_layout(
        height=80,width=88,
    )
    return indicator



def indicator_sum(cur_data, last_data, businessLine, tableValue):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data[cur_data['业务线'].str.contains(businessLine)][tableValue].sum(),
        delta = {"reference": last_data[last_data['业务线'].str.contains(businessLine)][tableValue].sum(), "valueformat": ".0f"},
        title = {"text": tableValue},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=12,number_font_size=28,title_font_size=15
    )
    indicator.update_layout(
        height=120,width=135,
    )
    return indicator


def indicator_value0(cur_data, last_data, businessLine, tableValue,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data[cur_data['业务线'] == businessLine][tableValue].values[0],
        delta = {"reference": last_data[last_data['业务线'] == businessLine][tableValue].values[0], "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3, delta_font_size=12, number_font_size=28, title_font_size=15
    )
    indicator.update_layout(
        height=120,width=135,
    )
    return indicator


def indicator_avg(cur_data, last_data, businessLine, tableValue1, tableValue2, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data[cur_data['业务线'].str.contains(businessLine)][tableValue1].sum()/cur_data[cur_data['业务线'].str.contains(businessLine)][tableValue2].sum(),
        delta = {"reference": last_data[last_data['业务线'].str.contains(businessLine)][tableValue1].sum()/last_data[last_data['业务线'].str.contains(businessLine)][tableValue2].sum(), "valueformat": ".0f"},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3, delta_font_size=12, number_font_size=28, title_font_size=15
    )
    indicator.update_layout(
        height=120,width=135,
    )
    return indicator





def indicator_rate(cur_data, last_data, businessLine, tableValue1, tableValue2, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(cur_data[cur_data['业务线'].str.contains(businessLine)][tableValue1].sum()/cur_data[cur_data['业务线'].str.contains(businessLine)][tableValue2].sum()*100,1),
        number={"suffix": "%"},
        title = {"text": reName},
        align="center",
        delta={"reference": round(last_data[last_data['业务线'].str.contains(businessLine)][tableValue1].sum() /
                                  last_data[last_data['业务线'].str.contains(businessLine)][tableValue2].sum() * 100,
                                  1), "valueformat": ".0f"},

    ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=12,number_font_size=28,title_font_size=15
    )
    indicator.update_layout(
        height=120,width=135,
    )
    return indicator


def indicator_gpu_percentage_large(cur_data,last_data,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        number={"suffix": "%"},
        delta = {"reference": last_data, "valueformat": ".0f",},
        title = {"text": reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3,delta_font_size=16,number_font_size=30,title_font_size=16
    )
    indicator.update_layout(
        height=320,width=150,
    )
    return indicator

def indicator_gpu_percentage_small(cur_data,last_data,reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        number={"suffix": "%"},
        title = {"text": reName},
        align="center",
        delta={"reference": last_data,
               "valueformat": ".0f"},

    ))
    indicator.update_traces(
        domain_column=2, domain_row=2, delta_font_size=12, number_font_size=20, title_font_size=15
    )
    indicator.update_layout(
        height=80, width=100,
    )
    return indicator

def try_except(value, default):
    try:
        return value
    except KeyError:
        return default

def indicator_lessMore(cur_data, last_data, businessLine, tableValue, lessMore, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = try_except(cur_data[cur_data['业务线'] == businessLine][tableValue].value_counts()[lessMore], 0),
        delta = {"reference": try_except(last_data[last_data['业务线'] == businessLine][tableValue].value_counts()[lessMore], 0), "valueformat": ".0f"},
        title = {"text":reName},
        align="center",
        ))
    indicator.update_traces(
        domain_column=1, domain_row=3, delta_font_size=12, number_font_size=28, title_font_size=15
    )
    indicator.update_layout(
        height=120,width=135,
    )
    return indicator


def indicator(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center"
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2,delta_font_size=12,number_font_size=20,title_font_size=15
    )
    indicator.update_layout(
        height=80,width=100,
    )
    return indicator


def indicator_ppl(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center"
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2,delta_font_size=12,number_font_size=18,title_font_size=13
    )
    indicator.update_layout(
        height=80,width=88,
    )
    return indicator

def indicator_ppls(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center"
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2,delta_font_size=12,number_font_size=18,title_font_size=13
    )
    indicator.update_layout(
        height=80,width=80,
    )
    return indicator

def indicator_pplss(cur_data, last_data, reName):
    indicator = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cur_data,
        delta = {"reference": last_data, "valueformat": ".0f"},
        title = {"text": reName},
        align="center"
        ))
    indicator.update_traces(
        domain_column=2, domain_row=2,delta_font_size=12,number_font_size=18,title_font_size=13
    )
    indicator.update_layout(
        height=120,width=80,
    )
    return indicator

def irdc_summary_large(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                  # "border-radius": "5px",
                     "background-color": "#f9f9f9",
                     "box-shadow": "2px 2px 2px lightgrey",
                     "position": "relative",
                     "width":'150px'
                     })

def irdc_summary_large_wbs(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                  # "border-radius": "5px",
                     "background-color": "#f9f9f9",
                     "box-shadow": "2px 2px 2px lightgrey",
                     "position": "relative",
                     "margin-bottom": "1px",
                     "width":'620px'
                     })


def irdc_summary_large_ppl(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'120px'
                     })


def callBack_irdc_summary_large_ppl(id):
    return dcc.Graph(id=id, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'120px'
                     })



def irdc_summary_large_ppls(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'100px'
                     })

def irdc_wh_large(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'180px'
                     })


def irdc_wh_largeGpu(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'300px'
                     })

def irdc_wh_middle(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'90px'
                     })

def irdc_wh_middleBL(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'120px'
                     })

def irdc_wh_middleGpu(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'150px'
                     })


def irdc_wh_largeL(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'400px'
                     })

def irdc_wh_largeLL(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'620px'
                     })

def irdc_wh_middleL(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'200px'
                     })


def irdc_wh_middleLL(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'310px'
                     })

def irdc_wh_middleLS(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'120px'
                     })

def irdc_wh_small(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                  "margin-bottom": "1px",
                     "width":'90px'
                     })

def irdc_summary_smWider_ppl(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                  "background-color": "#f9f9f9",
                  "box-shadow": "1px 1px 1px lightgrey",
                  "position": "relative",
                  "margin-bottom": "1px",
                  "margin-left": "-12px",
                  "width": '88px'
                     })


def irdc_summary_smWider_ppls(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                  "background-color": "#f9f9f9",
                  "box-shadow": "1px 1px 1px lightgrey",
                  "position": "relative",
                  "margin-bottom": "1px",
                  "margin-left": "-12px",
                  "width": '80px'
                     })

def irdc_summary_smWider(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                  # "border-radius": "5px",
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                     "margin-bottom": "1px",
                  "width":"110px",
                     })

def irdc_summary_sm(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={
                  # "border-radius": "5px",
                     "background-color": "#f9f9f9",
                     "box-shadow": "1px 1px 1px lightgrey",
                     "position": "relative",
                     "margin-bottom": "1px",
                  "width":"85px",
                     })

def irdc_graph(id, fig):
    return dcc.Graph(id=id, figure=fig, config={'displayModeBar': False},
              style={"border-radius": "5px",
                     "background-color": "#f9f9f9",
                     "box-shadow": "2px 2px 2px lightgrey",
                     "position": "relative",
                     "margin-bottom": "15px"
                     }
              )


def collapse_btn_table(btn_id, tb_id, tb_data,output_id):
    return html.Div([
        dbc.Button(
            "查看数据原表",
            id=btn_id,
            className= "mb-3",
            color="info",
            n_clicks=0,
        ),
        dbc.Collapse(
            dash_table.DataTable(
                id=tb_id,
                columns=[{"name": i, "id": i, } for i in tb_data.columns],
                sort_action="native",
                sort_mode="multi",
                page_size=10,
                data=tb_data.to_dict('records'),
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'border': '1px solid white'
                },
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{预估填报} = 不满',
                            'column_id': '预估填报'
                        },
                        'color': 'orange',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{理论填报} = 不满',
                            'column_id': '理论填报'
                        },
                        'color': 'orange',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{预估填报} = 超载',
                            'column_id': '预估填报'
                        },
                        'color': 'tomato',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{理论填报} = 超载',
                            'column_id': '理论填报'
                        },
                        'color': 'tomato',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{预估填报} = 合理',
                            'column_id': '预估填报'
                        },
                        'color': 'green',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{理论填报} = 合理',
                            'column_id': '理论填报'
                        },
                        'color': 'green',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{WBS类型} = D',
                            'column_id': 'WBS类型'
                        },
                        'backgroundColor': 'dodgerblue',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{WBS类型} = P',
                            'column_id': 'WBS类型'
                        },
                        'backgroundColor': 'RebeccaPurple',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{WBS类型} = R',
                            'column_id': 'WBS类型'
                        },
                        'backgroundColor': 'hotpink',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{WBS类型} = M',
                            'column_id': 'WBS类型'
                        },
                        'backgroundColor': 'grey',
                        'color': 'white',

                    },

                ],
                style_cell={'border': '1px solid lightgrey'}
            ),
            is_open=False,
            id=output_id
        ),
    ])

def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append(
            {
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #0074D9 0%,
                    #0074D9 {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
        })
    return styles

def tbl_style():
    return [
                                                     {
                                                         'if': {
                                                             'filter_query': '{预估填报} = 不满',
                                                             'column_id': '预估填报'
                                                         },
                                                         'color': 'orange',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{理论填报} = 不满',
                                                             'column_id': '理论填报'
                                                         },
                                                         'color': 'orange',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{预估填报} = 超载',
                                                             'column_id': '预估填报'
                                                         },
                                                         'color': 'tomato',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{理论填报} = 超载',
                                                             'column_id': '理论填报'
                                                         },
                                                         'color': 'tomato',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{预估填报} = 合理',
                                                             'column_id': '预估填报'
                                                         },
                                                         'color': 'green',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{理论填报} = 合理',
                                                             'column_id': '理论填报'
                                                         },
                                                         'color': 'green',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{未填次数} contains "2"'
                                                         },
                                                         'backgroundColor': 'dodgerblue',
                                                         'color': 'white'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{WBS类型} = D',
                                                             'column_id': 'WBS类型'
                                                         },
                                                         'backgroundColor': 'dodgerblue',
                                                         'color': 'white',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{WBS类型} = P',
                                                             'column_id': 'WBS类型'
                                                         },
                                                         'backgroundColor': 'RebeccaPurple',
                                                         'color': 'white',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{WBS类型} = R',
                                                             'column_id': 'WBS类型'
                                                         },
                                                         'backgroundColor': 'hotpink',
                                                         'color': 'white',
                                                         'fontWeight': 'bold'
                                                     },
                                                     {
                                                         'if': {
                                                             'filter_query': '{WBS类型} = M',
                                                             'column_id': 'WBS类型'
                                                         },
                                                         'backgroundColor': 'grey',
                                                         'color': 'white',

                                                     },
                                                 ]


def collapse_btn_table2(btn_id, tb_id, tb_data,output_id,tableValue):
    return html.Div([
        dbc.Button(
            "查看数据原表",
            id=btn_id,
            className= "mb-3",
            color="info",
            n_clicks=0,
        ),
        dbc.Collapse(
            dash_table.DataTable(
                id=tb_id,
                columns=[{"name": i, "id": i, } for i in tb_data.columns],
                sort_action="native",
                sort_mode="multi",
                data=tb_data.to_dict('records'),
                # style_header={
                #     'backgroundColor': 'rgb(210, 210, 210)',
                #     'color': 'black',
                #     'fontWeight': 'bold',
                #     'border': '1px solid white'
                # },
                style_data_conditional=(data_bars(tb_data, tableValue)),
                style_cell={
                    'width': '100px',
                    'minWidth': '100px',
                    'maxWidth': '100px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'border': '1px solid lightgrey'
                },
            ),
            is_open=False,
            id=output_id
        ),
    ])


def dash_table_not_collapse(tb_id, tb_data):
    return dash_table.DataTable(
                                    id=tb_id,
                                    columns=[{"name": i, "id": i, } for i in tb_data.columns],
                                    sort_action="native",
                                    sort_mode="multi",
                                    data=tb_data.to_dict('records'),
                                    page_size = 10,
                                    style_header={
                                        'backgroundColor': 'rgb(210, 210, 210)',
                                        'color': 'black',
                                        'fontWeight': 'bold',
                                        'border': '1px solid white'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 不满',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'orange',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 不满',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'orange',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 超载',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'tomato',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 超载',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'tomato',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 合理',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'green',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 合理',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'green',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{未填次数} contains "2"'
                                            },
                                            'backgroundColor': 'dodgerblue',
                                            'color': 'white'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = D',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'dodgerblue',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = P',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'RebeccaPurple',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = R',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'hotpink',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = M',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'grey',
                                            'color': 'white',

                                        },
                                    ],
                                    style_cell={'border': '1px solid lightgrey'}
                                )

def dash_table_not_collapseLeftAlign(tb_id, tb_data):
    return dash_table.DataTable(
                                    id=tb_id,
                                    columns=[{"name": i, "id": i, } for i in tb_data.columns],
                                    sort_action="native",
                                    sort_mode="multi",
                                    data=tb_data.to_dict('records'),
                                    page_size = 10,
                                    style_header={
                                        'backgroundColor': 'rgb(210, 210, 210)',
                                        'color': 'black',
                                        'fontWeight': 'bold',
                                        'border': '1px solid white'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 不满',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'orange',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 不满',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'orange',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 超载',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'tomato',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 超载',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'tomato',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 合理',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'green',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 合理',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'green',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{未填次数} contains "2"'
                                            },
                                            'backgroundColor': 'dodgerblue',
                                            'color': 'white'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = D',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'dodgerblue',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = P',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'RebeccaPurple',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = R',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'hotpink',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = M',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'grey',
                                            'color': 'white',

                                        },
                                    ],
                                    style_cell={'border': '1px solid lightgrey'}
                                )


def dash_table_not_collapse_showAll(tb_id, tb_data):
    return dash_table.DataTable(
                                    id=tb_id,
                                    columns=[{"name": i, "id": i, } for i in tb_data.columns],
                                    sort_action="native",
                                    sort_mode="multi",
                                    data=tb_data.to_dict('records'),

                                    style_header={
                                        'backgroundColor': 'rgb(210, 210, 210)',
                                        'color': 'black',
                                        'fontWeight': 'bold',
                                        'border': '1px solid white'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 不满',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'orange',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 不满',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'orange',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 超载',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'tomato',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 超载',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'tomato',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{预估填报} = 合理',
                                                'column_id': '预估填报'
                                            },
                                            'color': 'green',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{理论填报} = 合理',
                                                'column_id': '理论填报'
                                            },
                                            'color': 'green',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{未填次数} contains "2"'
                                            },
                                            'backgroundColor': 'red',
                                            'color': 'white'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = D',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'dodgerblue',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = P',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'RebeccaPurple',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = R',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'hotpink',
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{WBS类型} = M',
                                                'column_id': 'WBS类型'
                                            },
                                            'backgroundColor': 'grey',
                                            'color': 'white',

                                        },
                                    ],
                                    style_cell={'border': '1px solid lightgrey'}
                                )
def fig员工所属部门汇总(data, type, title):
    fig员工所属部门汇总 = go.Figure()
    data = data.sort_values(by="实际人天")
    fig员工所属部门汇总.add_bar(y=list(data[type])
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="auto"
                                , name="实际人天", orientation='h')
    fig员工所属部门汇总.add_trace(
        go.Scatter(y=list(data[type]), x=list(data.理论人天), mode='markers',
                   name='理论人天', marker=dict(
                color='red', size=10,
                line=dict(
                    color='MediumPurple',
                    width=2))))
    fig员工所属部门汇总.update_layout(title=title,autosize=True,template='plotly_white', xaxis_title='总人天')
    return fig员工所属部门汇总


def fig员工所属部门汇总byFilterP(data):
    # graph staff apartment
    fig员工所属部门汇总 = go.Figure()
    data = data.sort_values(by="实际人天")
    fig员工所属部门汇总.add_bar(y=list(data.员工所属部门)
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="auto"
                                , name="实际人天", orientation='h')
    fig员工所属部门汇总.add_trace(
        go.Scatter(y=list(data.员工所属部门), x=list(data.理论人天), mode='markers',
                   name='理论人天', marker=dict(
                color='red', size=10,
                line=dict(
                    color='MediumPurple',
                    width=2))))
    fig员工所属部门汇总.update_layout(title='总人天（按实际人天倒序排序）',autosize=True,template='plotly_white', xaxis_title='总人天')
    return fig员工所属部门汇总


def fig资源池byFilterP(data,month):
    # graph staff apartment
    fig员工所属部门汇总 = go.Figure()
    data = data.sort_values(by="实际人天")
    fig员工所属部门汇总.add_bar(y=list(data.资源池)
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="auto"
                                , name="实际人天", orientation='h')
    fig员工所属部门汇总.add_trace(
        go.Scatter(y=list(data.资源池), x=list(data.理论人天), mode='markers',
                   name='理论人天', marker=dict(
                color='red', size=10,
                line=dict(
                    color='MediumPurple',
                    width=2))))
    fig员工所属部门汇总.update_layout(title=str(month)+'月总人天（按实际人天倒序排序）',autosize=True,template='plotly_white', xaxis_title='总人天')
    return fig员工所属部门汇总


def fig资源池汇总():
    # graph staff apartment
    fig资源池汇总 = go.Figure()
    data = 资源池汇总.sort_values(by="实际人天")
    fig资源池汇总.add_bar(y=list(data.资源池)
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="auto"
                                , name="实际人天", orientation='h')
    # fig资源池汇总.add_bar(y=list(data.资源池)
    #                             , x=list(data.理论人天)
    #                             , name="理论人天", orientation='h')
    fig资源池汇总.add_trace(
        go.Scatter(y=list(data.资源池), x=list(data.理论人天), mode='markers',
                   name='理论人天', marker=dict(
                color='red', size=15,
                line=dict(
                    color='MediumPurple',
                    width=2))))
    fig资源池汇总.update_layout(title='部门资源池总人天（按实际人天倒序排序）', template='plotly_white', xaxis_title='总人天')
    return fig资源池汇总

def fig岗位名称汇总(data, title):
    # graph staff apartment
    fig岗位名称汇总 = go.Figure()
    data = data.sort_values(by="实际人天")
    fig岗位名称汇总.add_bar(y=list(data.岗位名称)
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="auto"
                                , name="实际人天", orientation='h')
    fig岗位名称汇总.add_trace(
        go.Scatter(y=list(data.岗位名称), x=list(data.理论人天), mode='markers',
                   name='理论人天', marker=dict(
                color='red', size=10,
                line=dict(
                    color='MediumPurple',
                    width=2))))
    fig岗位名称汇总.update_layout(title=title, template='plotly_white', xaxis_title='总人天')
    return fig岗位名称汇总


def fig岗位名称汇总BL(data):
    # graph staff apartment
    fig岗位名称汇总 = go.Figure()
    data = data.sort_values(by="实际人天")
    fig岗位名称汇总.add_bar(y=list(data.岗位名称)
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="auto"
                                , name="实际人天", orientation='h')
    fig岗位名称汇总.add_trace(
        go.Scatter(y=list(data.岗位名称), x=list(data.理论人天), mode='markers',
                   name='理论人天', marker=dict(
                color='red', size=10,
                line=dict(
                    color='MediumPurple',
                    width=2))))
    fig岗位名称汇总.update_layout(title='部门岗位名称总人天（按实际人天倒序排序）', template='plotly_white', xaxis_title='总人天')
    return fig岗位名称汇总


def fig员工所属部门人均人天(data, type, title):
    fig员工所属部门人均人天 = go.Figure()
    data = data.sort_values(by="实际人均")
    fig员工所属部门人均人天.add_bar(y=list(data[type])
                                    , x=list(data.实际人均), text=list(data.实际人均), textposition="auto"
                                    , name="实际人均", orientation='h')
    fig员工所属部门人均人天.add_bar(y=list(data[type])
                                    , x=list(data.理论人均), text=list(data.理论人均), textposition="auto"
                                    , name="理论人均", orientation='h')
    fig员工所属部门人均人天.add_trace(go.Scatter(
        y=list(data[type]),
        x=list(data.部门实际人均),
        mode="markers+lines",
        name="部门实际人均人天",
        line=dict(
            color="black")))
    fig员工所属部门人均人天.update_layout(title=title, template='plotly_white', xaxis_title='人均人天')
    return fig员工所属部门人均人天

def fig员工所属部门人均人天byFilterP(data):
    fig员工所属部门人均人天 = go.Figure()
    data = data.sort_values(by="实际人均")
    # fig员工所属部门人均人天.add_bar(y=list(data.员工所属部门)
    #                                 , x=list(data.预估人均)
    #                                 , name="预估人均", orientation='h')
    fig员工所属部门人均人天.add_bar(y=list(data.员工所属部门)
                                    , x=list(data.实际人均), text=list(data.实际人均), textposition="auto"
                                    , name="实际人均", orientation='h')
    fig员工所属部门人均人天.add_bar(y=list(data.员工所属部门)
                                    , x=list(data.理论人均), text=list(data.理论人均), textposition="auto"
                                    , name="理论人均", orientation='h')
    fig员工所属部门人均人天.add_trace(go.Scatter(
        y=list(data.员工所属部门),
        x=list(data.部门实际人均),
        mode="markers+lines",
        name="部门实际人均人天",
        line=dict(
            color="black")))
    fig员工所属部门人均人天.update_layout(title='人均人天（按实际人均倒序排序）', template='plotly_white', xaxis_title='人均人天')
    return fig员工所属部门人均人天



def fig资源池人均人天byFilterP(data, month):
    fig员工所属部门人均人天 = go.Figure()
    data = data.sort_values(by="实际人均")
    # fig员工所属部门人均人天.add_bar(y=list(data.员工所属部门)
    #                                 , x=list(data.预估人均)
    #                                 , name="预估人均", orientation='h')
    fig员工所属部门人均人天.add_bar(y=list(data.资源池)
                                    , x=list(data.实际人均), text=list(data.实际人均), textposition="auto"
                                    , name="实际人均", orientation='h')
    fig员工所属部门人均人天.add_bar(y=list(data.资源池)
                                    , x=list(data.理论人均), text=list(data.理论人均), textposition="auto"
                                    , name="理论人均", orientation='h')
    fig员工所属部门人均人天.add_trace(go.Scatter(
        y=list(data.资源池),
        x=list(data.部门实际人均),
        mode="markers+lines",
        name="部门实际人均人天",
        line=dict(
            color="black")))
    fig员工所属部门人均人天.update_layout(title=str(month)+'月人均人天（按实际人均倒序排序）', template='plotly_white', xaxis_title='人均人天')
    return fig员工所属部门人均人天



# fig员工所属部门实际填报率 = go.Figure()
# fig员工所属部门实际填报率.add_trace(
#     go.Scatter(x=list(员工所属部门汇总1.员工所属部门), y=list(员工所属部门汇总1.预估填报率),
#                mode="markers+lines", name="预估填报率", line=dict(color="blue")))
# fig员工所属部门实际填报率.add_trace(
#     go.Scatter(x=list(员工所属部门汇总1.员工所属部门), y=list(员工所属部门汇总1.理论填报率),
#                mode="markers+lines", name="理论填报率", line=dict(color="red")))
# fig员工所属部门实际填报率.update_layout(title='员工所属部门预估实际填报率', template='plotly_white',
#                                         yaxis_title='工时填报率%')


# fig = px.line(df, x="月份", y="lifeExp", color='country')


def fig员工所属门固定资产总值(data, sortBy, bar1, bar2, bar3, line1, strper):
    fig员工所属门固定资产总值 = go.Figure()
    data = clean固定资产by部门(data).sort_values(by=sortBy)
    fig员工所属门固定资产总值.add_bar(y=list(data.员工所属部门)
                                    , x=list(data[bar1]), text=list(data[bar1]), textposition="auto"
                                    , name=bar1, orientation='h')
    fig员工所属门固定资产总值.add_bar(y=list(data.员工所属部门)
                                    , x=list(data[bar2]), text=list(data[bar2]), textposition="auto"
                                    , name=bar2, orientation='h')
    fig员工所属门固定资产总值.add_bar(y=list(data.员工所属部门)
                                    , x=list(data[bar3]), text=list(data[bar3]), textposition="auto"
                                    , name=bar3, orientation='h')
    fig员工所属门固定资产总值.add_trace(go.Scatter(
        y=list(data.员工所属部门),
        x=list(data[line1]),
        mode="markers+lines",
        name=line1,
        line=dict(
            color="black")))
    title = '员工部门固定资产' + strper + '金额（按折旧倒序排序）'
    fig员工所属门固定资产总值.update_layout(title=title, template='plotly_white', xaxis_title='资产金额CNY')
    return fig员工所属门固定资产总值



def fig资源池固定资产总值(data, sortBy, bar1, bar2, bar3, line1, strper):
    fig资源池固定资产总值 = go.Figure()
    data = clean固定资产by资源池(data).sort_values(by=sortBy)
    fig资源池固定资产总值.add_bar(y=list(data.资源池)
                                    , x=list(data[bar1]), text=list(data[bar1]), textposition="auto"
                                    , name=bar1, orientation='h')
    fig资源池固定资产总值.add_bar(y=list(data.资源池)
                                    , x=list(data[bar2]), text=list(data[bar2]), textposition="auto"
                                    , name=bar2, orientation='h')
    fig资源池固定资产总值.add_bar(y=list(data.资源池)
                                    , x=list(data[bar3]), text=list(data[bar3]), textposition="auto"
                                    , name=bar3, orientation='h')
    fig资源池固定资产总值.add_trace(go.Scatter(
        y=list(data.资源池),
        x=list(data[line1]),
        mode="markers+lines",
        name=line1,
        line=dict(
            color="black")))
    title = '资源池固定资产' + strper + '金额（按折旧倒序排序）'
    fig资源池固定资产总值.update_layout(title=title, template='plotly_white', xaxis_title='资产金额CNY')
    return fig资源池固定资产总值





def fig业务线pie(实际pie, 理论pie, title):
    labels业务线 = list(实际pie['实际人天'].keys())
    fig业务线pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(实际pie['实际人天']), name="实际"), 1, 1)
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(理论pie['理论人天']), name="理论"), 1, 2)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='员工所属部门 (按占比倒序)',
                               title_text=title,
                               annotations=[dict(text='实际', x=0.205, y=0.5, font_size=18, showarrow=False),
                                            dict(text='理论', x=0.795, y=0.5, font_size=18, showarrow=False)])
    return fig业务线pie


def fig业务线pie资源池(name):
    labels业务线 = list(业务线pieFilter("实际人天",staff_apartment_table(cleanDF资源池(cur_mon_staff,name)))['实际人天'].keys())
    fig业务线pie = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(业务线pieFilter("实际人天",staff_apartment_table(cleanDF资源池(cur_mon_staff,name)))['实际人天']), name="实际"), 1, 1)
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(业务线pieFilter("理论人天",staff_apartment_table(cleanDF资源池(cur_mon_staff,name)))['理论人天']), name="理论"), 1, 2)
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(业务线pieFilter("预估人天",staff_apartment_table(cleanDF资源池(cur_mon_staff,name)))['预估人天']), name="预估"), 1, 3)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='员工所属部门 (按占比倒序)',
                               title_text="总工时占比",
                               annotations=[dict(text='实际', x=0.120, y=0.5, font_size=20, showarrow=False),
                                            dict(text='理论', x=0.500, y=0.5, font_size=20, showarrow=False),
                                            dict(text='预估', x=0.880, y=0.5, font_size=20, showarrow=False)])
    return fig业务线pie



def fig业务线pieBL(data, month, groupBy):
    labels业务线 = list(资源池pieFilter("实际人天", data, groupBy)['实际人天'].keys())
    fig业务线pie = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(资源池pieFilter("实际人天",data, groupBy)['实际人天']), name="实际"), 1, 1)
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(资源池pieFilter("理论人天",data, groupBy)['理论人天']), name="理论"), 1, 2)
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(资源池pieFilter("预估人天",data, groupBy)['预估人天']), name="预估"), 1, 3)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text=groupBy+' (按占比倒序)',
                               title_text=str(month)+"月总工时占比",
                               annotations=[dict(text='实际', x=0.120, y=0.5, font_size=20, showarrow=False),
                                            dict(text='理论', x=0.500, y=0.5, font_size=20, showarrow=False),
                                            dict(text='预估', x=0.880, y=0.5, font_size=20, showarrow=False)])
    return fig业务线pie

def fig固定资产pie(df):
    data = clean固定资产by部门(df)[['员工所属部门','折旧','净值','总值']]
    labels业务线 = list(data['员工所属部门'])
    fig固定资产pie = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig固定资产pie.add_trace(go.Pie(labels=labels业务线, values=list(data[['员工所属部门','折旧']]['折旧']), name="折旧"), 1, 1)
    fig固定资产pie.add_trace(go.Pie(labels=labels业务线, values=list(data[['员工所属部门','净值']]['净值']), name="净值"), 1, 2)
    fig固定资产pie.add_trace(go.Pie(labels=labels业务线, values=list(data[['员工所属部门','总值']]['总值']), name="总值"), 1, 3)
    fig固定资产pie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    fig固定资产pie.update_traces(textposition='inside')
    fig固定资产pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='员工所属部门',
                               title_text="部门总资产金额占比",
                               annotations=[dict(text='折旧', x=0.120, y=0.5, font_size=20, showarrow=False),
                                            dict(text='净值', x=0.500, y=0.5, font_size=20, showarrow=False),
                                            dict(text='总值', x=0.880, y=0.5, font_size=20, showarrow=False)])
    return fig固定资产pie



def fig固定资产资源池pie(df):
    data = clean固定资产by资源池(df)[['资源池','折旧','净值','总值']]
    labels业务线 = list(data['资源池'])
    fig固定资产pie = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig固定资产pie.add_trace(go.Pie(labels=labels业务线, values=list(data[['资源池','折旧']]['折旧']), name="折旧"), 1, 1)
    fig固定资产pie.add_trace(go.Pie(labels=labels业务线, values=list(data[['资源池','净值']]['净值']), name="净值"), 1, 2)
    fig固定资产pie.add_trace(go.Pie(labels=labels业务线, values=list(data[['资源池','总值']]['总值']), name="总值"), 1, 3)
    fig固定资产pie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    fig固定资产pie.update_traces(textposition='inside')
    fig固定资产pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='资源池',
                               title_text="资源池总资产金额占比",
                               annotations=[dict(text='折旧', x=0.120, y=0.5, font_size=20, showarrow=False),
                                            dict(text='净值', x=0.500, y=0.5, font_size=20, showarrow=False),
                                            dict(text='总值', x=0.880, y=0.5, font_size=20, showarrow=False)])
    return fig固定资产pie

# def fig资源池pie():
#     fig员工所属部门汇总 = go.Figure()
#     data = 员工所属部门汇总1.sort_values(by="实际人天")
#     fig员工所属部门汇总.add_bar(y=list(data.员工所属部门)
#                                 , x=list(data.预估人天)
#                                 , name="预估人天", orientation='h')
#     fig员工所属部门汇总.add_bar(y=list(data.员工所属部门)
#                                 , x=list(data.理论人天)
#                                 , name="理论人天", orientation='h')
#
#     labels岗位 = list(实际资源池pie['实际人天'].keys())
#     fig岗位pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
#     fig岗位pie.add_trace(go.Pie(labels=labels岗位, values=list(实际资源池pie['实际人天']), name="实际"), 1, 1)
#     fig岗位pie.add_trace(go.Pie(labels=labels岗位, values=list(理论资源池pie['理论人天']), name="理论"), 1, 2)
#     fig岗位pie.update_traces(hole=.4, hoverinfo="label+percent+name")
#     fig岗位pie.update_traces(textposition='inside')
#     fig岗位pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='资源池 (按占比倒序)',
#                                title_text="资源池总工时占比",)
#     return fig岗位pie



def fig岗位pie():
    labels岗位 = list(实际岗位pie['实际人天'].keys())
    fig岗位pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig岗位pie.add_trace(go.Pie(labels=labels岗位, values=list(实际岗位pie['实际人天']), name="实际"), 1, 1)
    fig岗位pie.add_trace(go.Pie(labels=labels岗位, values=list(理论岗位pie['理论人天']), name="理论"), 1, 2)
    fig岗位pie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    fig岗位pie.update_traces(textposition='inside')
    fig岗位pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='岗位名称 (按占比倒序)',
                               title_text="岗位总工时占比",
                               annotations=[dict(text='实际', x=0.205, y=0.5, font_size=20, showarrow=False),
                                            dict(text='理论', x=0.795, y=0.5, font_size=20, showarrow=False)])
    return fig岗位pie




def figDcppie(dataLast, type, dataNew, title):
    labelsdcp = list(dcppie(dataNew, type)[type])
    figDcppie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    figDcppie.add_trace(go.Pie(labels=labelsdcp, values=list(dcppie(dataLast, type)['费用(元)']), name="上月"), 1, 1)
    figDcppie.add_trace(go.Pie(labels=labelsdcp, values=list(dcppie(dataNew, type)['费用(元)']), name="本月"), 1, 2)
    figDcppie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    figDcppie.update_traces(textposition='inside')
    figDcppie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text=type,
                               title_text=title,
                               annotations=[dict(text='上月', x=0.205, y=0.5, font_size=18, showarrow=False),
                                            dict(text='本月', x=0.795, y=0.5, font_size=18, showarrow=False)])
    return figDcppie



def figWBSTypepie(data, title):
    act = wbs类型pie(data, '实际人天').reset_index()
    est = wbs类型pie(data, '预估人天').reset_index()
    labels业务线 = list(act['WBS类型'])
    fig业务线pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(act['实际人天']), name="实际"), 1, 1)
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(est['预估人天']), name="预估"), 1, 2)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='WBS类型实际人天 (按占比倒序)',
                               title_text=title,
                               annotations=[dict(text='实际', x=0.205, y=0.5, font_size=18, showarrow=False),
                                            dict(text='预估', x=0.795, y=0.5, font_size=18, showarrow=False)])
    return fig业务线pie

def figWBSTypepie细分(data, month):
    act = wbs类型pie细分(data,'实际人天').reset_index()
    est = wbs类型pie细分(data,'预估人天').reset_index()
    labels业务线 = list(act['WBS类型'])
    fig业务线pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(act['实际人天']), name="实际"), 1, 1)
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(est['预估人天']), name="预估"), 1, 2)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+percent+name+value", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text='WBS类型实际人天 (按占比倒序)',
                               title_text= str(month)+"月WBS类型实际人天占比",
                               annotations=[dict(text='实际', x=0.205, y=0.5, font_size=18, showarrow=False),
                                            dict(text='预估', x=0.795, y=0.5, font_size=18, showarrow=False)])
    return fig业务线pie


def figWBSTypepie细分2(data, value, month):
    act = wbs类型pie细分(data,value).reset_index()
    labels业务线 = list(act['WBS类型'])
    fig业务线pie = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(act[value]), ), 1, 1)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+value+percent", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(
        uniformtext_minsize=15,
        uniformtext_mode='hide',legend_title_text="WBS类型"+value,
                               title_text= str(month) + "月WBS类型"+value+"占比",
                               annotations=[dict(text=value, x=0.5, y=0.5,  showarrow=False)])
    return fig业务线pie


def figWBSpie员工组(data,groupBy, month):
    act = wbs员工组pie细分(data, groupBy).reset_index()
    labels业务线 = list(act[groupBy])
    fig业务线pie = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(act["实际人天"])), 1, 1)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+value+percent", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text=groupBy,
                               title_text= str(month) + "月"+groupBy+"实际人天占比",
                               annotations=[dict(text="实际人天", x=0.5, y=0.5,  showarrow=False)])
    return fig业务线pie



def figNotActiveWBSpie(data, groupBy, month):
    act = notActiveWbs_pie(data).reset_index()
    labels业务线 = list(act[groupBy])
    fig业务线pie = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])
    fig业务线pie.add_trace(go.Pie(labels=labels业务线, values=list(act["项目名称"])), 1, 1)
    fig业务线pie.update_traces(hole=.4, hoverinfo="label+value+percent", textinfo='label+value+percent')
    fig业务线pie.update_traces(textposition='inside')
    fig业务线pie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',legend_title_text=groupBy+"项目个数",
                               title_text= str(month) + "月起近四个月内WBS活跃时长的项目数占比",
                               annotations=[dict(text="项目数", x=0.5, y=0.5,  showarrow=False)])
    return fig业务线pie




def fig员工部门员工组(data, title):
    fig员工部门员工组 = px.bar(data, x="工时类别", y="总人天", facet_col="员工所属部门", color="员工组", text_auto=True)
    fig员工部门员工组.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门员工组.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门员工组.update_xaxes(categoryorder = 'total ascending')
    return fig员工部门员工组


def fig员工部门员工组资源池细分(name):
    fig员工部门员工组 = px.bar(理论实际业务线汇总资源池细分(name), x="工时类别", y="总人天", facet_col="员工所属部门", color="员工组", text_auto=True)
    fig员工部门员工组.update_layout(title='资源池员工组人天', yaxis_title='总实际人天')
    fig员工部门员工组.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门员工组.update_xaxes(categoryorder = 'total ascending')
    return fig员工部门员工组


def fig员工部门员工组资源池细分BL(data, name, month):
    fig员工部门员工组 = px.bar(理论实际业务线汇总资源池细分BL(data, name), x="工时类别", y="总人天", facet_col="资源池", color="员工组", text_auto=True)
    fig员工部门员工组.update_layout(title=str(month)+'月员工所属部门员工组人天', yaxis_title='总实际人天')
    fig员工部门员工组.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门员工组.update_xaxes(categoryorder = 'total ascending')
    return fig员工部门员工组


def fig员工部门资源池(data, title):
    fig员工部门资源池 = px.bar(data, x="工时类别", y="总人天", facet_col="员工所属部门", color="资源池", text_auto=True)
    fig员工部门资源池.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门资源池.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门资源池.update_xaxes(categoryorder='total ascending')
    return fig员工部门资源池

def fig员工部门岗位名称(data, title):
    fig员工部门岗位名称 = px.bar(data, x="工时类别", y="总人天", facet_col="员工所属部门", color="岗位名称", text_auto=True)
    fig员工部门岗位名称.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门岗位名称.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门岗位名称.update_xaxes(categoryorder='total ascending')
    return fig员工部门岗位名称

def fig员工部门岗位名称资源池细分(name):
    fig员工部门岗位名称 = px.bar(理论实际岗位名称汇总资源池细分(name), x="工时类别", y="总人天", facet_col="员工所属部门", color="岗位名称", text_auto=True)
    fig员工部门岗位名称.update_layout(title='资源池岗位名称人天', yaxis_title='总实际人天')
    fig员工部门岗位名称.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门岗位名称.update_xaxes(categoryorder='total ascending')
    return fig员工部门岗位名称


def fig员工部门岗位名称资源池细分BL(data, name, month):
    fig员工部门岗位名称 = px.bar(理论实际岗位名称汇总资源池细分BL(data, name), x="工时类别", y="总人天", facet_col="资源池", color="岗位名称", text_auto=True)
    fig员工部门岗位名称.update_layout(title=str(month)+'月员工所属部门岗位名称人天', yaxis_title='总实际人天')
    fig员工部门岗位名称.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门岗位名称.update_xaxes(categoryorder='total ascending')
    return fig员工部门岗位名称



def fig资源池员工部门员工组(data, title):
    fig员工部门员工组 = px.bar(data, x="工时类别", y="总人天", facet_col="资源池", color="员工组", text_auto=True)
    fig员工部门员工组.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门员工组.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig员工部门员工组

def fig资源池员工部门资源池(data, title):
    fig员工部门资源池 = px.bar(data, x="工时类别", y="总人天", facet_col="资源池", color="员工所属部门", text_auto=True)
    fig员工部门资源池.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门资源池.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig员工部门资源池

def fig资源池员工部门岗位名称(data, title):
    fig员工部门岗位名称 = px.bar(data, x="工时类别", y="总人天", facet_col="资源池", color="岗位名称", text_auto=True)
    fig员工部门岗位名称.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门岗位名称.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig员工部门岗位名称


def fig员工部门不同维度wbs(data, color, title):
    fig员工部门不同维度 = px.bar(data, x="工时类别", y="总人天", facet_col="员工所属部门", color=color, text_auto=True)
    fig员工部门不同维度.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门不同维度.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig员工部门不同维度



def fig员工部门不同维度wbs2(data, color, title, facet_col):
    fig员工部门不同维度 = px.bar(data, x="工时类别", y="总人天", facet_col=facet_col, color=color, text_auto=True)
    fig员工部门不同维度.update_layout(title=title, yaxis_title='总实际人天')
    fig员工部门不同维度.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig员工部门不同维度


def fig员工部门不同维度wbs22(data, axis, color, title):
    data = groupBy_act_days_percentage(data, axis)
    data = replaceDF(data)
    fig员工部门不同维度 = px.bar(data, x="总人天", y=axis,  color=color, text_auto=True)
    fig员工部门不同维度.update_layout(title=title, template='plotly_white', yaxis_title='总实际人天', yaxis={'categoryorder':'total ascending'})
    fig员工部门不同维度.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig员工部门不同维度.update_traces(
        # textfont_size=8,
        textangle=0)
    # fig员工部门不同维度.update_layout(
    #     yaxis=dict(
    #         tickfont=dict(size=10)),
    # ),
    return fig员工部门不同维度

def fig集群分区不同维度gpu(data, color, title, yaxis):
    fig集群分区不同维度 = px.bar(data, x="类别", y=yaxis, facet_col="分区", color=color, text_auto=True)
    fig集群分区不同维度.update_layout(title=title, yaxis_title=yaxis)
    fig集群分区不同维度.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig集群分区不同维度

def fig集群分区不同维度gpuRelative(data, color, title, yaxis):
    fig集群分区不同维度 = px.bar(data, x="类别", y=yaxis, facet_col="分区", color=color, text_auto=True)
    fig集群分区不同维度.update_layout(title=title, yaxis_title=yaxis)
    fig集群分区不同维度.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig集群分区不同维度.update_layout(barmode='relative')
    return fig集群分区不同维度


def fig固定资产detail不同Attri(data, color, title, yaxis, axisPercentage, facCol):
    fig固定资产detail不同Attri = px.bar(data, x=axisPercentage, y=yaxis, facet_col=facCol, color=color, text_auto=True)
    fig固定资产detail不同Attri.update_layout(title=title, yaxis_title=yaxis)
    fig固定资产detail不同Attri.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig固定资产detail不同Attri


def fig固定资产detail不同员工部门(data, color, title, yaxis):
    fig固定资产detail不同员工部门 = px.bar(data, x="金额占比", y=yaxis, facet_col="员工所属部门", color=color, text_auto=True)
    fig固定资产detail不同员工部门.update_layout(title=title, yaxis_title=yaxis)
    fig固定资产detail不同员工部门.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig固定资产detail不同员工部门


def fig固定资产detail不同员工部门数量(data, color, title, yaxis):
    fig固定资产detail不同员工部门 = px.bar(data, x="个数占比", y=yaxis, facet_col="员工所属部门", color=color, text_auto=True)
    fig固定资产detail不同员工部门.update_layout(title=title, yaxis_title=yaxis)
    fig固定资产detail不同员工部门.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig固定资产detail不同员工部门


def fig固定资产detail不同月(data, color, title, yaxis, xaxis, facet_col):
    fig固定资产detail不同月 = px.bar(data, x=xaxis, y=yaxis, facet_col=facet_col, color=color, text_auto=True)
    fig固定资产detail不同月.update_layout(title=title, yaxis_title=yaxis)
    fig固定资产detail不同月.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig固定资产detail不同月





def fig固定资产detail不同资源池(data, color, title, yaxis):
    fig固定资产detail不同资源池 = px.bar(data, x="金额占比", y=yaxis, facet_col="资源池", color=color, text_auto=True)
    fig固定资产detail不同资源池.update_layout(title=title, yaxis_title=yaxis)
    fig固定资产detail不同资源池.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig固定资产detail不同资源池



def fig固定资产detail不同资源池数量(data, color, title, yaxis):
    fig固定资产detail不同资源池 = px.bar(data, x="个数占比", y=yaxis, facet_col="资源池", color=color, text_auto=True)
    fig固定资产detail不同资源池.update_layout(title=title, yaxis_title=yaxis)
    fig固定资产detail不同资源池.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig固定资产detail不同资源池


def fig员工历史wbs人天(data):
    fig员工历史wbs人天 = px.bar(对比部门汇总4(data, '预估人天','实际人天'), x="工时类别", y="总人天", facet_col="工时月份", color="项目名称", text_auto=True)
    fig员工历史wbs人天.update_layout(title='员工历史WBS人天', height=600, yaxis_title='总人天',
                                     hovermode="x unified",
                                     xaxis=dict(
                                         showspikes=True,
                                         spikethickness=2,
                                         spikedash="dot",
                                         spikecolor="#999999",
                                         spikemode="across",
                                     ),
                                     )
    fig员工历史wbs人天.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig员工历史wbs人天


def fig历史wbs人天(data,color):
    fig历史wbs人天 = px.bar(对比wbs汇总(data, color, '预估人天','实际人天'), x="工时类别", y="总人天", facet_col="工时月份", color=color, text_auto=True)
    fig历史wbs人天.update_layout(title='历史WBS项目人天', height=600, yaxis_title='总人天',
                                     )
    fig历史wbs人天.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig历史wbs人天




def fig员工历史人天(data):
    fig员工历史人天 = go.Figure()
    fig员工历史人天.add_trace(go.Scatter(
        y=list(data.预估人天),
        x=list(data.工时月份),
        mode="markers+lines",
        name="预估人天",
        line=dict(
            color="black")))
    fig员工历史人天.add_trace(go.Scatter(
        y=list(data.理论人天),
        x=list(data.工时月份),
        mode="markers",
        name="理论人天",
        marker=dict(
            color="red", size=10,line=dict(
            color='MediumPurple',
            width=2),)))
    fig员工历史人天.add_trace(go.Scatter(
        y=list(data.实际人天),
        x=list(data.工时月份),
        mode="markers+lines",
        name="实际人天",
        line=dict(
            color="blue",width=3,)))
    fig员工历史人天.update_layout(title='员工历史人天', height=400, template='plotly_white',
                                  xaxis_title='工时月份', yaxis_title='总人天',
                                  hovermode="x",
                                  xaxis=dict(
                                      showspikes=True,
                                      spikethickness=2,
                                      spikedash="dot",
                                      spikecolor="#999999",
                                      spikemode="across",
                                  ),
                                  )
    return fig员工历史人天


def fig历史实际人均人天(data):
    fig历史实际人均人天 = px.line(data, x="月份", y=data.columns,
              # hover_data={"月份": "x"},
              title='部门实际人均人天趋势',
            )
    fig历史实际人均人天.update_layout(yaxis_title='实际人均人天',template='plotly_white',
                                      legend_title_text='员工所属部门',
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史实际人均人天


def fig历史实际人均人天细分(data):
    fig历史实际人均人天 = px.line(data, x="月份", y=data.columns,
              # hover_data={"月份": "x"},
              title='实际人均人天趋势',
            )
    fig历史实际人均人天.update_layout(yaxis_title='实际人均人天',template='plotly_white',
                                      legend_title_text='员工所属部门',
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史实际人均人天


def fig历史实际人均人天_irdc(data):
    fig历史实际人均人天_irdc = px.line(data[['月份','海外研发中心']], x="月份", y=data[['月份','海外研发中心']].columns,
              # hover_data={"月份": "x"},
              title='部门实际人均人天趋势',
            )
    fig历史实际人均人天_irdc.update_layout(yaxis_title='实际人均人天',template='plotly_white', legend_title_text='IRDC')
    return fig历史实际人均人天_irdc


def fig历史固定资产金额(data, type, toavg):
    data = data[data['用途'] == type].reset_index(drop= True)
    data = data[data['类别'] == toavg].reset_index(drop=True)[['月份','总值','净值','折旧']]
    if toavg =='Total':
        title = '历史'+type+'总资产趋势'
    elif toavg =='Avg':
        title = '历史'+type+'人均资产趋势'

    fig历史固定资产金额 = px.line(data, x="月份", y=data.columns,
              title= title,
            )
    fig历史固定资产金额.update_layout(yaxis_title='资产金额CNY',template='plotly_white',
                                      legend_title_text='金额类别',
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史固定资产金额


def fig历史理论填报率():
    fig历史理论填报率 = px.line(all_logic_percentage, x="月份", y=all_logic_percentage.columns,
              # hover_data={"月份": "|%B, %Y"},
              title='部门填报率')
    fig历史理论填报率.update_layout(yaxis_title='理论填报率',template='plotly_white',
                                    legend_title_text='员工所属部门',
                                    hovermode="x",
                                    xaxis=dict(
                                        showspikes=True,
                                        spikethickness=2,
                                        spikedash="dot",
                                        spikecolor="#999999",
                                        spikemode="across",
                                    ),
                                    )
    return fig历史理论填报率


def fig历史理论填报率_irdc():
    fig历史理论填报率_irdc = px.line(all_logic_percentage[['月份','海外研发中心']], x="月份", y=all_logic_percentage[['月份','海外研发中心']].columns,
              # hover_data={"月份": "|%B, %Y"},
              title='部门填报率')
    fig历史理论填报率_irdc.update_layout(yaxis_title='理论填报率', template='plotly_white',legend_title_text='IRDC')
    return fig历史理论填报率_irdc


def fig全量实际vs理论人天():
    fig全量实际vs理论人天 = px.scatter(cur_mon_staff, x="实际人天", y="理论人天", color="员工所属部门",
                                       size="实际人天", hover_data=['员工姓名','员工组','资源池','岗位名称'])
    fig全量实际vs理论人天.update_layout(
        title='员工"实际人天"v."理论人天"',
        xaxis=dict(
            title='实际人天',
            gridcolor='white',
            gridwidth=2,
        ),
        yaxis=dict(
            title='理论人天',
            gridcolor='white',
            gridwidth=2,
        ),
    )
    return fig全量实际vs理论人天

def fig全量实际vs预估人天():
    fig全量实际vs预估人天 = px.scatter(cur_mon_staff, x="实际人天", y="预估人天", color="员工所属部门",
                                       size="实际人天", hover_data=['员工姓名','员工组','资源池','岗位名称'])
    fig全量实际vs预估人天.update_layout(
        title='员工"实际人天"v."预估人天"',
        xaxis=dict(
            title='实际人天',
            gridcolor='white',
            gridwidth=2,
        ),
        yaxis=dict(
            title='预估人天',
            gridcolor='white',
            gridwidth=2,
        ),
    )
    return fig全量实际vs预估人天

def figUserHistoryWBSDays(data):
    fig = go.Figure()
    # data = data.groupby(['工时年份', '工时月份']).sum('实际人天')
    fig.add_trace(go.Scatter(y = list(data.工时月份), x = list(data.实际人天),
                             mode='lines+markers',
                             name='实际人天'))
    fig.add_trace(go.Scatter(y = list(data.工时月份), x = list(data.预估人天),
                             mode='lines+markers',
                             name='预估人天'))
    fig.update_layout(title='员工历史实际人天趋势', yaxis_title='实际人天',template='plotly_white')
    return fig


def fig理论填报分布():
    理论填报filterData = cur_mon_staff[['员工姓名','理论填报']]
    fig理论填报分布 = px.pie(理论填报filterData, values=理论填报filterData['理论填报'].value_counts().values,
                             names=理论填报filterData['理论填报'].value_counts().index)
    # fig理论填报分布.update_traces(hoverinfo='label+percent', textinfo='value')
    fig理论填报分布.update_layout(
        title='理论填报情况',
    )
    return fig理论填报分布

def fig未填工时分布():
    未填工时filterData = 本月未填工时名单()
    fig未填工时分布 = px.pie(未填工时filterData, values=未填工时filterData['员工所属部门'].value_counts().values,
                             names=未填工时filterData['员工所属部门'].value_counts().index)
    fig未填工时分布.update_layout(
        title='未填工时情况',
    )
    return fig未填工时分布

def fig标注数据包打回():
    fig标注数据包打回 = px.pie(data_back_biaozhu(), values=data_back_biaozhu()['业务线'].value_counts().values,
                             names=data_back_biaozhu()['业务线'].value_counts().index)
    fig标注数据包打回.update_layout(
        title='标注验收有数据包打回情况',
    )
    return fig标注数据包打回

def fig标注任务延期():
    fig标注任务延期 = px.pie(data_delay_biaozhu(), values=data_delay_biaozhu()['业务线'].value_counts().values,
                             names=data_delay_biaozhu()['业务线'].value_counts().index)
    fig标注任务延期.update_layout(
        title='标注任务延期超过5天情况',
    )
    return fig标注任务延期



def figWBS部门pie():
    labelsWBS = list(实际部门wbspie['实际人天'].keys())
    figWBSpie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    figWBSpie.add_trace(go.Pie(labels=labelsWBS, values=list(实际部门wbspie['实际人天']), name="实际"), 1, 1)
    figWBSpie.add_trace(go.Pie(labels=labelsWBS, values=list(预估部门wbspie['预估人天']), name="预估"), 1, 2)
    figWBSpie.update_traces(hole=.4, hoverinfo="label+percent+name")
    figWBSpie.update_traces(textposition='inside')
    figWBSpie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',
                               title_text="WBS部门总工时",
                               annotations=[dict(text='实际', x=0.205, y=0.5, font_size=20, showarrow=False),
                                            dict(text='预估', x=0.795, y=0.5, font_size=20, showarrow=False)])
    return figWBSpie


def figWBS类型pie():
    labelsWBS = list(实际类型wbspie['实际人天'].keys())
    figWBSpie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    figWBSpie.add_trace(go.Pie(labels=labelsWBS, values=list(实际类型wbspie['实际人天']), name="实际"), 1, 1)
    figWBSpie.add_trace(go.Pie(labels=labelsWBS, values=list(预估类型wbspie['预估人天']), name="预估"), 1, 2)
    figWBSpie.update_traces(hole=.4, hoverinfo="label+percent+name")
    figWBSpie.update_traces(textposition='inside')
    figWBSpie.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',
                               title_text="WBS类型总工时",
                               annotations=[dict(text='实际', x=0.205, y=0.5, font_size=20, showarrow=False),
                                            dict(text='预估', x=0.795, y=0.5, font_size=20, showarrow=False)])
    return figWBSpie


def figWBS预估填报分布():
    理论填报filterData = 本月WBS维度()[['WBS所属部门', '项目编号', '项目名称', 'WBS类型', 'PM姓名', '实际人天', '预估人天','预估填报率','预估填报']]
    fig理论填报分布 = px.pie(理论填报filterData, values=理论填报filterData['预估填报'].value_counts().values,
                             names=理论填报filterData['预估填报'].value_counts().index)
    # fig理论填报分布.update_traces(hoverinfo='label+percent', textinfo='value')
    fig理论填报分布.update_layout(
        title='预估WBS填报情况',
    )
    return fig理论填报分布

def figWBS预估填报异常部门分布():
    fig理论填报分布 = px.pie(logic_rate_abnormal_tb_WBS(), values=logic_rate_abnormal_tb_WBS()['WBS所属部门'].value_counts().values,
                             names=logic_rate_abnormal_tb_WBS()['WBS所属部门'].value_counts().index)
    # fig理论填报分布.update_traces(hoverinfo='label+percent', textinfo='value')
    fig理论填报分布.update_layout(
        title='WBS部门填报异常个数',
    )
    return fig理论填报分布

def figWBStop5填报分布(data, title):
    fig理论填报分布 = px.pie(wbs_top5_distribution(data), values='实际人天',
                             names='Rate')
    fig理论填报分布.update_layout(
        title=title,
    )
    return fig理论填报分布

def figWBStop填报分布Filter(data, month):
    fig理论填报分布 = px.pie(data, values='实际人天',
                             names='项目名称')
    fig理论填报分布.update_layout(
        title= str(month) + '月WBS实际人天占比',
    )
    # fig理论填报分布.update_traces(hoverinfo="name+value+percent", textinfo='value+percent')
    return fig理论填报分布

def figWBStop5填报类型分布():
    data = wbs_top5_distribution().groupby(['WBS类型']).agg({'实际人天':'sum'}).reset_index()
    others_act_days = 本月WBS维度()['实际人天'].sum() - data['实际人天'].sum()
    other_row = {'实际人天':others_act_days,'WBS类型':'非Top10WBS'}
    data = data.append(other_row, ignore_index=True)
    fig理论填报分布 = px.pie(data, values='实际人天',
                             names='WBS类型')
    fig理论填报分布.update_layout(
        title='Top10 WBS实际人天的类型占比',
    )
    return fig理论填报分布


def figBZBilltop5分布():
    fig理论填报分布 = px.pie(biaozhu_top5_distribution(), values='费用（元）',
                             names='Rate')
    fig理论填报分布.update_layout(
        title='标注任务费用Top10占比情况',
    )
    return fig理论填报分布


def figWBS预估无实际分布():
    未填报filterData = est_no_act_df()
    fig理论填报分布 = px.pie(未填报filterData, values=未填报filterData['WBS所属部门'].value_counts().values,
                             names=未填报filterData['WBS所属部门'].value_counts().index)
    # fig理论填报分布.update_traces(hoverinfo='label+percent', textinfo='value')
    fig理论填报分布.update_layout(
        title='预估并未实际填写WBS情况',
    )
    return fig理论填报分布

def figWBS实际未预估填报分布():
    未填报filterData = act_no_est_df()
    fig理论填报分布 = px.pie(未填报filterData, values=未填报filterData['WBS所属部门'].value_counts().values,
                             names=未填报filterData['WBS所属部门'].value_counts().index)
    # fig理论填报分布.update_traces(hoverinfo='label+percent', textinfo='value')
    fig理论填报分布.update_layout(
        title='实际填写并未预估WBS情况',
    )
    return fig理论填报分布

def figWBS连续预估2月未填写分布():
    fig理论填报分布 = px.pie(est_twice_wbs(), values=est_twice_wbs()['WBS所属部门'].value_counts().values,
                             names=est_twice_wbs()['WBS所属部门'].value_counts().index)
    # fig理论填报分布.update_traces(hoverinfo='label+percent', textinfo='value')
    fig理论填报分布.update_layout(
        title='连续两月预估无实际填写WBS情况',
    )
    return fig理论填报分布

# def figWBS超过1年分布():
#     fig未填工时分布 = px.pie(get_more_than1yr_wbs(), values=get_more_than1yr_wbs()['WBS所属部门'].value_counts().values,
#                              names=get_more_than1yr_wbs()['WBS所属部门'].value_counts().index)
#     fig未填工时分布.update_layout(
#         title='建立超过1年WBS情况',
#     )
#     return fig未填工时分布

def figWBS部门Top5(data, title):
    figWBS部门Top5 = go.Figure()
    data = wbs_top5_actual(data).sort_values(by='实际人天', ascending=True)
    figWBS部门Top5.add_bar(y=list(data.项目名称)
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="auto"
                                , name="实际人天",orientation='h')
    figWBS部门Top5.update_layout(title=title, template='plotly_white', xaxis_title='总人天',)
    figWBS部门Top5.update_traces(
        # textfont_size=12,
        textangle=0, textposition="outside", cliponaxis=False)
    return figWBS部门Top5


def figWBS部门Top(data, month):
    figWBS部门Top = go.Figure()
    data = data[data['WBS类型'] != 'Z'].reset_index(drop=True)

    data = data.sort_values(by='实际人天', ascending=True).tail(10)

    figWBS部门Top.add_bar(y=list(data.项目名称)
                                , x=list(data.实际人天), text=list(data.实际人天), textposition="outside", cliponaxis=False, textangle = 0
                                , name="实际人天",orientation='h')
    figWBS部门Top.update_layout(title= str(month) + '月WBS项目TOP10实际人天', template='plotly_white', xaxis_title='总人天',)
    # figWBS部门Top.update_layout(
    #     yaxis=dict(tickfont=dict(size=10)),)
    figWBS部门Top.update_layout(
        yaxis={
            'tickmode': 'array',
            'tickvals': list(range(len(renameDf(data)))),
            'ticktext': renameDf(data)['项目名称'].tolist(),
        }
    )

    return figWBS部门Top

def figGpuUserTop10():
    figGpuUserTop10 = go.Figure()
    data = clean_gpu_avg_sum_nodes(monthly_gpu())
    figGpuUserTop10.add_bar(y=list(data.用户)
                                , x=list(data.使用节点数), text=list(data.使用节点数), textposition="auto"
                                , name="使用节点数",orientation='h')
    figGpuUserTop10.update_layout(title='本月用户累计使用GPU节点（按使用节点数倒序排序）', template='plotly_white', xaxis_title='累计使用节点数',)
    return figGpuUserTop10


def fig资产Top10(df, type, property_values):
    fig资产Top10 = go.Figure()
    data = df.sort_values(by=[property_values], ascending=True).reset_index(drop=True)
    fig资产Top10.add_bar(y=list(data.实际保管人)
                                , x=list(data[property_values]), text=list(data[property_values]), textposition="auto"
                                , name=property_values,orientation='h')
    fig资产Top10.update_layout(title='本月'+type+'资产'+property_values+'Top 10', template='plotly_white', xaxis_title='资产金额CNY',)
    return fig资产Top10


def figGpuUserTimeTop10():
    figGpuUserTop10 = go.Figure()
    data = clean_gpu_avg_sum_time(monthly_gpu())
    figGpuUserTop10.add_bar(y=list(data.用户)
                                , x=list(data.累计使用时长), text=list(data.累计使用时长), textposition="auto"
                                , name="累计使用时长",orientation='h')
    figGpuUserTop10.update_layout(title='本月用户累计使用时长（按累计使用时长倒序排序）', template='plotly_white', xaxis_title='累计使用时长',)
    return figGpuUserTop10

def figGpuUserTimeTop10资源池(data):
    figGpuUserTop10 = go.Figure()
    data = clean_gpu_avg_sum_time(data)
    figGpuUserTop10.add_bar(y=list(data.用户)
                                , x=list(data.累计使用时长), text=list(data.累计使用时长), textposition="auto"
                                , name="累计使用时长",orientation='h')
    figGpuUserTop10.update_layout(title='本月用户累计使用时长（按累计使用时长倒序排序）', template='plotly_white', xaxis_title='累计使用时长',)
    return figGpuUserTop10


def figBZBillTop5():
    figWBS部门Top5 = go.Figure()
    data = bzBill_top5()
    figWBS部门Top5.add_bar(y=list(data['Rate'])
                                , x=list(data['费用（元）']), text=list(data['费用（元）']), textposition="auto"
                                , name="费用（元）",orientation='h')
    figWBS部门Top5.update_layout(title='标注任务费用TOP5', template='plotly_white', yaxis_title='费用（元）',)
    return figWBS部门Top5


def fig历史WBS类型(data):
    fig历史WBS类型 = px.line(data, x="月份", y=data.columns,
              title='WBS类型实际人天趋势',)
    fig历史WBS类型.update_layout(yaxis_title='实际总人天',template='plotly_white',
                                 legend_title_text='WBS类型',
                                 hovermode="x unified",
                                 xaxis=dict(
                                     showspikes=True,
                                     spikethickness=2,
                                     spikedash="dot",
                                     spikecolor="#999999",
                                     spikemode="across",
                                 ),
                                 )
    return fig历史WBS类型



def fig历史gpu使用(data, x, y, title, color):
    fig历史gpu使用 = px.line(data, x=x,  y=y, color=color,
              title=title,template='plotly_white')
    fig历史gpu使用.update_layout(legend_title_text=color,
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史gpu使用



def fig历史gpu使用具体时间点(data, time, x, y, title):
    data = data[data['Time'] == time]
    fig历史gpu使用 = px.line(data, x=x,  y=y, color='分区',
              title=title,template='plotly_white')
    fig历史gpu使用.update_layout(legend_title_text='分区',
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史gpu使用




def fig历史业务线采标费用(df,title):
    fig2 = go.Figure()
    histroy = df
    num = 1
    for i in range(len(list(set(histroy['月份'])))):
        index = []
        for i in range(len(histroy)):
            if int(histroy.loc[i, '月份'][0]) == num:
                index.append(i)

        temp = histroy.iloc[index].reset_index(drop=True)
        num += 1

        fig2.add_trace(go.Bar(
            y=list(temp['业务线']),
            x=list(temp['费用']), text=list(temp['费用']), textposition="auto",
            name=temp.loc[0, '月份'],
            orientation='h',
        ))

    fig2.update_layout(barmode='stack', title= title,template='plotly_white')
    return fig2



def figDcpTop10(data):
    figDcpTop10 = go.Figure()
    data = dcpTop10(data)
    figDcpTop10.add_bar(y=list(data['用户名'])
                                , x=list(data['费用(元)']), text=list(data['费用(元)']), textposition="auto"
                                , name="费用(元)",orientation='h')
    figDcpTop10.update_layout(title='本月DCP费用(元)Top10', template='plotly_white', xaxis_title='费用(元)',)
    return figDcpTop10



def fig历史dcp():
    fig历史dcp = px.line(历史资源费用(), x="月份", y=历史资源费用().columns,
              # hover_data={"月份": "x"},
              title='部门历史资源费用(元)',
            )
    fig历史dcp.update_layout(yaxis_title='费用(元)',template='plotly_white', legend_title_text='资源类型')
    fig历史dcp.update_layout(legend_title_text='月份',
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史dcp


def fig历史资源费用(data):
    fig历史dcp = px.line(data, x="月份", y=data.columns,
              # hover_data={"月份": "x"},
              title='历史资源总费用(元)',
            )
    fig历史dcp.update_layout(yaxis_title='费用(元)',template='plotly_white', legend_title_text='资源类型')
    fig历史dcp.update_layout(legend_title_text='月份',
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史dcp


def fig历史gpu(data, title):
    fig历史gpu = px.line(data, x="月份", y=data.columns,
              title='部门历史GPU'+title,
            )
    fig历史gpu.update_layout(yaxis_title=title,template='plotly_white', legend_title_text='GPU类型')
    fig历史gpu.update_layout(legend_title_text='GPU卡类型',
                                      hovermode="x",
                                      xaxis=dict(
                                          showspikes=True,
                                          spikethickness=2,
                                          spikedash="dot",
                                          spikecolor="#999999",
                                          spikemode="across",
                                      ),
                                      )
    return fig历史gpu