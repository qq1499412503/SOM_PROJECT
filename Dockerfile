FROM ubuntu
# init system
RUN apt-get update && apt-get -y upgrade && apt-get install -y nano openssh-server mongodb
RUN apt-get install -y git

#config sshd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN sed -i "/UsePAM yes/cUsePAM no" /etc/ssh/sshd_config
RUN mkdir /run/sshd

#init root user with passwd Som123
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo 'root:Som123' | chpasswd

#init package management tool
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh && /bin/bash ~/anaconda.sh -b -p /opt/conda && rm ~/anaconda.sh && echo "export PATH=/opt/conda/bin:$PATH" >> ~/.bashrc
ENV PATH /opt/conda/bin:$PATH
# init package
RUN conda install -y -c anaconda django
RUN pip install djongo MiniSom
RUN conda install -y -c conda-forge djangorestframework
# git clone the project
# RUN https://qq1499412503:c5b225f3d0b50ab610eca2f4a6bc6812ca459f09@github.com/qq1499412503/SOM_PROJECT.git

# untested --test when upload
# CMD service mongodb start && tail -F /var/log/mongodb/mongodb.log


