FROM ubuntu:latest
MAINTAINER Shubham Mahawar "shubhamm033@gmail.com"
RUN apt-get update -y


RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y libssl-dev libffi-dev 
RUN pip install -U pip setuptools

COPY . /app


WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]
EXPOSE 5000