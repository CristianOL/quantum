FROM python:latest

WORKDIR /back

RUN apt update 

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./backend/ .

#EXPOSE 5000

CMD ["python3", "apiBack.py"]
