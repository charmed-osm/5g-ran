FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install libtool net-tools openssh-server curl --fix-missing
RUN apt-get clean

RUN apt-get install -y python-pip && python -m pip install kubernetes
COPY free5gc/rantest /root/rantest
RUN chmod +777 /root/rantest
COPY free5gc/ran.so /root/ran.so
COPY free5gc/loadbalancerip.conf /root/loadbalancerip.conf
COPY init_ran.sh init_ran.sh
RUN ["chmod", "+x", "init_ran.sh"]
COPY lbip.py lbip.py
RUN chmod +x lbip.py

EXPOSE 9487
EXPOSE 2152

ENTRYPOINT  ["./init_ran.sh", "&"]
