FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

RUN python manage.py migrate

EXPOSE 8000

RUN mkdir -p /code/data

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]