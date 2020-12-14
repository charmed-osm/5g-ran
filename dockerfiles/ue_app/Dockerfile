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
COPY pjsip_install.sh pjproject/pjsip_install.sh
COPY alice.cfg pjproject/alice.cfg
RUN sh pjproject/pjsip_install.sh
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
