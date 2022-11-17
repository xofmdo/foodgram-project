FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

COPY . ./

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && pip install -r requirements.txt \


CMD ["gunicorn", "foodgram_project.wsgi:application", "--bind", "0:8000" ]
