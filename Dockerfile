FROM python:3.7.7-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install

COPY Pipfile* /usr/src/app/
RUN cd /usr/src/app/ && pipenv lock --requirements > requirements.txt
RUN pip install --upgrade pip --no-cache-dir -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

RUN chmod +x /usr/src/app/start.sh

CMD ["/bin/bash", "/usr/src/app/start.sh"]


