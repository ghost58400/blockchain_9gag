FROM centos

ADD . /root
WORKDIR /root
RUN yum install -y dhclient net-tools
RUN sh /root/install.sh
RUN rm -rf /root/.git*

CMD ["/bin/bash"]
