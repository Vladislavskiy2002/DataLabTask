FROM python:3.8
WORKDIR /front
COPY . /front/
RUN pip install streamlit
RUN pip install psycopg2
RUN pip install plotly
CMD ["streamlit", "run", "menu.py","0.0.0.0", "--server.port", "8501"]