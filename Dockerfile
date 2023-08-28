FROM python:3.8

ENV FLASK_APP=runner.py
ENV FLASK_ENV=development

COPY requirements.txt requirements.txt
COPY . .

RUN pip install -r requirements.txt


CMD ["flask", "run", "--host","0.0.0.0"]
