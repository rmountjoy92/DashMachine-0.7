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

RUN addgroup --system --gid 1000 dm_user_group
RUN chown :1000 /DashMachine
RUN chmod 775 /DashMachine
RUN chmod g+s /DashMachine
RUN adduser --system --home /DashMachine --shell /bin/bash --no-create-home --gid 1000 dm_user

USER dm_user

EXPOSE 5000
VOLUME /DashMachine/config
VOLUME /DashMachine/vscode_integration/config

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app" ]
