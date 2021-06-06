FROM ubuntu
# init system
RUN apt-get update && apt-get -y upgrade && apt-get install -y nano openssh-server mongodb nginx gcc libpcre3 libpcre3-dev && systemctl enable nginx && systemctl enable mongodb && apt-get install -y build-essential python3 && apt-get install -y python3-dev python3-pip

RUN pip3 install Django==2.2.5 sqlparse==0.2.4 djangorestframework uwsgi djongo MiniSom numpy pandas matplotlib bokeh && apt-get install -y uwsgi-plugin-python3


SHELL ["/bin/bash", "-o", "pipefail", "-c"]
#config sshd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && sed -i "/UsePAM yes/cUsePAM no" /etc/ssh/sshd_config && mkdir /run/sshd && echo 'root:Som123' | chpasswd && mkdir /SOM_PROJECT




COPY . /SOM_PROJECT/


RUN service mongodb start && python3 /SOM_PROJECT/manage.py makemigrations && python3 /SOM_PROJECT/manage.py migrate && python3 /SOM_PROJECT/manage.py collectstatic --noinput && echo "daemon off;" >> /etc/nginx/nginx.conf



CMD ["/bin/bash","SOM_PROJECT/config.sh","start"]