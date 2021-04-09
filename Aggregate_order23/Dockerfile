FROM centos:7
ENV LC_ALL=C
#ADD ./web /root/web
# httpd install
#RUN rpm --rebuilddb; yum install -y httpd
# update
RUN yum -y upgrade
RUN yum -y update
# text editer install
RUN yum install -y vim
# ssh install
RUN yum -y install openssh-server
RUN yum -y install openssh-clients
# sudo install
# RUN yum -y install sudo
# RUN yum -y install sshpass
#RUN sed -i -e 's/# %wheel\tALL=(ALL)\tNOPASSWD: ALL/%wheel\tALL=(ALL)\tNOPASSWD: ALL/' /etc/sudoers
#RUN sed -i -e 's/%wheel\tALL=(ALL)\tALL/# %wheel\tALL=(ALL)\tALL/' /etc/sudoers
#RUN visudo -c
# RUN echo "root:password" | chpasswd
# python install
# RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python3 python3-libs python3-devel python3-pip
# python lib install
RUN pip3.6 install python-twitter requests pytz bs4
# DB create
#RUN touch /root/db/video_eval.db
#RUN python3.6 /root/db/db_create.py

RUN localedef -f UTF-8 -i ja_JP ja_JP
# cron install
RUN yum install -y cronie
# cron config
RUN cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

#RUN echo "* */1 * * * sshpass -p 'password' scp -o StrictHostKeyChecking=no /root/Statistics/video_eval.db root@172.18.0.2:/root/" > /var/spool/cron/root
#RUN python3.6 /root/main.py
#RUN mv /root/nicorand_tweet /etc/cron.d/
#RUN chmod 0644 /etc/cron.d/nicorand_tweet
#RUN crontab /etc/cron.d/nicorand_tweet
# FOREGROUND change access
CMD ["/usr/bin/ssh", "-D", "FOREGROUND"]