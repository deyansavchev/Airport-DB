import steamlit as st
import psycopg2
import pandas as pd

# 1.Връзка с база данни в pgAdmin
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Airport_DB",
        user="postgres",
        password="11062004",
        port="5432"
    )

st.title("Система за управление на летище")

# Меню за навигация (за справките от заданието)
option = st.sidebar.selectbox(
    'Изберете справка:',
    ['Начало', 'Списък на полети', 'Пътници и багаж', 'Продажба на билети']
)

if option == 'Списък на полети':
    st.header("Всички активни полети")
    conn = get_connection()
    # Изпълнение на заявка
    query = "SELECT * FROM Flight"
    df = pd.read_sql(query, conn)
    st.dataframe(df)
    conn.close()

elif option == 'Продажба на билет':
    st.header("Регистрация на нов билет")
    # CRUD
    with st.form("ticker_form"):
        flight_id = st.number_input("ID на полет", step=1)
        price = st.number_input("Цена")
        seat = st.text_input("Място")
        submitted = st.form_submit("Запази билета")

        if submitted:
            # Stored procedure
            st.success("Билетът е успешно добавен в базата!")
