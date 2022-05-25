FROM python:3.8.13-slim-bullseye

ARG BUILD_ENV=CI

RUN if [ "$BUILD_ENV" = "LOCAL" ]; \
    then sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list; \
    fi

RUN apt-get update \
	&& apt-get install -y openjdk-11-jdk git \
	&& rm -rf /var/lib/apt/lists/*

COPY ./ /opt/onesphere_reporter

WORKDIR /opt/onesphere_reporter

RUN mkdir -p /opt/reports \
    && ln -s /opt/onesphere_reporter/onesphere_reporter_cli.py /usr/local/bin/onesphere_reporter_cli \
    && ln -s /opt/onesphere_reporter/onesphere_reporter_service.py /usr/local/bin/onesphere_reporter_service

RUN if [ "$BUILD_ENV" = "LOCAL" ]; \
    then pip install -r /opt/onesphere_reporter/requirements.txt -i https://pypi.douban.com/simple; \
	else pip install -r /opt/onesphere_reporter/requirements_ci.txt; \
    fi

CMD ["onesphere_reporter_service" ]