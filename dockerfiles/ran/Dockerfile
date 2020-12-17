FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install libtool net-tools openssh-server curl --fix-missing
RUN apt-get clean

RUN apt-get install -y python-pip && python -m pip install kubernetes
COPY rantest /root/rantest
RUN chmod +777 /root/rantest
COPY ran.so /root/ran.so
RUN echo "0.0.0.0"> /root/loadbalancerip.conf
RUN echo "import sys\n\
import os\n\
from kubernetes import client, config\n\
config.load_incluster_config()\n\
c=client.CoreV1Api()\n\
result=c.list_namespaced_service(sys.argv[1])\n\
for ip in result.items:\n\
    if(ip.metadata.name == 'udpnew-lb'):\n\
        lbip = ip.status.load_balancer.ingress[0]\n\
        print(lbip.ip)\n\
        cmd = 'sed -i \"s/0.0.0.0/{}/g\" /root/loadbalancerip.conf'.format(lbip.ip)\n\
        os.system(cmd)"> lbip.py
RUN chmod +x lbip.py
SHELL ["/bin/bash", "-c"]
RUN echo $'#!/bin/bash\n\
lbip=$(echo $MODEL)\n\
python lbip.py $lbip\n\
cd /root/\n\
./rantest > application.log 2>&1\n\
while true; do echo '.'; sleep 100; done'> init_ran.sh
RUN ["chmod", "+x", "init_ran.sh"]
RUN chmod +x init_ran.sh
EXPOSE 9487
EXPOSE 2152

ENTRYPOINT  ["./init_ran.sh", "&"]
