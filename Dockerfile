FROM python:3.10-slim

ARG PIP_TRUSTED_HOST=mirrors.aliyun.com
ARG PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple

RUN pip config set global.trusted-host ${PIP_TRUSTED_HOST}  \
    && pip config set global.index-url ${PIP_INDEX_URL}

WORKDIR /app

COPY . /app 

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["python3", "main.py"]
