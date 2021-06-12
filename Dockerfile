FROM python 3:8

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY main.py main.py

CMD ["python","-u" ,"./main.py"]

