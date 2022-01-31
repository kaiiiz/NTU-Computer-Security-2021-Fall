FROM ubuntu:20.04

MAINTAINER LJP-TW <ljp.cs10@nycu.edu.tw>

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=en_US.UTF-8

RUN apt-get update && \
    apt-get upgrade -y && \
    apt install -yq zsh dropbear

COPY ./run.sh /run.sh
RUN chmod -R 774 /run.sh
RUN chmod -R 755 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run

COPY ./dropbear /usr/sbin/dropbear

RUN chmod -R 755 /usr/sbin/dropbear

CMD ["/run.sh"]
