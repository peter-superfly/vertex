FROM ubuntu:20.04

RUN apt-get update \
  && apt-get install -y -qq haproxy

# add missing socket path
RUN mkdir /run/haproxy


COPY dhparams.pem /etc/haproxy/dhparams.pem

COPY haproxy.cfg /etc/haproxy/haproxy.cfg

COPY meet.kenyacourts.org.pem /etc/haproxy/certs/meet.kenyacourts.org.pem


CMD ["/usr/sbin/haproxy","-W","-db","-f","/etc/haproxy/haproxy.cfg"]