# Use the official Ubuntu 20.04 base image
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# Update the package lists and upgrade installed packages
RUN apt update && apt upgrade -y

# Install net-tools
RUN apt install -y net-tools

# Install git
RUN apt install -y git

# Install Java 8
RUN apt install -y openjdk-11-jdk

# Export Java 8 as JAVA_HOME

# Install Open V Switch
RUN apt install -y openvswitch-switch

# Install wget
RUN apt install -y wget

# Install Python and Pip
RUN apt install -y python3.8
RUN apt install -y python3-pip

# Install RYU
RUN git clone https://github.com/faucetsdn/ryu.git
RUN cd ryu && pip install .

# Install OpenDaylight
RUN cd /tmp && wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.tar.gz
RUN cd /tmp && tar -zxvf karaf-0.8.4.tar.gz
RUN mv /tmp/karaf-0.8.4 /opt/karaf-0.8.4


# Copy Sample RYU Project
COPY RYU-Projects /home/RYU-Projects

# Expose required ports
EXPOSE 6633
EXPOSE 6653
EXPOSE 1099
EXPOSE 8180
EXPOSE 8181

# Copy bash profile
COPY .bashrc /root/.bashrc

# Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Clean up to reduce image size
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
