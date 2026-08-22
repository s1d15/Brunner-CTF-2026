FROM debian@sha256:6b4b9cd657a3960935657e0d150e8c0ded01e9e0faedcf8cd9bdf64f54d1eabd

WORKDIR /app

RUN apt-get update && apt-get install -y \
    socat

COPY flag.txt .
COPY stocks .

RUN chmod 444 flag.txt
RUN chmod 555 stocks

RUN useradd -Ms /bin/bash ctf

USER ctf

EXPOSE 1337

CMD socat tcp-l:1337,reuseaddr,fork exec:/app/stocks,pty,echo=0,raw,iexten=0
