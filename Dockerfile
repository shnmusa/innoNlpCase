FROM python:3.8-slim-buster
COPY . .
RUN apt-get update -y
RUN apt-get install -y git
RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py" ]

