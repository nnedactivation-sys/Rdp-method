# Dockerfile - FIXED SYNTAX
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV USER=root
ENV PASSWORD=Antyrx@123
ENV RESOLUTION=1920x1080

RUN apt-get update && apt-get upgrade -y

# Install essential packages - SAHI SYNTAX!
RUN apt-get install -y \
    xfce4 \
    xfce4-goodies \
    firefox \
    chromium-browser \
    nano \
    vim \
    wget \
    curl \
    git \
    python3 \
    python3-pip \
    tigervnc-standalone-server \
    tigervnc-common \
    novnc \
    websockify \
    supervisor \
    xrdp \
    xorgxrdp \
    dbus-x11 \
    nginx \
    && apt-get clean

# Install Chrome Remote Desktop
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome-remote-desktop/deb stable main" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y chrome-remote-desktop

# Install NoMachine
RUN wget https://download.nomachine.com/download/8.10/Linux/nomachine_8.10.1_1_amd64.deb \
    && dpkg -i nomachine_8.10.1_1_amd64.deb || apt-get install -f -y \
    && rm nomachine_8.10.1_1_amd64.deb

# Setup VNC
RUN mkdir -p /root/.vnc \
    && echo "$PASSWORD" | vncpasswd -f > /root/.vnc/passwd \
    && chmod 600 /root/.vnc/passwd

# Copy configuration files
COPY start.sh /start.sh
COPY setup.py /setup.py
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set permissions
RUN chmod +x /start.sh
RUN chmod +x /setup.py

# Create nginx directory if not exists
RUN mkdir -p /etc/nginx

# Ports
EXPOSE 3389 8080 5901 4000 8000 80 443

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
