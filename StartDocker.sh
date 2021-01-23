#! /bin/bash

docker run -it --rm --name my-python3 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /usr/bin/docker:/usr/bin/docker \
    -v /usr/lib/x86_64-linux-gnu/libdevmapper.so.1.02.1:/usr/lib/x86_64-linux-gnu/libdevmapper.so.1.02.1 \
    -v /opt/Devorkin.net/Staging/Docker/Pi-Hole/etc-pihole/setupVars.conf:/usr/src/app/setupVars.conf \
    -v /opt/Devorkin.net/Staging/Docker/Pi-Hole/etc-dnsmasq.d/01-pihole.conf:/usr/src/app/01-pihole.conf \
    -v "$PWD":/usr/src/app \
    -w /usr/src/app my-python-app python ping.py $1