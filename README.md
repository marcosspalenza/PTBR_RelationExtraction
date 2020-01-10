# Relation Extraction using SpaCy

Simple Flask service for Portuguese Natural Language Processing to analyze sentence dependencies and extract relations using SpaCy.

## Requirements: 
Docker Container Ubuntu 18.04

- Python 3.6

- [SpaCy](https://spacy.io/) v2.2.3

- [Flask](https://flask.palletsprojects.com/) v1.0.4

- [Graphviz](https://www.graphviz.org/) v2.40.1 / py v0.13.2


## Usage

Create via Dockerfile:
```
docker build -t nlp_relex .
```


Clone via DockerHub:
```
docker push marcosspalenza/nlp_relex:lattest
```

Start and access the container IP. The service will be runing on localhost port 5000.
