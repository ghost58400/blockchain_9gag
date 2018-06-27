FROM centos

EXPOSE 80
EXPOSE 1234
ADD ./install.sh /root
WORKDIR /root
RUN sh /root/install.sh
RUN rm -f /root/install.sh
ADD . /root
RUN cd /root/scriptTest/; sh test2.sh; cd

CMD ["/bin/bash"]
