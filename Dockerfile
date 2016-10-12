FROM ubuntu:14.04
MAINTAINER Steve Arnett <steve@stevearnett.com>

#update and install deps
RUN apt-get -yqq update
RUN apt-get install -yqq git libffi-dev libxml2-dev libxslt1-dev libxslt-dev python python-dev build-essential make gcc locales python-pip libatlas-base-dev zlib1g-dev
RUN easy_install lxml

#copy in code
ADD . /app
WORKDIR /app

#install app pip deps
RUN pip install -r requirements.txt

# Add crontab to the cron dir
ADD crontab /etc/cron.d/podcast

# Give execution rights to cron
RUN chmod 0644 /etc/cron.d/podcast


CMD python feed.py
EXPOSE 5001
