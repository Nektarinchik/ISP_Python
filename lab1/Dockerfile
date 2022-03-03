FROM ubuntu:latest

RUN apt update

RUN apt install python3.8 -y

WORKDIR /usr/app/src

COPY main.py ./

CMD [ "python3.8", "main.py", "Hello, my dear friend. Some text blablabla!", "5", "3"]
