# Base image
FROM ubuntu:18.04

# Install python, pip and it's dependencies
RUN apt-get update 
RUN apt-get install -y \
    python3.7\
    python3.7-dev\
    python3-pip
    
# Make python3.7 the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1

ENV APP_HOME=/app
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y \
    postgresql\
    postgresql-contrib\
    python-psycopg2\
    libpq-dev\
    libgl1-mesa-glx

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt $APP_HOME/requirements.txt
RUN pip install -r requirements.txt

# # copy project
COPY . $APP_HOME

EXPOSE 4141

ENV SECRET_KEY kenyacourts@peterappserverkey
ENV DB_HOST main-db.ctuuj30yb4vw.us-east-2.rds.amazonaws.com
ENV DB_PORT 5432
ENV DB_NAME kenyacourt
ENV DB_USER postgres
ENV DB_PASSWORD ycG7BRjK9LHmTQVt

# start app
CMD ["gunicorn", "--bind", "0.0.0.0:4141", "main.wsgi"]

