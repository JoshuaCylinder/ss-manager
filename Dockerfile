FROM ubuntu:22.04
WORKDIR /ss-manager-controller
RUN apt update && apt install -y shadowsocks-libev cron python3 python3-pip &&  \
    apt clean && apt autoclean && apt autoremove && pip install --no-cache prettytable
COPY ./utils ./utils
COPY main.py settings.py ./

ENTRYPOINT ["python3", "main.py", "run"]