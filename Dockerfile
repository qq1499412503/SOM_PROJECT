FROM ubuntu
# init system
RUN apt-get update && apt-get -y upgrade && apt-get install -y nano openssh-server

#config sshd
RUN echo "PermitRootLogin yes" > /etc/ssh/sshd_config
RUN sed -i "/UsePAM yes/cUsePAM no" /etc/ssh/sshd_config
RUN mkdir /run/sshd

#
#RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 11 ubuntu -p @Ubuntu123
#USER ubuntu
#WORKDIR /home/ubuntu
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo 'root:@Som123' | chpasswd

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh && /bin/bash ~/anaconda.sh -b -p /opt/conda && rm ~/anaconda.sh && echo "export PATH=/opt/conda/bin:$PATH" >> ~/.bashrc
ENV PATH /opt/conda/bin:$PATH
# init package
RUN conda install -y -c anaconda django
RUN pip install MiniSom

# following

