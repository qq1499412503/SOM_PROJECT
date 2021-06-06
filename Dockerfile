FROM ubuntu
# init system
RUN apt-get update && apt-get -y upgrade && apt-get install -y nano openssh-server mongodb nginx gcc libpcre3 libpcre3-dev && systemctl enable nginx && apt-get install -y build-essential python3 && apt-get install -y python3-dev python3-pip
#&& wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh && /bin/bash ~/anaconda.sh -b -p /opt/conda && rm ~/anaconda.sh && echo "export PATH=/opt/conda/bin:$PATH" >> ~/.bashrc
#ENV PATH /opt/conda/bin:$PATH
#RUN conda update --all && conda install python=3.6 && conda install -y -c anaconda django && conda install -y -c conda-forge djangorestframework && conda install -y -c conda-forge djangorestframework uwsgi && pip install djongo MiniSom

RUN pip3 install Django==2.2.5 sqlparse==0.2.4 djangorestframework uwsgi djongo MiniSom numpy pandas matplotlib bokeh && apt-get install -y uwsgi-plugin-python3


SHELL ["/bin/bash", "-o", "pipefail", "-c"]
#config sshd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && sed -i "/UsePAM yes/cUsePAM no" /etc/ssh/sshd_config && mkdir /run/sshd && echo 'root:Som123' | chpasswd && mkdir /SOM_PROJECT

#init root user with passwd Som123

#RUN echo 'root:Som123' | chpasswd

#init package management tool
#RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh && /bin/bash ~/anaconda.sh -b -p /opt/conda && rm ~/anaconda.sh && echo "export PATH=/opt/conda/bin:$PATH" >> ~/.bashrc
#ENV PATH /opt/conda/bin:$PATH


COPY . /SOM_PROJECT/

RUN service mongodb start && cd /SOM_PROJECT && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py collectstatic --noinput && cd /SOM_PROJECT/SOM_PROJECT && uwsgi --ini uwsgi.ini

RUN chmod 777 SOM_PROJECT.sock && cp SOM_PROJECT/nginx.conf /etc/nginx/sites-enabled/ && service nginx restart

# untested --test when upload
CMD ["nginx", "-g", "daemon off;"]
CMD service mongodb start && tail -F /var/log/mongodb/mongodb.log

#RUN systemctl enable mongodb.service
