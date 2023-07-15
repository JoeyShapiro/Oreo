FROM python:alpine

RUN pip install flask requests

ADD src /src

WORKDIR /mnt/oreo
CMD [ "python", "/mnt/oreo/oreo.py" ]
