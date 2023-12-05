FROM python:3.11

COPY . /

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

RUN apt update -y
RUN apt upgrade -y
RUN apt install curl -y

EXPOSE 80

ENTRYPOINT [ "python", "main.py" ]