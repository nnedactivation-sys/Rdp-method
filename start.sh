#!/bin/bash
# start.sh

echo "🔥 Starting RDP Server..."

# Kill existing VNC sessions
vncserver -kill :1 > /dev/null 2>&1
vncserver -kill :2 > /dev/null 2>&1

# Start VNC server
vncserver -localhost no :1 -geometry ${RESOLUTION:-1920x1080} -depth 24

# Start noVNC (Web VNC)
websockify -D --web=/usr/share/novnc 8080 localhost:5901

# Start RDP
/etc/init.d/xrdp start

# Start Chrome Remote Desktop
/etc/init.d/chrome-remote-desktop start

# Start NoMachine
/etc/NX/nxserver --startup

# Start file server
python3 /root/setup.py &

# Keep container running
tail -f /dev/null