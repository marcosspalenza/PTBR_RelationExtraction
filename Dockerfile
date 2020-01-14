FROM ubuntu:18.04

MAINTAINER Marcos Spalenza "marcos.spalenza@gmail.com"

RUN apt-get update -y && \ 
	apt-get install -y python3 python3-pip python3-dev

RUN apt-get -y install graphviz

RUN pip3 install Flask
RUN pip3 install spacy
RUN pip3 install graphviz


RUN python3 -m spacy download pt_core_news_sm

WORKDIR /app

COPY . /app

RUN mkdir -p /app/static/

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
