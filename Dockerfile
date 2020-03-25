FROM python:3.7-slim
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
ADD src /src
WORKDIR /src
CMD gunicorn -b 0.0.0.0:8000 -w 5\
    --proxy-allow-from "*" --forwarded-allow-ips "*"\
    --proxy-protocol bot:app
