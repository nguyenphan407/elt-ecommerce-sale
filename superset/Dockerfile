FROM apache/superset:latest

USER root

RUN pip install psycopg2-binary

ENV SUPERSET_ADMIN $SUPERSET_ADMIN
ENV SUPERSET_PASSWORD $SUPERSET_PASSWORD
ENV SUPERSET_SECRET_KEY $SUPERSET_SECRET_KEY

COPY ./superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh
RUN chown superset:superset /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]