FROM python
ADD kukkohelper.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir /config
CMD ["python", "-u", "./kukkohelper.py"]
