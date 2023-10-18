# syntax=docker/dockerfile:1

FROM python:3.9

RUN apt-get update && apt-get install -y ffmpeg


RUN apt-get update
RUN apt-get install -y build-essential libssl-dev ca-certificates libasound2 wget

RUN wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf -
RUN cd openssl-1.1.1u
RUN ./config --prefix=/usr/local
RUN make -j $(nproc)
RUN make install_sw install_ssldirs
RUN ldconfig -v
RUN export SSL_CERT_DIR=/etc/ssl/certs

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app" ,"--host", "0.0.0.0", "--port", "8000", "--reload"]