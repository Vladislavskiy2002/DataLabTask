### Використовуйте офіційний образ Python
##FROM python:3.8
##
### Перемістіть робочу директорію в папку з вашим фронтендом
##WORKDIR /code/front
##
##FROM python:3.8
##COPY ./requirements.txt /requirements.txt
##RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt
##COPY . /code/front
##EXPOSE 8081
###CMD ["streamlit", "run", "app.py"]
###CMD ["streamlit", "run", "menu.py", "0.0.0.0", "--port", "81", "--reload", "--reload-dir", "/app"]
###CMD ["streamlit", "run", "menu.py", "--host", "0.0.0.0", "--server.port", "81", "--server.enableCORS", "false", "--reload", "--reload-dir", "/app"]
###CMD ["streamlit", "run", "menu.py", "--server.port", "81", "--server.enableCORS", "false", "--reload", "--reload-dir", "/app"]
##CMD ["streamlit", "run", "front/menu.py", "--server.port", "81", "--server.enableXsrfProtection", "false", "/app"]
#
#
## Використовуйте офіційний образ Python
#FROM python:3.8
#
## Перемістіть робочу директорію в папку з вашим фронтендом
#WORKDIR /front
#
## Копіюйте requirements.txt та встановіть залежності
##COPY ./requirements.txt /front/requirements.txt
##RUN pip install --no-cache-dir --upgrade -r /front/requirements.txt
#
## Копіюйте всі файли з поточного каталогу в контейнер
#COPY . /front/
#RUN pip install --no-cache-dir streamlit
## Відкрийте порт 8081 для Streamlit
#EXPOSE 8081
#
## Запустіть Streamlit, вказавши шлях до menu.py
#CMD ["streamlit", "run", "/front/menu.py", "--server.port", "81", "--server.enableXsrfProtection", "false"]

# Використовуйте офіційний образ Python
FROM python:3.8

# Перемістіть робочу директорію в папку з вашим фронтендом
WORKDIR /front

# Копіюйте всі файли з поточного каталогу в контейнер
COPY . /front/
RUN pip install --no-cache-dir streamlit
#
## Відкрийте порт 8081 для Streamlit
#EXPOSE 8081

# Запустіть Streamlit, вказавши шлях до menu.py
#CMD ["streamlit", "run", "menu.py", "--server.port", "81", "--server.enableXsrfProtection", "false"]
#CMD ["streamlit", "run", "menu.py"] working
CMD ["streamlit", "run", "menu.py","0.0.0.0", "--server.port", "8501"]
