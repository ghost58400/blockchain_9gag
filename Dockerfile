FROM centos

ADD . /root
WORKDIR /root
RUN yum install -y dhclient net-tools
RUN sh /root/install.sh

CMD ["/bin/bash"]
