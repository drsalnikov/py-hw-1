import time
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import duckdb as db
import seaborn as sns
from pathlib import Path

def preload_content():
    path = Path(__file__).parent

    bank = Image.open(f"{path}\\image\\bank.jpg")
    corr = Image.open(f"{path}\\image\\corr.png")
    pairplot = Image.open(f"{path}\\image\\pairplot.png")

    D_agreement = pd.read_csv(f"{path}\\datasets\\D_agreement.csv")
    D_clients = pd.read_csv(f"{path}\\datasets\\D_clients.csv")
    D_close_loan = pd.read_csv(f"{path}\\datasets\\D_close_loan.csv")
    D_job = pd.read_csv(f"{path}\\datasets\\D_job.csv")
    D_last_credit = pd.read_csv(f"{path}\\datasets\\D_last_credit.csv")
    D_loan = pd.read_csv(f"{path}\\datasets\\D_loan.csv")
    D_pens = pd.read_csv(f"{path}\\datasets\\D_pens.csv")
    D_salary = pd.read_csv(f"{path}\\datasets\\D_salary.csv")
    D_work = pd.read_csv(f"{path}\\datasets\\D_work.csv")

    D_client_loan = db.sql("SELECT l.ID_CLIENT, COUNT(l.ID_LOAN) as LOAN_NUM_TOTAL, SUM(cl.CLOSED_FL) as LOAN_NUM_CLOSED "
                        + " FROM D_loan l "
                        + " left join D_close_loan cl on l.ID_LOAN = cl.ID_LOAN "
                        + " GROUP BY l.ID_CLIENT"
                        + " HAVING COUNT(l.ID_LOAN) > 1"
                        ).fetchdf()
    
    df = db.sql("SELECT a.TARGET, c.ID as ID_CLIENT, a.AGREEMENT_RK, c.AGE, c.SOCSTATUS_WORK_FL, c.SOCSTATUS_PENS_FL, c.GENDER, c.CHILD_TOTAL, c.DEPENDANTS, "
                + " s.PERSONAL_INCOME, cl.LOAN_NUM_TOTAL, cl.LOAN_NUM_CLOSED "
                + " FROM D_agreement a "
                + " left join D_clients c on a.ID_CLIENT = c.ID "
                + " left join D_salary s on s.ID_CLIENT = c.ID "
                + " left join D_last_credit lc on lc.ID_CLIENT = c.ID "
                + " left join D_client_loan cl on cl.ID_CLIENT = c.ID "
                ).fetchdf()

    return df, bank, pairplot, corr


def render_page(df, bank, pairplot, corr):

    st.title('Эффективность взаимодействия банка с клиентами')
    st.subheader('Изучаем стримлит за 24 секунды')
    st.write('Материал - опросы клиентов по удовлетворенности')
    st.image(bank)

    st.sidebar.markdown("## Задание")
    st.sidebar.markdown('''Один из способов повысить эффективность взаимодействия банка с клиентами — отправлять предложение о новой услуге не всем клиентам,
     а только некоторым, которые выбираются по принципу наибольшей склонности к отклику на это предложение.  
    **Задача** заключается в том, чтобы предложить алгоритм, который будет выдавать склонность клиента к положительному или отрицательному отклику на предложение банка.
    Предполагается, что, получив такие оценки для некоторого множества клиентов, банк обратится с предложением только к тем, от кого ожидается положительный отклик.''')


    tab1, tab2, tab3, tab4 = st.tabs(
        [':mag: Попарные графики', ':mage: Корреляция', ':vertical_traffic_light: Данные', 'Предсказать'])

    with tab1:
        st.write('Исследуем наши данные :sparkles:')
        st.image(pairplot)

        # g = sns.pairplot(df, diag_kind="kde")
        # st.pyplot(g)

    with tab2:
        st.write('Строим матрицу корреляции')
        st.image(corr)

        # fig, ax = plt.subplots(figsize=(16, 16)) 
        # sns.heatmap(df.corr(), cmap='BuPu', annot=True, vmin=-1, vmax=1)
        # st.pyplot(fig)

    with tab3:
        st.write('**Что самое важное в данных?**')
        st.table(df.describe())

        st.write('**А что практически не важно?**')
        st.dataframe(df)

    with tab4:
        st.metric(label="Время вышло!", value="0 sec", delta="-24 sec")


def load_page():
    """ loads main page """
    df, bank, pairplot, corr = preload_content()
    st.set_page_config(layout="wide",
                       page_title="Эффективность взаимодействия банка с клиентами",
                       page_icon=':bank:')

    render_page(df, bank, pairplot, corr)


if __name__ == "__main__":
    load_page()
