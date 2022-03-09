# set base image (host OS)
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
FROM python:3.8.6-buster

# set the working directory in the container
# WORKDIR /usr/src/ser

# copy the dependencies file to the working directory
COPY requirements.txt /requirements.txt
COPY SportsBook_model.joblib /SportsBook_modeljoblib


RUN apt-get -o Acquire::Max-FutureTime=86400 update \
  && apt-get upgrade -y \
  && apt-get install -y \
  && apt-get -y install apt-utils gcc libpq-dev libsndfile-dev

# install dependencies & upgrade
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ser /ser
COPY api /api

# When first connecting to GCP. Need creds
# COPY /Users/pankajpatel/.gcppankaj/wagon-bootcamp-322818-752a3eb15b98.json /wagon-bootcamp-322818-752a3eb15b98.json

# command to run on container start
# load web server with code autoreload
# CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT

# CMD streamlit run app.py  --server.port 8080
