import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from scipy import stats
from scipy.stats import mannwhitneyu

st.title("Homework_2")
uploaded_file = st.file_uploader("Выберите CSV или XLSX файл для загрузки", type = ['csv','xlsx'])

if uploaded_file is not None:
    dataset = pd.read_csv(uploaded_file)
    st.write(dataset)
else:
    st.warning("загрузите файл")


stolb_1 = st.selectbox(
    'Выберите первый столбик',
    options = dataset.columns,
    help= "Столбики не должны быть одинаковыми и данные должны быть одинакового типа",
    index = 5) #выпадающий список для выбора 1 столбика

stolb_2 = st.selectbox(
    'Выберите второй столбик',
    options = dataset.columns,
    index = 7) #выпадающий список для выбора 2 столбика

key = False #Условия для выбора столбиков
if stolb_1 == stolb_2:
    st.error("Выбрали одинаковые столбики")
    key = True
elif dataset[stolb_1].dtype != dataset[stolb_2].dtype:
    st.error("У столбиков разные типы данных")
    key = True 

if st.button("Создать общую гистограмму", disabled = key):
   fig = go.Figure()
   fig.add_trace(go.Histogram(x = dataset[stolb_1], name = stolb_1))
   fig.add_trace(go.Histogram(x = dataset[stolb_2], name = stolb_2))
   fig.update_layout( 
       xaxis_title = "Значение",
       yaxis_title = "Количество персонажей",
       #barmode='overlay' #наложение гистограмм друг на друга
   )
   st.plotly_chart(fig) #создание гистограммы с 1 и 2 столбиком
   

if st.button("Отдельные гистограммы", disabled = key):
    fig_1 = go.Figure(data=[go.Histogram(x = dataset[stolb_1], name = stolb_1)])
    fig_1.update_layout( 
       title=f"Гистограмма распределения {stolb_1}",
       xaxis_title = "Значение",
       yaxis_title = "Количество персонажей",
   )   
    st.plotly_chart(fig_1) #создание гистограммы 1 столбика
    
    fig_2 = go.Figure(data=[go.Histogram(x = dataset[stolb_2], name = stolb_2)])
    fig_2.update_layout( 
       title=f"Гистограмма распределения {stolb_2}",
       xaxis_title = "Значение",
       yaxis_title = "Количество персонажей",
   )   
    st.plotly_chart(fig_2) #создание гистограммы 1 столбика
    
algoritm = st.selectbox(
    'Выберите алгоритм теста гипотез',
    ("A/B тестирование","T-test","U-test")) #выпадающий список


if stolb_1 == stolb_2:
    st.error("Выбрали одинаковые столбики")
elif dataset[stolb_1].dtype != dataset[stolb_2].dtype:
    st.error("У столбиков разные типы данных")
elif algoritm == "A/B тестирование":
    mean_stolb_1 = dataset[stolb_1].mean()
    mean_stolb_2 = dataset[stolb_2].mean()
    st.write(f"среднее значение {stolb_1} = {mean_stolb_1 / 1:.4f}")
    st.write(f"среднее значение {stolb_2} = {mean_stolb_2 / 1:.4f}")
    st.write(f"A/B-тест — это эксперимент с двумя группами для определения лучшего из двух вариантов. При сравнении двух столбцов ({stolb_1} и {stolb_2}) видно, что среднее значение одного столбца больше, чем среднее згначение второго, а значит его выбор предпочтительнее.")

elif algoritm == "T-test":
    res = stats.ttest_ind(dataset[stolb_1], dataset[stolb_2], equal_var = False)
    
    st.write(f"p-value = {res.pvalue/ 1:.6}")
    st.write(f"p-value - это вероятность получить для данной вероятностной модели распределения значения случайной величины. Маленькие значения p-value показывают, что значения получены не случайно")
    
elif algoritm == "U-test":
    U_test = mannwhitneyu(dataset[stolb_1],dataset[stolb_2])
    st.write(f"p-value = {U_test.pvalue/ 1:.6}")
    st.write(f"Темт Манна-Уитни (U-Test), так же оценивает значимость как и t-test, только он менее чувствителен к нормальности распрежделения. Чем меньше значение p-value, тем меньше вероятность что значения получены случайно")

    

    