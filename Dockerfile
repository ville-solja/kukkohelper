FROM python
ADD kukkohelper.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD ["python", "-u", "./kukkohelper.py"]