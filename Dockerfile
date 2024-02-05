FROM debian:12-slim
RUN apt update && apt -y install --no-install-recommends\
                python3\
                python3-pip\
                librdkit1

RUN pip install --break-system-packages matplotlib dash dash-html-components dash-core-components dash-daq openbabel-wheel rdkit gunicorn

COPY . /purge
WORKDIR purge
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["/purge/entrypoint.sh"]
