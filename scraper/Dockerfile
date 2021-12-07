FROM selenium/standalone-chrome:4.1.0-20211123

RUN sudo apt-get update
RUN sudo apt-get install -y python3 python3-pip

WORKDIR /usr/scraper

COPY . .

RUN pip3 install -r requirements.txt