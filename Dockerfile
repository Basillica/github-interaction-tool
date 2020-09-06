# FROM python:3.8.5
FROM python:alpine3.7
COPY . /project
WORKDIR /project
RUN pip install -r requirements.txt 
EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "run.py" ]
