FROM ubuntu:20.04

MAINTAINER K1a <kia@csie.io>

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y xinetd python3

RUN adduser --disabled-password --gecos ""  ovo8

COPY ./ovo8 /home/ovo8
COPY ./xinetd /etc/xinetd.d/ovo8

RUN chown -R root:root /home/ovo8
RUN chmod -R 755 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run

CMD ["/usr/sbin/xinetd","-dontfork"]
