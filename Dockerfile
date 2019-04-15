FROM jjanzic/docker-python3-opencv

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install requests

EXPOSE 5000

CMD ["python", "app.py"]