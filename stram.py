import streamlit as st
from sqlalchemy import create_engine 
import psycopg2 
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh


# обновление данных кждые 10 секунд
st_autorefresh(interval=10000)


# Запрос выбора даты
# date_list = pd.read_sql("SELECT DISTINCT date FROM asdasdad ORDER BY date", con=conn)['date'].tolist()
# selected_date = st.sidebar.selectbox("Выберите дату", date_list)
# if selected_date:


# соеденение с базой данных
db = create_engine('postgresql+psycopg2://lol:dblol@127.0.0.1/mydblol') 
conn = db.connect() 
times_df = pd.read_sql("SELECT DISTINCT times FROM asdasdad ORDER BY times", con=conn)
times_list = times_df['times'].tolist()


# Боковая панель
with st.sidebar:

    tims1, tims2 = st.select_slider(
        "Select a range of times",
        options=times_list,
        value=(times_list[0], times_list[-1])
    )
    
    station = st.selectbox(
        "Select a range of station",
        options=pd.read_sql("SELECT DISTINCT station_id FROM asdasdad ORDER BY station_id", con=conn)
    )
    
# st.dataframe(pd.read_sql(f"select * from asdasdad where times between '{tims1}' and '{tims2}' AND station_id ='{station}'", con=conn))
st.write("______________________________________________________________________________________")


# SQL-запрос, вычисляющий загруженность станции в процентах относительно максимальной загруженности
st.title(f'Загруженность станции {station} в процентах относительно максимальной загруженности в заданные промежутки времени от {tims1} до {tims2}')
with db.connect() as connection:
    df = pd.read_sql(f"""SELECT 
   CONCAT(CAST(ROUND(passenger_count*100 / CAST(max_load AS FLOAT)) AS VARCHAR), ' ПРОЦЕНТОВ') AS lol 
FROM 
    asdasdad
    WHERE times between '{tims1}' and '{tims2}' AND station_id ='{station}';""", connection)
    try:
        zagruzka = df['lol'].iloc[0]
    except:
        zagruzka = 'в это время не хватает данных'
st.header(zagruzka)
st.write("______________________________________________________________________________________")

# SQL-запрос, вычисляющий топ загруженных станций

st.title('Топ загруженных станций')
with db.connect() as connection:
    df1 = pd.read_sql(f"""SELECT distinct(station_id) ,
   CONCAT(CAST(ROUND(passenger_count*100 / CAST(max_load AS FLOAT)) AS VARCHAR), ' процент') AS lol 
FROM 
    asdasdad
    WHERE times between '{tims1}' and '{tims2}' 
    order by lol
    asc 
    limit 3;""", connection)
    # обработка исключений
    top1 ="мало данных"
    top2 ="мало данных"
    top3 ="мало данных"
    try:

        top1 =  "Станция номер:"+ str(df1['station_id'].iloc[0]) + ", загруженость = " +str(df1['lol'].iloc[0]) 
        top2 = "Станция номер:"+ str(df1['station_id'].iloc[1]) + ", загруженость = " +str(df1['lol'].iloc[1])
        top3 = "Станция номер:"+ str(df1['station_id'].iloc[2]) + ", загруженость = " +str(df1['lol'].iloc[2])
    except:
        top1 ="мало данных"
        top2 ="мало данных"
        top3 ="мало данных"
st.header(f'Топ 1: {top1}')
st.header(f'Топ 2: {top2}')
st.header(f'Топ 3: {top3}')
st.write("______________________________________________________________________________________")


# SQL-запрос, вычисляющий среднее количество пассажиров на станциях

st.title('Среднее количество пассажиров на станциях')
with db.connect() as connection:
    df2 = pd.read_sql(f"""SELECT 
   avg(passenger_count) AS lol 
FROM 
    asdasdad
    WHERE times between '{tims1}' and '{tims2}';""", connection)
    try:
        count_stat = "Количество человек = "+str(round(df2['lol'].iloc[0]))
    except:
        count_stat = "нет данных в это время"
st.header(count_stat)
st.write("______________________________________________________________________________________")

# Продемонстрирован SQL-запрос, вычисляющий количество станций без инфраструктуры для маломобильных граждан


st.title('Количество станций без инфраструктуры для маломобильных граждан')
with db.connect() as connection:
    df3 = pd.read_sql(f"""SELECT 
   count(passenger_count) AS lol
FROM 
    asdasdad                   
    where station_id = {station};""", connection)
st.header(df3['lol'].iloc[0])
st.write("______________________________________________________________________________________")
df_time = pd.read_sql(f"select * from asdasdad", con=conn)
st.line_chart(df_time,x="passenger_count",y='max_load')
