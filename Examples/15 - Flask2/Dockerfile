FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-dev
WORKDIR /flask
COPY . /flask/
RUN pip install -r requirements.txt
ENTRYPOINT [ "bash" ] 
CMD [ "start.sh" ]