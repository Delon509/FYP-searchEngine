FROM python:3.7-slim
RUN mkdir /server
COPY searchrequirements.txt /server/searchrequirements.txt
RUN pip install -r /server/searchrequirements.txt
COPY . .
ENV FLASK_APP=main.py
CMD gunicorn -w 4 -b 0.0.0.0:80 --timeout 300 --log-level=debug --keep-alive 5 main:app
