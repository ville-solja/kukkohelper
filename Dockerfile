FROM python
ADD kukkohelper.py /
ADD dota.py /
ADD general.py /
ADD setup_logger.py /
ADD requirements.txt /
ADD archive.py /
ADD admin_tools.py /
ADD nsfw.py /
ADD stats.py /
RUN pip install -r requirements.txt
RUN mkdir /config
CMD ["python", "-u", "./kukkohelper.py"]
