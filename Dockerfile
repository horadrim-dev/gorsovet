FROM python:3.11-alpine

ENV PYTHONBUFFERED 1

RUN mkdir /app
WORKDIR /app

# install psycopg2 dependencies
RUN apk update && apk add --update py3-pip \
	&& apk add  postgresql-dev gcc freetype-dev python3-dev musl-dev jpeg-dev zlib-dev \
	graphviz-dev \
	curl 

# mysql dependencies
# RUN apk add pkg-config  
# RUN apk add libmysqlclient-dev 
RUN apk add mysql-dev


	#python3-setuptools
	
 
# install dependencies
RUN pip install --upgrade pip
RUN pip install "setuptools<58.0.0" wheel

COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

#COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#RUN pip install -r requirements.txt
