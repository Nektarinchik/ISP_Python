FROM ubuntu:latest

RUN apt update

RUN apt install python3.8 -y

WORKDIR /usr/app/src

COPY main.py ./

ENTRYPOINT [ "python3.8", "main.py", "China's government has neither condemned nor condoned the attack and has even refrained from calling it an invasion in the first place. Mr Somename has always said that it does not interfere in the internal affairs of others, a core principle of its foreign policy.", "5", "3" ]
