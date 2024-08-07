FROM python:3.10
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
ENV TOKEN=7258791962:AAEOFhkcLfYLzYlmhvToQ2annPTcS0344vE
CMD python main.py
