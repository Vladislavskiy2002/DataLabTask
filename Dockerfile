FROM python:3.8
COPY ./requirements.txt /requirements.txt
#
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./db.sql /docker-entrypoint-initdb.d/
COPY ./app /app
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "/app"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--reload-dir", "/app"]
#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "81", "--reload", "--reload-dir", "/app/pages"]

#FROM python:3.8
#
## Перемістіть робочу директорію в папку з вашим фронтендом
#WORKDIR /front
##
##COPY ./requirements.txt /requirements.txt
###
##RUN pip install --upgrade -r /requirements.txt
## Копіюйте всі файли з поточного каталогу в контейнер
#COPY . /front/
#RUN pip install streamlit
#RUN pip install psycopg2
##
### Відкрийте порт 8081 для Streamlit
##EXPOSE 8501
#
## Запустіть Streamlit, вказавши шлях до menu.py
##CMD ["streamlit", "run", "menu.py", "--server.port", "81", "--server.enableXsrfProtection", "false"]
##CMD ["streamlit", "run", "menu.py"] working
#CMD ["streamlit", "run", "menu.py","0.0.0.0", "--server.port", "8501"]
##CMD ["streamlit", "run", "menu.py"]