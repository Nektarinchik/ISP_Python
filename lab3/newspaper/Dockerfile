FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/src/newspaper

WORKDIR /usr/src/newspaper

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install --upgrade pip && pip install -r /usr/src/requirements.txt

COPY . /usr/src/newspaper

#open on port 8000
EXPOSE 8000
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
