FROM ubuntu:14.04
MAINTAINER Steve Arnett <steve@stevearnett.com>

#update and install deps
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev git yum nginx
RUN sudo yum -y groupinstall "Development Tools"
RUN sudo yum -y install nginx
RUN sudo yum -y install libxml2-devel

#copy in code
ADD . /app
WORKDIR /app

#install app pip deps
RUN pip install -r requirements.txt

CMD python app.py
EXPOSE 5001