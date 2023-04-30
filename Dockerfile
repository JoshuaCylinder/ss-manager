FROM ubuntu:22.04
RUN apt update && apt install -y shadowsocks-libev cron python3 python3-pip &&  \
    apt clean && apt autoclean && apt autoremove && pip install --no-cache prettytable
COPY ss_manager ./ss_manager
WORKDIR /ss_manager
ENV CONTAINER="true"

ENTRYPOINT ["python3", "main.py", "run"]