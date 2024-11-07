FROM debian:12-slim
RUN apt update && apt -y install --no-install-recommends\
                python3\
                python3-pip\
                librdkit1

COPY . /pur-gen
WORKDIR pur-gen
RUN pip install --break-system-packages -r requirements.txt
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["/pur-gen/entrypoint.sh"]
