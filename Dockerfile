FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& apt-get install gunicorn3 -y \
&& apt-get install python3.9-dev -y \
&& apt-get install libcurl4-gnutls-dev librtmp-dev -y \
&& apt-get install libnss3 libnss3-dev -y
RUN touch /var/log/stamp.log
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb
WORKDIR /stampbox
COPY requirements.txt /stampbox/
RUN pip install -r requirements.txt
COPY . /stampbox/

EXPOSE 8000
