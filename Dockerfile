FROM python:alpine

RUN pip install flask requests

WORKDIR /mnt/oreo
CMD [ "python", "/mnt/oreo/oreo.py" ]
