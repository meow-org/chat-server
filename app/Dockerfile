FROM python:3
RUN groupadd -r meow && useradd -m -r -g meow meow
COPY requirements.txt /home/meow
WORKDIR /home/meow
RUN pip install -r requirements.txt
COPY . /home/meow
EXPOSE 5000
USER meow