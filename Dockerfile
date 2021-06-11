FROM python 3:8

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
WORKDIR src/

CMD ["python","-u" ,"./main.py"]

