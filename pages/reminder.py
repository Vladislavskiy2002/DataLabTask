import streamlit as st
import time

# Встановлення нагадування
reminder_time = st.slider("Час нагадування (секунди):", min_value=1, max_value=60)
reminder_set = st.button("Встановити нагадування")

if reminder_set:
    st.success(f"Нагадування буде встановлено через {reminder_time} секунд.")

    # Затримка на 2 секунди
    time.sleep(2)

    # Відображення сповіщення браузера
    st.warning("Нагадування! Перевірте, що вам потрібно зробити.")
