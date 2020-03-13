FROM ubuntu:18.04
RUN apt-get update
RUN apt install python3-pip -y


RUN pip3 install --upgrade pip
RUN apt-get install git -y
RUN git clone https://github.com/Flagy/COVID-19.git
RUN pip3 install -r COVID-19/requirements.txt
CMD python3 COVID-19/main.py
