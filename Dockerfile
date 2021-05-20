FROM python:3.8

WORKDIR /code
ADD . /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code
ENV DOCKERIZE_VERSION v0.6.1

CMD ["python3", "-m", "app.main"]