FROM nvidia/cuda:9.1-devel
MAINTAINER DJ Enriquez <dj@glympse.com>

RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*


ENV APP_DIR=/cudamon
WORKDIR $APP_DIR

COPY ./requirements.txt $APP_DIR

RUN  pip install -r requirements.txt

COPY . $APP_DIR

CMD ["./main"]