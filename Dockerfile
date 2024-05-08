FROM ubuntu:latest
LABEL authors="feride"

ENTRYPOINT ["top", "-b"]