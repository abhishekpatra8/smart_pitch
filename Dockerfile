FROM python:3.10.0

WORKDIR /app

ADD requirement.txt/app

RUN python -m pip install --upgrade pip

RUN pip install requirement.txt

CMD ["uvicorn","main","app"]