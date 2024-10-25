FROM python:3.11-bookworm

WORKDIR /app

COPY . /app

ADD requirements.txt /app/

RUN apt-get -y update && apt-get -y install && apt-get clean

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# RUN ["python", "-c", "import nltk; nltk.download('stopwords')"]

# RUN ["python", "-c", "import nltk; nltk.download('punkt')"]

CMD ["python", "main.py"]