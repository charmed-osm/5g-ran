FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y openssh-server git
RUN apt-get -y install netcat tcpdump iproute2 libtool wget net-tools iputils-ping vim
RUN mkdir /var/run/sshd
RUN sed -i 's/#*PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
RUN sed -i 's/#*PermitUserEnvironment no/PermitUserEnvironment yes/g' /etc/ssh/sshd_config
RUN echo 'root:root' | chpasswd
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
RUN git clone https://github.com/pjsip/pjproject.git
RUN echo '--id sip:alice@mnc001.mcc001.3gppnetwork.org\n\
--registrar sip:mnc001.mcc001.3gppnetwork.org:4070;\n\
--realm mnc001.mcc001.3gppnetwork.org\n\
--username alice@mnc001.mcc001.3gppnetwork.org\n\
--password alice\n\
--outbound sip:pcscf.mnc001.mcc001.3gppnetwork.org:4070;' > pjproject/alice.cfg
RUN  apt-get install -y python-dev libasound2-dev make gcc binutils build-essential manpages-dev vim \
 && cd pjproject/  \
 && ./configure CFLAGS='-O2 -fPIC' \
 && make dep \
 && make \
 && cd pjsip-apps/src/python/ \
 && make \
 && python ./setup.py install \
 && cd ../../../ \
 && cp pjsip-apps/bin/pjsua-x86_64-unknown-linux-gnu /usr/local/bin/pjsua
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
