FROM centos

EXPOSE 80
ADD ./install.sh /root
WORKDIR /root
RUN sh /root/install.sh
RUN rm -f /root/install.sh
ADD . /root

CMD ["/bin/bash"]
