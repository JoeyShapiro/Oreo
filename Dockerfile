FROM python:alpine

RUN apk add python3-flask

CMD [ "python", "/mnt/oreo/oreo.py" ]
