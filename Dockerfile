FROM python:alpine

RUN pip install flask requests

ADD src /src

CMD [ "python", "/src/oreo.py" ]
