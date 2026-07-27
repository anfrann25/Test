FROM ubuntu:24.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    sudo curl nano vim git build-essential python3 file xxd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash player \
    && echo 'player:player' | chpasswd \
    && usermod -aG sudo player \
    && printf 'player ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/hackthebasics-player \
    && chmod 0440 /etc/sudoers.d/hackthebasics-player

COPY labs/linux/linux_challenges/ /home/player/linux_challenges/
COPY tools/htb-cli/ /opt/hackthebasics/

RUN chmod +x /opt/hackthebasics/setup.sh \
    /opt/hackthebasics/uninstall.sh \
    /opt/hackthebasics/redeem \
    /opt/hackthebasics/htb \
    && cd /opt/hackthebasics \
    && ./setup.sh \
    && chown -R root:root /home/player/linux_challenges \
    && find /home/player/linux_challenges -type d -exec chmod 755 {} \; \
    && find /home/player/linux_challenges -type f -exec chmod 644 {} \; \
    && chmod +x /home/player/linux_challenges/lvl4/runme \
        /home/player/linux_challenges/lvl6/getEncryptedflag \
        /home/player/linux_challenges/lvl7/getflag \
        /home/player/linux_challenges/lvlEnd10/login

WORKDIR /home/player
USER player
CMD ["/bin/bash"]
