FROM python:3.6

ADD kukkohelper.py  /
ADD tokens/KEY /
ADD tokens/TOKEN /
ADD requirements.txt /

RUN apt-get update
RUN apt-get install -y vim

CMD [ "python", "./kukkohelper.py" ]