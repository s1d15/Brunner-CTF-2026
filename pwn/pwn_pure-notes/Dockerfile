FROM debian@sha256:96031e9923cd9ee1ceeffae75849c9386476006df0f8d13c9b3e0dbfa31d5868

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ghc \
    socat

COPY Main.hs .
COPY flag.txt .

RUN ghc Main.hs

EXPOSE 1337

CMD socat tcp-l:1337,reuseaddr,fork exec:/app/Main,pty,echo=0,raw,iexten=0
