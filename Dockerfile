FROM python
ADD kukkohelper.py /
ADD club.py /
ADD dota.py /
ADD general.py /
ADD setup_logger.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir /config
CMD ["python", "-u", "./kukkohelper.py"]
