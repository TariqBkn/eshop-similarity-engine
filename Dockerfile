FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python python-pip
RUN pip install --upgrade pip
#RUN apt install python-pip
RUN pip install mysql-connector
RUN pip install Flask
RUN pip install pandas
RUN pip install numpy
RUN pip install scikit-learn
RUN pip install Flask-RESTful
COPY . /opt/

EXPOSE 8080
ENTRYPOINT FLASK_APP=/opt/main_controller.py flask run --host=0.0.0.0 --port=8080