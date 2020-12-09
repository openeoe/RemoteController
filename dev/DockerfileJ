FROM 129.254.165.43:5000/ubuntu_exobrain_java:1.4
ENV LC_ALL=C.UTF-8
RUN sed -i "s/^exit 101$/exit 0/" /usr/sbin/policy-rc.d
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
CMD ["/usr/sbin/sshd", "-D"]
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
RUN echo "apt-get install -y language-pack-ko" >> /etc/profile
RUN echo "export LANG=ko_KR.UTF-8" >> /etc/profile
RUN echo "export LANGAUGE=ko_KR:ko" >> /etc/profile

MAINTAINER hwi
COPY ./module /root/grpc_nanum/module
WORKDIR /root/grpc_nanum/
RUN ./compile.sh
