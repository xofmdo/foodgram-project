FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

COPY . ./

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && pip install -r requirements.txt \

LABEL author=sashakuzmich69@yandex.ru version=1.0.0

CMD ["gunicorn", "foodgram_project.wsgi:application", "--bind", "0:8000" ]
