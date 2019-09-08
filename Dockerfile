FROM debian

# install packages
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install sudo
RUN sudo apt-get -y install python3
RUN sudo apt-get -y install python3-pip
RUN sudo apt-get -y install git

RUN sudo python3 --version
RUN sudo git clone https://github.com/AndreHenkel/traffic_gym.git
RUN sudo pip3 install -e traffic_gym/



