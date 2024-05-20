FROM mysql:latest
COPY embeddings.sql /docker-entrypoint-initdb.d/
COPY /speakermodels /embeddings
ENV MYSQL_ROOT_PASSWORD root
