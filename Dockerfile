FROM python:3.6
ADD kukkohelper.py  /
#ADD KEY /
#ADD TOKEN /
ADD RepeatedTimer.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./kukkohelper.py" ]