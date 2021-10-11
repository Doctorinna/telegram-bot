FROM python:3.9

WORKDIR /opt/doctorinna_tg
COPY bot/ bot/

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "-m", "bot"]