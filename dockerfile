FROM python:3

WORKDIR /app

COPY main.py ./
COPY requirements.txt ./
COPY .env ./ 

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 5000:5000
CMD ["python", "main.py"]
