FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-dev
WORKDIR /flask
COPY ./requirements.txt /flask/requirements.txt
COPY ./myapp.py /flask/myapp.py
RUN pip install -r requirements.txt
EXPOSE 5010
ENTRYPOINT [ "python3" ] 
CMD [ "myapp.py" ]