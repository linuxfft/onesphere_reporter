FROM python:3.8.13-slim-bullseye

RUN set -eux; \
	apt-get update; \
	apt-get install -y \
		openjdk-11-jdk \
	; \
	rm -rf /var/lib/apt/lists/* \

COPY ./ /opt/onesphere_reporter

WORKDIR /opt/onesphere_reporter

RUN mkdir -p /opt/reports \
    && ln -s /opt/onesphere_reporteronesphere_reporter_cli.py /usr/local/bin/onesphere_reporter_cli \
    && ln -s /opt/onesphere_reporteronesphere_reporter_service.py /usr/local/bin/onesphere_reporter_service

RUN pip install -r /requirements.txt

CMD ["onesphere_reporter_service" ]