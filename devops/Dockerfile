FROM ubuntu:latest
FROM python:3.10

RUN apt-get -y update && apt-get install -y libmagic-dev

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /alerto

RUN addgroup --system django \
    && adduser --system --ingroup django django


COPY --chown=django:django ./devops/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh


COPY --chown=django:django ./devops/celery_worker.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh


COPY --chown=django:django ./devops/celery_beat.sh /start-celerybeat.sh
RUN sed -i 's/\r$//g' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh


ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . .