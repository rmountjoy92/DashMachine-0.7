FROM python:3.8-slim

RUN apt-get update -q \
  && apt-get install --no-install-recommends -qy \
    inetutils-ping \
  && rm -rf /var/lib/apt/lists/*

COPY [ "requirements.txt", "/DashMachine/" ]

WORKDIR /DashMachine

RUN pip install --no-cache-dir --progress-bar off gunicorn
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY [".", "/DashMachine/"]

ENV PRODUCTION=true

EXPOSE 5000
VOLUME /DashMachine/config

RUN chown -R 1000 /DashMachine/config
RUN chmod -R 775 /DashMachine/config
RUN chmod -R g+s /DashMachine/config

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app" ]
