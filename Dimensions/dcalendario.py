import datetime
from datetime import date
import holidays
import pandas as pd
import calendar as c
import numpy as np
t_mes = {'id_mes':[1,2,3,4,5,6,7,8,9,10,11,12],
        'Mês':['01.Jan','02.Fev','03.Mar','04.Abr',
               '05.Mai','06.Jun','07.Jul','08.Ago',
               '09.Set','10.Out','11.Nov','12.Dez'],
        'comp':['01','02','03','04','05','06',
                '07','08','09','10','11','12']}
tab_m = pd.DataFrame(t_mes)
t_dia = {'id_dia':[0,1,2,3,4,5,6],
        'dia_semana':['seg','ter','qua','qui','sex','sab','dom']}
tab_d = pd.DataFrame(t_dia)
br_holidays = holidays.country_holidays('BR')
hoje = date.today()
ano= hoje.year
mes= hoje.month
cdg_m = str(ano)+'-'+str(mes)
dcstart = datetime.date(2022, 1, 1)
ld = c.monthrange(
    hoje.year,
    hoje.month)[1]
l_data = date(
    ano,
    mes,
    ld)
cld = pd.date_range(
    start=dcstart, 
    end=l_data)
datas = pd.DataFrame(
    {"Data":cld,
     "Ano":cld.year,
     "Trimestre":cld.quarter,
     "id_mes":cld.month,
     "Dia":cld.day,
     "id_dia":cld.weekday})

d_inicio = dcstart.year
d_fim = date.today().year+1
anos = list(range(d_inicio,d_fim))

f = sorted(
    holidays.BR(
        years=anos).items())
feriados = pd.DataFrame(
    data=f, 
    index=None).rename(columns={0: 'Data'}).rename(columns={1: 'Feriado'})
feriados['Data'] = pd.DataFrame(
    pd.to_datetime(
        feriados['Data'], 
	errors='coerce',
        format='%Y-%m-%d'))
dcalendario = datas.merge(
    feriados, 
    on='Data', 
    how='left').merge(tab_m, 
                      on='id_mes', 
                      how='left').merge(tab_d, 
                                        on='id_dia', 
                                        how='left')
dcalendario['m_relativo'] = dcalendario['Ano'].map(str)+"-"+dcalendario['Mês'].map(str)
dcalendario['comp'] = dcalendario['Ano'].map(str)+"-"+dcalendario['comp']
dcalendario['cdgm'] = dcalendario['Ano'].map(str)+"-"+dcalendario['id_mes'].map(str)
dcalendario['Período'] = np.where(
    dcalendario['cdgm'] == cdg_m, 
    'Mês Vigente', 
    dcalendario['Ano'].map(str)+"-"+dcalendario['Mês'].map(str))
dcalendario['d_util'] = np.where(dcalendario['Feriado'] == None ,dcalendario['dia_semana'].map(str),dcalendario['Feriado'].map(str))
dcalendario['d_util'] = np.where(dcalendario['d_util'] == 'nan' ,dcalendario['dia_semana'].map(str),dcalendario['Feriado'].map(str))
dcalendario['d_util'] = np.where(dcalendario['d_util'] == 'seg','Dia Útil',dcalendario['d_util'].map(str))
dcalendario['d_util'] = np.where(dcalendario['d_util'] == 'ter','Dia Útil',dcalendario['d_util'].map(str))
dcalendario['d_util'] = np.where(dcalendario['d_util'] == 'qua','Dia Útil',dcalendario['d_util'].map(str))
dcalendario['d_util'] = np.where(dcalendario['d_util'] == 'qui','Dia Útil',dcalendario['d_util'].map(str))
dcalendario['d_util'] = np.where(dcalendario['d_util'] == 'sex','Dia Útil',dcalendario['d_util'].map(str))
dcalendario['d_util'] = np.where(dcalendario['d_util'] == 'sab','Dia Útil',dcalendario['d_util'].map(str))
dcalendario = dcalendario.drop(columns=['id_mes', 'id_dia','Mês','m_relativo','cdgm'])
del(datas,feriados,tab_d,tab_m)
