FROM python:3.6

ADD kukkohelper.py  /
ADD KEY /
ADD TOKEN /

RUN pip install --upgrade pip
RUN pip install requests
RUN pip install discord
RUN apt-get update
RUN apt-get install -y vim

CMD [ "python", "./kukkohelper.py" ]