FROM python:3.6

ADD kukkohelper.py  /
ADD KEY /
ADD TOKEN /
ADD RepeatedTimer.py /
ADD requirements.txt /

RUN pip install -r requirements.txt
#RUN apt-get update
#RUN apt-get install -y vim

CMD [ "python", "./kukkohelper.py" ]